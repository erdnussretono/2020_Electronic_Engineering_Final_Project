import tkinter
import serial

ser = serial.Serial('/dev/ttyAMA0',9600)
tsensor='/sys/bus/w1/devices/28-03089794462b/w1_slave'

print(ser.portstr)

global a
global b
global c
global d
a=b=c=d='0'

def WaterINClick():
    ser.write(b'A')
    
def WaterOUTClick():
    ser.write(b'B')
    
def FeedClick():
    ser.write(b'C')
    
def LedONClick():
    ser.write(b'D')
    
def LedOFFClick():
    ser.write(b'E')
    
def T20():
    global a
    a = '1'
    if int(settemp())<20:
        ser.write(b'F')
    

def T23():
    global b
    b = '1'    
    if int(settemp())<23:
        ser.write(b'F')
    
def T25():
    global c
    c = '1'
    if int(settemp())<25:
        ser.write(b'F')
    
def T27():
    global d
    d = '1'
    if int(settemp())<27:
        ser.write(b'F')
        
def close_TEMP():
    newwindow.destroy()
        
def TEMPBOX():
    newwindow = tkinter.Toplevel(window)
    newwindow.geometry("800x480+0+0")
    t20 = tkinter.Button(newwindow, text = "20", font=('Roman, Sans',25), command = T20)
    t23 = tkinter.Button(newwindow, text = "23", font=('Roman, Sans',25), command = T23)
    t25 = tkinter.Button(newwindow, text = "25", font=('Roman, Sans',25), command = T25)
    t27 = tkinter.Button(newwindow, text = "27", font=('Roman, Sans',25), command = T27)
    
    t20.pack(side = "left", fill="both",expand=True)
    t23.pack(side = "left", fill="both",expand=True)
    t25.pack(side = "left", fill="both",expand=True)
    t27.pack(side = "left", fill="both",expand=True)
        
def traw():
    f=open(tsensor,'r')
    lines=f.readlines()
    f.close()
    return lines

def readtemp():
    lines=traw()
    while lines[0].strip()[-3:]!='YES':
        time.sleep(0.2)
        lines=traw()
    tout=lines[1].find('t=')
    if tout!=-1:
        tstr=lines[1].strip()[tout+2:]
        tc = round(float(tstr)/1000,1)
        space=('C')
        return tc,space

def settemp():
    lines=traw()
    while lines[0].strip()[-3:]!='YES':
        time.sleep(0.2)
        lines=traw()
    tout=lines[1].find('t=')
    if tout!=-1:
        tstr=lines[1].strip()[tout+2:]
        tc = round(float(tstr)/1000,1)
        
        return tc
    
def hitteroff():
    global a
    global b
    global c
    global d
    
    if int(settemp())<23:
        a = '0';
    
    if int(settemp())>25:
        b = '0';
    
    if int(settemp())>27:
        c = '0';
    
    if int(settemp())>30:
        d = '0';
        
    if a=='0' and b=='0' and c=='0' and d=='0':
        ser.write(b'G')
    
def on_alarm(top_level_window):
        global var
        var.set(readtemp())
        hitteroff()
        
        top_level_window.after(1000,on_alarm,top_level_window)

window=tkinter.Tk()
window.title("Aquarium")
window.resizable(True,True)

var=tkinter.StringVar()
label=tkinter.Label(window,font=('Roman, Sans',40),fg='red',textvariable = var)
label.pack(anchor="nw",fill="x")

WaterIN = tkinter.Button(window, text = "Water IN", font=('Roman, Sans',20),command = WaterINClick)
WaterOUT = tkinter.Button(window, text = "Water OUT", font=('Roman, Sans',20),command = WaterOUTClick)
Feed = tkinter.Button(window, text = "FEED", font=('Roman, Sans',20),command = FeedClick)
LedON = tkinter.Button(window, text= "LedON", font=('Roman, Sans',20),command = LedONClick)
LedOFF = tkinter.Button(window, text= "LedOFF", font=('Roman, Sans',20),command = LedOFFClick)
HITTER = tkinter.Button(window, text= "SetTEMP", font=('Roman, Sans',20),command = TEMPBOX)
WaterIN.pack(side="left",fill="both",expand=True)
WaterOUT.pack(side="left",fill="both",expand=True)
Feed.pack(side="left",fill="both",expand=True)
LedON.pack(side="left",fill="both",expand=True)
LedOFF.pack(side="left",fill="both",expand=True)
HITTER.pack(side="right",fill="both",expand=True)
window.after(1000, hitteroff)
window.after(1000, on_alarm, window)
window.mainloop()