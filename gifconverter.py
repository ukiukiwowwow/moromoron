import tkinter as Tk
from tkinter import filedialog
import sys
import glob
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import shutil
import re
plt.rcParams['savefig.bbox'] = 'tight'

class Application(Tk.Frame):
    def __init__(self, master=None):
        Tk.Frame.__init__(self, master)
        self.master.title('gif fps')
        self.master.geometry('300x100')

        # 変数初期化
        self.ToDoNumber = 0
        self.ToDo = []
        self.txt = []
        self.spent = []
        self.spentNumber = []
        self.filename=""
        action = Tk.IntVar()
        action.set(0)
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        menubar = Tk.Menu(self)

        # ウィジェットの生成・配置
        
        file = Tk.Menu(menubar, tearoff = False)
        file.add_command(label = u"ファイル", under = 0, command = self.file)
        file.add_separator
        file.add_separator
        file.add_command(label = u"終了", under = 0, command = sys.exit)
        menubar.add_cascade(label="file", underline = 0, menu=file)
        #self.create_widgets()
        self.entry = Tk.Entry(self, bd=1,width=30)
        self.entry.insert(0, u'Enter gif animation fps')
        self.entry.bind('<FocusIn>', self.on_entry_click)
        self.entry.bind('<FocusOut>', self.on_focusout)
        self.entry.config(fg = 'grey')
        #self.entry.pack(side="left")
        
        self.entry.grid(row=0,column=0)
        self.Button = Tk.Button(self, text='変換')
        self.Button.bind('<Button-1>', self.convert)
        self.Button.grid(row=0, column=1)
        self.error=u""
        self.Static1 = Tk.Label(self,text=self.error,foreground='#ff0000')
        self.Static1.grid(row=2,column=0)
        self.writedirectory=u"./"
        master.configure(background='white',menu = menubar)
        
        


        self.pack()



    def on_entry_click(self,event):
        print(00)
        if self.entry.get() == u'Enter gif animation fps':
           self.entry.delete(0, "end") # delete all the text in the entry
           self.entry.insert(0, u'') #Insert blank for user input
           self.entry.config(fg = 'black')
           print(self.filename)
    def on_focusout(self,event):
        print(10)
        if self.entry.get() == u'':
            self.entry.delete(0, "end");self.entry.insert(0, u'Enter gif animation fps');print(1)
            self.entry.config(fg = 'grey')
    def file(self): 
        self.readfilename=u""
        self.readfilename = filedialog.askopenfilename()
        self.Static1 = Tk.Label(self,text=u"")
        self.Static1 = Tk.Label(self,text=self.readfilename)
        self.Static1.grid(row=1,column=0)
    
    
    def convert(self,event): 
        fps=self.entry.get()
        self.error=u""
        self.Static1 = Tk.Label(self,text=u"			",foreground='#ffffff')
        self.Static1.grid(row=2,column=0)
        try:
            fps=int(fps)
        except:
            self.error=u"Input string is not number."
            self.Static1 = Tk.Label(self,text=self.error,foreground='#ff0000')
            self.Static1.grid(row=2,column=0)
            return
        if fps<=0:
            self.error=u"Fps must be greater than 0."
            self.Static1 = Tk.Label(self,text=self.error,foreground='#ff0000')
            self.Static1.grid(row=2,column=0)
            return
        else:
            self.error=u""
            self.Static1 = Tk.Label(self,text=self.error,foreground='#ff0000')
            self.Static1.grid(row=2,column=0)
            #self.writedirectory= filedialog.askdirectory(initialdir=self.writedirectory)
            self.f=filedialog.asksaveasfilename(defaultextension=".gif")
            w,h=self.processImage(self.readfilename)
            self.makegif(fps=fps,width=w,height=h,directory=self.writedirectory)
            shutil.rmtree("./gifwork")
            
    def processImage(self,infile):
        try:
            im = Image.open(infile)
            os.mkdir("./gifwork")
        except IOError:
            print("Cant load", infile)
            sys.exit(1)
        i = 0
        mypalette = im.getpalette()

        try:
            while 1:
                im.putpalette(mypalette)
                new_im = Image.new("RGBA", im.size)
                width,height=im.size
                new_im.paste(im)
                new_im.save("./gifwork/"+str(i)+'.png')

                i += 1
                im.seek(im.tell() + 1)

        except EOFError:
            return width,height
            pass 
            
    def makegif(self,fps=60,width=100,height=100,directory=u"./"):
        folderName="gifwork"
        picList = glob.glob(folderName + "\*.png")
        L=[(re.search("[0-9]+", x).group(), x) for x in picList]
        L.sort(key=lambda x:int(x[0]))
        picList=[x[1] for x in L]
        if(width!=0 and height!=0):
            fig = plt.figure(figsize=(int(width/100),int(height/100)))
        else:
            fig = plt.figure()
        ax = plt.gca() # get current axis
        ax.spines["right"].set_color("none")  
        ax.spines["left"].set_color("none")   
        ax.spines["top"].set_color("none")   
        ax.spines["bottom"].set_color("none")
        
        plt.tick_params(labelbottom='off')
        plt.tick_params(labelleft='off')
        plt.axis("off")
        #空のリストを作る
        ims = []

        for i in range(len(picList)):
        
            tmp = Image.open(picList[i])
        
            ims.append([plt.imshow(tmp,aspect='auto',interpolation="spline36")])
            #
        plt.tight_layout(pad=0.0, w_pad=0.0, h_pad=0.0)
        ani = animation.ArtistAnimation(fig, ims)
        ani.save(self.f,writer="imagemagick", fps=fps)
        


root = Tk.Tk()
app  = Application(master=root)
app.mainloop()