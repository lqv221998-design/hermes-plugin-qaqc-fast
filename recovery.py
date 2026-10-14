"""Controlled lifecycle repair of the bound QAQC Chrome, not a controller fallback."""
import json
from pathlib import Path
import socket
import subprocess
import time
from urllib.request import ProxyHandler,build_opener
from .mineru import NoRedirect


def browser_owners():
    script = Path(__file__).with_name('browser_owners.ps1')
    result = subprocess.run(['powershell.exe','-NoProfile','-File',str(script)],capture_output=True,encoding='utf-8',timeout=15,check=True)
    data = json.loads(result.stdout.lstrip('\ufeff'))
    return data if isinstance(data,list) else [data] if isinstance(data,dict) else []


def canonical(value):
    return str(Path(value).resolve()).casefold()


def endpoint_version(port):
    opener = build_opener(ProxyHandler({}),NoRedirect())
    try:
        with opener.open(f'http://127.0.0.1:{port}/json/version',timeout=0.5) as response:
            data = json.load(response)
        return data if isinstance(data,dict) and str(data.get('Browser','')).startswith('Chrome/') else None
    except (OSError,ValueError):
        return None


def launch_chrome(argv):
    return subprocess.Popen(argv,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,
                            creationflags=getattr(subprocess,'CREATE_NEW_PROCESS_GROUP',0))


def recover_owned_browser(executable,profile,port,*,launch_fn=None,owner_probe=None):
    exe,profile = Path(executable),Path(profile)
    if not exe.is_file() or exe.name.lower()!='chrome.exe' or not profile.is_dir() or type(port) is not int or not 1024<=port<=65535:
        raise ValueError('browser_restore_binding_unverified')
    launch_fn,owner_probe = launch_fn or launch_chrome,owner_probe or browser_owners
    def exact_owner():
        owners = owner_probe()
        same_profile = [x for x in owners if x.get('UserDataDir') and canonical(x['UserDataDir'])==canonical(profile)]
        matched = [x for x in same_profile if x.get('DebugPort')==port and x.get('Executable') and canonical(x['Executable'])==canonical(exe)]
        return same_profile,matched
    same,matched = exact_owner()
    live = endpoint_version(port)
    if live and len(matched)==1:
        return {'ok':True,'status':'browser_owner_verified','restored':False,'business_verified':False,'pid':matched[0]['Pid']}
    if same:
        return {'ok':False,'status':'owner_process_exists_needs_human_lifecycle_repair','restored':False,'business_verified':False}
    with socket.socket() as reserve:
        try:
            reserve.bind(('127.0.0.1',port))
        except OSError:
            return {'ok':False,'status':'port_owned_or_unavailable_no_launch','restored':False,'business_verified':False}
    # Existing recipient profile only: no copy, no reset, no kill, no connector change.
    argv = [str(exe),'--user-data-dir='+str(profile),'--remote-debugging-port='+str(port),
            '--remote-debugging-address=127.0.0.1','--new-window','https://qaqc.newtecons.vn/']
    launch_fn(argv)
    deadline = time.monotonic()+15
    while time.monotonic()<deadline:
        if endpoint_version(port):
            _,matched = exact_owner()
            if len(matched)==1:
                return {'ok':True,'status':'browser_owner_restored','restored':True,'business_verified':False,'pid':matched[0]['Pid'],
                        'instruction':'Use original executor pages/inspect. Human login/project selection may remain pending.'}
        time.sleep(0.25)
    return {'ok':False,'status':'browser_restore_uncertain_no_replay','restored':False,'business_verified':False}
