"""Selected-file MinerU adapter. Local operator binding only; never retry POST."""
import hashlib
import json
from pathlib import Path
import time
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener
from uuid import uuid4
from .documents import verify_selected_file

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        return None


def mineru_parse_file(path, base_url):
    source = verify_selected_file(path)
    path = Path(source['path'])
    url = urlsplit(base_url)
    if url.scheme!='http' or url.hostname not in ('127.0.0.1','localhost') or not url.port or url.path not in ('','/') or url.query or url.fragment or url.username or url.password:
        raise ValueError('explicit_local_mineru_binding_required')
    if path.suffix.lower() not in ('.pdf','.png','.jpg','.jpeg','.webp'):
        raise ValueError('mineru_pdf_or_image_only')
    opener = build_opener(ProxyHandler({}),NoRedirect())
    base = base_url.rstrip('/')
    with opener.open(base+'/openapi.json',timeout=10) as response:
        schema = json.load(response)
    request_schema = schema.get('components',{}).get('schemas',{}).get('Body_file_parse_file_parse_post',{})
    if '/file_parse' not in schema.get('paths',{}) or 'hybrid-engine' not in request_schema.get('properties',{}).get('backend',{}).get('enum',[]):
        raise ValueError('mineru_contract_mismatch')
    boundary = 'qaqc-'+uuid4().hex
    data = bytearray()
    options = {'backend':'hybrid-engine','effort':'high','parse_method':'ocr',
               'formula_enable':'true','table_enable':'true','image_analysis':'true',
               'return_md':'true','return_middle_json':'true','return_content_list':'true',
               'return_model_output':'false','return_images':'true','response_format_zip':'false',
               'return_original_file':'false','client_side_output_generation':'false',
               'start_page_id':'0','end_page_id':'99999'}
    for key,value in options.items():
        data.extend(f'--{boundary}\r\nContent-Disposition: form-data; name="{key}"\r\n\r\n{value}\r\n'.encode('ascii'))
    filename = 'selected-input'+path.suffix.lower()
    data.extend(f'--{boundary}\r\nContent-Disposition: form-data; name="files"; filename="{filename}"\r\nContent-Type: application/octet-stream\r\n\r\n'.encode('ascii'))
    data.extend(path.read_bytes())
    data.extend(f'\r\n--{boundary}--\r\n'.encode('ascii'))
    request = Request(base+'/file_parse',data=bytes(data),method='POST',headers={'Content-Type':'multipart/form-data; boundary='+boundary})
    start = time.perf_counter()
    with opener.open(request,timeout=180) as response:
        raw = response.read(64*1024*1024+1)
    if len(raw)>64*1024*1024:
        raise ValueError('mineru_output_budget_exceeded_not_complete')
    result = json.loads(raw)
    if hashlib.sha256(path.read_bytes()).hexdigest()!=source['sha256']:
        raise ValueError('source_changed_during_mineru')
    output = result.get('results') if isinstance(result,dict) else None
    observed = isinstance(output,dict) and bool(output) and any(isinstance(x,dict) and any(k in x for k in ('md_content','content_list')) for x in output.values())
    return {'ok':observed,'status':'mineru_output_observed' if observed else 'mineru_response_pending',
            'file':source,'options':options,'service_schema_version':schema.get('info',{}).get('version'),
            'raw_response':result,'raw_response_sha256':hashlib.sha256(raw).hexdigest(),
            'wall_seconds':time.perf_counter()-start,'normative':False,'review_status':'unreviewed',
            'full_document_read':False,'gaps':['OCR interpretation needs source verification; raw output is not reviewed truth'],
            'retried':False}
