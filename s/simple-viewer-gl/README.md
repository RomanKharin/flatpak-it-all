# Simple Viewer GL

## Building

    flatpak-builder --repo=test-repo build manifest.json
    
## Install via test repository

    flatpak --user remote-add --no-gpg-verify --if-not-exists test-flatpak-sviewgl test-repo
    
    flatpak --user install test-flatpak-sviewgl test.flatpak.simple_viewer_gl_2_82
    
## Run

    flatpak run test.flatpak.simple_viewer_gl_2_82
    
## Notes:

1. Based on org.freedesktop.Platform
1. Glfw built from sources
1. All home dir are availiable
1. Uses GL
1. There are bug with flatpak+nvidia

## Bug monitoring list:

1. [NVIDIA: Issues with OpenGL support](https://github.com/flatpak/flatpak/issues/138)
1. [Notes from Alexander Larsson](https://blogs.gnome.org/alexl/2015/09/23/playing-games-with-runtime-extensions/)
1. [Extension utilities / docs](https://github.com/flatpak/flatpak/issues/72)
1. [Outdated script for generating GL extension](https://cgit.freedesktop.org/xdg-app/freedesktop-sdk-images/tree/make-nvidia-image.sh)
    
## Links and sources

1. https://bitbucket.org/andreyu/simple-viewer-gl

