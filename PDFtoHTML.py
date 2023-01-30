#Written with ♥ by Harlan for Communicadia / Arcadia Housing Co-op
import aspose.words as aw #this is free but watermarks the final html. also converts pdf to badly formatted html
from bs4 import BeautifulSoup #this formats the html nicely
import os #needed to remove auto generated png that aw makes


#in the string array, find 'Aspose.Words' then loop backwards until you reach '<'
#loop forwards from 'Aspose.Words' until you find '>', then delete that range of indices
#find reference to generated watermark and delete reference tag and after, delete the png file
def remTags(string, filePath):
    ref = 1
    while ref == 1:
        openTag = 0
        closedTag = 0
        remAsp = string.find("Aspose.Words")
        
        if remAsp == -1:
            break
        else:
            #loop backwards from Aspose until you find the opening tag
            for i in range(remAsp,0,-1):
                if(string[i] == "<"):
                    openTag = i
                    break
            #loop forwards until closing tag
            for i in range(remAsp,len(string),1):
                if(string[i] == ">"):
                    closedTag = i
                    break
            
            if(openTag != 0 and closedTag != 0): 
                string = string.replace(string[openTag:closedTag+1],"")

            else:
                print("Issue locating tags. Check if input is valid HTML")    
                return -1
    ref = 1
    while ref == 1:
        pathPNG = filePath.replace(".html",".001.png") #aspose creates a png with a similar title to file name. 
        remPNG = string.find(pathPNG)

        if remPNG == -1: #find() returns -1 if not found 
            break
        
        else:

            for i in range(remPNG,0,-1):
                if(string[i] == "<"):
                    openTag = i
                    break
            #loop forwards until closing tag
            for i in range(remPNG,len(string),1):
                if(string[i] == ">"):
                    closedTag = i
                    break

            if(openTag != 0 and closedTag != 0): 
                string = string.replace(string[openTag:closedTag+1],"")
                os.remove(pathPNG) #removes the png that is generated from aw

            else:
                print("Issue locating tags. Check if input is valid HTML")    
                return -1

    return string



#convert pdf file to html string using the path of the pdf file on local machine
def PDFtoHTML(filePath):

    doc = aw.Document(filePath)
    name = filePath.replace(".pdf",".html")
    doc.save(name)

    #making html file into a string variable in order to prettify
    with open(name) as f:
        rawHTML = f.read()

    #call my function to remove all 'Aspose' ads from the module
    noWatermark = remTags(rawHTML,name)  
    os.remove(name) #function returns string, don't need to keep the file created above to work. File created is not parsed for unwanted tags
    readableHTML = BeautifulSoup(noWatermark, 'html.parser').prettify()
    return readableHTML

   
# if __name__ == "__main__":
    

    # html = PDFtoHTML("revised_schedule.pdf")
    
    #makes file in current directory

    # myFile = open("testHTML.html",'w')
    # myFile.write(html)
    # myFile.close()


