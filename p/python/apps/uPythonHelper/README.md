# uPythonHelper

## Building

Compile full version

    flatpak-builder --repo=test-repo buildupythonhelper manifest.json
    
Compile minimal runnable version (85% smaller)

    flatpak-builder --repo=test-repo buildupythonhelper manifest_pack.json

## Install via test repository

    flatpak --user remote-add --no-gpg-verify --if-not-exists test-flatpak-upythonhelper test-repo
    
    flatpak --user install test-flatpak-upythonhelper test.flatpak.upythonhelper
    
## Run

Run python interpreter

    flatpak run test.flatpak.upythonhelper
    
## Notes:

1. Based on org.freedesktop.Platform
1. All home dir are availiable
1. Depencies are embedded (pyserial2, serial-device2)
    
## Links and sources

1. https://github.com/casten/uPythonHelper

