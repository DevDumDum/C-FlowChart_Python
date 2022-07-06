from turtle import fillcolor
import cv2
import math
import numpy as np
from tkinter import *
import tkinter as tk
from traceback import print_tb
from PIL import Image, ImageDraw,ImageFont
from array import array

# flowchart = [
#    ['process~|~int a,d,sum,ab,ba = 0;\nchar asd,aa = "asd";', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
#    ['v ', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
#    ['if~|~a<5', '->', 'if~|~a==(int)sum', '->', 'output~|~printf("nice");', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
#    ['v ', None, 'v ', None, None, None, 'L ', '<-', '<-', '<-', '<-', '<-', '<-', '<-', '<-', '<-', '<-', '<-', '<-', '<-', '<-', '<-', ' R', None],
#    ['v ', None, 'else if~|~asd=="asd"', '->', 'if~|~asd=="asd"', '->', 'while~|~d<=23', '->', 'if~|~d<=23', '->', 'output~|~printf("aho");', None, None, None, None, None, None, None, None, None, None, None, '^ ', None],['v ', None, None, None, 'v ', None, None, None, 'v ', None, None, None, None, None, None, None, None, None, None, None, None, None, '^ ', None],
#    ['v ', None, None, None, 'v ', None, None, None, 'else~|~else', '->', 'output~|~printf("nuys");', None, None, None, None, None, None, None, None, None, None, None, '^ ', None],
#    ['v ', None, None, None, 'v ', None, None, None, 'v ', None, 'L ', '<-', '<-', '<-', ' R', None, None, None, None, None, None, None, '^ ', None],
#    ['v ', None, None, None, 'v ', None, None, None, 'v ', None, 'while~|~d<=23', '->', 'output~|~printf("nuys");', '->', 'endloop~|~\n                    d++;', None, None, None, None, None, None, None, '^ ', None],    
#    ['v ', None, None, None, 'v ', None, None, None, 'L ', '<-', '<-', '<-', ' R', None, None, None, None, None, None, None, None, None, '^ ', None],
#    ['v ', None, None, None, 'v ', None, None, None, 'while~|~d<=23', '->', 'output~|~printf("nuys");', '->', 'endloop~|~\n                    d++;', None, None, None, None, None, None, None, None, None, '^ ', None],    
#    ['v ', None, None, None, 'v ', None, None, None, 'v ', None, 'L ', '<-', '<-', '<-', '<-', '<-', '<-', '<-', '<-', '<-', ' R', None, '^ ', None],
#    ['v ', None, None, None, 'v ', None, None, None, 'process~|~intd=0;', '->', 'for~|~d<=23', '->', 'output~|~printf("nuys");', None, None, None, None, None, None, None, '^ ', None, '^ ', None],
#    ['v ', None, None, None, 'v ', None, None, None, None, None, None, None, 'v ', None, 'L ', '<-', '<-', '<-', ' R', None, '^ ', None, '^ ', None],
#    ['v ', None, None, None, 'v ', None, None, None, None, None, None, None, 'process~|~intd=0;', '->', 'for~|~d<=23', '->', 'output~|~printf("nuys");', '->', 'endFloop~|~d++;', '->', 'endFloop~|~d++;', '->', 'endloop~|~\n                        d++;', None],
#    ['v ', None, None, None, 'v ', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
#    ['v ', None, None, None, 'else~|~else', '->', 'output~|~printf("wala na");', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
#    ['v ', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
#    ['else if~|~aa=="aa"', '->', 'output~|~printf("a");', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
#    ['L ', '<-', '<-', '<-', ' R', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
#    ['while~|~d<=23', '->', 'output~|~printf("a");', '->', 'endloop~|~\n    d--;', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
# ]


def scaleF(txt, h, w, total):
   fontsize = 1
   font = ImageFont.truetype("arial.ttf", fontsize)
   while font.getsize(txt)[0] < w-20 and font.getsize(txt)[1]*total < h-10:
      # iterate until the text size is just larger than the criteria
      fontsize += 1
      font = ImageFont.truetype("arial.ttf", fontsize)

   return font


def arrowedLine(im, ptA, ptB, color, width=2):
    """Draw line from ptA to ptB with arrowhead at ptB"""
    # Get drawing context
    draw = ImageDraw.Draw(im)
    # Draw the line without arrows
    draw.line((ptA,ptB), width=width, fill=color)

    # Now work out the arrowhead
    # = it will be a triangle with one vertex at ptB
    # - it will start at 95% of the length of the line
    # - it will extend 8 pixels either side of the line
    x0, y0 = ptA
    x1, y1 = ptB
    # Now we can work out the x,y coordinates of the bottom of the arrowhead triangle
    xb = 0.80*(x1-x0)+x0
    yb = 0.80*(y1-y0)+y0

    # Work out the other two vertices of the triangle
    # Check if line is vertical
    if x0==x1:
       vtx0 = (xb-5, yb)
       vtx1 = (xb+5, yb)
    # Check if line is horizontal
    elif y0==y1:
       vtx0 = (xb, yb+5)
       vtx1 = (xb, yb-5)
    else:
       alpha = math.atan2(y1-y0,x1-x0)-90*math.pi/180
       a = 8*math.cos(alpha)
       b = 8*math.sin(alpha)
       vtx0 = (xb+a, yb+b)
       vtx1 = (xb-a, yb-b)

    #draw.point((xb,yb), fill=(255,0,0))    # DEBUG: draw point of base in red - comment out draw.polygon() below if using this line
    #im.save('DEBUG-base.png')              # DEBUG: save

    # Now draw the arrowhead triangle
    draw.polygon([vtx0, vtx1, ptB], fill=color)
    return im


def draw_flowchart(flowchart):
   lastX = 20
   lastY = 20

   height = 150
   width = 150
   pColor = (153,255,153)
   processColor = (255,50,50)
   rectangelColor = (255,255,100)
   windowWidth =  width*(int(len(flowchart[0])/2))+(int(width/2)*(int(len(flowchart[0])/2)))
   windowHeight = ( 100*( int((len(flowchart)+3)/2) ) ) + 50*( int((len(flowchart)+3)/2) )
   img = Image.new('RGB', (windowWidth, windowHeight), (128, 128, 128))
   draw = ImageDraw.Draw(img)
   # text = "d<0"
   # pointA = (100,50 )
   # pointB = (100,100)
   # draw.text((20,30), text, fill ="red", align ="center")
   # draw.rectangle((pointA, pointB), fill=(0, 192, 192), outline=(255, 255, 255))


   #========= start =============
   x1 = lastX+20  #top right     , x position
   y1 = lastY  #top left    , y position
   x2 = x1+(width-40)  #bottom right , x position
   y2 = y1+(height/2)-20  #bottom left , y position
   pointA = (x1,y1)
   pointB = (x2,y2)
   draw.ellipse((pointA,pointB), fill=pColor, outline=(0, 0, 0)) #start

   text = "START"
   font = ImageFont.truetype("arial.ttf", 2)
   font = scaleF(text, height/2, width/2, 1)
   # print(font.getsize(text))
   # print(x1)
   # print(y1)
   draw.text((x1+28,y1+16), text, font=font, fill ="black", align ="center")

   lastY = y2
   x1 = lastX+width/2
   y1 = lastY
   x2 = x1
   y2 = y1+(height/3)-20
   pointA = (x1,y1)
   pointB = (x2,y2)
   img = arrowedLine(img, pointA, pointB, (0,0,0))

   lastY = y2+10

   #check if odd or even will be set to blocks
   if flowchart[0][0] == "v ":
      status = 1
   else:
      status = 0

   currentBlockRow = 0

   tempX = 20
   while currentBlockRow < len(flowchart):
      currentBlockColumn = 0
      lastX = 20
      while currentBlockColumn < len(flowchart[currentBlockRow]):
         
         label = flowchart[currentBlockRow][currentBlockColumn]
         if(label != None):
            text = label.split('~|~')

         if currentBlockRow%2==status:
            height = 100
            width = 150
         else:
            height = 50
            width = 150

         if label == None:
            x1 = lastX
            y1 = lastY
            if currentBlockColumn%2==0:
               x2 = x1+width
            else:
               x2 = x1+width/2
            y2 = y1+height
            pointA = (x1,y1)
            pointB = (x2,y2)
            draw.rectangle((pointA,pointB), outline="grey")
            lastX = x2

         elif text[0] == "process" or text[0] == "endFloop" or text[0] == "endloop":

            if (text[0] == "process"):
               strLength = 0
               tempText = ""
               arr = text[1].split('\n')
               for s in range(len(arr)):
                  if strLength < len(arr[s]):
                     strLength = len(arr[s])
                     tempText = arr[s]
               total = len(arr)
            else:
               text[1] = text[1].replace("\t","")
               text[1] = text[1].replace("\n","")
               text[1] = text[1].replace(" ","")
               tempText = text[1]
            font = scaleF(tempText, height, width, total)
            if font.getsize(tempText)[1] > 20:
               font = ImageFont.truetype("arial.ttf", 20)
            x1 = lastX  #top right     , x position
            y1 = lastY  #top left    , y position
            x2 = x1+width  #bottom right , x position
            y2 = y1+height  #bottom left , y position
            pointA = (x1,y1)
            pointB = (x2,y2)
         
            draw.rectangle((pointA,pointB), fill=rectangelColor, outline=(0, 0, 0)) #start
            draw.text((x1+((width/2)-(font.getsize(tempText)[0]/2)),y1+((height/2) - (font.getsize(text[1])[1]/2)*total)), text[1], font=font ,fill ="black", align ="center")

            lastX = x2

         elif text[0] == "for" or text[0] == "while" or text[0] == "if" or text[0] == "else if" :
            #           A
            #        B     C
            #           D
            #=A=
            x1 = lastX+width/2
            y1 = lastY
            #=B=
            x2 = lastX
            y2 = lastY+height/2
            #=C=
            x3 = lastX+width
            y3 = lastY+height/2
            #=D=
            x4 = lastX+width/2
            y4 = lastY+height

            pointA = (x1,y1)
            pointB = (x2,y2)
            pointC = (x3,y3)
            pointD = (x4,y4)

            strLength = 0
            tempText = ""
            text[1] = text[0]+" "+text[1]
            arr = text[1].split('\n')
            for s in range(len(arr)):
               if strLength < len(arr[s]):
                  strLength = len(arr[s])
                  tempText = arr[s]
            total = len(arr)

            font = scaleF(tempText, height, width/2, total)
            if font.getsize(tempText)[1] > 20:
               font = ImageFont.truetype("arial.ttf", 20)
            draw.polygon([pointA, pointB, pointD ,pointC], fill = (255,102,102))
            draw.text((x2+((width/2)-(font.getsize(text[1])[0]/2)),y2-(font.getsize(text[1])[1]/2)), text[1], font=font ,fill ="black", align ="center")
            lastX = x3

         elif text[0] == "input" or text[0] == "output":
            #         A       C
            #       B       D
            #=A=
            x1 = lastX+(width/6)
            y1 = lastY
            #=B=
            x2 = lastX
            y2 = lastY+height
            #=C=
            x3 = lastX+width
            y3 = lastY
            #=D=
            x4 = lastX+(width-(width/6))
            y4 = lastY+height

            pointA = (x1,y1)
            pointB = (x2,y2)
            pointC = (x3,y3)
            pointD = (x4,y4)
            if text[0] == "output":
               pcolor = (255,153,255)
            else:
               pcolor = (102,255,255)


            strLength = 0
            tempText = ""
            arr = text[1].split('\n')
            for s in range(len(arr)):
               if strLength < len(arr[s]):
                  strLength = len(arr[s])
                  tempText = arr[s]
            total = len(arr)

            font = scaleF(tempText, height, width-(width/6), total)
            if font.getsize(tempText)[1] > 20:
               font = ImageFont.truetype("arial.ttf", 20)
            draw.polygon([pointA, pointB, pointD ,pointC], fill = pcolor)
            draw.text((x1,y1+(height/2-(font.getsize(text[0])[1]/2))), text[1], font=font ,fill ="black", align ="center")
            lastX = x3

         elif text[0] == "v " or text[0] == "^ ":
            x1 = lastX+width/2
            y1 = lastY
            x2 = x1
            y2 = y1+height
            if text[0] == "^ ":
               pointA = (x2,y1)
               pointB = (x1,y2)
            else:
               pointA = (x1,y1)
               pointB = (x2,y2)
            img = arrowedLine(img, pointA, pointB, (0,0,0))
            lastX = x1+width/2
         
         elif text[0] == "else":
            x1 = lastX+width/2
            y1 = lastY
            x2 = x1
            y2 = y1+height/2

            pointA = (x1,y1)
            pointB = (x2,y2)

            draw.line((pointA, pointB), fill = "red", width = 2)

            if currentBlockRow+1 < len(flowchart):
               if flowchart[currentBlockRow+1][currentBlockColumn] != None:
                  draw.line(((x1,y2), (x2,y2+height/2)), fill = "black", width = 2)

            x1 = x2
            y1 = y2
            x2 = x1+width/2
            y2 = y1

            pointA = (x1,y1)
            pointB = (x2,y2)

            draw.line((pointA, pointB), fill = "red", width = 2)

            lastX = lastX+width

         elif text[0] == " R" or text[0] == "L ":
            x1 = lastX
            y1 = lastY+height/2
            x2 = x1+width/2
            y2 = y1

            if text[0] == "L ":
               pointA = (x2,y1)
               pointB = (x1+width,y2)
            else:
               pointA = (x1,y1)
               pointB = (x2,y2)
            
            draw.line((pointA, pointB), fill ="blue", width = 2)
                  #  ( x , y )
            x1 = lastX+width/2
            y2 = y1+height/2

            pointA = (x1,y1)
            pointB = (x2,y2)

            if flowchart[currentBlockRow+1][currentBlockColumn-1] == None:
               img = arrowedLine(img,(x1,lastY), (x2,y1), (0,0,0))
            
            if text[0] == "L ":
               img = arrowedLine(img, pointA, pointB, (0,0,255))
            else:
               draw.line((pointA, pointB), fill ="blue", width = 2)

            lastX = lastX+width

         elif text[0] == "rPointer":
            x1 = lastX
            y1 = lastY+(height/2)
            x2 = x1+(width/4)
            y2 = y1
            pointA = (x1,y1)
            pointB = (x2,y2)
            img = arrowedLine(img, pointA, pointB, (0,0,0))
 
            x1 = x2
            y1 = lastY+((height-width/4)/2)
            x2 = x1+width/4
            y2 = y1+width/4
            pointA = (x1,y1)
            pointB = (x2,y2)
         
            draw.ellipse((pointA,pointB), fill=(51,255,51), outline=(0, 0, 0))
            font = scaleF(text[1], width/4, width/4, 1)
            draw.text((x1+((width/4)/2),y1), text[1], font=font ,fill ="black", align ="center")
            lastX += width/2

         elif text[0] == "lPointer":
            x1 = lastX+(width/4)
            y1 = lastY+(height/2)
            x2 = x1+(width/4)
            y2 = y1
            pointA = (x1,y1)
            pointB = (x2,y2)
            img = arrowedLine(img, pointA, pointB, (0,0,0))

            x1-=10
            y1 = lastY+((height-width/4)/2)
            x2 = x1+(width/4)
            y2 = y1+width/4
            pointA = (x1,y1)
            pointB = (x2,y2)
            draw.ellipse((pointA,pointB), fill=(51,255,51), outline=(0, 0, 0))
            font = scaleF(text[1], width/4, width/4, 1)
            draw.text((x1+((width/4)/4),y1), text[1], font=font ,fill ="black", align ="center")
            lastX += width/2

         elif text[0] == "tPointer":
            x1 = lastX+width/2
            y1 = lastY
            x2 = x1
            y2 = y1+height
            pointA = (x1,y1)
            pointB = (x2,y2)
            img = arrowedLine(img, pointA, pointB, (0,0,0))

            x1 = lastX+(width/3)+5
            y1 = lastY
            x2 = x1+(width/3)-10
            y2 = y1+(width/3)-10
            pointA = (x1,y1)
            pointB = (x2,y2)
            draw.ellipse((pointA,pointB), fill=(51,255,51), outline=(0, 0, 0))
            font = scaleF(text[1], width/4, width/4, 1)
            draw.text((x1+((width/4)/4),y1), text[1], font=font ,fill ="black", align ="center")
            lastX += width

         elif text[0] == "->" or text[0] == "<-":
            x1 = lastX
            y1 = lastY+height/2
            if currentBlockColumn%2==0:
               x2 = x1+width
            else:
               x2 = x1+width/2
            y2 = y1
            if text[0] == "<-":
               pointA = (x2,y1)
               pointB = (x1,y2)
               draw.line((pointA, pointB), fill ="blue", width = 2)
            else:
               pointA = (x1,y1)
               pointB = (x2,y2)
               
               if currentBlockColumn-1 >= 0 :
                  text = flowchart[currentBlockRow][currentBlockColumn-1].split("~|~")
                  if text[0] == "else":
                     img = arrowedLine(img, pointA, pointB, (255,0,0))
                  else:
                     img = arrowedLine(img, pointA, pointB, (0,0,0))
               else:
                  img = arrowedLine(img, pointA, pointB, (0,0,0))
            
            lastX = x2

         else:
            print(text[0])
            x1 = lastX
            if currentBlockColumn%2==0:
               x2 = x1+width
            else:
               x2 = x1+width/2
            y1 = lastY
            y2 = y1+height
            pointA = (x1,y1)
            pointB = (x2,y2)
            draw.rectangle((pointA,pointB), outline="grey")
            lastX = x2



         currentBlockColumn+=1

      if currentBlockRow%2==status:
         lastY = y2
      else:
         lastY = y2

      currentBlockRow+=1
   img.save(str(windowWidth)+"x"+str(windowHeight)+".jpg")
   img = Image.open(str(windowWidth)+"x"+str(windowHeight)+".jpg")
   img.show()


#draw_flowchart(flowchart)
# x1 = lastX  #top right     , x position
# y1 = lastY  #top left    , y position
# x2 = x1+80  #bottom right , x position
# y2 = y1+50  #bottom left , y position
# pointA = (x1,y1)
# pointB = (x2,y2)
# draw.ellipse((pointA,pointB), fill=(100, 100, 250), outline=(0, 0, 0)) #start