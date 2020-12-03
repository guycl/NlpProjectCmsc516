import re
import os

indir = "Development Data Converted/"
annotationdir = "Development Ground Truth/"
outdir = "Development Data Annotated/"

# Create directory for output files
if not os.path.exists(outdir):
    os.makedirs(outdir)

def convert_file(indir, anndir, outdir):

    filelist = os.listdir(indir)
    #print(filelist)

    outputfilecombined = open(outdir+'combined.csv', 'w')

    firstline = "Line #,Sentence #,Word,Tag\n"
    outputfilecombined.writelines(firstline)

    isentence = 1

    for currentfile in filelist:

        print(currentfile)

        inputfile = open(indir+currentfile)

        annfilename = re.sub('.csv','_gold.entries',currentfile)
        annfile = open(anndir+annfilename)

        outputfile = open(outdir+currentfile, 'w')

        tagpairs = []

        # Get annotations and store in 2D tuple
        for line in annfile:

            splitline = line.split('||')

            for sline in splitline:

                secondsplit = sline.split('"')

                # Get tags
                thistag = secondsplit[0]
                thistag = thistag.split()
                thistag = thistag[0]
                thistag = thistag.split('=')
                thistag = thistag[0]

                if (secondsplit[1] != 'nm') and (thistag != 'ln') and (thistag != 'e') and (thistag != 'c') and (thistag != 't'):

                    # Get start and end positions
                    positions = re.split('="|"', sline)
                    positions = positions[-1]
                    positions = re.split(' |,', positions)
                    positions = positions[1:]

                    if len(positions) > 2:
                        #tagpairs.append(positions)
                        a=1
                        #print(positions)
                    else:
                        tagstart = positions[0]
                        tagstart = tagstart.split(':')
                        tagend = positions[1]
                        tagend = tagend.split(':')
                        tagpairs.append([thistag, tagstart[0], tagstart[1], tagend[0], tagend[1]])
                        #print(tagstart)

        outputfile.writelines(firstline)

        iline = 0
        iword = 0

        # Skip header row
        next(inputfile)

        endofsentence = 0

        for line in inputfile:

            tokenparts = line.split(',')
            linepart = tokenparts[0]
            wordpart = tokenparts[2]

            # Determine if current word marks a sentence boundary
            

            if (iline == 0) and (iword == 0):
                currentsentence = "Sentence: "
                currentsentence += str(isentence)
                line = line.replace('SSS', currentsentence)
                isentence += 1
            # else if the end of sentence was detected at previous word
            elif endofsentence == 1:
                currentsentence = "Sentence: "
                currentsentence += str(isentence)
                line = line.replace('SSS', currentsentence)
                isentence += 1
                endofsentence = 0
            # else if the word is a .
            elif re.match(r"\.", wordpart):
                endofsentence = 1
                line = line.replace('SSS', '')
            # else if the word ends in a . and is more than 4 letters
            elif (re.match(r"[A-Za-z]+\w\.", wordpart)) and (len(wordpart)>4):
                endofsentence = 1
                line = line.replace('SSS', '')
            # else if the word ends in a : and is more than 4 letters
            elif (re.match(r"[A-Za-z]+\w\:", wordpart)) and (len(wordpart)>4):
                endofsentence = 1
                line = line.replace('SSS', '')
            else:
                line = line.replace('SSS', '')

            # Get line and token number to determine current word position
            if linepart != '':
                linepart = linepart.split()
                iline = int(linepart[1])
                iword = 0
            else:
                iword += 1

            currentposition = (100 * iline) + iword

            # Replace default tag with tag from annotation
            # if current position matches location of an annotation
            for tag in tagpairs:
                taglinestart = int(tag[1])
                taglineend = int(tag[3])
                tagwordstart = int(tag[2])
                tagwordend = int(tag[4])

                tagpositionstart = (100 * taglinestart) + tagwordstart
                tagpositionend = (100 * taglineend) + tagwordend

                if (currentposition >= tagpositionstart) and (currentposition <= tagpositionend):
                    line = line.replace('OOO', tag[0])

            outputfile.writelines(line)
            outputfilecombined.writelines(line)
    
        inputfile.close()
        annfile.close()
        outputfile.close()
    outputfilecombined.close()

convert_file(indir, annotationdir, outdir)
