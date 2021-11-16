import math
def countlistOfComponents(verilog_file_name):
    listOfComponents=[]
    inputfile=open(verilog_file_name,"r")
    for line in inputfile:
        if line.find("sky130") != -1 :
            sky=line.partition("(")[0] 
            sky=sky.replace(" ","")
            listOfComponents.append(sky)
    inputfile.close()
    return listOfComponents




def calculate_cell_area(listOfComponents,LEF_file_name):
    cells_h=0.0
    cells_w=0.0
    cells_area=0.0
    edited_list=[]
    
    
    for sky in listOfComponents:
         s=sky[-1]
         i=2
         while(sky[-i]!='_'):
                s=sky[-i]+s
                i+=1
         s=sky[-i]+s
         sky=sky.replace(s,"")   
         edited_list.append(sky)
 

    for sky in edited_list:
        found=False
        lef_file=open(LEF_file_name,"r")
        for line in lef_file:
            line_s=line.split()
            if ((line.find("MACRO")!=-1) and (line_s[1]==sky)):
                found=True
                for line2 in lef_file:
                    if  line2.find("SIZE")!=-1:
                        line3=line2.split()
                        cells_w=float(line3[1])
                        cells_h=float(line3[3])
                        cells_area=cells_area+(cells_h*cells_w)
                        break
                if(found):
                   lef_file.close()
                   break
    return cells_area

def calculatewidth( core_area , aspect_ratio):
    width =math.sqrt(core_area/aspect_ratio)
    if(width%0.46!=0):
        width=math.ceil(width/0.46)*0.46
    return width

def calculateheight(die_area_width , aspect_ratio) :
    height=aspect_ratio*die_area_width
    if(height%2.72!=0):
        height=math.ceil(height/2.72)*2.72
    return height


def printComponents(outputfile,components_number,listOfComponents):
    outputfile.write("Components " + str(components_number) +";\n")
    for sky in listOfComponents:
        s=sky[-1]
        i=2
        while(sky[-i]!='_'):
                s=sky[-i]+s
                i+=1
        s=sky[-i]+s
        sky=s+sky.replace(s,"")
        outputfile.write(" - "+sky+";" +'\n')
    outputfile.write("END COMPONENTS")






def main():
   verilog_file_name=input("Please Enter the Verilog netlist file name \n")
   LEF_file_name=input("Please Enter the  library LEF file name \n")
   #pinLoaction_file_name=input("Please Enter the pin location file name \n")
   core_utilization=float(input("Please Enter the core area utilization percentage \n"))
   aspect_ratio=float(input("Please Enter the core area aspect_ratio \n"))
   h_margin=float(input("Please Enter the vertical margin \n"))
   w_margin=float(input("Please Enter the horizonal margin \n"))

  

   outputfile_name =  verilog_file_name.replace(".synthesis.v",".floorplan.def")
   outputfile= open(outputfile_name,'w+')
   listOfComponents=countlistOfComponents(verilog_file_name)
   components_number=len(listOfComponents)

   cells_area=calculate_cell_area(listOfComponents,LEF_file_name)
   core_area =cells_area/core_utilization
   die_area_width= calculatewidth(core_area , aspect_ratio) +(2*w_margin)
   die_area_height= calculateheight(die_area_width , aspect_ratio) +(2*h_margin)

   outputfile.write("VERSION 5.8;" +'\n')
   outputfile.write("DIVIDERCHAR \"/\" ;" +'\n')
   outputfile.write("DUSBITCHARS \"[]\" ;" +'\n')
   outputfile.write("DESIGN " + verilog_file_name.replace(".synthesis.v" ,"")+ " ;" +'\n')
   outputfile.write("UNITS DISTANCE MICRONS 1000;" +'\n')
   outputfile.write("DIEAREA ( 0 0 ) ("+ str(die_area_width) + ","+ str(die_area_height) +");" +'\n')

   printComponents(outputfile,components_number,listOfComponents)
   








   

if __name__ == "__main__": 
    main()