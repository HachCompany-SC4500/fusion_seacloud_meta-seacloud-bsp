# Check pin configuration tool #
This tool is used to compare the actual pin configuration of the Eagle controller's main processor, with the desired pin configuration specified in a CSV file, and report the result on the console.

## Components of the tool ##

Block diagram of the tool: [check\\_pin\\_configuration\\_tool.png](http://stash.waterqualitytools.com/projects/FCFW/repos/fusion_seacloud_meta-seacloud-bsp/browse/scripts/check-pin-configuration-tool/check_pin_configuration_tool.PNG?at=SCR2)

- **extract\_pin\_info.py** 

	Python script that runs on the development machine.

	It extracts the pin information from the Linux header files and creates a CSV file.

	It is located in [Fusion\\_SeaCloud\_meta-seacloud-bsp/scripts/check-pin-configuration-tool/extract\\_pin\\_info.py](http://stash.waterqualitytools.com/projects/FCFW/repos/fusion_seacloud_meta-seacloud-bsp/browse/scripts/check-pin-configuration-tool/extract_pin_info.py?at=refs%2Fheads%2FSCR2)

- **pin\_configuration\_vba.xlsm**

	Excel sheet that runs on the development machine. 
	
	It is used to generate the desired pin configuration file.

	It is located in [Fusion\\_SeaCloud\_meta-seacloud-bsp/scripts/check-pin-configuration-tool/pin\\_configuration\\_vba.xlsm](http://stash.waterqualitytools.com/projects/FCFW/repos/fusion_seacloud_meta-seacloud-bsp/browse/scripts/check-pin-configuration-tool/pin_configuration_vba.xlsm?at=SCR2)

- **check\_pin\_config.py**
	
	Python script that runs on the Eagle controller. 

	It compares the desired pin configuration from a CSV file with the actual one and reports the result on the console.

	It is contained in the Linux image, and can be found in the following folder of the Eagle controller: "/home/root/1370-testtools/".

	It is located in [Fusion\\_SeaCloud\\_meta-seacloud/recipes/recipes-diagnose/files/1370-testtools/check\\_pin\\_config.py](http://stash.waterqualitytools.com/projects/FCFW/repos/fusion_seacloud_meta-seacloud/browse/recipes/recipes-diagnose/files/1370-testtools/check_pin_config.py?at=refs%2Fheads%2FSCR2)

- **pin_info.csv**
	
	CSV file that contains generic pin information.

	It is contained in the Linux image, and can be found in the following folder of the Eagle controller: "/home/root/1370-testtools/".

	It is located in [Fusion\\_SeaCloud\_meta-seacloud/recipes/recipes-diagnose/files/1370-testtools/pin\\_info.csv](http://stash.waterqualitytools.com/projects/FCFW/repos/fusion_seacloud_meta-seacloud/browse/recipes/recipes-diagnose/files/1370-testtools/pin_info.csv?at=SCR2).
		
- **desired\_pin\_configuration.csv**
	
	CSV file that contains the desired pin configuration.

	It is located in [Fusion\\_SeaCloud\_meta-seacloud/recipes/recipes-diagnose/files/1370-testtools/desired\\_pin\\_configuration.csv](http://stash.waterqualitytools.com/projects/FCFW/repos/fusion_seacloud_meta-seacloud/browse/recipes/recipes-diagnose/files/1370-testtools/desired_pin_configuration.csv?at=SCR2).
	
	It is contained in the Linux image, and can be found in the following folder of the Eagle controller: "/home/root/1370-testtools.

## Usage ##

Although this section describes all the steps to setup the tool, the Eagle controller contains all the necessary scripts and the last up to date CSV files in the folder "/home/root/1370-testools/". So, the normal usage is to execute only the last three points of "Step 4: Check pin configuration in Eagle controller".
   
**1. Generate pin_info**

This step needs to be executed only once. 

The goal is to generate the "pin_info.csv" file, which is needed by pin\_configuration\_vba.xlsm, and also by check\_pin\_configuration.py

The file has been already generated (see "Components of the tool" section to know its location), but you can see below the steps to generate it: 

- Create a folder in your Linux development machine, e.g. "extract\_pin\_info"
- Copy the following files in that folder:
	- extract\_pin\_info.py 
	- imx7d-pinfunc.h, located in [Fusion\\_SeaCloud\_linux/arch/arm/boot/dts/imx7d-pinfunc.h](http://stash.waterqualitytools.com/projects/FCFW/repos/fusion_seacloud_linux/browse/arch/arm/boot/dts/imx7d-pinfunc.h)
	- imx7d-pinfunc-lpsr.h, located in [Fusion\\_SeaCloud\_linux/arch/arm/boot/dts/imx7d-pinfunc-lpsr.h](http://stash.waterqualitytools.com/projects/FCFW/repos/fusion_seacloud_linux/browse/arch/arm/boot/dts/imx7d-pinfunc-lpsr.h)
- Execute the Ptyhon script: "./extract\_pin\_info.py".The "pin\_info.csv" file will be created in the same folder. For further details and options regarding extract\_pin\_info.py, execute "./extract\_pin\_info.py -h"


**2. Setup up the pin information of the Excel sheet**

This step needs to be executed only once (or, of course, everytime pin\_info.csv file is updated)

The goal is to provide all information about pins to the the Excel sheet used to generate the desired pin configuration CSV file.

The Excel sheet has been already set up (see "Components of the tool" section to know its location), but yo can see below the steps to setup it:

- Create a folder in your Windows development machine, e.g. "generate\_desired\_configuration"
- Copy the following files in that folder:
	- pin\_info.csv file obtained in Step 1
	- pin\_configuration\_vba.xlsm 
- In the Excel sheet, select the tab named "Pin Mux data source"
- Clear the contents of all cells
- Focus on cell A1, and go to menu Data--> Obtain data --> From File --> From text/CSV, and select pin\_info.csv file 
- Select "Transform Data" button on the dialog box that will appear. 
- Choose menu option "Transform" on the top of the window, and select "Use first row as header"
- Choose menu option "File" on the top of the window, select "Close and Load in...", and select "Existing sheet"

**3. Generate the desired pin configuration file**

This step needs to be executed everytime you change the pin configuration.
The goal is to generate the CSV file which contains the desired pin configuration.

- Copy the file pin\_configuration\_vba.xlsm in your Windows development machine
- Open the Excel sheet and select the tab named "Generate desired pin config"
- Configure pin by choosing the desired parameters of the drop down lists "mux function", "driver strenght", etc.
- Once you're satisfied, click the button "Export to CSV file" to generate and save the .CSV file
- It is recommended to name the file as "desired\_pin\_configuration.csv", to match what is described in "Components of the tool" section. 

**4. Check pin configuration in Eagle controller**

The goal is to check if the actual pin configuration of the controller matches the one described in the desired pin configuration file

- Copy the desired pin configuration generated in step 3 to the Eagle controller, in the folder "/home/root/1370-testtool/", by using SCP, for instance
- Connect to the controller, via debug cable or SSH, and go to folder "/home/root/1370-testtool/"
- Execute the Ptyhon script: "./check\_pin\_config.py -pcf <desired pin configuration file\>", where <desired pin configuration file\> is the desired pin configuration CSV file 
- You will see the result of the comparison on the console


