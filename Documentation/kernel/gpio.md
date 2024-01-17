## GPIO management
This is a cheatsheet that can used during gpio configuration.

Typical usage of GPIO are:
* properly configure a GPIO in the dtb
* configure/set a gpio in u-boot or drivers

To do that, it is needed to:
* identify a GPIO
* properly reference a GPIO in dtb, u-boot or drivers
* check setting of a given GPIO

### Identifying a GPIO
To find the GPIO connected to a SODIMM pins use the Toradex documentation (colibri_arm_som_imx7_datasheet.pdf) that gives the i.MX7 Ball Name for each SODIMM pin.  
It will quickly provide the GPIO Ball Name.

### Reference a GPIO
The gpio can be reference by different way:
* By gpio integer
It is used by:
* some dtb properties
* by gpio_set_value command from u-boot or some kernel driver
* by /sys/class/gpio/export interface

The gpio integer reference number can be computed from the gpio with the following formula: gpio integer = (gpio - 1) * 32 + IO  
e.g. : for SODIMM 98 - Ball Name SD2_RESET_B - ALT5 gpio is gpio5.IO[11], the gpio integer is 139 : gpio numer = (5 - 1) * 32 + 11 = 139

### Check GPIO settings
There is different options to get gpio settings.  
It is possible to quickly list pin in gpio mode with "cat /sys/kernel/debug/gpio". It lists if it is an input/output, the level and if it is linked to an IRQ.  
It is possible to get detailed configuration from /sys/kernel/debug/pinctrl/xxxx/ interface.  
For each pins:
/sys/kernel/debug/pinctrl/30330000.iomuxc/pinconf-pins gives the pad settings (pull up/down, etc)  
/sys/kernel/debug/pinctrl/30330000.iomuxc/pinmux-pins gives the mux configurations (which driver use it) and pin group.
