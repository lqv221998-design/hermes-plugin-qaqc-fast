"""Readers preserve selected original files. No OCR fallback or credential access."""
import csv
from datetime import date, datetime
import hashlib
from pathlib import Path
import time
import zipfile

ALLOWED = {'.xlsx','.pdf','.docx','.csv','.png','.jpg','.jpeg','.webp','.zip'}


def verify_selected_file(path):
    path = Path(path).resolve(strict=True)
    if path.suffix.lower() not in ALLOWED or not path.is_file():
        raise ValueError('unsupported_selected_file')
    if any(x.lower() in ('.env','auth.json','config.yaml','credentials','secrets') for x in path.parts):
        raise ValueError('secret_source_forbidden')
    if any(path.with_name(path.name+x).exists() for x in ('.crdownload','.part')):
        raise ValueError('download_incomplete')
    first = path.stat()
    if not 0<first.st_size<=100*1024*1024:
        raise ValueError('file_size_out_of_bounds')
    time.sleep(0.05)
    second = path.stat()
    if (first.st_size,first.st_mtime_ns)!=(second.st_size,second.st_mtime_ns):
        raise ValueError('file_changing')
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    third = path.stat()
    if (second.st_size,second.st_mtime_ns)!=(third.st_size,third.st_mtime_ns):
        raise ValueError('file_changed_during_hash')
    suffix = path.suffix.lower()
    if suffix in ('.xlsx','.docx','.zip'):
        with zipfile.ZipFile(path) as archive:
            if sum(x.file_size for x in archive.infolist())>250*1024*1024:
                raise ValueError('archive_expansion_out_of_bounds')
            if archive.testzip() is not None:
                raise ValueError('zip_crc_invalid')
            required = {'.xlsx':'xl/workbook.xml','.docx':'word/document.xml'}.get(suffix)
            if required and required not in archive.namelist():
                raise ValueError('wrong_office_format')
    return {'path':str(path),'bytes':third.st_size,'sha256':digest,'format':suffix[1:],
            'mtime_ns':third.st_mtime_ns,'file_verified':True,'source_provenance':'explicitly_selected_local_file; not a verified remote download'}


def serializable(value):
    return value.isoformat() if isinstance(value,(datetime,date)) else value


def read_document_file(path):
    receipt = verify_selected_file(path)
    suffix = Path(path).suffix.lower()
    if suffix=='.pdf':
        from pypdf import PdfReader
        with Path(path).open('rb') as handle:
            if not handle.read(8).startswith(b'%PDF-'):
                raise ValueError('wrong_pdf_format')
        reader = PdfReader(path,strict=True)
        if reader.is_encrypted:
            return {'ok':False,'status':'encrypted_document_requires_human','file':receipt}
        if len(reader.pages)>3000:
            raise ValueError('page_budget_exceeded_no_partial_read')
        units = [{'page':i+1,'text':page.extract_text() or ''} for i,page in enumerate(reader.pages)]
        pending = [u['page'] for u in units if not u['text'].strip()]
        if hashlib.sha256(Path(path).read_bytes()).hexdigest()!=receipt['sha256']:
            raise ValueError('source_changed_during_read')
        return {'ok':not pending,'status':'ocr_or_empty_page_review_required' if pending else 'text_layer_read',
                'file':receipt,'units':units,'unit_count':len(units),'pending_pages':pending,
                'full_document_read':False,'coverage':'all_pdf_text_layers','ocr_provider':'MinerU only',
                'gaps':['images and page-layout meaning not interpreted']}
    if suffix!='.xlsx':
        return {'ok':False,'status':'reader_not_supported','file':receipt}
    from openpyxl import load_workbook
    book = load_workbook(path,read_only=False,data_only=False,keep_links=False)
    cached = load_workbook(path,read_only=True,data_only=True,keep_links=False)
    units = []
    try:
        if sum(s.max_row*s.max_column for s in book.worksheets)>2_000_000:
            raise ValueError('cell_budget_exceeded_no_partial_read')
        for sheet in book.worksheets:
            units.append({'sheet':sheet.title,'state':sheet.sheet_state,
                          'rows':[[serializable(x) for x in row] for row in sheet.iter_rows(values_only=True)],
                          'cached_rows':[[serializable(x) for x in row] for row in cached[sheet.title].iter_rows(values_only=True)],
                          'merged_ranges':[str(x) for x in sheet.merged_cells.ranges],
                          'max_row':sheet.max_row,'max_column':sheet.max_column})
    finally:
        cached.close()
        book.close()
    if hashlib.sha256(Path(path).read_bytes()).hexdigest()!=receipt['sha256']:
        raise ValueError('source_changed_during_read')
    return {'ok':True,'status':'cells_read','file':receipt,'units':units,
            'unit_count':len(units),'cell_content_complete':True,'formulas_calculated':False,
            'full_document_read':False,'gaps':['drawings/charts not interpreted','cached formula values can be absent; no recalculation']}
