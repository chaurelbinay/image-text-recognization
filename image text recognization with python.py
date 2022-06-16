import time
from tkinter import *
import cv2 as cv2
from PIL import Image
import numpy as np
import pandas as pd
import sys
import os
from pydub import AudioSegment
from pydub.playback import play
import csv
from scipy import spatial
from playsound import playsound
import pygame

#check and divide based on q
def createFileList3(myDir, format='.png'):
    fileList = []
    #print(myDir)
    for root, dirs, files in os.walk(myDir, topdown=False):
        for name in files:
            if name.endswith(format):
                fullName = os.path.join(root, name)
                fileList.append(fullName)
                os.remove(fullName)
    return fileList
#check and divide based on q
def createFileList1(myDir, format='.png'):
    fileList = []
    #print(myDir)
    for root, dirs, files in os.walk(myDir, topdown=False):
        for name in files:
            if name.endswith(format):
                fullName = os.path.join(root, name)
                fileList.append(fullName)
    return fileList



#Useful function
def createFileList(myDir, format='.png'):
    fileList = []
    #print(myDir)
    for root, dirs, files in os.walk(myDir, topdown=False):
        for name in files:
            if name.endswith(format):
                fullName = os.path.join(root, name)
                fileList.append(fullName)
    return fileList

# load the original image
myFileList = createFileList('C:\img1')

for file in myFileList:
    #print(file)
    img_file = Image.open(file)
    #img_file.show()

    # get original image parameters...
    width, height = img_file.size
    format = img_file.format
    mode = img_file.mode

    # Make image Greyscale
    img_grey = img_file.convert('L')
    #img_grey.save('result.png')
    #img_grey.show()

    # Save Greyscale values
    value = np.asarray(img_grey.getdata(), dtype=np.int).reshape((img_grey.size[1], img_grey.size[0]))
    value = value.flatten()
    m=[0]*width
    n = [0] * (width*height)
   # fb = open('aaa7.csv', 'w')
    # print(value[width])
    # with open("img_pixels.csv", 'a') as f:
    #   writer = csv.writer(f)
    #  writer.writerow(value)
    upp_row = 0
    upp_col = 0

    #writer = csv.writer(fb)
    for y in range(0,height):
        i=0
        for x in range(0+(y*(width)),(width)+(y*(width))):
            m[i]=value[x]
            if m[i]<100:
                m[i]=255
                value[x]=255
                if upp_row==0:
                    upp_row=i
                    upp_col=y
                  #  value[x]=120
                   # m[i]=120

            else:
                m[i]=0
                value[x]=0
            i+=1

      #  writer.writerow(m)
    #fb.close()
    left=0
    right=0
    top=0
    down=0
    count=0
    #finding top coordinate
    for y in range(0,height):
        count=0
        for x in range(0+(y*(width)),(width)+(y*(width))):
            if(value[x]>0):
                count=count+1
              #  print(count)
        if(count>0):
            top=y
            #print('top=')
            #print(top)
            break

        # finding down coordinate
    for y in range(height-1, 0,-1):
        count = 0
        for x in range(0 + (y * (width)), (width) + (y * (width))):
            if (value[x] > 0):
                count = count + 1
                #  print(count)
        if (count > 2):
            down = y+1
            #print('down=')
            #print(down)
            break

    pxls1=value.reshape(height,width)

    # finding left coordinate
    for x in range(0, width):
        count = 0
        for y in range(0, height):
            if (pxls1[y,x] > 0):
                count = count + 1
        if (count >0):
            #print('left=')
            left=x
            #print(left)
            break
        # finding right coordinate
    for x in range(width, left+1,-1):
        count = 0
        for y in range(0, height):
            if (pxls1[y-1, x-1] > 0):
                count = count + 1
        if (count > 0):
            #print('right=')
            right = x
            #print(right)
            break
#    m=[0]*width
    n = [0] * width
   # fn = open('aaa6.csv', 'w')
   # writer = csv.writer(fn)
    #writing to file
    for y in range(0, height):
        count = 0
        for x in range(0, width):
            m[count]=pxls1[y,x]
            if(y==down):
                if (x == left):
                    #print('left,down=')
                    #print(x, y)
                    #pxls1[y, x] = 120
                    m[count] = pxls1[y, x]
                if (x == right):
                    #print('right,down=')
                    #print(x, y)
                    #pxls1[y, x] = 120
                    m[count] = pxls1[y, x]
            if(y==top):
                if(x==left):
                    #print('left,top=')
                    #print(x,y)
                    #pxls1[y, x] = 120
                    m[count] = pxls1[y, x]
                if(x==right):
                    #print('right,top=')
                    #print(x,y)
                    #pxls1[y,x]=120
                    m[count]=pxls1[y,x]


            count=count+1

        #writer.writerow(m)
    #fn.close()
   #extracting required text image
    result=[]
    fou = open('result.csv', 'w')
    writer = csv.writer(fou)
    for i in range(top-1,down+1):
        aux=[]
        for j in range(left-1,right+1):
            aux.append(pxls1[i,j])
        writer.writerow(aux)
        result.append(aux)
    fou.close()
   # print('element=')

    #print(result)
    #pxls1[upp_row,upp_col]=120
    #print(pxls1[4,10])
   # array=np.array(pxls1,dtype=np.uint8)
    array = np.array(result)
    im1=Image.fromarray(array)
    width1,height1=im1.size
    #print(width1,height1)
    im1.show()
    #abcd
    righ1=0
    position=0
    p=0
    i=0
    pos=[0]*5000

#13 ra neww
    for x in range(0,width1):
        count=0
        for y in range(0,height1):
            if(array[y,x]>0):
                count=count+1
        if(count==0):
            p=x
            break

    for x in range(0,width1):
        count=0

        for y in range(0,height1):
            if(array[y,x]>0):
               count=count+1
        if(count==0):
            if(x==(p+1)):
                p=p+1
            else:
                #print(p)
                pos[i]=p
                p=x
                i=i+1
                #print('start')
               # print(x)
                pos[i]=x
                i=i+1
        if(x==width-1):
            #print('last')
            #print(p)
            pos[i]=p
            i=i+1
            #print(x)
            pos[i]=x


    #print(x,y)
    #print('abcdef')
    #for x in range(1,i):
        #print(pos[x])

    #print('hello')
    iii=0
    alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'I', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
             'W', 'X', 'Y', 'Z','K']
    pos11=0
    q=[0]*20
    for x in range(2, i):
        #print(pos[x])
         if((x%2)==0):
             im11 = im1.crop((pos[x], 0, pos[x+1] + 1, height1))
             newsiz = (30, 25)
             im11 = im11.resize(newsiz)
             ar1 = np.asarray(im11)
             ar1 = ar1.flatten()
             sim = [0] * 50
             #im1.show()

             # aaa comp
             im2 = Image.open('aa.png')
             ar2 = np.asarray(im2)
             aa = ar2.flatten()
             sim[0] = 1 - spatial.distance.cosine(ar1, aa)
             # bb comp
             im2 = Image.open('bb.png')
             ar2 = np.asarray(im2)
             bb = ar2.flatten()
             sim[1] = 1 - spatial.distance.cosine(ar1, bb)
             # ccc comp
             im2 = Image.open('cc.png')
             ar2 = np.asarray(im2)
             cc = ar2.flatten()
             sim[2] = 1 - spatial.distance.cosine(ar1, cc)
             # dd comp
             im2 = Image.open('dd.png')
             ar2 = np.asarray(im2)
             dd = ar2.flatten()
             sim[3] = 1 - spatial.distance.cosine(ar1, dd)
             # ee comp
             im2 = Image.open('ee.png')
             ar2 = np.asarray(im2)
             ee = ar2.flatten()
             sim[4] = 1 - spatial.distance.cosine(ar1, ee)
             # ff com
             im2 = Image.open('ff.png')
             ar2 = np.asarray(im2)
             ff = ar2.flatten()
             sim[5] = 1 - spatial.distance.cosine(ar1, ff)
             # gg comp
             im2 = Image.open('gg.png')
             ar2 = np.asarray(im2)
             gg = ar2.flatten()
             sim[6] = 1 - spatial.distance.cosine(ar1, gg)
             # hh comp
             im2 = Image.open('hh.png')
             ar2 = np.asarray(im2)
             hh = ar2.flatten()
             sim[7] = 1 - spatial.distance.cosine(ar1, hh)
             # jj com
             im2 = Image.open('jj.png')
             ar2 = np.asarray(im2)
             jj = ar2.flatten()
             sim[8] = 1 - spatial.distance.cosine(ar1, jj)
             # kk comp
             im2 = Image.open('ii.png')
             ar2 = np.asarray(im2)
             ii = ar2.flatten()
             sim[9] = 1 - spatial.distance.cosine(ar1, ii)
             # ll comp
             im2 = Image.open('ll.png')
             ar2 = np.asarray(im2)
             ll = ar2.flatten()
             sim[10] = 1 - spatial.distance.cosine(ar1, ll)
             # mm com
             im2 = Image.open('mm.png')
             ar2 = np.asarray(im2)
             mm = ar2.flatten()
             sim[11] = 1 - spatial.distance.cosine(ar1, mm)
             # nn comp
             im2 = Image.open('nn.png')
             ar2 = np.asarray(im2)
             nn = ar2.flatten()
             sim[12] = 1 - spatial.distance.cosine(ar1, nn)
             # oo comp
             im2 = Image.open('oo.png')
             ar2 = np.asarray(im2)
             oo = ar2.flatten()
             sim[13] = 1 - spatial.distance.cosine(ar1, oo)
             # pp com
             im2 = Image.open('pp.png')
             ar2 = np.asarray(im2)
             pp = ar2.flatten()
             sim[14] = 1 - spatial.distance.cosine(ar1, pp)
             # qq comp
             im2 = Image.open('qq.png')
             ar2 = np.asarray(im2)
             qq = ar2.flatten()
             sim[15] = 1 - spatial.distance.cosine(ar1, qq)
             # rr comp
             im2 = Image.open('rr.png')
             ar2 = np.asarray(im2)
             rr = ar2.flatten()
             sim[16] = 1 - spatial.distance.cosine(ar1, rr)
             # ss com
             im2 = Image.open('ss.png')
             ar2 = np.asarray(im2)
             ss = ar2.flatten()
             sim[17] = 1 - spatial.distance.cosine(ar1, ss)
             # tt comp
             im2 = Image.open('tt.png')
             ar2 = np.asarray(im2)
             tt = ar2.flatten()
             sim[18] = 1 - spatial.distance.cosine(ar1, tt)
             # uu comp
             im2 = Image.open('uu.png')
             ar2 = np.asarray(im2)
             uu = ar2.flatten()
             sim[19] = 1 - spatial.distance.cosine(ar1, uu)
             # vv com
             im2 = Image.open('vv.png')
             ar2 = np.asarray(im2)
             vv = ar2.flatten()
             sim[20] = 1 - spatial.distance.cosine(ar1, vv)
             # ww comp
             im2 = Image.open('ww.png')
             ar2 = np.asarray(im2)
             ww = ar2.flatten()
             sim[21] = 1 - spatial.distance.cosine(ar1, ww)
             # xx comp
             im2 = Image.open('xx.png')
             ar2 = np.asarray(im2)
             xx = ar2.flatten()
             sim[22] = 1 - spatial.distance.cosine(ar1, xx)
             # yy com
             im2 = Image.open('yy.png')
             ar2 = np.asarray(im2)
             yy = ar2.flatten()
             sim[23] = 1 - spatial.distance.cosine(ar1, yy)
             # zz comp
             im2 = Image.open('zz.png')
             ar2 = np.asarray(im2)
             zz = ar2.flatten()
             sim[24] = 1 - spatial.distance.cosine(ar1, zz)
             # kk comp
             im2 = Image.open('kk.png')
             ar2 = np.asarray(im2)
             kk = ar2.flatten()
             sim[25] = 1 - spatial.distance.cosine(ar1, kk)
             mx = max(sim)
             ind = sim.index(mx)
             #print(alpha[ind])

             if (alpha[ind] == 'Q'):
                 #print('position')
                 pos11 = pos11 + 1
                 q[pos11]=pos[x]
                 #print(q[pos11])
                 pos11 = pos11 + 1
                 q[pos11]=pos[x+1]
                 #print(q[pos11])

    #print('posi')
    q[0]=0
    pos11=pos11+1
    q[pos11]=width1
    ##print(q[6])
    for x in range(0,pos11):
        if((q[x+1]-q[x])>1):
            im11 = im1.crop((q[x], 0, q[x+1] + 1, height1))
            name=os.path.join('C:\img',alpha[x]+'.png')
            im11.save(name)
            #im11.show()
            #print(alpha[x])

# load the original image
myFileList = createFileList1('C:\img')

for file in myFileList:
    #print(file)
    img_file = Image.open(file)
    width, height = img_file.size
    format = img_file.format
    mode = img_file.mode
    #img_file.show()
    value1=np.asarray(img_file)
    value = value1.flatten()
    down=0
    # finding down coordinate
    for y in range(height - 1, 0, -1):
        count = 0
        for x in range(0 + (y * (width)), (width) + (y * (width))):
            if (value[x] > 0):
                count = count + 1
                #  print(count)
        if (count > 2):
            down = y + 1
            #print('down=')
            #print(down)
            break
    result = []
    fou = open('result.csv', 'w')
    writer = csv.writer(fou)
    for i in range(0, down + 1):
        aux = []
        for j in range(0, width):
            aux.append(value1[i, j])
        writer.writerow(aux)
        result.append(aux)
    fou.close()
    array = np.array(result)
    im1 = Image.fromarray(array)
    width1, height1 = im1.size

    #print('down of last=')
    #print(height)
    #print(down)
    righ1 = 0
    position = 0
    p = 0
    i = 0
    pos = [0] * 5000
    for x in range(0,width1):
        count=0
        for y in range(0,height1):
            if(array[y,x]>0):
                count=count+1
        if(count==0):
            p=x
            break

    for x in range(0,width1):
        count=0

        for y in range(0,height1):
            if(array[y,x]>0):
               count=count+1
        if(count==0):
            if(x==(p+1)):
                p=p+1
            else:
                #print(p)
                pos[i]=p
                p=x
                i=i+1
                #print('start')
                #print(x)
                pos[i]=x
                i=i+1
        if(x==width-1):
            #print('last')
            #print(p)
            pos[i]=p
            i=i+1
            #print(x)
            pos[i]=x


    #print(x,y)
    #print('abcdef')
    #for x in range(1,i):
     #   print(pos[x])
    pygame.init()
    iii = 0
    alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'I', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U','V','W', 'X', 'Y', 'Z', 'K']
    for x in range(2, i-1):
        #print(pos[x])
         if((x%2)==0):
             im11 = im1.crop((pos[x], 0, pos[x+1] + 1, height1))
             newsiz = (30, 25)
             im11 = im11.resize(newsiz)
             ar1 = np.asarray(im11)
             ar1 = ar1.flatten()
             sim = [0] * 50
             #im1.show()

             # aaa comp
             im2 = Image.open('aa.png')
             ar2 = np.asarray(im2)
             aa = ar2.flatten()
             sim[0] = 1 - spatial.distance.cosine(ar1, aa)
             # bb comp
             im2 = Image.open('bb.png')
             ar2 = np.asarray(im2)
             bb = ar2.flatten()
             sim[1] = 1 - spatial.distance.cosine(ar1, bb)
             # ccc comp
             im2 = Image.open('cc.png')
             ar2 = np.asarray(im2)
             cc = ar2.flatten()
             sim[2] = 1 - spatial.distance.cosine(ar1, cc)
             # dd comp
             im2 = Image.open('dd.png')
             ar2 = np.asarray(im2)
             dd = ar2.flatten()
             sim[3] = 1 - spatial.distance.cosine(ar1, dd)
             # ee comp
             im2 = Image.open('ee.png')
             ar2 = np.asarray(im2)
             ee = ar2.flatten()
             sim[4] = 1 - spatial.distance.cosine(ar1, ee)
             # ff com
             im2 = Image.open('ff.png')
             ar2 = np.asarray(im2)
             ff = ar2.flatten()
             sim[5] = 1 - spatial.distance.cosine(ar1, ff)
             # gg comp
             im2 = Image.open('gg.png')
             ar2 = np.asarray(im2)
             gg = ar2.flatten()
             sim[6] = 1 - spatial.distance.cosine(ar1, gg)
             # hh comp
             im2 = Image.open('hh.png')
             ar2 = np.asarray(im2)
             hh = ar2.flatten()
             sim[7] = 1 - spatial.distance.cosine(ar1, hh)
             # jj com
             im2 = Image.open('jj.png')
             ar2 = np.asarray(im2)
             jj = ar2.flatten()
             sim[8] = 1 - spatial.distance.cosine(ar1, jj)
             # kk comp
             im2 = Image.open('ii.png')
             ar2 = np.asarray(im2)
             ii = ar2.flatten()
             sim[9] = 1 - spatial.distance.cosine(ar1, ii)
             # ll comp
             im2 = Image.open('ll.png')
             ar2 = np.asarray(im2)
             ll = ar2.flatten()
             sim[10] = 1 - spatial.distance.cosine(ar1, ll)
             # mm com
             im2 = Image.open('mm.png')
             ar2 = np.asarray(im2)
             mm = ar2.flatten()
             sim[11] = 1 - spatial.distance.cosine(ar1, mm)
             # nn comp
             im2 = Image.open('nn.png')
             ar2 = np.asarray(im2)
             nn = ar2.flatten()
             sim[12] = 1 - spatial.distance.cosine(ar1, nn)
             # oo comp
             im2 = Image.open('oo.png')
             ar2 = np.asarray(im2)
             oo = ar2.flatten()
             sim[13] = 1 - spatial.distance.cosine(ar1, oo)
             # pp com
             im2 = Image.open('pp.png')
             ar2 = np.asarray(im2)
             pp = ar2.flatten()
             sim[14] = 1 - spatial.distance.cosine(ar1, pp)
             # qq comp
             im2 = Image.open('qq.png')
             ar2 = np.asarray(im2)
             qq = ar2.flatten()
             sim[15] = 1 - spatial.distance.cosine(ar1, qq)
             # rr comp
             im2 = Image.open('rr.png')
             ar2 = np.asarray(im2)
             rr = ar2.flatten()
             sim[16] = 1 - spatial.distance.cosine(ar1, rr)
             # ss com
             im2 = Image.open('ss.png')
             ar2 = np.asarray(im2)
             ss = ar2.flatten()
             sim[17] = 1 - spatial.distance.cosine(ar1, ss)
             # tt comp
             im2 = Image.open('tt.png')
             ar2 = np.asarray(im2)
             tt = ar2.flatten()
             sim[18] = 1 - spatial.distance.cosine(ar1, tt)
             # uu comp
             im2 = Image.open('uu.png')
             ar2 = np.asarray(im2)
             uu = ar2.flatten()
             sim[19] = 1 - spatial.distance.cosine(ar1, uu)
             # vv com
             im2 = Image.open('vv.png')
             ar2 = np.asarray(im2)
             vv = ar2.flatten()
             sim[20] = 1 - spatial.distance.cosine(ar1, vv)
             # ww comp
             im2 = Image.open('ww.png')
             ar2 = np.asarray(im2)
             ww = ar2.flatten()
             sim[21] = 1 - spatial.distance.cosine(ar1, ww)
             # xx comp
             im2 = Image.open('xx.png')
             ar2 = np.asarray(im2)
             xx = ar2.flatten()
             sim[22] = 1 - spatial.distance.cosine(ar1, xx)
             # yy com
             im2 = Image.open('yy.png')
             ar2 = np.asarray(im2)
             yy = ar2.flatten()
             sim[23] = 1 - spatial.distance.cosine(ar1, yy)
             # zz comp
             im2 = Image.open('zz.png')
             ar2 = np.asarray(im2)
             zz = ar2.flatten()
             sim[24] = 1 - spatial.distance.cosine(ar1, zz)
             # kk comp
             im2 = Image.open('kk.png')
             ar2 = np.asarray(im2)
             kk = ar2.flatten()
             sim[25] = 1 - spatial.distance.cosine(ar1, kk)
             mx = max(sim)
             ind = sim.index(mx)
             if (alpha[ind] == 'I' and iii == 1):
                 print('I')
                 name = os.path.join('E:\loice', 'i' + '.mp3')
                 pygame.mixer.music.load(name)
                 pygame.mixer.music.play()
                 time.sleep(5)

             elif (alpha[ind] == 'I'):
                 iii = 1

             else:
                 if (iii == 1):
                     if (alpha[ind] == 'K'):
                         print(alpha[ind])

                         name = os.path.join('E:\loice', alpha[ind].lower() + '.mp3')
                         pygame.mixer.music.load(name)
                         pygame.mixer.music.play()
                         time.sleep(5)
                         iii = 0
                     else:
                         print('I')
                         name = os.path.join('E:\loice', 'i' + '.mp3')
                         pygame.mixer.music.load(name)
                         pygame.mixer.music.play()
                         time.sleep(5)
                         print(alpha[ind])
                         name = os.path.join('E:\loice', alpha[ind].lower() + '.mp3')
                         pygame.mixer.music.load(name)
                         pygame.mixer.music.play()
                         time.sleep(5)
                         iii = 0
                 else:
                     print(alpha[ind])
                     name = os.path.join('E:\loice', alpha[ind].lower() + '.mp3')
                     pygame.mixer.music.load(name)
                     pygame.mixer.music.play()
                     time.sleep(5)
    if (iii == 1):
        print('I')
        name = os.path.join('E:\loice', 'i' + '.mp3')
        pygame.mixer.music.load(name)
        pygame.mixer.music.play()
        time.sleep(5)
        iii = 0
    myFileList = createFileList3('C:\img')

    #audio=AudioSegment.from_file(name)


