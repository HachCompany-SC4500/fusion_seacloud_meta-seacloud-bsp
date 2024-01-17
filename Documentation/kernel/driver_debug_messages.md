## Enable linux kernel driver dev_dbg debug messages
This is a cheat sheet that can be used during kernel driver debug activities.  
The complete documentation can be read in linux kernel documentation: "Documentation/dynamic-debug-howto.txt".

The symbol dev_dbg() disappears at compile-time to allow developer to keep debug code without runtime penalties.
It is possible to reactivate them for a whole module, a file or a specific line in a file.  
Pay attention that the way to enable them is different if the driver is a kernel module or if it is a built-in driver.

### Activate dynamic debug in kernel configuration
* With menuconfig, set the configuration "CONFIG_DYNAMIC_DEBUG" to yes.
* With menuconfig set CONFIG_MESSAGE_LOG_LEVEL_DEFAULT to 7. (maybe not necessary...)
* Then replace defconfig file with the new configuration file.

### Built-in driver: select the part of code for which you want to enable the dev_dbg messages
The code for which debug messages must be enabled can be selected by passing an argument to the kernel command line.  
For example, for having all debug messages concerning the USB driver, pass to the kernel the argument:
* dyndbg="file drivers/usb/* +plmf"

The double quotes must be properly included.  
To do so, in SCR2, starts the board with the debug cable, stops uboot and at uboot prompt type:
* setenv defargs dyndbg="\"file drivers/usb/* +pmlf\""
* saveenv

To check the arguments given to the kernel:
* cat /proc/cmdline

The flags as "pmlf" are described in "dynamic-debug-howto.txt" article.

### Retrieve messages
They can be seen with dmesg command.
* dmesg | grep -i USB

