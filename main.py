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

def if_condition(res, i, if_bracketStart, if_bracketEnd, func):
    temp_cond = "" #text to be placed inside the shape
    parenthesis1Count = 0 #para makuha parin as string yung mga may parenthesis sa loob ng condition
    parenthesis2Count = 0 #para makuha parin as string yung mga may parenthesis sa loob ng condition
    print("Shape = Diamond")
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

    print("Type = "+func[0][if_bracketStart])
    print("Inside Shape = "+temp_cond)
    print("")

    return i, if_bracketStart, if_bracketEnd


# Button
def clicked():
    res = text.get("1.0",'end-1c')
    text_code_count = len(res)
    if_bracketStart = 0
    if_bracketEnd = 0
    total_if = 0
    total_else_if = 0
    
    func = []
    func.append([])
    func.append([])

    i = 0
    print('total characters = '+str(text_code_count))
    print("")
    while (text_code_count > i ):
        if(text_code_count > i+6): #check if posible pa magka else if
            if str(res[i])+str(res[i+1])+str(res[i+2])+str(res[i+3])+str(res[i+4])+str(res[i+5])+str(res[i+6]) == "else if":
                func[0].append("else if")
                temp = 0
                if if_bracketStart != if_bracketEnd:
                    x = 0
                    while (x < len(func[0])): #search for first if
                        if func[0][x] == "if":
                            temp = x
                        x+=1
                    func[1].append(temp)
                else:
                    x = 0
                    while (x < len(func[0])): #search for first if
                        if func[0][x] == "if":
                            temp = x
                            break
                        x+=1
                    func[1].append(temp)
                total_else_if += 1
                i+=7
                print("--------------------")
                print(str(if_bracketStart) + ":" + str(if_bracketEnd))
                i, if_bracketStart, if_bracketEnd = if_condition(res, i, if_bracketStart, if_bracketEnd, func)
        # if(text_code_count > i+5):
        #     print("")
        # if(text_code_count > i+4):
        #     print("")

        # if(text_code_count > i+3):
        #     print("")

        # if(text_code_count > i+2):
        #     print("")
        

        if(text_code_count > i+1): #check if posible pa magka if
            if  str(res[i])+str(res[i+1]) == "if":
                func[0].append("if")
                if len(func[1]) == 0:
                    func[1].append(None)
                else:
                    func[1].append(if_bracketStart-1)
                total_if+=1
                print(total_if)
                i+=2
                print("--------------------")
                i, if_bracketStart, if_bracketEnd = if_condition(res, i, if_bracketStart, if_bracketEnd, func)
        if(text_code_count > i ):
            if res[i] == "{":
                if_bracketStart+=1
                i+=1
            elif res[i] == "}":
                if_bracketEnd+=1
                i+=1
            elif res[i] == " ":
                i+=1
            elif res[i] != "":
                i+=1
    print(func[0])
    print(func[1])
    print(str(if_bracketStart) + ":" + str(if_bracketEnd))



bt = tk.Button(root,text="Convert",bg="green",fg="white",command=clicked)
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