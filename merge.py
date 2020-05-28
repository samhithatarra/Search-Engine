
# --- Source Citation ---
# https://thispointer.com/how-to-merge-two-or-more-dictionaries-in-python/
# Used above link to understand how to merge dictionaries
# -----------------------

import ast

def merge_files(file1, file2, file3):
    filehandle1 = file1 
    filehandle2 = file2 
    filehandle3 = file3 
    f1 = open(filehandle1, 'r+')
    f2 = open(filehandle2, 'r+')
    f3 = open(filehandle3, 'w+')
    line1 = f1.readline()
    line2 = f2.readline()

    while line1 != "" and line2 != "":

        line1_eval = ast.literal_eval(line1)
        line2_eval = ast.literal_eval(line2)
        line1_key = [*line1_eval.keys()][0]
        line2_key = [*line2_eval.keys()][0]

        if line1_key < line2_key:

            f3.write(str(line1_eval))
            f3.write('\n')
            line1 = f1.readline()

        elif line1_key > line2_key:
         
            f3.write(str(line2_eval))
            f3.write('\n')
            line2 = f2.readline()
            
        else: 
            value1 = line1_eval[line1_key]
            value2 = line2_eval[line1_key]

            merged_dict = {**value1,**value2}
            line1_eval[line1_key] = merged_dict

            f3.write(str(line1_eval))
            f3.write('\n')
        
            line1 = f1.readline()
            line2 = f2.readline()

    # Add any remaining lines if one file is larger than the other 

    if line1 == "" and line2 != "":  
       
        while line2 != "":
            line2 = ast.literal_eval(line2)
            f3.write(str(line2))
            f3.write('\n')
            line2 = f2.readline()

    elif line1 != "" and line2 == "":  
    
        while line1 != "":
            line1 = ast.literal_eval(line1)
            f3.write(str(line1))
            f3.write('\n')
            line1 = f1.readline()
    
    f1.close()
    f2.close()
    f3.close()

        
        

        
    

