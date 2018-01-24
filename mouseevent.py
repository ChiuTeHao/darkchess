from tkinter import *
wnd=Tk()
wnd.title('簡單的滑鼠事件')
def callback(event):
  print('滑鼠座標:x-{} y-{}'.format(event.x,event.y))
def printval():
  print(var1.get(),var2.get())
var1=IntVar()
var2=IntVar()
checkbutton1=Checkbutton(wnd,text='A',variable=var1,onvalue=1,offvalue=0,command=printval)
checkbutton2=Checkbutton(wnd,text='B',variable=var2,onvalue=1,offvalue=0,command=printval)
checkbutton2.pack()
checkbutton1.pack()
frame=Frame(wnd,width=300,height=300)
frame.bind('<Button-1>',callback)
frame.pack()
wnd.mainloop()
