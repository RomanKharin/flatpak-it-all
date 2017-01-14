# Micropython 1.8.7 for unix

## Building

    flatpak-builder --repo=test-repo build manifest_unix.json
    
## Install via test repository

    flatpak --user remote-add --no-gpg-verify --if-not-exists test-flatpak-micropython test-repo
    
    flatpak --user install test-flatpak-micropython test.flatpak.micropython
    
## Run

Run micropython interpreter

    flatpak run test.flatpak.micropython
    
## Notes:

1. Based on org.freedesktop.Platform
1. Built from git branch v1.8.7
1. All home dir are availiable
    
## Links and sources

1. Micropython https://github.com/micropython/micropython

