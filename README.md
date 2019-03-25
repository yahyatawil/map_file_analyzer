## How to use
This script searches in .map file, generated from GCC-Tool chain, for information related to memory usage

User has to change settings in the associated file "map_settings.txt" to set:
* Directory to .map file
* Sections defined in linker script that has unique start and end address keywords (.i.e `__bss_start__`)
* Sections defined in linker script with no unique start and end address keywords. User must specify start keyword and next section keyword ... look bellow:
```
....
*(.dtors)
*(.rodata*)

KEEP(*(.eh_frame*))
....
```
that was part from linker script. *(.eh_frame*) is the unique keyword that make the map_file_analyzer.py knows where *(.rodata*) ends.

<p align="center">
<img src="https://github.com/yahyatawil/map_file_analyzer/blob/master/python_map_ana.JPG" alt="Script in action">
</p>

## Tested Using ...

* Python 2.7 (64 bit) and Python 3.7.2 (32 bit) on Winodws 10 and using linker script of NRF52 SDK (nrf5x_common.ld)
