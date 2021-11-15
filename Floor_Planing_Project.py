#! /usr/bin/env python 


import sys 
import hdlparse.vhdl_parser as vhdl
import hdlparse.verilog_parser as vlog



#def printTrack(outfile):

def printComponents(size,listofComp ,outfile):
    outfile.write("Components " + str(size) +'\n')
    for i in listofComp:
        outfile.write("- _#_ " + i +" ;" +'\n')
    outfile.write("END COMPONENTS")




def printROW(outfile):
 i=10
 while i!=0 :
     outfile.write("ROW ROW_"+str(10-i)+ " unithd 5520 10880 N DO 191 BY 1 STEP 460 0 ;"+'\n') #check number of ROWS and Value (191)
     outfile.write("ROW ROW_"+str(10-i+1)+ " unithd 5520 13600 FS DO 191 BY 1 STEP 460 0 ;"+'\n') #check number of ROWS and Value (191)
     i-=2

    

def extract(file_name , outfile):

    inputs=[]
    outputs=[]
    listOfComponents=[]
  
    inputfile=open(file_name,"r")
    code=inputfile.read()


    vlog_ex = vlog.VerilogExtractor()
    vlog_mods = vlog_ex.extract_objects_from_source(code)

 
    for i in vlog_mods :
        for j in i.ports:
            if j.mode == "input":
                inputs.append(j.name)
            elif j.mode == "output":
                 outputs.append(j.name)
    inputfile.close()

    inputfile=open(file_name,"r")
    components = 0

    for line in inputfile:
        if line.find("sky130") != -1 :
            components+=1
            listOfComponents.append(line.partition("(")[0])
    
    printComponents(components , listOfComponents , outfile)
    inputfile.close()



#create file -> name it as file name . def 
# write the heading 


def main():
   #create output file 
   i=1;
   while(sys.argv[i].find(".v") == -1):
       if(sys.argv[i].find(".lef") != -1):
            lef_file =sys.argv[i] 
       i+=1
   file_name=sys.argv[i] 
   outputfile_name = file_name.replace(".synthesis.v",".floorplan.def")
   outputfile= open(outputfile_name,'w+')
   outputfile.write("VERSION 5.8;" +'\n')
   outputfile.write("DIVIDERCHAR \"/\" ;" +'\n')
   outputfile.write("DUSBITCHARS \"[]\" ;" +'\n')
   outputfile.write("DESIGN " + file_name.removesuffix(".synthesis.v")+ " ;" +'\n')
   outputfile.write("UNITS DISTANCE MICRONS 1000;" +'\n')
   outputfile.write("DIEAREA ( 0 0 ) ( area area );" +'\n') #waiting for the area (end corner )

   printROW(outputfile)
   extract (file_name ,outputfile)






   

if __name__ == "__main__": 
    main()