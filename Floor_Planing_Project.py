#! /usr/bin/env python 


import sys 
import hdlparse.vhdl_parser as vhdl
import hdlparse.verilog_parser as vlog






#create file -> name it as file name . def 
# write the heading 

def main():
   #create output file 
   i=1;
   while(sys.argv[i][len(sys.argv[i])-1]!='v'):
       i+=1
   file_name=sys.argv[i] 
   outputfile_name = file_name.replace(".v",".def")
   outputfile= open(outputfile_name,'w+')
   
   outputfile.write("VERSION 5.7;" +'\n')
   outputfile.write("DIVIDERCHAR \" \\ \" ;" +'\n')
   outputfile.write("DUSBITCHARS \" [] \" ;" +'\n')
   outputfile.write("DESIGN c17;" +'\n')
   outputfile.write("UNITS DISTANCE MICRONS 1000;" +'\n')
   outputfile.write('\n')
   outputfile.write("DIEAREA ( 0 0 ) ( area area );" +'\n') #waiting for the area






   

if __name__ == "__main__": 
    main()

    len(sample_str)
# Get last character of string i.e. char at index position len -1
last_char = sample_str[length -1]
# Get last character of string i.e. char at index position len -1
last_char = sample_str[length -1]