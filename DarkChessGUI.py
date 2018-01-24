from tkinter import *
from tkinter import messagebox
import demo
chessboardphoto=None   #棋盤照片
chesstypephoto=[['兵.png','炮.png','紅馬.png','俥.png','相.png','仕.png','帥.png'],
                ['卒.png','包.png','黑馬.png','車.png','象.png','士.png','將.png']]
chessphoto=[[None,None,None,None,None,None,None,None,],    #棋子照片陣列
            [None,None,None,None,None,None,None,None,],
            [None,None,None,None,None,None,None,None,],
            [None,None,None,None,None,None,None,None,]]
chessboard=None   #棋盤canvas
window=None       #視窗變數
frame=None        #Frame變數
chesscolor=[[2,2,2,2,2,2,2,2],      #每格方格內棋子顏色，黑色為1，紅色為0，沒棋子為2
            [2,2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2,2]]
chesstype=[[8,8,8,8,8,8,8,8],
          [8,8,8,8,8,8,8,8],
          [8,8,8,8,8,8,8,8],
          [8,8,8,8,8,8,8,8]]  #棋子棋種變數
spacewidth=83                 #棋盤空格寬度間距
spaceheight=100;              #棋盤空格長度間距
center_w=39
center_h=50
window2=None
'''
chesstypeword=['卒(兵)','包(炮)','馬(紅馬)','車(俥)','象(相)','士(仕)','將(帥)']
chesscolorword=['紅','黑']
chesstypecheckbutton=[None,None,None,None,None,None,None]
chesscolorcheckbutton=[None,None]
chesstypecheckbuttonvar=[None,None,None,None,None,None,None]
chesscolorcheckbuttonvar=[None,None]'''
ismove=False
lastmoveh=0
lastmovew=0
turn=0
def Clickbutton(w,h,ismove):   #翻暗子後
  global chesstypecheckbuttonvar,chesscolorcheckbuttonvar,chesscolorcheckbutton
  global chesstypecheckbutton,chesstypephoto,chessphoto
  if (chesscolorcheckbuttonvar[0].get()==0) & (chesscolorcheckbuttonvar[1].get()==0) :
    messagebox.showerror(title='警告:錯誤產生',message='請選擇紅色或黑色')
    window2.destroy()
    return
  if (chesscolorcheckbuttonvar[0].get()==1) & (chesscolorcheckbuttonvar[1].get()==1):
    messagebox.showerror(title='警告:錯誤產生',message='只能選一種顏色')
    window2.destroy()
    return
  tmp=0
  for index in range(0,7):
    tmp+=chesstypecheckbuttonvar[index].get()
  if tmp==0 :
    messagebox.showerror(title='警告:錯誤產生',message='請選擇棋種')
    window2.destroy()
    return
  elif tmp>1:
    messagebox.showerror(title='警告:錯誤產生',message='只能選一種棋種')
    return
  chessboard.delete(chessphoto[h][w])
  nextcolor=0
  nexttype=0
  for index in range(0,2):
    if chesscolorcheckbuttonvar[index].get()==1:
      nextcolor=index
  for index in range(0,7):
    if chesstypecheckbuttonvar[index].get()==1:
      nexttype=index
  chesscolor[h][w]=nextcolor
  chesstype[h][w]=nexttype
  nextphoto=PhotoImage(file=chesstypephoto[nextcolor][nexttype])
  chessphoto[h][w]=nextphoto
  chessboard.create_image(10+w*spacewidth,20+h*spaceheight,anchor='nw',image=chessphoto[h][w])
  chessboard.place(x=0,y=0)
  window2.destroy()
  return
def callback(event):
  global spacewidth,spaceheight,chesstype
  w=(int)((event.x-10)/spacewidth)
  h=(int)((event.y-20)/spaceheight)
  global window2,chesstypeword,chesscolorword,chesstypecheckbutton,chesstypecheckbuttonvar
  global chesscolorcheckbuttonvar,chesscolorcheckbutton,ismove,lastmoveh,lastmovew
  if (ismove==False) & (chesstype[h][w]==8):         #暗子
    demo.flip(demo.state,h*8+w,demo.chesspos[h*8+w])
    newchesstype=demo.getType(demo.state,h*8+w)
    chesscolor[h][w]=newchesstype//7
    chesstype[h][w]=newchesstype%7
    nextphoto=PhotoImage(file=chesstypephoto[newchesstype//7][newchesstype%7])
    chessphoto[h][w]=nextphoto
    chessboard.create_image(10+w*spacewidth,20+h*spaceheight,anchor='nw',image=chessphoto[h][w])
    chessboard.place(x=0,y=0)
    '''window2=Toplevel()
    window2.title('請選擇棋種')
    window2.geometry('400x400')
    for index in range(0,2,1):
      chesscolorcheckbuttonvar[index]=IntVar()
      chesscolorcheckbutton[index]=Checkbutton(window2,text=chesscolorword[index],
      variable=chesscolorcheckbuttonvar[index],onvalue=1,offvalue=0)
      chesscolorcheckbutton[index].place(x=100+index*100,y=30)
    for index in range(0,7,1):
      chesstypecheckbuttonvar[index]=IntVar()
      chesstypecheckbutton[index]=Checkbutton(window2,text=chesstypeword[index],
      variable=chesstypecheckbuttonvar[index],onvalue=1,offvalue=0)
      chesstypecheckbutton[index].place(x=100,y=70+index*25)
      okbutton=Button(window2,text='確定',width=10,height=2,command=lambda:Clickbutton(w,h,ismove))
      okbutton.place(x=150,y=300)'''
  elif ismove==False:                 
    window2.destroy()
    lastmoveh=h
    lastmovew=w
    ismove=True
  else:
    chessboard.delete(chessphoto[h][w])
    chessboard.place(x=0,y=0)
    chessboard.delete(chessphoto[lastmoveh][lastmovew])
    chessboard.place(x=0,y=0)
    chessphoto[h][w]=None
    chessphoto[lastmoveh][lastmovew]=None
    chesscolor[h][w]=chesscolor[lastmoveh][lastmovew]
    chesstype[h][w]=chesstype[lastmoveh][lastmovew]
    chesstype[lastmoveh][lastmovew]=None
    chesscolor[lastmoveh][lastmovew]=None
    nextphoto=PhotoImage(file=chesstypephoto[chesscolor[h][w]][chesstype[h][w]])
    chessphoto[h][w]=nextphoto
    chessboard.create_image(10+w*spacewidth,20+h*spaceheight,anchor='nw',image=nextphoto)
    chessboard.place(x=0,y=0)
    ismove=False
def check(window,toll,var1,var2):   #檢查程式開始執行是玩家選的表單選項是否正確
  global turn
  if (var1.get()+var2.get())==0:
    messagebox.showerror(title='警告:錯誤產生',message='請選擇先手或後手')
    return
  elif (var1.get()+var2.get())==2:
    messagebox.showerror(title='警告:錯誤產生',message='請選擇先手或後手')
  else:
    turn=var1.get()
    window.attributes("-topmost",True)
    toll.destroy()
def Createwindow():
  global chessboard,chesstype,window,frame,chessphoto,chessboardphoto
  window=Tk()
  window.title('MyWindow')
  window.geometry('870x600')
  frame=Frame(window,width=870,height=660)
  chessboardphoto=PhotoImage(file='board2.png')
  chessboard=Canvas(window,width=665,height=416)
  chessboard.bind('<Button-1>',callback)
  chessboard.pack()
  chessboard.create_image(0,0,anchor='nw',image=chessboardphoto)
  for h in range(0,4,1):
    for w in range(0,8,1):
      chessphoto[h][w]=PhotoImage(file='棋子背面2.png')
      chessboard.create_image(10+w*spacewidth,20+h*spaceheight,anchor='nw',image=chessphoto[h][w])
  chessboard.place(x=0,y=0)
  toll=Toplevel()
  toll.geometry('300x300')
  toll.attributes("-topmost",True)
  var1=IntVar()
  var2=IntVar()
  checkbutton1=Checkbutton(toll,text='先手',variable=var1,onvalue=1,offvalue=0)
  checkbutton1.place(x=150,y=20)
  checkbutton2=Checkbutton(toll,text='後手',variable=var2,onvalue=1,offvalue=0)
  checkbutton2.place(x=150,y=120)
  button=Button(toll,text='確定',command=lambda:check(window,toll,var1,var2))
  button.place(x=150,y=200)
demo.shuffleBoard(demo.chesspos)
print(demo.chesspos)
Createwindow()
mainloop()

