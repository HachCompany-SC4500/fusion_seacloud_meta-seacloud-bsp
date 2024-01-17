# Replace original Toradex git URL

# For u-boot-toradex
SRC_URI_remove = "git://git.toradex.com/u-boot-toradex.git;branch=${SRCBRANCH}"
# For u-boot-toradex-fsl-fw-utils_git
SRC_URI_remove = "git://git.toradex.com/u-boot-toradex.git;protocol=git;branch=${SRCBRANCH}"
# Since BSP 3.0
SRC_URI_remove = "git://git.toradex.com/u-boot-toradex.git;protocol=https;branch=${SRCBRANCH}"

SRC_URI_prepend = "git://github.com/HachCompany-SC4500/fusion_seacloud_u-boot.git;branch=${SRCBRANCH} "

# Revision to be used for current branch
SRCREV = "27ea0369b962c5b3b611b27cb32c2da6d82df1de"
SRCBRANCH="github_publication_SC4500"

# Use AUTOREV only during development to follow automatically new commits on a branch
#SRCREV = "${AUTOREV}"
#SRCBRANCH = "feature/FCON2-935-activate-ips-support"
