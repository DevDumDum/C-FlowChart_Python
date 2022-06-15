from tkinter import *
import tkinter as tk
import math
from traceback import print_tb
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
    column_assigned = []  #add in-between per shape for arrows
    row_assigned = [] #row assignment
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
        column_assigned.append(func[2][x]*2)

        if func[2][x] > total_column:
            total_column = func[2][x]
        x+=1
    total_column *= 2
    textt=""
    for i in range(len(func[0])):
        textt += func[0][i][0]
    
    #column_assigned[x] = column location
    #flowchart[r][c]
    x = 0 
    #print(column_assigned)
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
        if column_assigned[x] > zz:
            while column_assigned[x] > zz:
                flowchart[current_row].append(None)
                zz = len(flowchart[current_row])-1
        row_assigned.append(total_row)
        flowchart[current_row][column_assigned[x]] = func[0][x][0]+func[0][x][1] #str(row_assigned[x])+":"+str(column_assigned[x])#
        #print(flowchart[current_row])

        if x+1<total:
            if column_assigned[x] < column_assigned[x+1]:
                flowchart[current_row].append("->")
            else:
                flowchart.append([])
                total_row+=1
                current_row+=1
                zz = len(flowchart[current_row])-1

                if column_assigned[x+1] > zz:
                    while column_assigned[x+1] > zz:
                        flowchart[current_row].append(None)
                        zz = len(flowchart[current_row])-1
                flowchart[current_row][column_assigned[x+1]] = "v "
                
                #search for last connection
                tempr = x
                while tempr >= 0:
                    if column_assigned[x+1] == column_assigned[tempr]:
                        break
                    tempr-=1

                wstatus = 0
                while wstatus == 0:
                    cr = row_assigned[tempr]+1
                    status = 0
                    while cr < total_row:
                        if flowchart[cr][column_assigned[x+1]] != None:
                            status = 1
                        cr+=1
                    cr = row_assigned[tempr]+1
                    if status == 0:
                        while cr < total_row:
                            flowchart[cr][column_assigned[x+1]] = "v "
                            cr+=1
                        wstatus = 1
                    else:
                        flowchart[cr-1].insert(column_assigned[x+1]+1,"->")
                        while cr < total_row:
                            flowchart[cr].insert([column_assigned[x+1]],None)
                            cr+=1
                total_row+=1
                current_row+=1
        last_row = current_row
        x+=1
        #print("vvvvvvvvvvvvvv")
        #print(column_assigned)

    # #optimizing else || wag nalang gawing arrow nalang
    # xx = 0
    # while xx < total:
    #     if func[0][xx] == "else":
    #         y = xx+1
    #         while y < total:
    #             if column_assigned[xx] > column_assigned[y]:
    #                 break
    #             y+=1
    #         flowchart[row_assigned[xx]].pop(column_assigned[xx])
    #         flowchart[row_assigned[xx]].pop(column_assigned[xx])
    #         flowchart[row_assigned[xx]-1][column_assigned[xx]] = "ev"
    #     xx+=1
            

    #arrows for loops
    x = total-1
    while x >= 0:
        count = 0
        if func[0][x] == "while":
            y = x+1
            while y < total:
                count+=1
                if column_assigned[x] > column_assigned[y]:
                    break
                y+=1
            # print("Row: "+str(row_assigned))
            # print(row_assigned[x])
            # print(column_assigned[x])
            # print(column_assigned[y-1])

            wstatus = 0
            temp_row = row_assigned[x]+1 
            colAs_1st = column_assigned[x]
            colAs_2nd = column_assigned[y-1]

            #if no next row, add row
            if len(flowchart)-1 < temp_row:
                flowchart.append([])
                ww = 0
                while ww <= colAs_2nd:
                    flowchart[-1].append(None)
                    ww+=1
            for z in range(len(flowchart)):
                print(flowchart[z])

            if temp_row+1 < len(flowchart):
                wx = 0
                wwstatus = 1
                while wwstatus == 1: #1st column of loop
                    if colAs_1st < len(flowchart[temp_row+wx]):
                        if flowchart[temp_row][colAs_1st] != None:
                            column_assigned[colAs_1st] +=2
                            xx = 0
                            while xx < count+1:
                                column_assigned[x + xx] +=2
                                xx+=1
                            colAs_1st +=2

                            print(column_assigned)
                            ttr = row_assigned[x]+1
                            while ttr < temp_row+1:
                                flowchart[ttr].insert(colAs_1st, str(colAs_1st)+str(colAs_2nd))
                                flowchart[ttr].insert(colAs_1st, str(colAs_1st)+str(colAs_2nd))
                                ttr+=1
                            flowchart[0].insert(colAs_1st-1, ".>")
                            flowchart[0].insert(colAs_1st-1, ".>")
                            print(column_assigned)
                            print(colAs_1st)
                            print(">>>>>>>>>>>>"+str(colAs_1st-1))
                        else:
                            break
                        wx+=1
                        end_row = temp_row
                        #placing arrow
                        # print("----")
                        # print(colAs_2nd)
                        # print(end_row)
                        temp = len(flowchart[temp_row])-1
                        while temp < colAs_2nd:
                            flowchart[temp_row].append(None)
                            temp+=1
                        flowchart[end_row][colAs_1st] = "L"
                        tr = colAs_1st+1
                        while tr < colAs_2nd:
                            flowchart[temp_row][tr] = "<"
                            tr+=1
                        flowchart[end_row][colAs_2nd] = "R"

                        lu = row_assigned[x]+1
                        while lu < temp_row:
                            flowchart[lu][colAs_1st] = "^"
                            flowchart[lu][colAs_2nd] = "v"
                            lu+=1
                        wstatus = 1
                    else:
                        temp = len(flowchart[temp_row])-1
                        
                        
                        obstacle = 0
                        if temp > colAs_2nd:
                            if flowchart[temp_row][colAs_1st] != None or flowchart[temp_row][colAs_2nd] != None:
                                obstacle+=1
                                break
                            tc = colAs_1st
                            while tc < colAs_2nd:
                                if flowchart[temp_row][tc] != None:
                                    obstacle+=1
                                tc+=1

                            

                        if obstacle == 0:
                            while temp < colAs_1st-1:
                                flowchart[temp_row].append(None)
                                temp+=1
                            flowchart[temp_row].append("L")
                            temp = colAs_1st
                            while temp < colAs_2nd-1:
                                flowchart[temp_row].append("<- ")
                                temp+=1
                            flowchart[temp_row].append("R")
                            wwstatus = 0
                            wstatus = 1
                        else:
                            while temp < colAs_2nd:
                                flowchart[temp_row].append(None)
                                temp+=1
                            temp_row+=1
                            wwstatus = 0
                            wstatus = 1



                    # colAs_2nd = column_assigned[y-1]
                    # if colAs_2nd < len(flowchart[temp_row+1]):
                    #     if flowchart[temp_row+1][colAs_2nd] != None:
                    #         column_assigned[colAs_2nd] +=2
                    #         colAs_2nd +=2
                    #         print(">>>>"+str(colAs_2nd))

                    #         ttr = row_assigned[x]+1
                    #         while ttr < temp_row+1:
                    #             flowchart[ttr].append(None)
                    #             flowchart[ttr].append(None)
                    #             ttr+=1

                    # www = len(flowchart[row_assigned[x]])
                    # while www < colAs_2nd:
                    #     flowchart[row_assigned[x]].insert(colAs_2nd-2, str(colAs_2nd-2)+"!>")
                    #     flowchart[row_assigned[x]].insert(colAs_2nd-2, "!>")
                    #     www+=1

                    # www = len(flowchart[row_assigned[x]])
                    # while www < colAs_1st:
                    #     if column_assigned[x] < column_assigned[x-1]:
                    #         flowchart[row_assigned[x]].insert(colAs_1st, str(colAs_1st-2)+"?>")
                    #         flowchart[row_assigned[x]].insert(colAs_1st, "?>")
                    #     else:
                    #         flowchart[row_assigned[x]].insert(colAs_1st, None)
                    #         flowchart[row_assigned[x]].insert(colAs_1st, None)
                    #     www+=1
                else:
                    wstatus = 1
                # for z in range(len(flowchart)):
                #     print(flowchart[z])
            
            zz = len(flowchart[temp_row])-1
            if column_assigned[colAs_2nd] > zz:
                while column_assigned[x+1] > zz:
                    flowchart[current_row].append(None)
                    zz = len(flowchart[temp_row])-1
        x-=1
    print("=========================")
    print(colAs_1st)
    print(colAs_2nd)
    print("total row: "+str(total_row))
    #print(func[0])
    print("Row: "+str(row_assigned))
    print("Column: "+str(column_assigned))
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
                    i+=4
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