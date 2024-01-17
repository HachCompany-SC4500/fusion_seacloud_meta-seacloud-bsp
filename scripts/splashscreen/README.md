
# Prepare image for u-boot and kernel boot time

## Based on:
For u-boot:
https://developer.toradex.com/knowledge-base/u-boot-splash-screen
For linux:
https://developer.toradex.com/knowledge-base/splash-screen-linux

## Initial image
The image must be sized: **320x240**
LCD can RGB666 images (6 bits per color)
Some samples are available in **sources** folder

## Low color images
Kernel and bootloader can only display 224 indexed colors images
Use GIMP to move your 32bit RGB color to an indexed 224 color image (Image > Mode > Indexed ... and allow only 224 colors max), this will give better results than using automatic color selection by the Makefile commands.
Then switch back the image into RGB (Image > Mode > RGB).

## U-boot splash screen
Export the image as **hach.bmp** file (options 'Run-Length Encoded' not ticked and 'Do not write color space information' ticked) in the uboot folder and launch 'make' command.
Then copy the **toradex.bmp** generated file to overwrite **u-boot-toradex/tools/logos/toradex.bmp**

## Kernel splash screen
Export the image as **hachlogo_320x240.ppm** file (ppm format in RAW mode) in the kernel folder and launch 'make' command.
Then copy the **logo_custom_clut224.ppm** generated file to overwrite **linux-toradex/drivers/video/logo/logo_custom_clut224.ppm**.

## Image generation
Now, you just have to rebuild an image (u-boot, kernel and final image) and you will have the updated splash screens



