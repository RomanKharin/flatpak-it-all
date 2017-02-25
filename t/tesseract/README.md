# Tesseract

## Building

    flatpak-builder --repo=test-repo build manifest.json
    
## Install via test repository

    flatpak --user remote-add --no-gpg-verify --if-not-exists test-flatpak-tesseract test-repo
    
    flatpak --user install test-flatpak-tesseract test.flatpak.tesseract
    
## Run

Run tesseract

    flatpak run test.flatpak.tesseract
    
## Notes:

1. Based on org.freedesktop.Platform
1. Master
1. Do no use ccache while build
    
## Links and sources

1. https://github.com/tesseract-ocr/tesseract

