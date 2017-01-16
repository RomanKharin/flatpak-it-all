#!/usr/bin/env python3
# -*- coding: utf8 -*-

# Find unused files and directories
# romiq.kh@gmail.com, 2017
#
# strace -f -e open,process flatpak run some.test.app 2& > strace.log
# findunused.py strace.log builddir/files/

import sys
import os
import argparse
import pathlib
import json

def sizeof_fmt(num, suffix = "B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, "Yi", suffix)

def main(stracelog, builddir, usejson = False, verbose = False, 
        python_specific = []):
    # parse log
    usedfiles = set()
    if verbose and not usejson:
        print("Parse file strace log:\t%s" % stracelog)
    usedlinks = set()
    def adduseditem(item):
        if not path.startswith("/app"): return
        usedfiles.add(item)
        
    with open(stracelog, "r") as f:
        for line in f.readlines():
            line = line.rstrip()
            if line.startswith("[pid "):
                p = line.find("]", 5) # len("[pid ") == 5
                if p >= 0:
                    line = line[p + 1:].lstrip()
            dline = ""
            if line.startswith("open("):
                dline = line[5:]
            elif line.startswith("execve("):
                dline = line[7:]
            if dline:
                p = dline.find("\"", 1)
                if p >= 0:
                    path = dline[1:p]
                    adduseditem(path)
                    # detect symbolic links
                    full = path[4:]
                    if full.startswith("/"):
                        full = full[1:]
                    full = os.path.join(builddir, full)
                    if os.path.exists(full):
                        link = pathlib.Path(full)
                        if link.is_symlink():
                            usedlinks.add(path)
                            rel = os.path.relpath(
                                str(link.resolve()), os.path.dirname(full))
                            dst = os.path.join(os.path.dirname(path), rel)
                            if verbose and not usejson:
                                print("  link %s -> %s" % (path, dst))
                            adduseditem(dst)
                    # python_specific
                    if path.endswith(".pyc") and python_specific:
                        if verbose and not usejson:
                            print("  cache %s" % (path))
                        for ps in python_specific:
                            if path.endswith("." + ps + ".pyc"):
                                # find module name
                                p2 = path.split("/")
                                if len(p2) >= 2 and p2[-2] == "__pycache__":
                                    modname = p2[-1][:-len(ps) - 5] + ".py"
                                    modpath = "/".join(p2[:-2] + [modname])
                                    if verbose and not usejson:
                                        print("  -> file %s" % (modpath))
                                    adduseditem(modpath)                                
                        
    if verbose and not usejson:
        print("  found:\t\t%d items" % len(usedfiles))

    unusedfiles = []
    unuseddirs = []
    szused = 0
    cntused = 0
    szunused = 0
    cntunused = 0
    for root, dirs, files in os.walk(builddir, topdown = False):
        assert root.startswith(builddir)
        approot = root[len(builddir):]
        if not approot.startswith("/"):
            approot = "/" + approot
        # /app prefix is not required for cleanup option
        cleanroot = approot
        approot = "/app" + approot
        if verbose and not usejson:
            print("Scan folder %s" % approot)
        cntud = 0
        unuseditems = []
        dusedd = []
        for dname in dirs:
            if os.path.join(approot, dname) in unuseddirs:
                cntud += 1
                unuseditems.append(dname + "/")
            else:
                dusedd.append(dname)
        cntu = 0
        dszused = 0
        dszunused = 0
        dused = []
        for fname in files:
            appfname = os.path.join(approot,fname)
            full = os.path.join(root, fname)
            sz = os.path.getsize(full)
            # do not count links
            link = pathlib.Path(full)
            if link.is_symlink():
                sz = 0
            if not appfname in usedfiles:
                # add to unused
                szunused += sz
                dszunused += sz
                cntunused += 1
                cntu += 1
                unuseditems.append(fname)
            else:
                szused += sz
                dszused += sz
                cntused += 1
                dused.append((fname, sz))
        if verbose and not usejson:
            print("  folders:\t%d" % len(dirs))
            print("  files:\t%d, %s" % (len(files),
                sizeof_fmt(dszused + dszunused)))
            if dusedd:
                print("  used folders:\t%d" % len(dusedd))
                for item in dusedd:
                    print("    %s" % item)
            if dused:
                print("  used files:\t%d, %s" % (len(dused),
                    sizeof_fmt(dszused)))
                for item, sz in dused:
                    print("    %s, %s" % (item, sizeof_fmt(sz)))

        if len(files) == cntu and len(dirs) == cntud:
            unuseddirs.append(approot)
            if verbose and not usejson:
                print("  all unused")
        else:
            # append all unused
            if verbose and not usejson:
                print("  unused items: (%d)" % len(unuseditems))
            for item in unuseditems:
                unusedfiles.append(os.path.join(cleanroot, item))
                if verbose and not usejson:
                    print("    %s" % item)

    unusedfiles.sort()
    if usejson:
        print(json.dumps(unusedfiles, indent = 4))
    else:
        print("Processed files:\t%d, %s" % (cntused + cntunused, 
            sizeof_fmt(szused + szunused)))
        print("    used:\t\t%d, %s" % (cntused, sizeof_fmt(szused)))
        print("  unused:\t\t%d, %s" % (cntunused, sizeof_fmt(szunused)))
        print("Exclude items: (%d)" % len(unusedfiles))
        for item in unusedfiles:
            print(item)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stracelog", help = \
        "strace log file (strace -f -e open,process ...)")
    parser.add_argument("builddir", help = \
        "path to files directory (/app root)")
    parser.add_argument("--json", help = \
        "output unused files and directories in JSON format",
        action = "store_true")
    parser.add_argument("-v", "--verbose", help = \
        "verbose outout",
        action = "store_true")
    parser.add_argument("-pc", "--python-specific", action = "append",
        help = "detect __pycache__/module.PYTHON_SPECIFIC.pyc"\
        " using as module.py")
    args = parser.parse_args()

    main(stracelog = args.stracelog, builddir = args.builddir, 
        usejson = args.json, verbose = args.verbose, 
        python_specific = args.python_specific)

