#!/usr/bin/env python3
#
# susi-config
# Konfiguration of SUSI.AI, via the config.json

# TODO
# - configuration of susi server dedicated user in system install
# - creation of susi server user etc (see below)
# - uninstall: rm -rf ~/SUSI.AI  ~/.config/SUSI.AI/ ~/.local/share/systemd/user/ss-susi-*
#

import sys
import logging
from . import SusiConfig

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

Notes:
  - if path.base key is a literal . ("."), susi-config get path.base
    will try to return the absolute and resolved path of SUSI.AI directory
""")
    sys.exit(exitcode)



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

        else:
            raise ValueError("unknown action", args[1])

    except ValueError as ex:
        print("Invalid input: ", ex)
        usage(1)



if __name__ == '__main__':
    main(sys.argv)

