import re
import os

#test_list = os.listdir("Evaluation Data")
#print(test_list)

files = ["11995", "18563", "133875", "150406", "180195", "182909", "189350", "210958", "241468", "379569"]
indir = "Development Data/"
outdir = "Development Data Converted/"

# Create directory for output files
if not os.path.exists(outdir):
    os.makedirs(outdir)

def convert_file(filelist, indir, outdir):

    for currentfile in filelist:

        inputfile = open(indir+currentfile)
        outputfile = open(outdir+currentfile+".csv", 'w')

        firstline = "Line #,Sentence #,Word,Tag\n"
        outputfile.writelines(firstline)

        iline = 1

        for line in inputfile:

            #line = line.lower()
            line = line.replace(',', '_')
            line = line.replace('|', '')
            line = line.replace('*', '') 
            line = line.replace('@', '')
            line = re.sub('\.\.+', '.', line)

            splitline = line.split()

            iword = 1

            for word in splitline:

                newline = ""
                if iword == 1:
                    newline = newline + "Line: " + str(iline)

                # Add temporary flags for sentence number and tag
                outputfile.writelines(newline + ",SSS," + word + ",OOO\n")
                iword += 1

            iline += 1
    
        inputfile.close()
        outputfile.close()

convert_file(files, indir, outdir)
