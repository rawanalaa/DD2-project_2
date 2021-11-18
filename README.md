#DEF file Generator
How to use this tool :
You should create a Verilog file that includes an HDL code. Make sure to store the (.py) file, LEF file (.lef) and the (.v) file in the same directory.
How to run the code :
Firstly, open python file on verilog, then run the code, at the console you will be asked to enter the verilog netlist file, library LEF file, core area utilization percentage, aspect ratio, vertical margin, and horizontal margin
Code structure:
Firstly, the component counter function is created in which the verilog file is opened to find the list of components and then extract the components to be listed in the def file. 
Secondly, the cell area is calculated, then the width is calculated using aspect ratio, core area and width and height margins, and another function that calculates the height
Thirdly, a function that displays the rows in the def file that calculates the X and Y coordinates
Fourthly,  the components are printed in the def file through a function called print components. 
Fifthly, a function that gets the wires from the verilog file is created which also returns a list of nets. 
Then, the pins are created through the pins file. 
Then in the main function, the user is asked to enter the verilog netlist name, lef file name, area utilization percentage, aspect ratio, vertical margin, horizontal margin. Then we name the def file according to the verilog file name. Then we extract the list of wires and their numbers. We also initiate the version  by inserting it in the def file by “version 5.8”, as well as instiating the titles of the def file, we also insert the die area at the beginning of the def file, after that, we print the rows, the components and the pins. Finally, we end the design. 

What's not complete: 
system doesn't take pins location file and assume are north 
condition to shift to another side when one is full, is not implemented. 
