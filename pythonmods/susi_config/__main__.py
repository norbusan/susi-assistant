#!/usr/bin/env python3
#
# susi-config
# Konfiguration of SUSI.AI, via the config.json

import sys
import os
from pathlib import Path
from . import SusiConfig

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
  susi-config install links DIR
         Install links to user programs into DIR
  susi-config install desktop user|system
         Install desktop files into user or system directories
  susi-config install systemd user|system
         Install systemd service files into user or system directories

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
            print("Possible keys:")
            for i in cfg.defaults.keys():
                print(f"  {i}")

        elif args[1] == 'set':
            cfg = SusiConfig()
            for kv in args[2:]:
                k,v = kv.split('=', 2)
                if k in cfg.defaults:
                    pass
                else:
                    raise ValueError('unknown key', k)
                cfg.get_set(k,v)

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
            import susi_python as susi
            susi.sign_in(cfg.config['susi.user'],
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


        # susi-config install links DIR
        # susi-config install desktop user|system
        # susi-config install systemd user|system
        elif args[1] == 'install':
            if len(args) != 4:
                raise ValueError("incorrect invocation of install action", args[2:])

            if args[2] == 'links':
                if not os.path.exists(args[3]):
                    raise ValueError("target directory not existing", args[3])
                susiai_bin = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../../bin"))
                if not os.path.isdir(susiai_bin):
                    raise ValueError("cannot find SUSI.AI/bin directory", susiai_bin)
                for f in os.listdir(susiai_bin):
                    os.symlink(os.path.join(susiai_bin, f), os.path.join(args[3], f))  

            elif args[2] == 'desktop':
                if args[3] == 'user':
                    destdir = str(Path.home()) + '/.config/share/applications'
                elif args[3] == 'system':
                    destdir = '/usr/local/share/applications'
                else:
                    raise ValueError("unknown mode for install desktop", args[3])
                susiai_dir = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../.."))
                if not os.path.isdir(susiai_dir):
                    raise ValueError("cannot find SUSI.AI directory", susiai_dir)
                susi_linux_dir = os.path.join(susiai_dir, 'susi_linux')
                susi_server_dir = os.path.join(susiai_dir, 'susi_server')
                if not os.path.isdir(susi_linux_dir):
                    raise ValueError("cannot find SUSI.AI susi_linux directory", susi_linux_dir)
                if not os.path.isdir(susi_server_dir):
                    raise ValueError("cannot find SUSI.AI susi_server directory", susi_server_dir)
                if not os.path.exists(destdir):
                    os.makedirs(destdir)
                desktop_files = []
                for f in os.listdir(os.path.join(susi_server_dir, "system-integration/desktop")):
                    if f.endswith("desktop.in"):
                        desktop_files.append(f)
                for f in os.listdir(os.path.join(susi_linux_dir, "system-integration/desktop")):
                    if f.endswith("desktop.in"):
                        desktop_files.append(f)
                for f in desktop_files:
                    pass


                print(f"TODO installing desktop files into {destdir}")
            elif args[2] == 'systemd':
                # TODO should we install some services into systemduserunitdir = /usr/lib/systemd/user?
                if args[3] == 'user':
                    destdir = str(Path.home()) + "/.config/systemd/user"
                elif args[3] == 'system':
                    destdir = self.__run_pkgconfig("/lib/systemd/system",
                            'pkg-config', 'systemd', '--variable=systemdsystemunitdir')
                else:
                    raise ValueError
                print(f"TODO installing systemd files into {destdir}")
            else:
                raise ValueError("unknown variant of install action", args[2])

        else:
            raise ValueError("unknown action", args[1])

    except ValueError as ex:
        print("Invalid input: ", ex)
        usage(1)



if __name__ == '__main__':
    main(sys.argv)

