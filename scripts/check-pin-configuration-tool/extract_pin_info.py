#!/usr/bin/python
import csv
import sys
import os.path
import re

DELIMITER = ";"
INPUT_REGS_BASE_ADDRESS = "0x3033"
DEFAULT_OUTPUT_FILE_NAME = "pin_info.csv"

'''
Class PinDataInfo.
Contains data structures and functions to hold and manage all pin information
'''
class PinDataInfo:
	def __init__(self,item):
		'''
		Initialize class variables
		@item: string of parameters separated by DELIMITER
		'''
		(base_address, pin_name, function,mux_reg, conf_reg, input_reg, mux_mode, input_val) = item.split(DELIMITER)
		self.base_address = base_address
		self.pin_name = pin_name
		self.mux_reg = self.base_address + mux_reg[2:]
		self.conf_reg = self.base_address + conf_reg[2:]
		self.functions = [function,]
		self.input_regs = [INPUT_REGS_BASE_ADDRESS + input_reg[2:],]
		self.mux_modes = [mux_mode,]
		self.input_values = [input_val,]

	def add_function_block(self,item):
		'''
		Appends values to each corresponding list
		@item: string of parameters separated by DELIMITER
		'''
		(base_address, pin_name, function,mux_reg, conf_reg, input_reg, mux_mode, input_val) = item.split(DELIMITER)
		self.functions.append(function)
		self.input_regs.append(INPUT_REGS_BASE_ADDRESS + input_reg[2:])
		self.mux_modes.append(mux_mode)
		self.input_values.append(input_val)

	def get_full_data(self):
		'''
		Returns a list containing all information of the pin
		'''
		# Add "IGNORE" in the list of alternate functions
		self.functions.append("IGNORE")
		# Add number of alternate functions at the beggining, to easy column aligment process			
		return ([len(self.functions), self.pin_name, self.mux_reg, self.conf_reg] + self.functions + self.input_regs + self.mux_modes + self.input_values)


def show_usage_and_exit():
	'''
	Displays usage and exits with error
	'''
	print ""
        print "Usage is:"
	print "%s [command <parameters>]" % (sys.argv[0])
	print "Where [command]:"
	print "     -h                                  Shows usage and exits"
	print "     -i <input_file_name,base_address>   Defines a pair input_file_name,base_address"
	print "                                         base_address must be in hex format (e.g. 0xF012)"
	print "                                         Add one -i command for each pair you want to define"
	print "     -o <output_file_name>               Defines the output file name"	
	print "Examples:"
	print "     %s"  % (sys.argv[0])
	print "     %s -o my_pin_info_file.csv"  % (sys.argv[0])
	print "     %s -i imx7d-pinfunc-lpsr.h,0x302C " % (sys.argv[0])
	print "     %s -i imx7d-pinfunc-lpsr.h,0x302C -i imx7d-pinfunc.h,0x3033" % (sys.argv[0])
	print "     %s -i imx7d-pinfunc-lpsr.h,0x302C -o my_pin_info_file.csv" % (sys.argv[0])
	print "     %s -i imx7d-pinfunc-lpsr.h,0x302C -i imx7d-pinfunc.h,0x3033 -o my_pin_info_file.csv" % (sys.argv[0])	
        print ""
	print "Notes:"
	print "If -i command is not used, the default pairs 'imx7d-pinfunc-lpsr.h,0x302C' and 'imx7d-pinfunc.h,0x3033' will be used"
	print "If -o command is not used, the default output file 'pin_info.csv' will be used"
	print ""
	exit(1)


if __name__ == '__main__':

	output_file_name = DEFAULT_OUTPUT_FILE_NAME
	input_files  = []

	# Parse comand line arguments
	try:
		index = 1
		while index < len(sys.argv):
			if sys.argv[index] == "-h":
				show_usage_and_exit()
			elif sys.argv[index] == "-i":
				file_name = (sys.argv[index+1]).split(',')[0]
				base_address = (sys.argv[index+1]).split(',')[1]			
				input_files.append((file_name,base_address))
				index += 2			
			elif sys.argv[index] == "-o":
				output_file_name = sys.argv[index+1]
				index += 2
			else:
				index += 1
	except:
		print "Error parsing command line arguments"
		show_usage_and_exit()
	
	# If nt input files specified, use the default ones
	if len(input_files) == 0:
		input_files  = [("imx7d-pinfunc-lpsr.h","0x302C"),("imx7d-pinfunc.h","0x3033")]	# list of tupples made of (file_name, base address)
		
	# Check command line parameters
	parameters_ok = True
	for file_name, base_address in input_files:
		if not os.path.isfile(file_name):
			print "Input file %s doesn't exist" % file_name
			parameters_ok = False
		if re.match("^0x[0-9A-Fa-f]+$",base_address) is None:
			print "Base address %s is not in hex format (e.g. 0x01FC)" % base_address
			parameters_ok = False
	if not parameters_ok:	
		exit(1)

	#########################################################################################################################################################
	# Extract info from all input_files, and store it into pin_data[]. Add base address information								#
	# Each '#define' line of the .h file is converted into a string in pin_data[], formatted as described below:						#
	# "define MX7D_PAD_GPIO1_IO08__GPIO1_IO8 0x0014 0x026C 0x0000 0x0 0x0" --> ['0x302C;GPIO1_IO00;GPIO1_IO0;0x0000;0x0030;0x0000;0x0;0x0']			#
	# Example of pin_data contents:																#
	# pin_data = ['0x302C;GPIO1_IO00;GPIO1_IO0;0x0000;0x0030;0x0000;0x0;0x0', '0x302C;GPIO1_IO00;PWM4_OUT;0x0000;0x0030;0x0000;0x1;0x0', 			#
	#	      '0x302C;GPIO1_IO00;WDOD1_WDOG_ANY;0x0000;0x0030;0x0000;0x2;0x0', '0x302C;GPIO1_IO00;WDOD1_WDOG_B;0x0000;0x0030;0x0000;0x3;0x0',		#
	# 	      '0x302C;GPIO1_IO00;WDOD1_WDOG__RST_B_DEB;0x0000;0x0030;0x0000;0x4;0x0', ....... 	                                                        #
	#	      .....																	#
	#	     ]																		#
	# The contents above have been extracted from the following lines of the imx7d-pinfunc-lpsr.h:                                                          #
	#     #define MX7D_PAD_GPIO1_IO00__GPIO1_IO0                      0x0000 0x0030 0x0000 0x0 0x0                                                          #
	#     #define MX7D_PAD_GPIO1_IO00__PWM4_OUT                       0x0000 0x0030 0x0000 0x1 0x0                                                          #
	#     #define MX7D_PAD_GPIO1_IO00__WDOD1_WDOG_ANY                 0x0000 0x0030 0x0000 0x2 0x0                                                          #
	#     #define MX7D_PAD_GPIO1_IO00__WDOD1_WDOG_B                   0x0000 0x0030 0x0000 0x3 0x0                                                          #
	#     #define MX7D_PAD_GPIO1_IO00__WDOD1_WDOG__RST_B_DEB          0x0000 0x0030 0x0000 0x4 0x0                                                          #
	#########################################################################################################################################################
	pin_data = []	# List of strings
	for file_name, base_address in input_files:
		lines = tuple(open(file_name,"r"))
		for line in lines:
			if "#define MX7D_PAD_" in line:			
				line = re.sub(r'[\n\r\t]',"",line)
				line = re.sub("#define MX7D_PAD_","",line)
				line = re.sub("__",DELIMITER,line,count=1)	# Remove only the fisrt occurrence of "__" because alternate function names can contain "__"			
				line = re.sub(" +",DELIMITER,line)				
				pin_data.append(base_address + DELIMITER + line)

	#########################################################################################################################
	# Parse info in pin_data[], and create pin_data_list[]. 								#
	# Information in pin_data_list is formatted to be easily exported to a .CSV file					#
	# Each item of the list contains the full information of a pin. It is another list formatted as follows:		#
	# All items have the same item count (the one of the largest one. Blank items '' are added if needed			#
	# [pin_name, mux_reg, config_reg, 											#
	#  function1, function2,...,functionN, IGNORE,										#
	#  input_reg1, input_reg2,...,input_regN,										#
	#  mux_value1, mux_value2,...,mux_valueN,										#
	#  input_value1, input_value2,...,input_valueN										#
	# ]															#
	# Exampe of an item:													#
	# ['GPIO1_IO00', '0x302C0000', '0x302C0030',										#
	#  'GPIO1_IO0', 'PWM4_OUT', 'WDOD1_WDOG_ANY', 'WDOD1_WDOG_B', 'WDOD1_WDOG__RST_B_DEB', 'IGNORE', '', '', '', '', '',	# 
	#  '0x30330000', '0x30330000', '0x30330000', '0x30330000', '0x30330000', '', '', '', '', '',				#
	#  '0x0', '0x1', '0x2', '0x3', '0x4', '', '', '', '', '',								#
	#  '0x0', '0x0', '0x0', '0x0', '0x0', '', '', '', '', ''								#
	# ]															#
	#########################################################################################################################
	pin_data_list = [] # List of lists
	actual_pin_name = ""
	max_functions_count = 0
	for item in pin_data:
		base_address = item.split(DELIMITER)[0]		
		pin_name = item.split(DELIMITER)[1]
		if actual_pin_name != pin_name:			
			if actual_pin_name == "":
				# Create and initialilze the first pin data item		
				pin_data_item = PinDataInfo(item)			
			else:
				# New pin detected. The previous pin data has been all parsed
				# Add the previous pin data item to the list				
				pin_data_list.append(pin_data_item.get_full_data())
				if len(pin_data_item.functions) > max_functions_count:
					max_functions_count = len(pin_data_item.functions)
				# Create and initialize the new pin data item
				pin_data_item = PinDataInfo(item)			
			actual_pin_name = pin_name
		else:			
			# Add info to the actual pin data item being parsed
			pin_data_item.add_function_block(item)
	
	# Add the last pin data item to the list
	pin_data_list.append(pin_data_item.get_full_data())	
	if len(pin_data_item.functions) > max_functions_count:
		max_functions_count = len(pin_data_item.functions)

	# Column aligment (add blank items '' where needed)
	for item in pin_data_list:
		functions_count = item.pop(0)	# Get and remove the first element, which contains the number of functions. It is no longer needed after the column aligment process
		if functions_count < max_functions_count:
			index = 3+functions_count
			item[index:index] = [''] * (max_functions_count - functions_count)		
			for i in range(3):
				index += max_functions_count - 1 # Don't add ' ' for added function "IGNORE"
				item[index:index] = [''] * (max_functions_count - functions_count)

	#####################
	# Generete CSV file #
	#####################
	with open(output_file_name, mode='w') as csv_file:
		csv_writer = csv.writer(csv_file, delimiter=DELIMITER)					

		# Add header row
	 	header_item = ["Pin name", "MUX reg", "CONFIG reg"]
		function = []
		input_reg = []
		mux_mode = []
		input_val = []		
		for i in range(max_functions_count):
			function.append("Function %s" % (i))
		for i in range(max_functions_count-1):
			input_reg.append("INPUT reg %s" % (i))
			mux_mode.append("Mux mode %s" % (i))
			input_val.append("Input val %s" % (i))	
		header_item += function + input_reg + mux_mode + input_val
		csv_writer.writerow(header_item)

		# Add data		
		for item in pin_data_list:
			csv_writer.writerow(item)

	print "File '%s' successfully generated" % output_file_name

	exit(0)
