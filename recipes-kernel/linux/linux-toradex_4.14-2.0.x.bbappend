FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"

# Replace original Toradex git URL
SRC_URI_remove = "git://git.toradex.com/linux-toradex.git;protocol=git;branch=${SRCBRANCH}"
SRC_URI_prepend = "git://github.com/HachCompany-SC4500/fusion_seacloud_linux.git;branch=${SRCBRANCH} "

# Patch only used by EE for HALT test purpose
#SRC_URI += "file://0001-Use-high-maximum-temperature-300-C-limitation-for-HA.patch"

# Patch disabled as it caused issues to disable Watchdog during the reboot
# sequence; e.g. when the kernel hangs in a later reboot phase.
# It is kept here in the recipe in case it must be enabled again. However, it
# should not go in production for the mean time. See FCON2-2168 for more details.
#SCR_URI += "file://0014-add-restart-notifier-hook-to-stop-the-watchdog-durin.patch"

SRC_URI += "\
	file://0002-Add-RTL8821AU-preparations.patch \
	file://0003-Add-RTL8821AU-driver.patch \
	file://0004-Revert-block-Unexport-elv_register_queue-and-elv_unr.patch \
	file://0005-crypto-caam-add-backlogging-support.patch \
	file://0006-ARM-dts-imx7-add-alias-for-Ethernet-controllers.patch \
	file://0007-Fix-kernel-panic-hang.patch \
	file://0008-Add-detailed-logs-of-the-low-level-touchscreen-frame.patch \
	file://0009-MLK-22025-1-usb-chipidea-phy-enter-low-power-mode-wh.patch \
	file://0010-MLK-22025-3-usb-chipidea-enter-lpm-when-imx7d-host-s.patch \
	file://0011-Fix-fuse-programming.patch \
	file://0012-update-imx7d-configs-to-mask-out-unused-imx_rpmsg-dr.patch \
	file://0013-Add-DT-entry-for-rn5t618-watchdog-as-a-part-of-multi.patch \
"

# Revision to be used for current branch
SRCREV = "7cff19901a35ca9fbdaffec8e2526da0d8345896"
SRCBRANCH="github_publication_SC4500"

# Use AUTOREV only during development to follow automatically new commits on a branch
#SRCREV = "${AUTOREV}"
#SRCBRANCH = "feature/FCON2-3437-reduce-450mhz-noise-comming-from-2nd-ethernet"

