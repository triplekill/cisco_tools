#!/usr/bin/python
#This small python script changes the machine type and the base address of an ELF file's section and program headers.  This is
#primarily aimed at modifying ELF binaries so that xrefs in IDA Pro work more easily with irregular ELF binaries (such as CISCO
#IOS images).  This script requires my branch of elffile (until it gets pulled into main) that I added the ability to write 
#program headers with.  See https://bitbucket.org/jeffball/elffile/
import elffile, sys, argparse

parser = argparse.ArgumentParser(description="Move all of the ELF sections to a new image base in memory")
parser.add_argument('input_file', type=str, help='The executable to modify')
parser.add_argument('old_image_base', type=str, help='The old image base (in hex)')
parser.add_argument('new_image_base', type=str, help='The new image base (in hex)')
parser.add_argument('output_file', type=str, help='The filename to write the modified ELF file to')
parser.add_argument('-machine', type=str, default="", help='If specified, change the machine type to this value (in hex)')
args = parser.parse_args()

eo = elffile.open(name=args.input_file)
if args.machine != "":
	eo.fileHeader.machine = int(args.machine, 16)
old = int(args.old_image_base, 16)
new = int(args.new_image_base, 16)
eo.fileHeader.entry = eo.fileHeader.entry - old + new

for section_header in eo.sectionHeaders:
	section_header.addr = section_header.addr - old + new
for program_header in eo.programHeaders:
	program_header.vaddr = program_header.vaddr - old + new
	program_header.paddr = program_header.paddr - old + new

output_file = open(args.output_file, "wb")
output_file.write(eo.pack())
output_file.close()

