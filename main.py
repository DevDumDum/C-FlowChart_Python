from tkinter import *
import tkinter as tk
import math
from PIL import Image, ImageDraw
from array import array

img = Image.new('RGB', (500, 300), (128, 128, 128))
draw = ImageDraw.Draw(img)

root = Tk()
root.title("GUI")
root.configure(background="sky blue")

# Label
l1 = tk.Label(root,text="C to Flowchart",font=("Times New Roman",20))
l1.grid(column=0,row=0)

text = Text(root, height=20, width=40)
text.grid(column=0,row=1)

# Add a Scrollbar(horizontal)
v=Scrollbar(root, orient='vertical')
v.config(command=text.yview)
text.config(yscrollcommand=v.set)
v.grid(column=1, row=1, sticky='NS')
#======================================================

def condition(res, i, bracketStart, bracketEnd, func):
    temp_cond = "" #text to be placed inside the shape
    parenthesis1Count = 0 #para makuha parin as string yung mga may parenthesis sa loob ng condition
    parenthesis2Count = 0 #para makuha parin as string yung mga may parenthesis sa loob ng condition
    while i < len(res):
        status = 2
        if str(res[i]) == " " or str(res[i]) == "(":
            if str(res[i]) == "(":
                parenthesis1Count +=1
                if parenthesis1Count != 1: #para malaman if parenthesis ng condition or hindi
                    status = 1
                else:
                    i+=1
            else:
                i+=1
        elif str(res[i]) == ")":
            if parenthesis1Count == parenthesis2Count+1: #para malaman if nasa loob ng condition yung parenthesis
                parenthesis2Count +=1
                status=0
            else:
                parenthesis2Count +=1
                status = 1
        else:
            status = 1
        
        if status == 1:
            temp_cond += res[i]
            i+=1
        elif status == 0:
            break

    func[3].append(temp_cond)
    print("Type: "+func[0][len(func[0])-1])
    print("Label: "+temp_cond)
    print("")

    return i, bracketStart, bracketEnd, func

def process(res, i, func):
    process_label = ""

    while res[i] != ";":
        process_label += res[i]
        i+=1
    process_label +=res[i]
    func[3].append(process_label)

    print("Type: "+func[0][len(func[0])-1])
    print("Label: "+process_label)
    print("")

    return i, func

def position(func, tempBracketEnd):
    func[2].append(tempBracketEnd)
    return func

def checker(res):
    bracket = 0
    parenthesis = 0
    dqoute = 0
    sqoute = 0
    xx = 0
    status = False
    text = "Incomplete Code"
    color = "red"
    while xx < len(res):
        if res[xx] == "{":
            bracket+=1
        elif res[xx] == "}":
            bracket-=1
        elif res[xx] == "(":
            parenthesis+=1
        elif res[xx] == ")":
            parenthesis-=1
        elif res[xx] == '"':
            dqoute+=1
        elif res[xx] == "'":
            sqoute+=1
        xx+=1
    if bracket==0 and parenthesis==0 and dqoute%2!=1 and sqoute%2!=1:
        status = True
        text = "Converted"
        color = "green"
    else:
        print(bracket)
        print(parenthesis)
        print(parenthesis)
        print(dqoute%2)
        print(sqoute%2)

    return status, text, color

def optimize_process_function(func):
    x = 0
    total = len(func[0])-1
    while x <= total:
        if x+1 < total:
            if (func[0][x] == "process" or func[0][x] == "input" or func[0][x] == "output") and func[0][x] == func[0][x+1]:
                func[0].pop(x+1)
                func[2].pop(x+1)
                func[3][x] += "\n"+func[3][x+1]
                func[3].pop(x+1)
        x+=1
    return func

def mapping(func, flowchart):
    flowchart.append([])
    total = len(func[2])
    converted = []  #add in-between per shape for arrows
    x = 0
    tempn = 0
    total_column = 0
    total_row = 0
    current_row = 0
    last_column = 0
    last_row = 0
    left = 0

    #get max column
    while x < total:
        converted.append(func[2][x]*2)

        if func[2][x] > total_column:
            total_column = func[2][x]
        x+=1
    total_column *= 2
    textt=""
    for i in range(len(func[0])):
        textt += func[0][i][0]
    
    #converted[x] = column location
    #flowchart[r][c]
    x = 0 
    cx = 0#index for converted[]
    while x < total:
        current_row = last_row

        #check row
        zz = len(flowchart)-1
        if total_row > zz:
            while total_row > zz:
                flowchart.append([])
                zz = len(flowchart)-1
        #check column
        zz = len(flowchart[current_row])-1
        if converted[cx] > zz:
            while converted[cx] > zz:
                flowchart[current_row].append(None)
                zz = len(flowchart[current_row])-1

        flowchart[current_row][converted[cx]] = func[0][x][0]+func[0][x][1]
        #print(flowchart[current_row])

        if cx+1<total:
            if converted[cx] == converted[cx+1]-2:
                flowchart[current_row].append(">")
            else:
                total_row+=1
                current_row+=1
        last_row = current_row
        cx+=1
        x+=1
        
    print("=========================")
    print("total row: "+str(total_row))
    print("Position: "+str(converted))
    print("")
    for z in range(len(flowchart)):
        print(flowchart[z])
    return 0

# Button
def convertBtn():
    res = text.get("1.0",'end-1c')
    bt["text"] = str("Checking")
    status, tempText, BtnColor = checker(res)
    bt["text"] = str(tempText)
    bt["bg"] = BtnColor
    if status == True:
        text_code_count = len(res)

        bracketStart = 0
        bracketEnd = 0
        total_if = 0
        total_else_if = 0
        tempBracketEnd = 0
        
        func = []
        func.append([]) #label              0
        func.append([]) #bracket status     1
        func.append([]) #position           2
        func.append([]) #text_label         3

        flowchart = []  #map of flowchart

        i = 0
        print("")
        print('total characters = '+str(text_code_count))
        print("")
        while (text_code_count > i ):
            condStatus = 0
            if(text_code_count > i+7): #check if posible pa magka else if
                if str(res[i])+str(res[i+1])+str(res[i+2])+str(res[i+3])+str(res[i+4])+str(res[i+5])+str(res[i+6]) == "else if":
                    conType = "else if"
                    i+=7
                    condStatus = 1

            if(text_code_count > i+6):
                if str(res[i])+str(res[i+1])+str(res[i+2])+str(res[i+3])+str(res[i+4])+str(res[i+5]) == "double" and str(res[i+6]) == " ":
                    conType = "process"
                    condStatus = 1
                elif str(res[i])+str(res[i+1])+str(res[i+2])+str(res[i+3])+str(res[i+4])+str(res[i+5]) == "printf":
                    conType = "output"
                    condStatus = 1

            if(text_code_count > i+5):
                if str(res[i])+str(res[i+1])+str(res[i+2])+str(res[i+3])+str(res[i+4]) == "while":
                    conType = "while"
                    condStatus = 1
                    i+=5
                elif str(res[i])+str(res[i+1])+str(res[i+2])+str(res[i+3])+str(res[i+4]) == "float" and str(res[i+5]) == " ":
                    conType = "process"
                    condStatus = 1
                elif str(res[i])+str(res[i+1])+str(res[i+2])+str(res[i+3])+str(res[i+4]) == "scanf":
                    conType = "input"
                    condStatus = 1

            if(text_code_count > i+4):
                if str(res[i])+str(res[i+1])+str(res[i+2])+str(res[i+3]) == "else":
                    conType = "else"
                    i+=5
                    condStatus = 1
                elif str(res[i])+str(res[i+1])+str(res[i+2])+str(res[i+3]) == "char" and str(res[i+4]) == " ":
                    conType = "process"
                    condStatus = 1

            if(text_code_count > i+3):
                if str(res[i])+str(res[i+1])+str(res[i+2]) == "int" and str(res[i+3]) == " ":
                    conType = "process"
                    condStatus = 1

            # if(text_code_count > i+2):
            #     print("")

            if(text_code_count > i+1): #check if posible pa magka if
                if  str(res[i])+str(res[i+1]) == "if":
                    conType = "if"
                    i+=2
                    condStatus = 1
            
            if condStatus == 1:
                print("--------------------")
                func[0].append(conType)

                if conType == "else if" or conType == "if" or conType == "while" or conType == "for":
                    print("Shape: Diamond")
                    i, bracketStart, bracketEnd, func = condition(res, i, bracketStart, bracketEnd, func)
                elif conType == "process":
                    print("Shape: Rectangle")
                    i, func = process(res, i, func)
                elif conType == "input" or conType == "output":
                    print("Shape: Parrallelogram")
                    i, func = process(res, i, func)
                elif conType == "else":
                    print("else arrow")
                    func[3].append("else")

                
                func = position(func, tempBracketEnd)

            if text_code_count > i:
                if res[i] == "{":
                    bracketStart+=1
                    tempBracketEnd += 1
                    
                elif res[i] == "}":
                    # xx = len(func[1])-1
                    # while xx >= 0:
                    #     if func[1][xx] == 1:
                    #         func[1][xx] = 0
                    #         break
                    #     xx-=1
                    # bracketEnd+=1
                    tempBracketEnd -= 1
                i+=1
        func = optimize_process_function(func)
        flowchart = mapping(func, flowchart)
        print("--------------------")
        # print("Label: "+str(func[0]))
        # #print("Status: "+str(func[1]))
        # print("Position: "+str(func[2]))
        # print("Content: "+str(func[3]))

        #dapat nagawa na yung pang function para ma uncomment ito
        # if len(func[2]) != bracketStart/2:
        #     bt["text"] = "statement error"
        #     bt["bg"] = "red"
        #     print(len(func[2]))
        #     print(bracketStart)
    else:
        print(tempText)


bt = tk.Button(root,
            text="Convert",
            bg="green",
            fg="white",
            command=convertBtn)

bt.grid(column=0,row=2)

#======================================================

v.config(command=text.yview)

root.geometry('340x400')
root.mainloop()

# draw.rectangle((200, 100, 300, 200), fill=(0, 192, 192), outline=(255, 255, 255))
# img.show()
# draw.ellipse((100, 100, 200, 200), fill=(255, 0, 0), outline=(0, 0, 0))
# img.show()
# draw.line((350, 200, 450, 100), fill=(255, 255, 0), width=10)
# img.show()
# draw.rectangle((200, 100, 300, 200), fill=(0, 192, 192), outline=(255, 255, 255))
# draw.ellipse((100, 100, 100, 100), fill=(255, 0, 0), outline=(0, 0, 0))
# draw.line((350, 200, 450, 100), fill=(255, 255, 0), width=10)
# img.show()