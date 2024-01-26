FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"

# Replace original Toradex git URL
SRC_URI_remove = "git://git.toradex.com/linux-toradex.git;protocol=git;branch=${SRCBRANCH}"
SRC_URI_prepend = "git://github.com/HachCompany-SC4500/fusion_seacloud_linux.git;branch=${SRCBRANCH} "

# Patch only used by EE for HALT test purpose
#SRC_URI += "file://0001-Use-high-maximum-temperature-300-C-limitation-for-HA.patch"

SRC_URI += "\
	file://0002-Add-RTL8812AU-preparations.patch \
	file://0003-Add-RTL8812AU-driver.patch \
"

# To be used for master
SRCREV = "1feace70fa8e9f1b9aaf2e7fdc0dc47aa575fc3a"
SRCBRANCH="github_publication_SC4500"

# To be use during development to follow automatically new commits
#SRCREV = "${AUTOREV}"
#SRCBRANCH = "feature/FCON2-877-update-gpio-settings-to-new-1370"

# Add goodix to /etc/modules-load.d/ to be automatically loaded at startup
# Not needed for the Cypress driver (cyttsp5_i2c)
KERNEL_MODULE_AUTOLOAD += "goodix"
