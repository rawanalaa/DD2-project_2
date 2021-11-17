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
    return (cells_area*1000)
  

def calculatewidth(core_area , aspect_ratio , w_margin ,h_margin ):
    a = aspect_ratio 
    b= (aspect_ratio * w_margin)-h_margin 
    c= core_area *-1
    discriminant = (b*b)-(4.0*a*c)

    width =((-1.0*b) - math.sqrt(discriminant))/(2.0*a)
    if width < 0.0 :
         width =((-1.0*b) + math.sqrt(discriminant))/(2.0*a)
    if(width%(0.46*1000)!=0.0):
        width=int(round(width/(0.46*1000))*(0.46*1000))
    return width

def calculateheight(aspect_ratio,die_area_width,h_margin) :
    h=(aspect_ratio*die_area_width)-h_margin
    if(h%(2.72*1000)!=0.0):
        h=int(round(h/(2.72*1000))*(2.72*1000))

    return h

def printROW(outfile,die_area_height,die_area_width ,w_margin ,h_margin):
 i=int((die_area_height-(h_margin))/(2.72*1000))
 i_org=i
 orgiX=int(w_margin/2)
 orgiY=int(h_margin/2)
 step=int(0.46*1000)
 numX =int((die_area_width - w_margin)/step)
 
 while i>=0 :
     outfile.write("ROW ROW_"+str(i_org-i)+ " unithd " + str(orgiX)+" "+ str(orgiY) +" N DO "+ str(numX) +" BY 1 STEP "+str(step) +" 0 ;"+'\n') 
     orgiY+=int((2.72*1000))
     outfile.write("ROW ROW_"+str(i_org-i+1)+" unithd " + str(orgiX)+" "+ str(orgiY) +" FS DO "+ str(numX) +" BY 1 STEP "+str(step) +" 0 ;"+'\n')
     orgiY+=int((2.72*1000))
     i-=2

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
    outputfile.write("END COMPONENTS" +'\n')


def getWiresList(verilog_file_name):
    listOfNets=[]
    inputfile=open(verilog_file_name,"r")
    for line in inputfile:
        if (line.find("wire") != -1) or (line.find("input") != -1) or (line.find("output") != -1):
            wire_name=line.split()
            if(wire_name[1][0]=="["):
                z=1
                i=0
                while(wire_name[1][z]!=":"):
                    i=int(str(i)+wire_name[1][z])
                    z+=1
                while(i>=0):
                    name=wire_name[2]+"["+str(i)+"]"
                    listOfNets.append(name.replace(";",""))
                    i-=1
            else:
                wire_name[1]=wire_name[1].replace("\\","")
                listOfNets.append(wire_name[1].replace(";",""))

    inputfile.close()
    return listOfNets

def printNet(verilog_file_name,outputfile,wires_number,listOfWires):
    outputfile.write("Nets " + str(wires_number) + "; \n")
    for wire in listOfWires :
        outputfile.write(" - " + wire)
        inputfile=open(verilog_file_name,"r")
        for line in inputfile:
            if(line.find("sky")!=-1):
                sky=line
                for line2 in inputfile:
                    if(line2.find(str(wire))!=-1):
                        sky=sky.partition("(")[0]
                        sky =sky.replace(" ","")
                        s=sky[-1]
                        i=2
                        while(sky[-i]!='_'):
                            s=sky[-i]+s
                            i+=1
                        s=sky[-i]+s
                        z=1
                        word=""
                        line2=line2.partition("(")[0]
                        while(line2[-z]!="."):
                            print(line2[-z])
                            word=line2[-z]+word
                            z+=1
                        outputfile.write("(" +s+word.replace(" ","")+") ")
                        break
                    if(line2.find(";")!=-1):
                        break
        outputfile.write(" + USE SIGNAL ; \n")
        inputfile.close()






def main():
   verilog_file_name=input("Please Enter the Verilog netlist file name \n")
   LEF_file_name=input("Please Enter the  library LEF file name \n")
   #pinLoaction_file_name=input("Please Enter the pin location file name \n")
   core_utilization=float(input("Please Enter the core area utilization percentage \n"))
   aspect_ratio=float(input("Please Enter the aspect ratio \n"))
   h_margin=2*float(input("Please Enter the vertical margin \n"))
   w_margin=2*float(input("Please Enter the horizantal margin \n"))

  

   outputfile_name =  verilog_file_name.replace(".synthesis.v",".floorplan.def")
   outputfile= open(outputfile_name,'w+')
   listOfComponents=countlistOfComponents(verilog_file_name)
   components_number=len(listOfComponents)
   listOfWires=getWiresList(verilog_file_name)
   wires_number=len(listOfWires)


   cells_area=calculate_cell_area(listOfComponents,LEF_file_name)
   core_area =cells_area/core_utilization
   die_area_width= int(calculatewidth(core_area , aspect_ratio , w_margin ,h_margin ) +(w_margin))
   die_area_height= int(calculateheight(aspect_ratio,die_area_width,h_margin) +(h_margin))

   outputfile.write("VERSION 5.8;" +'\n')
   outputfile.write("DIVIDERCHAR \"/\" ;" +'\n')
   outputfile.write("DUSBITCHARS \"[]\" ;" +'\n')
   outputfile.write("DESIGN " + verilog_file_name.replace(".synthesis.v" ,"")+ " ;" +'\n')
   outputfile.write("UNITS DISTANCE MICRONS 1000;" +'\n')
   outputfile.write("DIEAREA ( 0 0 ) ("+ str(die_area_width) + ","+ str(die_area_height) +");" +'\n')

   printROW(outputfile,die_area_height,die_area_width ,w_margin ,h_margin)
   printComponents(outputfile,components_number,listOfComponents)
   printNet(verilog_file_name,outputfile,wires_number,listOfWires)
  

   outputfile.write("END DESIGN"+'\n')
   








   

if __name__ == "__main__": 
    main()