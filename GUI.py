'''
GUI負責事項
1.洗盤  .....完成
2.點選後負責判斷走步是否合法 .....完成
3.維護2維棋盤(MCS裡用bitboard儲存相同棋盤狀態)
4.走步後改變MCS裡的棋盤狀態  
5.判斷棋局是否結束  .....完成


0  紅兵  1  紅炮  2  紅馬  3  紅車  4  紅象 
5  紅仕  6  紅帥  7  黑兵  8  黑炮  9  黑馬 
10  黑車  11 黑象 12 黑士  13 黑將  14 暗子
15 空格
'''
from tkinter import *
from tkinter import messagebox
import MCS
import random
import threading
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
showboard=[[14,14,14,14,14,14,14,14],
          [14,14,14,14,14,14,14,14],
          [14,14,14,14,14,14,14,14],
          [14,14,14,14,14,14,14,14]]  #畫面上顯示的棋種變數
realboard=[[0,0,0,0,0,1,1,2],
          [2,3,3,4,4,5,5,6],
          [7,7,7,7,7,8,8,9],
          [9,10,10,11,11,12,12,13]]  #洗盤後的棋子分布
deathcnt=[0,0] #紅方和黑方死亡統計，前面是紅方後面是黑方
spacewidth=83                 #棋盤空格寬度間距
spaceheight=100;              #棋盤空格長度間距
center_w=39
center_h=50
ismove=False
lastmoveh=0
lastmovew=0
AIcolor=-1    #目前輪到哪一種顏色，0是紅色，1是黑色
def canMove(pos,newpos):
  global showboard
  if showboard[newpos//8][newpos%8]!=15:
    return False
  if pos//8==0 and pos-newpos==8: #在頂邊不能往上移
    return False
  if pos//8==3 and newpos-pos==8: #在底邊不能往下移
    return False
  if pos%8==0 and pos-newpos==1: #在最左邊不能往左移
    return False
  if pos%8==7 and newpos-pos==7: #在最右邊不能往右移
    return False
  if abs(newpos-pos)!=8 and abs(newpos-pos)!=1:
    return False
  return True
def canEat(pos,newpos):
  global showboard
  chess1=showboard[pos//8][pos%8]      #吃子的棋種
  chess2=showboard[newpos//8][newpos%8]   #被吃得棋種
  if (chess1//7==chess2//7) or (chess2==15):   #顏色相同不能互吃
    return False
  if chess1==14 or chess2==14: #其中一方為暗子
    return False
  if chess1==1 or chess1==8:
    if (pos%8!=newpos%8) and (pos//8!=newpos//8):
      return False
    start=stop=jump=cnt=0
    if pos%8==newpos%8:
      jump=8
    else:
      jump=1
    start=min(pos,newpos)
    stop=max(pos,newpos)
    for i in range(start+jump,stop,jump):
      if showboard[i//8][i%8]!=15:
        cnt+=1
    if cnt!=1:
      return False
    else:
      return True
  else:
    if abs(newpos-pos)!=8 and abs(newpos-pos)!=1:
      return False
    if pos%8==0 and pos-newpos==1:     #在左邊不能往左吃
      return False
    elif pos%8==7 and newpos-pos==1:   #在右邊不能往右吃
      return False
    elif pos//8==0 and pos-newpos==8:  #在頂邊不能往上吃
      return False
    elif pos//8==3 and newpos-pos==8:  #在下邊不能往下吃
      return False
    elif (chess1==13 and chess2==0) or (chess1==6 and chess2==7):#將不能吃兵，帥不能吃卒
      return False
    elif (chess1==0 and chess2==13) or (chess1==7 and chess2==6):#兵吃將，卒吃帥
      return True
    elif (chess1%7)>=(chess2%7) :
      return True
    else:
      return False
def action(center):
  global AIcolor,showboard,realboard,deathcnt
  searchdepth=6
  print('===========================================')
  print('before:')
  MCS.Max(AIcolor,MCS.state,MCS.darkchess,MCS.boarddic,MCS.boardstring,1,searchdepth,center,0) 
  bestpos=MCS.finalpos
  bestact=MCS.finalact
  #print(MCS.finalpos,MCS.finalact,MCS.finalscore)
  MCS.printBoard(MCS.state)
  #print('final decision ',bestpos,bestact)
  if bestact<4:
    direction=[-1,-8,1,8]
    h1=bestpos//8
    w1=bestpos%8
    h2=(bestpos+direction[bestact])//8
    w2=(bestpos+direction[bestact])%8
    MCS.Move(MCS.state,MCS.boardstring,showboard[h1][w1],h1*8+w1,h2*8+w2) 
    showboard[h2][w2]=showboard[h1][w1]
    showboard[h1][w1]=15
    changePicture(h2,w2,showboard[h2][w2])
    changePicture(h1,w1,showboard[h1][w1])
  elif bestact<8:
    direction=[-1,-8,1,8]
    h1=bestpos//8
    w1=bestpos%8
    if showboard[h1][w1]!=1 and showboard[h1][w1]!=8:
      h2=(bestpos+direction[bestact-4])//8
      w2=(bestpos+direction[bestact-4])%8
    else:
      tmp=MCS.findCannonTarget(MCS.state,bestpos,showboard[h1][w1],bestact-4)
      h2=tmp//8
      w2=tmp%8
    #print(bestact,bestpos,h1,w1,h2,w2)
    deathcnt[showboard[h2][w2]//7]+=1
    MCS.eat(MCS.state,MCS.boardstring,showboard[h1][w1],showboard[h2][w2],bestpos,h2*8+w2)
    showboard[h2][w2]=showboard[h1][w1]
    showboard[h1][w1]=15
    #print('In GUI ',showboard[h1][w1],'in pos',h1*8+w1,' can eat ',showboard[h2][w2],' in pos ',h2*8+w2)
    changePicture(h1,w1,showboard[h1][w1])
    changePicture(h2,w2,showboard[h2][w2])
  else:
    showboard[bestpos//8][bestpos%8]=realboard[bestpos//8][bestpos%8]
    #print('In GUI flip option in pos',bestpos,' chesstype ',showboard[bestpos//8][bestpos%8])
    MCS.flip(MCS.state,MCS.boardstring,bestpos,showboard[bestpos//8][bestpos%8])
    MCS.darkchess.remove(showboard[bestpos//8][bestpos%8])
    changePicture(bestpos//8,bestpos%8,showboard[bestpos//8][bestpos%8])
  #print('after')
  #MCS.printBoard(MCS.state)
def callback(event):     #點GUI後的處理
  global window
  global spacewidth,spaceheight,chesstype,deathcnt,AIcolor
  global ismove,lastmoveh,lastmovew,showboard,realboard,window
  needsearch=0
  searchdepth=6
  w=(int)((event.x-10)/spacewidth)
  h=(int)((event.y-20)/spaceheight)
  #print('************************************************')
  #MCS.printBoard(MCS.state)
  if (ismove==False) and (showboard[h][w]==14):         #暗子
    newchesstype=realboard[h][w]
    MCS.flip(MCS.state,MCS.boardstring,h*8+w,newchesstype)    #改變bitboard內容
    MCS.darkchess.remove(newchesstype)
    #MCS.printBoard(MCS.state)
    showboard[h][w]=newchesstype
    if AIcolor==-1:    #第一手是玩家，AI是另一色
        AIcolor=1-(showboard[h][w]//7)    #設定AI控制顏色
    needsearch=1
    changePicture(h,w,showboard[h][w])
  elif ismove==False and showboard[h][w]<=13 and AIcolor!=(showboard[h][w]//7):   #有明子                 
    lastmoveh=h
    lastmovew=w
    ismove=True
  elif AIcolor==(showboard[h][w]//7) and canEat(lastmoveh*8+lastmovew,h*8+w):#有明子可吃
    MCS.eat(MCS.state,MCS.boardstring,showboard[lastmoveh][lastmovew],showboard[h][w],lastmoveh*8+lastmovew,h*8+w)
    #MCS.printBoard(MCS.state)
    deathcnt[showboard[h][w]//7]+=1
    showboard[h][w]=showboard[lastmoveh][lastmovew]
    showboard[lastmoveh][lastmovew]=15
    changePicture(h,w,showboard[h][w])
    changePicture(lastmoveh,lastmovew,showboard[lastmoveh][lastmovew])
    ismove=False
    if deathcnt[0]!=16 and deathcnt[1]!=16:
      needsearch=1
  elif AIcolor!=(showboard[h][w]//7) and canMove(lastmoveh*8+lastmovew,h*8+w):#有空格可移
    MCS.Move(MCS.state,MCS.boardstring,showboard[lastmoveh][lastmovew],lastmoveh*8+lastmovew,h*8+w)
    #MCS.printBoard(MCS.state)
    showboard[h][w]=showboard[lastmoveh][lastmovew]
    showboard[lastmoveh][lastmovew]=15
    changePicture(h,w,showboard[h][w])
    changePicture(lastmoveh,lastmovew,showboard[lastmoveh][lastmovew])
    ismove=False
    needsearch=1
  else:
    messagebox.showerror(title='警告:錯誤產生',message='操作錯誤')
    ismove=False
  if needsearch==1:
    #MCS.Max(AIcolor,MCS.state,MCS.darkchess,1,searchdepth,h*8+w)
    t1=threading.Thread(target=lambda:action(h*8+w))
    t1.start()
  needsearch=0
  if deathcnt[0]==16:
    messagebox.showinfo("棋局結束","黑方勝")
  elif deathcnt[1]==16:
    messagebox.showinfo("棋局結束","紅方勝")
  #print('final best action is ',MCS.finalact,' on ',MCS.finalpos)
  #MCS.printBoard(MCS.state)
def changePicture(h,w,chesstype):
  global chessphoto,chessboard,chesscolor,showboard
  chessboard.delete(chessphoto[h][w])
  if chesstype!=15:
    nextphoto=PhotoImage(file=chesstypephoto[chesstype//7][chesstype%7])
    chessboard.create_image(10+w*spacewidth,20+h*spaceheight,anchor='nw',image=nextphoto)
    chessphoto[h][w]=nextphoto
    #print('Change picture in pos ',h*8+w,' with  not blank')
  else:
    chessphoto[h][w]=None
    #print('Change picture in pos ',h*8+w,' with blank')
  chessboard.place(x=0,y=0)
  #print('return from changePicture')
def check(window,toll,var1,var2):   #檢查程式開始執行是玩家選的表單選項是否正確
  global AIcolor
  if (var1.get()+var2.get())==0:
    messagebox.showerror(title='警告:錯誤產生',message='請選擇先手或後手')
    return
  if (var1.get()+var2.get())==2:
    messagebox.showerror(title='警告:錯誤產生',message='不能同時選')
  if var1.get()==0:
    pos=random.randint(0,31)
    showboard[pos//8][pos%8]=realboard[pos//8][pos%8]
    MCS.flip(MCS.state,pos,showboard[pos//8][pos%8])
    MCS.darkchess.remove(showboard[pos//8][pos%8])
    changePicture(pos//8,pos%8,showboard[pos//8][pos%8])
    AIcolor=showboard[pos//8][pos%8]//7
  window.attributes('-topmost',True)
  toll.destroy()
def shuffleBoard():
  global realboard
  for i in range(1,10000):
    pos1=random.randint(0,31)
    pos2=random.randint(0,31)
    h1=pos1//8
    w1=pos1%8
    h2=pos2//8
    w2=pos2%8
    tmp=realboard[h1][w1]
    realboard[h1][w1]=realboard[h2][w2]
    realboard[h2][w2]=tmp
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
  shuffleBoard()
Createwindow()
window.after(1000)
window.mainloop()

