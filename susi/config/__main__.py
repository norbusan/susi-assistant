#!/usr/bin/env python3
#
# susi-config
# Konfiguration of SUSI.AI, via the config.json

import sys
import os
import logging
import shutil
import urllib.request
from . import SusiConfig

FLITE_URL = 'http://www.festvox.org/flite/packed/flite-2.0/voices/cmu_us_slt.flitevox'
DEEPSPEECH_URL = 'https://github.com/mozilla/DeepSpeech/releases/download/v%s'

logger = logging.getLogger(__name__)

def usage(exitcode):
    print("""susi-config -- SUSI.AI configuration utility
Usage:
  susi-config init [-f]
         Create minimal configuration file, overwrite previous one with -f
  susi-config keys
         Lists all possible keys
  susi-config get [ key key ... ]
         Retrieves a set of keys, all if no argument is given
  susi-config set key=value [ key=value ... ]
         Sets a set of keys to values
  susi-config login
         Tries to log into the SUSI.AI Server
  susi-config (un)install flite-data
  susi-config (un)install deepspeech-data
         Install or uninstall flite TTS and deepspeech STT required data.

Notes:
  - if path.base key is a literal . ("."), susi-config get path.base
    will try to return the absolute and resolved path of SUSI.AI directory
""")
    sys.exit(exitcode)

def download_file_with_progress(url, target):
    dirn = os.path.dirname(target)
    if not os.path.exists(dirn):
        os.makedirs(dirn)
    with urllib.request.urlopen(url) as resp, open(target, "wb") as f:
        length = resp.getheader('content-length')
        if length:
            length = int(length)
            blocksize = max(4096, length//100)
        else:
            blocksize = 1000000 # just made something up

        print(f"Downloading file {url}, length={length}, using blocksize={blocksize}")

        size = 0
        while True:
            buf1 = resp.read(blocksize)
            if not buf1:
                break
            f.write(buf1)
            size += len(buf1)
            if length:
                print('{:.0f}%\rdone '.format(100.*(size/length)), end='')
        print()


def install_uninstall(args):
    if len(args) < 3:
        raise ValueError(f"incorrect invocation of {args[1]} action", args[2:])
    if args[2] == 'flite-data':
        if len(args) > 3:
            raise ValueError(f"incorrect invocation of {args[1]} action", args[2:])
    elif args[2] == 'deepspeech-data':
        if len(args) > 4:
            raise ValueError(f"incorrect invocation of {args[1]} action", args[2:])
        elif len(args) == 4 and args[3] != "en-US":
            raise ValueError(f"currently only en_US is supported language for DeepSpeech data", args[2:])
    else:
        raise ValueError(f"incorrect invocation of {args[1]} action", args[2:])

    cfg = SusiConfig()
    basepath = cfg.get('path.base')
    flitep = cfg.get('path.flite_speech')
    dsp = cfg.get('path.deepspeech')

    if not os.path.isabs(flitep):
        flitep = os.path.abspath(os.path.join(basepath, flitep))
    if not os.path.isabs(dsp):
        dsp = os.path.abspath(os.path.join(basepath, dsp, "en-US"))

    if args[1] == 'install':
        if args[2] == 'flite-data':
            if not os.path.exists(flitep):
                download_file_with_progress(FLITE_URL, flitep)
                print(f"Successfully installed {flitep}")
            else:
                print(f"Already available: {flitep}")
        elif args[2] == 'deepspeech-data':
            # need to find the currently used deepspeech version number
            import deepspeech
            ds_version = deepspeech.version()
            if not os.path.exists(dsp):
                os.makedirs(dsp)
            for ext in ['pbmm', 'tflite', 'scorer']:
                fn = f"deepspeech-{ds_version}-models.{ext}"
                url = f"{DEEPSPEECH_URL % ds_version}/{fn}"
                dest = os.path.join(dsp, fn)
                if not os.path.exists(dest):
                    download_file_with_progress(url, dest)
                else:
                    print(f"Already available: {dest}")
            print(f"Successfully install DeepSpeech model files in {dsp}")
        else: # already checked above, though ...
            raise ValueError(f"incorrect invocation of {args[1]} action", args[2:])

    elif args[1] == 'uninstall':
        if args[2] == 'flite-data':
            if os.path.exists(flitep):
                try:
                    os.remove(flitep)
                    print(f"Removed {flitep}")
                except OSError as e:
                    print(f"Cannot remove flite file {flitep}\nError: {e.strerror}")
            else:
                print(f"Not present: {flitep}, nothing to remove!")
        elif args[2] == 'deepspeech-data':
            if os.path.exists(dsp) and os.path.isdir(dsp):
                try:
                    shutil.rmtree(dsp)
                    print(f"Removed directory {dsp}")
                except OSError as e:
                    print(f"Cannot remove DeepSpeech data dir {dsp}\nError: {e.strerror}")
            else:
                print(f"Either not present or not a directory: {dsp}, nothing to remove!")
        else: # already checked above, though ...
            raise ValueError(f"incorrect invocation of {args[1]} action", args[2:])

    else:
        raise ValueError("unknown variant of install action", args[2])




def main(args):
    if len(args) == 1 or args[1] == "-h" or args[1] == "--help":
        usage(0)

    try:
        if args[1] == 'keys':
            cfg = SusiConfig()
            print("Possible keys (if no options listed then the value is free form):")
            for i in cfg.defaults.keys():
                if 'options' in cfg.defaults[i]:
                    print(f"  {i} -- possible values: {', '.join(cfg.defaults[i]['options'])}")
                else:
                    print(f"  {i}")

        elif args[1] == 'set':
            cfg = SusiConfig()
            ans = [ "Values set to:" ]
            for kv in args[2:]:
                k,v = kv.split('=', 2)
                if k in cfg.defaults:
                    pass
                else:
                    raise ValueError('unknown key', k)
                newv = cfg.get_set(k,v)
                ans.append(f"  {k} = {newv} (requested {v})")
            print("\n".join(ans))

        elif args[1] == 'get':
            cfg = SusiConfig()
            if len(args) == 2:
                args = list(cfg.defaults.keys())
            else:
                args = args[2:]
            ret = []
            for k in args:
                v = cfg.get_set(k)
                if type(v) != type('str'):
                    ret.append(k + " = (unset)")
                else:
                    ret.append(k + " = " + str(v))
            for i in ret:
                print(i)

        elif args[1] == 'login':
            cfg = SusiConfig()
            if len(args) > 2:
                raise ValueError("too many arguments for action", 'login')
            import susi.server_api as susi_server
            susi_server.sign_in(cfg.config['susi.user'],
                                cfg.config['susi.pass'],
                                room_name=cfg.config['roomname'])

        elif args[1] == 'init':
            if len(args) == 2:
                force = False
            elif len(args) == 3:
                if args[2] == '-f':
                    force = True
                else:
                    raise ValueError("unsupported option to init", args[2])
            else:
                raise ValueError("unsupported options to init", args[2:])

            cfg = SusiConfig()
            for k,v in cfg.defaults.items():
                if force:
                    cfg.config[k] = v['default']
                else:
                    cfg.config.setdefault(k,v['default'])

        elif args[1] == 'install' or args[1] == 'uninstall':
            install_uninstall(args)

        else:
            raise ValueError("unknown action", args[1])

    except ValueError as ex:
        print("Invalid input: ", ex)
        usage(1)



if __name__ == '__main__':
    main(sys.argv)

