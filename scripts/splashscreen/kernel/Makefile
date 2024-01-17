.SILENT:

all: logo_custom_clut224.ppm

logo_custom_clut224.ppm: hachlogo_320x240_224.ppm
	pnmnoraw $< > $@
	rm $<
	echo "You can now copy updated $@ into linux-toradex/drivers/video/logo/"

hachlogo_320x240_224.ppm: hachlogo_320x240.ppm
	ppmquant 224 $< > $@

hachlogo_320x240.ppm:
	echo "$@ file is missing"
	echo "It must be an 320x240 pixels image in ppm raw format"
	exit 2



