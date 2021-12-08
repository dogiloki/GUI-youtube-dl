from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from threading import Thread
from youtube_dl import YoutubeDL
import os
from database import *

class Gui(Frame):

    def __init__(self,master=None):
        super().__init__(master);
        self.pack()
        self.widgets()
        self.getVideos()

    # Cambiar ruta de almacenamiento
    def examinar(self):
        path=filedialog.askdirectory()
        if path!="":
            os.chdir(path)
            self.caja_path.insert(0,path)

    # Buscar video
    def search(self):
        self.caja_formats['values']={}
        self.btn_search['state']="disabled"
        dl_opts={}
        with YoutubeDL(dl_opts) as dl:
            features=[]
            try:
                features=dl.extract_info(self.caja_url.get(),download=False)
            except:
                messagebox.showinfo(message="URL no válida",title="Advertencia")
                self.btn_search['state']="normal"
            title=""
            try:
                title=features['title']
            except: title=""
            duration=0
            try:
                duration=int(features['duration'])
            except: duration=0
            channel=""
            try:
                channel=features['channel']
            except: channel=""
            self.text_url.config(text=self.caja_url.get())
            self.text_title.config(text=title)
            self.text_duration.config(text=str(int(duration/60))+":"+str(duration%60))
            self.text_canal.config(text=channel)
            for f in features['formats']:
                sublist=[]
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
                    filesize=self.formatSize(f['filesize'])
                except: filesize=""
                sublist.append(format_id)
                sublist.append(ext)
                sublist.append(vcodec)
                sublist.append(acodec)
                sublist.append(str(width)+"x"+str(height))
                sublist.append(format_note)
                sublist.append(str(fps)+"fps")
                sublist.append(filesize)
                self.list_formats.append(sublist)
        self.caja_formats['values']=self.list_formats
        self.btn_search['state']="normal"

    # Agregar video
    def add(self,btn):
        if self.caja_path.get()=='':
             messagebox.showinfo(message="Seleccione un lugar de almacenamiento",title="Advertencia")
             return 0
        btn['state']="disabled"
        format_id=""
        if self.caja_formats.current()>=0 and self.caja_path.get()!="":
            selection_format=self.caja_formats.current()
            format_id=self.list_formats[selection_format][0]
            self.text_espacio.config(text=self.list_formats[selection_format][7])
            DB().addVideo(self.connection,self.caja_url.get(),self.text_title["text"],self.text_duration["text"],self.text_espacio["text"],self.text_canal["text"],format_id,self.caja_path.get())
        self.getVideos()
        btn['state']="normal"

    def limiparBusqueda(self):
        self.text_url.config(text="")
        self.text_title.config(text="")
        self.text_duration.config(text="")
        self.text_espacio.config(text="")
        self.text_canal.config(text="")

    def getInfoVideos(self,url,id_format,fila):
        dl_opts={
           'format':str(id_format)
        }
        with YoutubeDL(dl_opts) as dl:
            features=dl.extract_info(url,download=False)
            self.tb.identify_row(fila)
            self.tb.item(self.tb.focus(),values=(features['title']))

    # Obtener videos
    def getVideos(self):
        data=DB().getVideos(self.connection)
        for fila in data:
            self.list_videos.append({
                'url':data[fila][1]
            })
            self.tb.insert("",fila,text=data[fila][5],values=(data[fila][2],data[fila][3],data[fila][4],"-","-","-","-",data[fila][1],data[fila][6]))
            #Thread(target=lambda:self.getInfoVideos(data[fila][1],data[fila][6],fila)).start()
        print(self.list_videos)
    
    # Selecionar video
    def seleVideo(self):
        if self.caja_path.get()=='':
            messagebox.showinfo(message="Seleccione un lugar de almacenamiento",title="Advertencia")
            return 0
        try:
            #id_tb=self.tb.item(self.tb.selection())['text']
            video_url=self.tb.item(self.tb.selection())['values'][7]
            video_id=self.tb.item(self.tb.selection())['values'][8]
            Thread(target=lambda:self.download(video_url,video_id)).start()
        except:
            messagebox.showinfo(message="Seleccione un video",title="Advertencia")

    # Descargar video
    def download(self,video_url,video_id):
        if video_id!=-1:
            dl_opts={
                'format':str(video_id),
                'outtmpl':self.caja_path.get()+"/%(title)s.%(ext)s",
                'progress_hooks':[my_hook]
            }
            with YoutubeDL(dl_opts) as dl:
                self.btn_download['state']="disabled"
                dl.download([str(video_url)])

    def formatSize(self,size):
        try:
            return str(round(size/1024/1024,2))+" MB"
        except:
            return " "
    def widgets(self):

        # Url
        Label(self,text="URL: ",font=("arial",12)).grid(row=0,column=0,sticky="w")
        self.caja_url=Entry(self,font=("arial",12))
        self.caja_url.grid(row=0,column=1)
        self.btn_search=Button(self,text="Buscar",font=("arial",10),command=lambda:Thread(target=self.search).start())
        self.btn_search.grid(row=0,column=2,sticky="w",padx=5,pady=5)

        # Destino
        Label(self,text="Destino: ",font=("arial",12)).grid(row=1,column=0,sticky="w")
        self.caja_path=Entry(self,font=("arial",12))
        self.caja_path.grid(row=1,column=1)
        self.btn_path=Button(self,text="Examinar",font=("arial",10),command=lambda:self.examinar())
        self.btn_path.grid(row=1,column=2,sticky="w",padx=5,pady=5)

        # Url
        Label(self,text="URL: ",font=("arial",10)).grid(row=2,column=0,sticky="w",padx=5,pady=5)
        self.text_url=Label(self,text="",font=("arial",10))
        self.text_url.grid(row=2,column=1,columnspan=2,sticky="w")

        # Título
        Label(self,text="Título: ",font=("arial",10)).grid(row=3,column=0,sticky="w",padx=5,pady=5)
        self.text_title=Label(self,text="",font=("arial",10))
        self.text_title.grid(row=3,column=1,columnspan=2,sticky="w")

        # Duración
        Label(self,text="Duración: ",font=("arial",10)).grid(row=4,column=0,sticky="w",padx=5,pady=5)
        self.text_duration=Label(self,text="",font=("arial",10))
        self.text_duration.grid(row=4,column=1,columnspan=2,sticky="w")

        # Espacio
        Label(self,text="Espacio: ",font=("arial",10)).grid(row=5,column=0,sticky="w",padx=5,pady=5)
        self.text_espacio=Label(self,text="",font=("arial",10))
        self.text_espacio.grid(row=5,column=1,columnspan=2,sticky="w")

        # Canal
        Label(self,text="Canal: ",font=("arial",10)).grid(row=6,column=0,sticky="w",padx=5,pady=5)
        self.text_canal=Label(self,text="",font=("arial",10))
        self.text_canal.grid(row=6,column=1,columnspan=2,sticky="w")

        # Opciones de descarga
        self.caja_formats=ttk.Combobox(self,width=60,font=("arial",10),state="readonly")
        self.caja_formats.grid(row=7,column=0,columnspan=2,sticky="w",padx=5,pady=5)
        btn_add_video=Button(self,text="Agregar",font=("arial",10),command=lambda:self.add(btn_add_video))
        btn_add_video.grid(row=7,column=2,sticky="w",padx=5,pady=5)
        btn_add_video_best=Button(self,text="Mejor video",font=("arial",10),command=lambda:self.add(btn_add_video_best))
        btn_add_video_best.grid(row=7,column=3,sticky="w",padx=5,pady=5)
        btn_add_audio_best=Button(self,text="Mejor audio",font=("arial",10),command=lambda:self.add(btn_add_audio_best))
        btn_add_audio_best.grid(row=7,column=4,sticky="w",padx=5,pady=5)
        btn_add_video_audio_best=Button(self,text="Mejor video con audio",font=("arial",10),command=lambda:self.add(btn_add_video_audio_best))
        btn_add_video_audio_best.grid(row=7,column=5,sticky="w",padx=5,pady=5)

        # Descargar propiedades y tabla
        self.tb=ttk.Treeview(self,columns=("#1","#2","#3","#4","#5","#6","#7","#8","#9"))
        self.tb.grid(row=8,column=0,columnspan=6,padx=5,pady=5,sticky="w")
        self.tb.column("#0",width=200)
        self.tb.column("#1",width=200)
        self.tb.column("#2",width=70)
        self.tb.column("#3",width=70)
        self.tb.column("#4",width=150)
        self.tb.column("#5",width=100)
        self.tb.column("#6",width=100)
        self.tb.column("#7",width=100)
        self.tb.column("#8",width=0)
        self.tb.column("#9",width=0)
        self.tb.heading("#0",text="Canal")
        self.tb.heading("#1",text="Título")
        self.tb.heading("#2",text="Duración")
        self.tb.heading("#3",text="Tamaño")
        self.tb.heading("#4",text="Porcentaje")
        self.tb.heading("#5",text="Velocidad")
        self.tb.heading("#6",text="Tiempo")
        self.tb.heading("#7",text="Estado")
        self.tb.heading("#8",text="Url")
        self.tb.heading("#9",text="Format id")
        self.btn_destino=Button(self,text="Carpeta de destino",font=("arial",10),command=lambda:Thread(target=properties_video).start())
        self.btn_destino.grid(row=9,column=0,padx=5,pady=5,sticky="w")
        self.btn_download=Button(self,text="Descargar",font=("arial",10),command=lambda:Thread(target=self.seleVideo).start())
        self.btn_download.grid(row=9,column=5,padx=5,pady=5,sticky="e")

    # Variables
    caja_url=None
    btn_search=None
    caja_path=None
    btn_path=None
    text_url=None
    text_title=None
    text_duration=None
    text_espacio=None
    text_canal=None
    caja_formats=None
    tb=None
    btn_destino=None
    btn_download=None
    list_formats=[]
    list_videos=[]
    connection=DB().main()

def my_hook(rs):
    progress_video=ttk.Progressbar(frame)
    progress_video.grid(row=1,column=1,padx=5,pady=5,sticky="w")
    print("\n-------"+str(rs))
    if rs['status']=='finished':
        progress_video.step(0)
        frame.btn_download['state']="normal"
    if rs['status']=='downloading':
        progress_video.step(float(rs['_percent_str'].replace('%','')))

root=Tk()
root.title("Descarga videos")
root.resizable(False,False)
frame=Gui(master=root)
frame.mainloop()