require recipes-bsp/u-boot/u-boot-hach.inc

FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI += " \
	file://fw_unlock_mmc.sh \
	file://fw_env.config \
"

install_unlock_emmc() {
    install -d ${D}${sysconfdir}/profile.d/
    install -m 0644 ${WORKDIR}/fw_unlock_mmc.sh ${D}${sysconfdir}/profile.d/fw_unlock_mmc.sh
    install -m 0644 ${WORKDIR}/fw_env.config ${D}${sysconfdir}/fw_env.config
}

do_install_append_colibri-imx7-emmc-1370() {
    install_unlock_emmc
}

