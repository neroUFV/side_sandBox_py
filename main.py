#==========================================================================================
from tkinter import *

import numpy as np
import cv2
from openni import openni2

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np

import threading

#==========================================================================================
    #Inicializando kinect
#==========================================================================================
dist = 0
openni2.initialize()
dev = openni2.Device.open_any()
depth_stream = dev.create_depth_stream()
depth_stream.start()

#==========================================================================================
    #Definindo função para vizualização das curvas de nível
#==========================================================================================
    
def exib_CURV():
    n1 = 40 #numero de curvas de niveis

    X = np.arange(0, 640, 1)
    Y = np.arange(0, 480, 1)
    X = X[80:]
    Y = Y[10:480]
    X, Y = np.meshgrid(X, Y)


    frame = depth_stream.read_frame()
    frame_data = frame.get_buffer_as_uint16()

    img = np.frombuffer(frame_data, dtype=np.uint16)
    
    
    Z = np.reshape(img, (480, 640))
    Z = Z[10:480, 80:]
    Z = np.rot90(Z, 2) # rotacionar matriz
    
    fig, ax = plt.subplots()
    CS = ax.contour(X, Y, Z, n1) 
    ax.clabel(CS, fontsize=9, inline=True)
    ax.set_title('Curva de nível')
    plt.show()
#==========================================================================================
    #Definindo função para vizualização em 3D
#==========================================================================================

def exib_3D():
    X = np.arange(0, 640, 1)
    Y = np.arange(0, 480, 1)
    X = X[80:]
    Y = Y[10:480]
    X, Y = np.meshgrid(X, Y)

    frame = depth_stream.read_frame()
    frame_data = frame.get_buffer_as_uint16()
    img = np.frombuffer(frame_data, dtype=np.uint16)
    Z = np.reshape(img, (480, 640))
    Z = Z[10:480, 80:]
    Z = np.fliplr(Z) # rotacionar matriz

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=True)                    
    ax.zaxis.set_major_formatter('{x:.02f}')
    fig.colorbar(surf, shrink=0.5, aspect=5)  
    plt.show()
    


def exib_TR(depth_stream, mapoption = cv2.COLORMAP_JET, walloption=2, curv = True, n=5, thicknesscurv= 2, siz = [0,0]):
    
    def onMouse(event, x, y, flags, param):
        global dist   
        if event == cv2.EVENT_MOUSEMOVE:
            dist = (val1/val2)*imgray[y, x]

     
    cv2.namedWindow("Curvas em tempo real com mapa de cores", cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback("Curvas em tempo real com mapa de cores", onMouse)            
    while(True):
        
        frame = depth_stream.read_frame()
        frame_data = frame.get_buffer_as_uint16()
        img = np.frombuffer(frame_data, dtype=np.uint16)

        img.shape = (1, 480, 640)
        img = np.fliplr(img)    
        img = np.swapaxes(img, 0, 2)
        img = np.swapaxes(img, 0, 1)
        img = img[10:480, 80:]

        val1 = np.amax(img)

        img = cv2.convertScaleAbs(img, alpha=0.1) 
        img = cv2.rotate(img, cv2.ROTATE_180) 
        
        im_color = cv2.applyColorMap(img, mapoption) 
        im_color1 = cv2.applyColorMap(img, cv2.COLORMAP_BONE)
        
        if (siz[0] != 0) & (siz[1] != 0):
            im_color = cv2.resize(im_color, siz, interpolation=cv2.INTER_LINEAR)
            im_color1 = cv2.resize(im_color1, siz, interpolation=cv2.INTER_LINEAR)    
        
        imgray = cv2.medianBlur(cv2.cvtColor (im_color1, cv2.COLOR_BGR2GRAY), 43)

        val2 = np.amax(imgray)
        
        whitewall = (np.ones(im_color.shape))*255
        if walloption == 1: wall = whitewall
        elif walloption == 2: wall = im_color
        if curv == True:
            for i in range(255):     
                ret, thresh = cv2.threshold (imgray, (n*i), 255, cv2.THRESH_BINARY)
                contours, his  = cv2.findContours (thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
                cv2.drawContours(wall, contours, -1, (0,0,0), thicknesscurv)
        if type(dist) == np.float32:
            cv2.putText(wall,str(int(dist)),(10,((np.size(wall,0))-30)),cv2.FONT_HERSHEY_DUPLEX,1,(255,255,255),1)
            
        cv2.imshow("Curvas em tempo real com mapa de cores", (wall))    
          
        cv2.waitKey(34)
      
        if cv2.getWindowProperty("Curvas em tempo real com mapa de cores", cv2.WND_PROP_VISIBLE) <1:
            break


#==========================================================================================
    #adicionando thread
#==========================================================================================

def m1():
    x = threading.Thread(target=exib_TR(depth_stream,cv2.COLORMAP_JET,2,True,5, 2, [0,0]))
    x.start()

def m4():
    x = threading.Thread(target= exib_CURV)
    x.start()

def m5():
    x = threading.Thread(target=exib_3D)
    x.start()
#==========================================================================================
    #Criando interface gráfica
#==========================================================================================

janela = Tk()
janela.geometry("300x400")
janela.title("Interface em desenvolvimento")

a = 20
b = 30
c = 10


botao1 = Button(janela, text="Exibir curvas em tempo real com mapa", command= m1 )
botao1.place(height=20, width=220, x=a, y=(c + 2*b))


texto = Label(janela, text="Escolha modo de exibição do frame capturado:")
texto.place(height=20, width=250, x=a, y=(c + 5*b))

botao4 = Button(janela, text="Exibir curvas", command= m4)
botao4.place(height=20, width=80,x=a, y=(c + 6*b))

botao5 = Button(janela, text="Exibir superficie", command=m5)
botao5.place(height=20, width=100, x=a, y=(c + 7*b))

janela.mainloop()