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

#chr(97)

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
        #if func[0][x][0]+func[0][x][1] != "en":
        flowchart[current_row][column_assigned[x]] = func[0][x][0]+func[0][x][1] #str(row_assigned[x])+":"+str(column_assigned[x])#
        #else:
        #    flowchart[current_row][column_assigned[x]] = str(row_assigned[x])+str(column_assigned[x])
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

    #feeling up the void columns
    #get maxcolumn
    mcol = 0
    maxColumn = 0
    for mcol in range(len(column_assigned)-1):
        if column_assigned[mcol] > maxColumn:
            maxColumn = column_assigned[mcol]

    #check and fill each row
    for z in range(len(flowchart)):
        tRow = len(flowchart[z])-1
        if tRow < maxColumn+1:
            while tRow < maxColumn+1:
                flowchart[z].append(None)
                tRow+=1
    print(column_assigned)
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
    # print(column_assigned)
    # print(func[0])
    # print(func[1])
    # print(func[2])
    # for z in range(len(flowchart)):
    #     print(flowchart[z])
    # print("")

    #arrows for loops
    x = total-1
    
    while x >= 0:
        count = 0
        if func[0][x] == "while":
            numWhile = 0
            yy = 0
            y = x+1
            #find index of partner endloop
            while y < len(func[0]):
                if func[0][y] == "while":
                    numWhile += 1
                if func[0][y] == "endloop":
                    numWhile -= 1
                    if 0 > numWhile:
                        # print(func[0][y])
                        count = y
                        break
                y+=1
            y = count
            # print(row_assigned)
            # print(column_assigned)
            # print(func[0])
            # print(y)
            # print(count)
            # print("")
            temp_row = row_assigned[x]+1
            temp_row2 = row_assigned[y-1]+1
            colAs_1st = column_assigned[x]
            colAs_2nd = column_assigned[y]

            # print(" x: "+str(x))
            # print("r1: "+str(temp_row))
            # print("r2: "+str(temp_row2))
            # print("c1: "+str(colAs_1st))
            # print("c2: "+str(colAs_2nd))


            #if no next row, add row
            flowchart.append([])
            for z in range(len(flowchart)):
                tRow = len(flowchart[z])-1
                while tRow < len(flowchart[temp_row2-1])-1:
                    flowchart[z].append(None)
                    tRow+=1

            
            #obstacle check
            wstatus = 0
            while wstatus == 0:
                maxBottom1st = 0
                maxBottom2nd = 0
                # print("cc1: "+str(colAs_1st))
                # print("cc2: "+str(colAs_2nd))
                # print(flowchart[temp_row][colAs_1st])
                # print(flowchart[temp_row2][colAs_2nd])

                #get Max row of endloop
                rowUnder_col2 = temp_row2
                while rowUnder_col2 < len(flowchart):
                    if flowchart[rowUnder_col2][colAs_2nd] != None:
                        break
                    rowUnder_col2+=1
                maxBottom2nd = rowUnder_col2-1

                #Get Max row of start loop
                rowUnder_col1 = temp_row
                while rowUnder_col1 < len(flowchart):
                    if flowchart[rowUnder_col1][colAs_1st] != None:
                        break
                    rowUnder_col1+=1
                maxBottom1st = rowUnder_col1-1
                
                # print(maxBottom1st)
                # print(maxBottom2nd)
                # print("")

                row_cleared = 0 #which row is clear
                #check for obstacles in between
                while True:
                    row_cleared = 0 #which row is clear
                    obStatus = 0
                    xx = temp_row
                    tempR = 0
                    while xx < maxBottom1st+1:
                        obStatus = 0
                        tempR = 0
                        xx2 = colAs_1st
                        while xx2 < colAs_2nd:
                            # print(">>: "+str(flowchart[xx][xx2]))
                            if flowchart[xx][xx2] != None:
                                obStatus = 1
                                break
                            xx2+=1
                        print("")
                        if obStatus == 0:
                            tempR = xx
                            break
                        xx+=1
                    if obStatus == 0:
                        row_cleared = tempR
                        flowchart[row_cleared][colAs_1st] = "L "
                        flowchart[row_cleared][colAs_2nd] = " R"
                        gg = colAs_1st+1
                        while gg < colAs_2nd:
                            flowchart[row_cleared][gg] = "<-"
                            gg+=1

                        gg = temp_row
                        while gg < row_cleared:
                            flowchart[gg][colAs_1st] = "^ "
                            gg+=1
                        
                        gg = temp_row2
                        while gg < row_cleared:
                            flowchart[gg][colAs_2nd] = " v"
                            gg+=1
                            
                        wstatus = 1
                        break
                    else:
                        if maxBottom2nd < maxBottom1st:
                            #inserting arrows before column 2
                            flowchart[temp_row2-1].insert(colAs_2nd-1, "->")
                            flowchart[temp_row2-1].insert(colAs_2nd-1, "->")
                            colAs_2nd+=2
                            
                            if colAs_2nd < len(flowchart[temp_row2-1])-1:
                                flowchart[temp_row2-1].pop(len(flowchart[temp_row2-1])-1)
                                flowchart[temp_row2-1].pop(len(flowchart[temp_row2-1])-1)

                        else:
                            #insert arrows on both before columns
                            print(":)")
                            inStatus = 0
                            print(colAs_1st)
                            print(colAs_2nd)
                            curCol = colAs_1st-1
                            while inStatus < len(flowchart):
                                if inStatus <= temp_row:
                                    flowchart[inStatus].insert(curCol, flowchart[inStatus][curCol])
                                    flowchart[inStatus].insert(curCol, flowchart[inStatus][curCol])
                                else:
                                    if flowchart[inStatus][curCol] != None:
                                        gg = 1
                                        while True:
                                            if flowchart[inStatus-1][curCol+gg] == None and flowchart[inStatus][curCol] != None :
                                                curCol+=1
                                            else:
                                                flowchart[inStatus].insert(curCol, None)
                                                flowchart[inStatus].insert(curCol, None)
                                                break
                                    else:
                                        flowchart[inStatus].insert(curCol, None)
                                        flowchart[inStatus].insert(curCol, None)
                                inStatus+=1

                            flowchart.insert(maxBottom1st+1,[])
                            for z in range(len(flowchart[maxBottom1st])-1):
                                if flowchart[maxBottom1st][z] == "^ " or flowchart[maxBottom1st][z] == "v " or maxBottom1st%2 == 0:
                                    flowchart[maxBottom1st+1].append(flowchart[maxBottom1st][z])
                                else:
                                    flowchart[maxBottom1st+1].append(None)


                            colAs_1st+=2
                            colAs_2nd+=2

                        # print(colAs_1st)
                        # print(colAs_2nd)
                        # print("")
                        #Fill gaps
                        for z in range(len(flowchart)):
                            tRow = len(flowchart[z])-1
                            while tRow < len(flowchart[temp_row2-1])-1:
                                flowchart[z].append(None)
                                tRow+=1
                        #get Max row of endloop
                        rowUnder_col2 = temp_row2
                        while rowUnder_col2 < len(flowchart):
                            print(flowchart[rowUnder_col2])
                            if flowchart[rowUnder_col2][colAs_2nd] != None:
                                print("s: "+str(flowchart[rowUnder_col2][colAs_2nd]))
                                break
                            rowUnder_col2+=1
                        maxBottom2nd = rowUnder_col2-1

                        #Get Max row of start loop
                        rowUnder_col1 = temp_row
                        while rowUnder_col1 < len(flowchart):
                            if flowchart[rowUnder_col1][colAs_1st] != None:
                                print("c: "+str(flowchart[rowUnder_col1][colAs_1st]))
                                break
                            rowUnder_col1+=1
                        maxBottom1st = rowUnder_col1-1

                        for z in range(len(flowchart)):
                            print(flowchart[z])
                        # print("mb1: "+str(maxBottom1st))
                        # print("mb2: "+str(maxBottom2nd))
                        # print("c1 : "+str(colAs_1st))
                        # print("c2 : "+str(colAs_2nd))
                        print("")

                    # print(row_cleared)
                    # print(maxBottom1st)
                    # print(maxBottom2nd)
                    # for z in range(len(flowchart)):
                    #     print(flowchart[z])
                    # print("")
                    
                    wstatus = 0
                    break
                # print(column_assigned)
                # print(row_assigned)
                for z in range(len(flowchart)):
                    print(flowchart[z])
                print("")
                # print("+===================+")
                # print(maxBottom1st)
                # print(maxBottom2nd)
                # print(temp_row)
                # print(row_assigned[y-1]+1)
                # print("+===================+")
        x-=1
    print("=========================")
    #print(func[1])
    print("total row: "+str(total_row))
    #print(func[0])
    print("   Row: "+str(row_assigned))
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
        tempBracketEnd = 0
        
        func = []
        func.append([]) #label              0
        func.append([]) #loop position      1
        func.append([]) #position           2
        func.append([]) #text_label         3
        func.append([]) #pointing           4

        tempW = []
        whileStatus = 0

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
                    tempW.append(1)
                    whileStatus += 1
                    # gg = len(tempW)
                    # while gg >= 0:
                    #     if tempW[gg-1] != 0:
                    #         whileIndex = gg
                    #     gg-=1

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
                    if whileStatus > 0:
                        for a in range(len(tempW)):
                            if tempW[a] != 0:
                                tempW[a] += 1
                    
                    
                elif res[i] == "}":
                    if whileStatus > 0:
                        tempN = None
                        gg = len(tempW)-1
                        while gg >= 0:
                            if tempW[gg] != 0:
                                tempW[gg] -= 1
                                if tempW[gg]-1 <= 0:
                                    func[0].append("endloop")
                                    func[1].append(gg+1)
                                    func[2].append(func[2][-1]+1)
                                    func[3].append("endloop")
                                    whileStatus-=1
                                    tempW[gg] = 0
                            gg-=1


                        # if tempW[tempWhile-1] == 0:
                        #     func[0].append("endloop")
                        #     func[1].append(len(tempW))
                        #     func[2].append(func[2][-1]+1)
                        #     func[3].append("endloop")
                        #     tempW[tempWhile-1] == None
                        #     tempWhile -= 1
                    tempBracketEnd -= 1

                i+=1
            print(tempW)
        print(func[0])
        print("")
        func = optimize_process_function(func)
        flowchart = mapping(func, flowchart)
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