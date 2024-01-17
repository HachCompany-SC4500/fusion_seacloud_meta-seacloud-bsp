
# u-boot recipe

## History
The original Toradex BSP point on a Toradex custom version of u-boot.
During SCR1 project, all modifications where applied as patches.

This is not convenient for:
* modifications: it is needed to start a devshell yocto environment and then use quilt tool to update patches
* reviews/history: it is very hard to read during reviews and in the git history the diff of patches

To simplify the modification (gpio, dtb, custom patches, etc), the u-boot repository of Toradex has been duplicated in Stash.
Now all modifications of the u-boot are done in that repository.

## Update to a newer BSP
To migrate to a newer BSP, you have to also update u-boot.

To do it, follow these steps:
* clone the repository locally (take several minutes)
> git clone ssh://git@stash.waterqualitytools.com:7999/fcfw/fusion_seacloud_u-boot.git
* add a new Toradex remote repository that points on original Toradex repository
> git add remote toradex https://git.toradex.com/u-boot-toradex.git/
* fetch new commits from Toradex remote
> git fetch toradex
* create a branch for the old branch
> git branch SCR2_2.8b3
* rebase the Hach modifications (from the old Toradex branch) on the new Toradex branch and fix conflict if any
> git rebase --onto [new toradex branch] [old toradex branch] SCR2

## Source repository
The original u-boot toradex repository is https://git.toradex.com/cgit/u-boot-toradex.git/ ( available at: https://git.toradex.com/u-boot-toradex.git/)


