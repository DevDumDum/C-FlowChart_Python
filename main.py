from tkinter import *
import tkinter as tk
import math
from PIL import Image, ImageDraw

img = Image.new('RGB', (500, 300), (128, 128, 128))
draw = ImageDraw.Draw(img)

root = Tk()
root.title("GUI")
root.configure(background="sky blue")

# Label
l1 = tk.Label(root,text="C to Flowchart",font=("Times New Roman",20))
l1.grid(column=0,row=0)

text = Text(root, height=10, width=40)
text.grid(column=0,row=1)

# Add a Scrollbar(horizontal)
v=Scrollbar(root, orient='vertical')
v.config(command=text.yview)
text.config(yscrollcommand=v.set)
v.grid(column=1, row=1, sticky='NS')
#======================================================

def if_Statement(res, i):
    num = 0
    temp_cond = "" #text to be placed inside the shape
    parenthesis1Count = 0 #para makuha parin as string yung mga may parenthesis sa loob ng condition
    parenthesis2Count = 0 #para makuha parin as string yung mga may parenthesis sa loob ng condition
    i+=2
    print("Diamond")
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
    num+=1
    print("if "+str(num)+": "+temp_cond)
    return i


# Button
def clicked():
    res = text.get("1.0",'end-1c')

    for i in range( len(res) ):
        if(len(res) > i+1): #check if posible pa magka if, while, etc
            if  str(res[i])+str(res[i+1]) == "if":
                i = if_Statement(res, i)
            elif res == "circle":
                print("2")
            elif res == "line":
                print("3")




bt = tk.Button(root,text="Convert",bg="green",fg="white",command=clicked)
bt.grid(column=0,row=2)

#======================================================

v.config(command=text.yview)

root.geometry('300x300')
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