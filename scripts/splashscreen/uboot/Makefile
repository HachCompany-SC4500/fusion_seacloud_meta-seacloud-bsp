.SILENT:

all: toradex.bmp

toradex.bmp: hach.bmp
	convert $< -type Palette -colors 224 -compress none -verbose BMP3:$@
	echo "You can now copy updated $@ over u-boot-toradex/tools/logos/toradex.bmp"

hach.bmp:
	echo "$@ file is missing"
	echo "It must be an 320x240 pixels image in RGB"
	exit 2


