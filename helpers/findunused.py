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

def main(stracelog, builddir, usejson = False):
    # parse log
    usedfiles = set()
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
                    if not path.startswith("/app"): continue
                    usedfiles.add(path)
                    # detect symbolic links
                    full = path[4:]
                    if full.startswith("/"):
                        full = full[1:]
                    full = os.path.join(builddir, full)
                    if os.path.exists(full):
                        link = pathlib.Path(full)
                        if link.is_symlink():
                            rel = os.path.relpath(str(link.resolve()), os.path.dirname(full))
                            dst = os.path.join(os.path.dirname(path), rel)
                            if dst.startswith("/app"):
                                usedfiles.add(dst)

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
        cntud = 0
        unuseditems = []
        for dname in dirs:
            if os.path.join(approot, dname) in unuseddirs:
                cntud += 1
                unuseditems.append(dname + "/")
        cntu = 0
        for fname in files:
            appfname = os.path.join(approot,fname)
            full = os.path.join(root, fname)
            sz = os.path.getsize(full)
            if not appfname in usedfiles:
                # add to unused
                szunused += sz
                cntunused += 1
                cntu += 1
                unuseditems.append(fname)
            else:
                szused += sz
                cntused += 1
        if len(files) == cntu and len(dirs) == cntud:
            unuseddirs.append(approot)
        else:
            # append all unused
            for item in unuseditems:
                unusedfiles.append(os.path.join(cleanroot, item))

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
    args = parser.parse_args()

    main(stracelog = args.stracelog, builddir = args.builddir, 
        usejson = args.json)

