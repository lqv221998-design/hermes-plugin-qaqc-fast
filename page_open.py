"""QAQC-only page opening through the reserved native MCP; never a browser fallback."""
import hashlib
import re
from .hybrid import Session

OPEN_ACTIONS = ['open_page', 'open_page_status']
OPEN_FIELDS = {'action', 'url', 'mode', 'page_id', 'expected_project', 'expected_discipline', 'destination_heading', 'operation_id'}


def page_ids(text):
    from . import Stop
    if not isinstance(text, str):
        raise Stop('unsupported_page_listing')
    return {int(x) for x in re.findall(r'^(\d+):', text, re.M)}


def pages(text):
    from . import source_url, Stop
    found = {}
    for pid, url in re.findall(r'^(\d+): .*?\((https://[^\s)]+)\)', text, re.M):
        try:
            source_url(url)
            found[int(pid)] = url
        except Stop:
            if url == 'https://qaqc.newtecons.vn/':
                found[int(pid)] = url
    return found


def run_open(ctx, args, **kwargs):
    from . import Stop, _LOCK, user_binding, describe, top_page_nodes
    if isinstance(args,dict) and args.get('action')=='open_page_status':
        return run_status(ctx,args,**kwargs)
    session, record, key, acquired = None, None, None, False
    try:
        if not isinstance(args, dict) or set(args)-OPEN_FIELDS or args.get('action') != 'open_page':
            raise Stop('invalid_input')
        from . import source_url
        url = args.get('url')
        bootstrap = url=='https://qaqc.newtecons.vn/'
        if not bootstrap:
            url = source_url(url)
        user_binding(ctx)
        if not bootstrap and (not isinstance(args.get('expected_project'), str) or not args['expected_project'].strip()):
            raise Stop('pending_project_selection')
        if ctx.get_config('allow_open_page', default=False) is not True:
            raise Stop('page_open_not_authorized')
        mode = args.get('mode')
        if mode not in ('new','reuse'):
            raise Stop('invalid_input')
        if bootstrap and mode!='new':
            raise Stop('bootstrap_new_tab_required')
        if mode=='new' and 'page_id' in args:
            raise Stop('invalid_input')
        if mode=='new' and ctx.get_config('allow_new_tab', default=False) is not True:
            raise Stop('new_tab_not_authorized')
        op = args.get('operation_id')
        if not isinstance(op, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,80}', op):
            raise Stop('operation_id_required')
        if not isinstance(kwargs.get('session_id'), str) or not kwargs['session_id']:
            raise Stop('session_context_required')
        active = ctx.state.get('page_open_active')
        if isinstance(active, dict) and active.get('status') != 'verified':
            raise Stop('open_page_pending_no_replay')
        key = 'page_open_'+hashlib.sha256(op.encode()).hexdigest()
        if ctx.state.get(key) is not None:
            raise Stop('operation_id_already_used_no_replay')
        session = Session(ctx, {**args, 'expected_project':args.get('expected_project') or 'Bootstrap-only-not-project-verified',
                               'page_id': 0 if mode=='new' else args.get('page_id')}, kwargs)
        acquired = _LOCK.acquire(blocking=False)
        if not acquired:
            raise Stop('controller_busy')
        active = ctx.state.get('page_open_active')
        if isinstance(active,dict) and active.get('status')!='verified':
            raise Stop('open_page_pending_no_replay')
        if ctx.state.get(key) is not None:
            raise Stop('operation_id_already_used_no_replay')
        before = session.call('list_pages', {})
        listing = before
        previous_nodes = None
        if mode=='reuse':
            if session.page_id not in pages(before):
                raise Stop('page_source_unverified')
            previous_nodes = session.snapshot()  # verify before replacing the chosen tab
        noop = previous_nodes is not None and previous_nodes[0]['url']==url
        record = {'operation_id': op, 'url': url, 'project': session.project, 'user': session.user,
                  'session_id': kwargs['session_id'], 'status': 'inflight', 'before_ids': sorted(page_ids(before)),
                  'expected_discipline':args.get('expected_discipline'),'destination_heading':args.get('destination_heading')}
        if mode=='reuse':
            record['page_id'] = session.page_id
        ctx.state.set(key, record)
        ctx.state.set('page_open_active', record)
        if mode=='new':
            session.call('new_page', {'url': url, 'background': True, 'timeout': 10000})
            listing = session.call('list_pages', {})
            new = page_ids(listing)-set(record['before_ids'])
            if len(new) != 1:
                raise Stop('new_page_identity_unverified')
            session.page_id = next(iter(new))
        elif not noop:
            session.call('navigate_page', {'pageId':session.page_id,'type':'url','url':url,
                                         'handleBeforeUnload':'dismiss','timeout':10000})
        record['page_id'] = session.page_id
        ctx.state.set(key, record)
        ctx.state.set('page_open_active', record)
        if bootstrap:
            if mode!='new' or pages(listing).get(session.page_id)!=url:
                raise Stop('bootstrap_destination_unverified')
            record['status'] = 'verified'
            ctx.state.set(key,record)
            ctx.state.set('page_open_active',record)
            return {'ok':True,'status':'bootstrap_page_opened','page_id':session.page_id,'url':url,
                    'business_verified':False,'project_verified':False,'user_verified':False,
                    'mcp_calls':session.calls,'retried':False,
                    'instruction':'Own tab opened; human login/project selection and inspect remain required.'}
        nodes = previous_nodes if noop else session.snapshot()
        if nodes is None:
            raise Stop('missing_semantic_root')
        if nodes[0]['url'] != url:
            raise Stop('destination_not_verified')
        heading = args.get('destination_heading')
        if heading is not None and (not isinstance(heading, str) or not heading or not any(n['name']==heading and n['role'] in ('heading','StaticText') for n in top_page_nodes(nodes))):
            raise Stop('destination_not_verified')
        record['status'] = 'verified'
        ctx.state.set(key, record)
        ctx.state.set('page_open_active', record)
        result = {'ok': True, 'status': 'page_opened_context_verified', 'page_id': session.page_id,
                  'source': describe(nodes, session.project), 'project_verified': True, 'user_verified': True,
                  'heading_verified': heading is not None, 'data_ready_verified': False, 'coverage': 'navigation_only',
                  'operation_id': op, 'navigation_noop':noop, 'retried': False}
    except Stop as exc:
        if record and key:
            record['status'] = 'pending_no_replay'
            record['last_status'] = exc.status
            ctx.state.set(key, record)
            ctx.state.set('page_open_active', record)
        result = {'ok': False, 'status': exc.status, 'retried': False}
    except Exception:
        if record and key:
            record['status'] = 'pending_no_replay'
            ctx.state.set(key, record)
            ctx.state.set('page_open_active', record)
        result = {'ok': False, 'status': 'host_failure', 'retried': False}
    finally:
        if acquired:
            _LOCK.release()
    result['mcp_calls'] = session.calls if session else 0
    return result


def run_status(ctx,args,**kwargs):
    from . import Stop, _LOCK, user_binding, describe, top_page_nodes
    session, acquired = None, False
    try:
        if set(args)-{'action','operation_id','expected_project','expected_discipline'}:
            raise Stop('invalid_input')
        op = args.get('operation_id')
        if not isinstance(op,str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,80}',op):
            raise Stop('operation_id_required')
        key = 'page_open_'+hashlib.sha256(op.encode()).hexdigest()
        record = ctx.state.get(key)
        user = user_binding(ctx)
        if not isinstance(record,dict) or record.get('user')!=user:
            raise Stop('page_open_scope_mismatch')
        bootstrap = record['url']=='https://qaqc.newtecons.vn/'
        if not bootstrap and record.get('project')!=args.get('expected_project'):
            raise Stop('page_open_scope_mismatch')
        if args.get('expected_discipline') is not None and args['expected_discipline']!=record.get('expected_discipline'):
            raise Stop('page_open_scope_mismatch')
        session = Session(ctx,{**args,'page_id':record.get('page_id',0),
                               'expected_discipline':record.get('expected_discipline')},kwargs)
        acquired = _LOCK.acquire(blocking=False)
        if not acquired:
            raise Stop('controller_busy')
        if 'page_id' not in record:
            listing = session.call('list_pages',{})
            candidates = [pid for pid,url in pages(listing).items() if pid not in record['before_ids'] and url==record['url']]
            if len(candidates)!=1:
                raise Stop('new_page_identity_unverified')
            session.page_id = candidates[0]
            record['page_id'] = session.page_id
        nodes = session.snapshot()
        if not bootstrap and nodes[0]['url']!=record['url']:
            raise Stop('destination_not_verified')
        heading = record.get('destination_heading')
        if heading is not None and not any(n['name']==heading and n['role'] in ('heading','StaticText') for n in top_page_nodes(nodes)):
            raise Stop('destination_not_verified')
        record['status'] = 'verified'
        ctx.state.set(key,record)
        active = ctx.state.get('page_open_active')
        if isinstance(active,dict) and active.get('operation_id')==op:
            ctx.state.set('page_open_active',record)
        result = {'ok':True,'status':'bootstrap_context_observed' if bootstrap else 'page_opened_context_verified',
                  'page_id':session.page_id,'source':describe(nodes,session.project),'project_verified':True,
                  'user_verified':True,'heading_verified':heading is not None,'business_verified':False,
                  'data_ready_verified':False,'coverage':'navigation_only','operation_id':op,'retried':False}
    except Stop as exc:
        result = {'ok':False,'status':exc.status,'retried':False}
    except Exception:
        result = {'ok':False,'status':'host_failure','retried':False}
    finally:
        if acquired:
            _LOCK.release()
    result['mcp_calls'] = session.calls if session else 0
    return result
