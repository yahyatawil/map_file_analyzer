# Author: Yahya Tawil 
# Licence: MIT License
# This script searches in .map file, generated from GCC-Tool chain, for information related to memory usage
# User has to change setting in the associated file "map_settings.txt" to set:
# 1- directory to .map file
# 2- sections defined in linker script that has unique start and end address keywords (.i.e __bss_start__)
# 3- sections defined in linker script with no unique start and end address keywords. User must specify start keyword and next section keyword ... look bellow:
        # ....
        # *(.dtors)

        # *(.rodata*)

        # KEEP(*(.eh_frame*))
        # ....
# that was part from linker script. *(.eh_frame*) is the unique keyword that make the map_file_analyzer.py knows where *(.rodata*) ends
 
import re

# read map file settings from map_setting.txt
setting_file = open("map_settings.txt","r")
settings = list()
general_sections=list() # these are sections that have clean start and stop address from linker file ex:__bss_start__ 
special_sections=list() # these are sections that don't have clean start and stop address from linker. only the section name 
map_dir = " "
number_sections = 0
number_special_sections = 0

for line in setting_file:
    settings.append(line.strip()) 
for line in settings:
    # print(line)
    if line.find("map_file_dir:") != -1:
       map_dir = line[line.find("map_file_dir:")+len("map_file_dir:"):] 
       # print(map_dir)    
    if line.find("sections:") != -1:
       general_sections =  line[line.find("sections:")+len("sections:"):].split(',') 
       # print(general_sections) 
    if line.find("special_sections:") != -1:
       special_sections = line[line.find("special_sections:")+len("special_sections:"):].split(',') 
       # print(special_sections)  

number_sections = len(general_sections)/2 
number_special_sections = len(special_sections)/2
################################################


# read map file
F = open(map_dir,"r") 
line_num = 1
mem_sec_num = 0
listOfLines = list()
memory = list()
for line in F:
    listOfLines.append(line.strip()) 
################################################


# Dicover memory sections definition from map file
for l in listOfLines:
    if l.find("Memory Configuration") != -1:
        # print("found")
        line_num = line_num +1
        if listOfLines[line_num].find("Name")!=-1 and listOfLines[line_num].find("Origin")!=-1 and listOfLines[line_num].find("Length")!=-1:
            line_num = line_num +1
            # print("found")
            for ll in listOfLines[line_num:]:
                # print(ll)
                if ll.find("*default*") !=-1:
                    # print("stop")
                    break
                memory.append(ll)
                mem_sec_num = mem_sec_num +1
    line_num = line_num +1
print ("**found ",mem_sec_num,"memory section**")
mem_dict = dict()

for mem in memory:
    sec = mem.split()
    mem_dict[sec[0]]=[sec[1],sec[2]]
    print (mem," ") 
# print (mem_dict)

for l in listOfLines:
    if l.find(".text") != -1 and len(l.split())==3:
        start_add = l.split()[1]
        if int(start_add,16)==int(mem_dict['FLASH'][0],16):
            print("Program size:",l.split()[2],'(',int(l.split()[2],16),' B)')
       
print ("***********************")   
################################################



# Dicover memory sections from map file
sec_num_iterator = 0
memory_sec_dict = dict()
for sec_num_iterator in range(0,int(number_sections),2):
    line_num = 1
    # print(sec_num_iterator)
    temp_memory_sec_list = list()
    for l in listOfLines:
        if l.find(general_sections[sec_num_iterator]) != -1:
            temp_memory_sec_list.append(l)
            for ll in listOfLines[line_num:]:
                if ll.find(general_sections[sec_num_iterator+1]) != -1:
                    temp_memory_sec_list.append(listOfLines[line_num])
                line_num = line_num +1
        line_num = line_num +1
    # print(temp_memory_sec_list)
    for item in temp_memory_sec_list:
        sec = item.split("PROVIDE")
        if len(sec) == 1:
            sec = item.split()
        # print(sec)
        reg_exp = '('+general_sections[sec_num_iterator] +'|'+ general_sections[sec_num_iterator+1]+')'
        # print (reg_exp)
        r1 = re.findall(reg_exp, sec[1])
        memory_sec_dict[r1[0]]=sec[0] 
        # print(sec)
    print("section length (",general_sections[sec_num_iterator+1],"-",general_sections[sec_num_iterator],"):",int(memory_sec_dict[general_sections[sec_num_iterator+1]], 16)-int(memory_sec_dict[general_sections[sec_num_iterator]], 16))
    print ("***********************")
# print (memory_sec_dict)
################################################

# Dicover special memory sections from map file
for special_sec_num_iterator in range(0,int(number_special_sections),2):
    line_num = 1
    sizeofSpecialSec = 0
    for l in listOfLines:
        if l.find(special_sections[special_sec_num_iterator]) != -1:
            for ll in listOfLines[line_num:]:
                if ll.find(special_sections[special_sec_num_iterator+1])!= -1:
                    break
                if len(ll.split())>2 and ll.split()[1].find("0x")!=-1 and ll.split()[2].find("0x")!=-1:
                    # print(ll.split()[1])
                    # print(" ")
                    sizeofSpecialSec = sizeofSpecialSec + int(ll.split()[2],16)
                line_num = line_num +1
        line_num = line_num +1
    print ("size of (",special_sections[special_sec_num_iterator],"):",sizeofSpecialSec)
    print ("***********************")
################################################