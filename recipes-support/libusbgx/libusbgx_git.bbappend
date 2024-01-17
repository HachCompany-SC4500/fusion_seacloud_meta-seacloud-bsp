# Disable usbg.service, as the support to usb gadget has been removed from Kernel
SYSTEMD_AUTO_ENABLE_${PN} = "disable"

