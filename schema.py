"""Public native tool schema; every verb remains validated by the executor."""
from .hybrid import ACTIONS

LEGACY_ACTIONS = ['capabilities','pages','inspect','open_module','read_list']
WRITE_ACTIONS = {'open_page','write_record','upload_attachment','transition_record','delete_record','native_step','begin_transfer','restore_browser','ocr_document','analyze_image'}


def properties(modules):
    text = lambda maximum=250: {'type':'string','minLength':1,'maxLength':maximum}
    fields = {'type':'object','minProperties':1,'maxProperties':80,'additionalProperties':{'type':'string','maxLength':20000}}
    result = {'action':{'type':'string','enum':list(dict.fromkeys(LEGACY_ACTIONS+['prepare','open_page','open_page_status']+ACTIONS))},
              'url':{**text(4096),'description':'Exact user-selected HTTPS QAQC URL; never rewrite route parameters or infer project.'},
              'mode':{'type':'string','enum':['new','reuse']},
              'page_id':{'type':'integer','minimum':0,'description':'Observed native QAQC page ID, never assume 1.'},
              'expected_project':{**text(200),'description':'Optional explicit target assertion. Omit to observe the project on the selected page automatically; required only as destination intent for project switching.'},
              'expected_discipline':{'type':'string','enum':['XÂY DỰNG','CƠ ĐIỆN']},
              'module':{'type':'string','enum':list(modules)},
              'menu_path':{'type':'array','items':text(),'minItems':1,'maxItems':6},
              'destination_heading':text(), 'from_project':text(200),
              'fields':fields, 'submit_label':text(), 'next_label':text(),
              'key_column':{'type':'integer','minimum':0},'max_pages':{'type':'integer','minimum':1,'maximum':1000},
              'iterations':{'type':'integer','minimum':1,'maximum':10},
              'record_id':text(),'detail_label':text(),'return_list_label':text(),
              'tabs':{'anyOf':[{'type':'array','items':text(),'maxItems':30},{'type':'string','enum':['all']}]},
              'pid':{'type':'integer','minimum':1},'window_id':{'type':'integer','minimum':1},
              'operation_id':{**text(80),'pattern':'^[A-Za-z0-9_-]+$'},
              'handoff_token':text(128),'reviewed_capture_sha256':{'type':'string','pattern':'^[0-9a-f]{64}$'},
              'purpose':{'type':'string','enum':['canvas','open_file_dialog','save_file_dialog']},
              'native_action':{'type':'object','required':['action'],'additionalProperties':False,
                               'properties':{'action':{'type':'string','enum':['click','double_click','drag','scroll','type','key','set_value']},
                                             'element':{'type':'integer','minimum':1},'from_element':{'type':'integer','minimum':1},'to_element':{'type':'integer','minimum':1},
                                             'coordinate':{'type':'array','items':{'type':'integer'},'minItems':2,'maxItems':2},
                                             'from_coordinate':{'type':'array','items':{'type':'integer'},'minItems':2,'maxItems':2},
                                             'to_coordinate':{'type':'array','items':{'type':'integer'},'minItems':2,'maxItems':2},
                                             'direction':{'type':'string','enum':['up','down','left','right']},'amount':{'type':'integer','minimum':1,'maximum':20},
                                             'text':text(4096),'keys':text(30),'value':text(4096),
                                             'delivery_mode':{'type':'string','enum':['background','foreground']}}},
              'transfer_kind':{'type':'string','enum':['export_excel','export_pdf','print','attachment']},
              'control_label':text(),'local_file':text(4096),'image_question':text(2000),
              'intent':{'type':'string','enum':['create','edit']},'create_label':text(),
              'expected_status':text(),'verify_fields':{'type':'object','maxProperties':80,'additionalProperties':{'type':'string','maxLength':20000}},
              'transition':{'type':'string','enum':['save','send','approve','reject','close']}}
    return result
