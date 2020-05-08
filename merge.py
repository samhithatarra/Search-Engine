import ast

def read_file(file1, file2):
    filehandle1 = "/Users/sarthakgupta/Search-Engine/{0}.txt".format(file1)
    filehandle2 = "/Users/sarthakgupta/Search-Engine/{0}.txt".format(file2)
    f1 = open(filehandle1, 'r+')
    f2 = open(filehandle2, 'r+')
    
    while f1.readline() != "" and f2.readline() != "":
        line1 = f1.readline()
        line2 = f2.readline()
        line1 = ast.literal_eval(line1)
        line2 = ast.literal_eval(line1)
        
        

        
    

