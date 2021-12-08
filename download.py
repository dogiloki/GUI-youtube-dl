from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from threading import Thread
from youtube_dl import YoutubeDL
import os

root=Tk()

root.title("Descarga videos")
root.resizable(False,False)

frame=Frame(root)
frame.pack(fill="x")
frame_video=Frame(root)
frame_video.pack(fill="x")
frame_videos=Frame(root,borderwidth=1)
frame_videos.pack(fill="x")

def sele_video():
    if caja_path.get()=='':
        messagebox.showinfo(message="Eliga un lugar de almacenamiento",title="Advertencia")
    else:
        try:
            id=tb.item(tb.selection())['text']
            url=text_url['text']
            Thread(target=lambda:download(url,id)).start()
        except:
            messagebox.showinfo(message="Eliga un formato",title="Advertencia")

#Tabla de videos
tb=ttk.Treeview(frame_videos,columns=("#1","#2","#3","#4","#5","#6","#7"))
tb.column("#0",width=80)
tb.column("#1",width=80)
tb.column("#2",width=80)
tb.column("#3",width=80)
tb.column("#4",width=80)
tb.column("#5",width=80)
tb.column("#6",width=80)
tb.column("#7",width=80)
tb.heading("#0",text="ID")
tb.heading("#1",text="Extensión")
tb.heading("#2",text="Video")
tb.heading("#3",text="Audio")
tb.heading("#4",text="Resolución")
tb.heading("#5",text="Calidad")
tb.heading("#6",text="FPS")
tb.heading("#7",text="Tamaño")
tb.grid(row=0,column=0,columnspan=2,padx=5,pady=5,sticky="w")
btn_download=Button(frame_videos,text="Descargar",font=("arial",10),command=sele_video)
btn_download.grid(row=1,column=0,padx=5,pady=5,sticky="w")

#--- Functions ---

def download(url,id):
    if id!=-1 and id!="":
        dl_opts={
            'format':str(id),
            'outtmpl':caja_path.get()+"/%(title)s.%(ext)s",
            'progress_hooks':[my_hook]
        }
        with YoutubeDL(dl_opts) as dl:
            btn_download['state']="disabled"
            dl.download([str(url)])

def my_hook(rs):
    progress_video=ttk.Progressbar(frame_videos)
    progress_video.grid(row=1,column=1,padx=5,pady=5,sticky="w")
    print("\n-------"+str(rs))
    if rs['status']=='finished':
        progress_video.step(0)
        btn_download['state']="normal"
    if rs['status']=='downloading':
        progress_video.step(float(rs['_percent_str'].replace('%','')))

def examinar():
    path=filedialog.askdirectory()
    if path!="":
        os.chdir(path)
        caja_path.insert(0,path)

def search():
    btn_search['state']="disabled"
    dl_opts={}
    with YoutubeDL(dl_opts) as dl:
        feactures=dl.extract_info(caja_url.get(),download=False)

        title=""
        try:
            title=feactures['title']
        except: title=""
        duration=0
        try:
            duration=int(feactures['duration'])
        except: duration=0
        channel=""
        try:
            channel=feactures['channel']
        except: channel=""
        text_url.config(text=caja_url.get())
        text_title.config(text=title)
        text_duration.config(text=str(int(duration/60))+":"+str(duration%60))
        text_canal.config(text=channel)

        for f in feactures['formats']:
            format_id=""
            try:
                format_id=f['format_id']
            except: format_id=""
            ext=""
            try:
                ext=f['ext']
            except: ext=""
            vcodec=""
            try:
                if f['vcodec']=="none":
                    vcodec="none"
                else:
                    vcodec="Video"
            except: vcodec=""
            acodec=""
            try:
                if f['acodec']=="none":
                    acodec="none"
                else:
                    acodec="Audio"
            except: acodec=""
            width=""
            try:
                width=f['width']
            except: width=""
            height=""
            try:
                height=f['height']
            except: height=""
            format_note=""
            try:
                format_note=f['format_note']
            except: format_note=""
            fps=""
            try:
                fps=f['fps']
            except: fps=""
            filesize=""
            try:
                filesize=int(f['filesize'])
                filesize=(filesize/1024)/1024
            except: filesize=""
            tb.insert("",END,text=str(format_id),values=(str(ext),str(vcodec),str(acodec),str(width)+"x"+str(height),str(format_note),str(fps)+str("fps"),str(filesize)))
    btn_search['state']="normal"

#--- Widget ---

#Url
Label(frame,text="URL: ",font=("arial",12)).grid(row=0,column=0,sticky="w")
caja_url=Entry(frame,font=("arial",12))
caja_url.grid(row=0,column=1)
btn_search=Button(frame,text="Buscar",font=("arial",10),command=lambda:Thread(target=search).start())
btn_search.grid(row=0,column=2,sticky="w",padx=5,pady=5)

#Destino
Label(frame,text="Destino: ",font=("arial",12)).grid(row=1,column=0,sticky="w")
caja_path=Entry(frame,font=("arial",12))
caja_path.grid(row=1,column=1)
btn_path=Button(frame,text="Examinar",font=("arial",10),command=examinar)
btn_path.grid(row=1,column=2,sticky="w",padx=5,pady=5)

#Título
Label(frame_video,text="URL: ",font=("arial",10)).grid(row=0,column=0,sticky="w",padx=5,pady=5)
text_url=Label(frame_video,text="",font=("arial",10))
text_url.grid(row=0,column=1,sticky="w")

#Título
Label(frame_video,text="Título: ",font=("arial",10)).grid(row=1,column=0,sticky="w",padx=5,pady=5)
text_title=Label(frame_video,text="",font=("arial",10))
text_title.grid(row=1,column=1,sticky="w")

#Duración
Label(frame_video,text="Duración: ",font=("arial",10)).grid(row=2,column=0,sticky="w",padx=5,pady=5)
text_duration=Label(frame_video,text="",font=("arial",10))
text_duration.grid(row=2,column=1,sticky="w")

#Canal
Label(frame_video,text="Canal: ",font=("arial",10)).grid(row=3,column=0,sticky="w",padx=5,pady=5)
text_canal=Label(frame_video,text="",font=("arial",10))
text_canal.grid(row=3,column=1,sticky="w")

root.mainloop()