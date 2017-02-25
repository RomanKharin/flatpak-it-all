# Python 3.6 with tkinter

## Building

    flatpak-builder --repo=test-repo build manifest.json
    
## Install via test repository

    flatpak --user remote-add --no-gpg-verify --if-not-exists test-flatpak-python test-repo
    
    flatpak --user install test-flatpak-python test.flatpak.python3_6
    
## Run

Run python interpreter

    flatpak run test.flatpak.python3_6
    
Run idle

    flatpak --command=idle3 run test.flatpak.python3_6

## Notes:

1. Based on org.freedesktop.Platform
1. Tcl and Tk built from sources
1. All home dir are availiable
    
## Links and sources

1. Python https://www.python.org/
1. Tcl and Tk https://tcl.tk/
1. Blender python [manifest(s) for flatpak-builder](https://framagit.org/bochecha/blender-flatpak/tree/master/python)

