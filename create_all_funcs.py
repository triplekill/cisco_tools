#!/usr/bin/python
#This script is a fixed up version of the one in the paper "Killing the myth of Cisco IOS rootkits DIK (Da Ios rootKit)".  It 
#appears to be made for an old version of IDA Pro with a different API.  To use, load the script then call the function with
#the start and end of the .text section as arguments.

def createUnresolvedFunctions(start, end):
	"""
	Analyze the code section to find every non-function byte and
	create a function at that position. This is highly reliable
	because CISCO compiler creates one function after another
	and every instruction is aligned to 4 bytes because of the
	RISC arch.
	"""
	counter = 0
	print ' Analyzing \'%s\' (0x%08x, 0x%08x)' % (SegName(start), start, end),
	# Start iteration on every non-function byte until we reach the end
	curr_address = start
	while curr_address < end:
		# Get the next address that is not a function recognized by IDA.
		next_address = idaapi.find_not_func(curr_address, SEARCH_DOWN)
		if next_address != BADADDR and next_address != 0xFFFFFFFF:
			if MakeFunction( next_address, BADADDR ) != 0:
				counter += 1
				if counter % 1000:
					print "[+] Created %d functions" % counter
			curr_address = next_address;

		# Check if we reached the end of the code segment
		if idaapi.get_item_size( curr_address ) == 0:
			break
		curr_address = idaapi.get_item_end( curr_address )

		# Detect an invalid item or function at the current position.
		if curr_address == BADADDR or curr_address == 0xFFFFFFFF:
			break
	print '[+] Done Created a total of %d new functions' % counter
