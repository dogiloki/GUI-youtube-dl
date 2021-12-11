from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from threading import Thread
from youtube_dl import YoutubeDL
import os
import sys
from database import *

class Gui(Frame):

    def __init__(self,root=None):
        super().__init__(root);
        self.pack()
        self.widgets()
        self.caja_storage.insert(0,DB().getStorage(self.connection))
        self.getVideos()

    # Cambiar ruta de almacenamiento
    def examinar(self):
        path=filedialog.askdirectory()
        if path!="":
            os.chdir(path)
            self.caja_storage.delete(0,END)
            self.caja_storage.insert(0,path)
            DB().changeStorage(self.connection,self.caja_storage.get())

    # Buscar video
    def search(self):
        self.limiparBusqueda()
        self.btn_search['state']="disabled"
        dl_opts={
            'format':'249',
            'ignoreerrors':True
        }
        with YoutubeDL(dl_opts) as ydl:
            print(ydl)
            features=[]
            try:
                features=ydl.extract_info(self.caja_url.get(),download=False)
            except:
                messagebox.showinfo(message="URL no válida",title="Advertencia")
                self.btn_search['state']="normal"
                return
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
            self.text_channel.config(text=channel)
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
        if self.caja_storage.get()=='':
             messagebox.showinfo(message="Seleccione un lugar de almacenamiento",title="Advertencia")
             return 0
        btn['state']="disabled"
        format_id=""
        if self.caja_formats.current()>=0 and self.caja_storage.get()!="":
            selection_format=self.caja_formats.current()
            format_id=self.list_formats[selection_format][0]
            self.text_size.config(text=self.list_formats[selection_format][7])
            DB().addVideo(self.connection,self.caja_url.get(),self.text_title["text"]+"_"+str(format_id),self.text_duration["text"],self.text_size["text"],self.text_channel["text"],format_id,self.caja_storage.get())
        btn['state']="normal"
        self.getVideos()

    # Eliminar video
    def deleteVideo(self):
        try:
            self.fila_sele=self.tb.selection()[0]
            if self.list_videos[int(self.fila_sele[1:])-1]['stop']==False:
                messagebox.showinfo(message="Detenga / pause el video",title="Error")
                return
            fila=int(self.fila_sele[1:])-1
            if DB().deleteVideo(self.connection,self.list_videos[fila]['id'])==False:
                messagebox.showinfo(message="Error al eliminar video o ya ha sido eliminado",title="Error")
            else:
                messagebox.showinfo(message="Video eleminado\n\nLos cambios se verán al reiniciar el programa",title="Advertencia")
        except:
            messagebox.showinfo(message="Seleccione un video",title="Advertencia")
        self.tb.config(self.fila_sele,"",END,tag=('fuente','BLACK'))

    def limiparBusqueda(self):
        self.text_url.config(text="")
        self.text_title.config(text="")
        self.text_duration.config(text="")
        self.text_size.config(text="")
        self.text_channel.config(text="")
        self.caja_formats['values']=[]
        self.list_formats=[]

    # Obtener videos
    def getVideos(self):
        #self.tb.insert("",)
        data=DB().getVideos(self.connection)
        if(len(self.list_videos)==0):
            for fila in data:
                self.list_videos.append({
                    'id':data[fila][0],
                    'url':data[fila][1],
                    'title':data[fila][2],
                    'duration':data[fila][3],
                    'size':data[fila][4],
                    'channel':data[fila][5],
                    'format_id':data[fila][6],
                    'storage':data[fila][7],
                    'filename':data[fila][8],
                    'stop':True
                })
                print(self.list_videos[fila]['filename'])
                self.tb.insert("",fila,text=data[fila][5],values=(data[fila][2],data[fila][3],data[fila][4],"-","-","-","-"))
        else:
            fila=len(self.list_videos)
            if len(data)>=1:
                self.list_videos.append({
                    'id':data[fila][0],
                    'url':data[fila][1],
                    'title':data[fila][2],
                    'duration':data[fila][3],
                    'size':data[fila][4],
                    'channel':data[fila][5],
                    'format_id':data[fila][6],
                    'storage':data[fila][7],
                    'filename':data[fila][8],
                    'stop':True
                })
                print(self.list_videos[fila]['filename'])
            self.tb.insert("",fila,text=data[fila][5],values=(data[fila][2],data[fila][3],data[fila][4],"-","-","-","-"))
    
    # Selecionar video
    def seleVideo(self):
        try:
            #messagebox.showinfo(message="Seleccione un lugar de almacenamiento",title="Advertencia")
            #video_format_id=self.tb.item(self.tb.selection())['text']
            self.fila_sele=self.tb.selection()[0]
            fila=int(self.fila_sele[1:])-1
            video_url=self.list_videos[fila]['url']
            video_format_id=self.list_videos[fila]['format_id']
            video_storage=self.list_videos[fila]['storage']
            if self.list_videos[int(self.fila_sele[1:])-1]['stop']==True:
                Thread(target=self.download,args=[video_url,video_format_id,video_storage,self.fila_sele],daemon=True).start()
                self.list_videos[int(self.fila_sele[1:])-1]['stop']=False
        except:
            messagebox.showinfo(message="Seleccione un video",title="Advertencia")

    # Descargar video
    def download(self,video_url,video_format_id,video_storage,fila_sele):
        def my_hook(rs):
            fila=int(fila_sele[1:])-1
            if self.list_videos[fila]['stop']==True:
                self.tb.set(fila_sele,"#7",value="Detenido")
                self.list_videos[fila]['stop']=False
                sys.exit()
            if(rs['status']=='downloading'):
                self.btn_download['state']="normal"
                self.tb.set(fila_sele,"#3",value=self.formatSize(rs['downloaded_bytes'])+" / "+self.list_videos[fila]['size'])
                self.tb.set(fila_sele,"#4",value=rs['_percent_str'])
                self.tb.set(fila_sele,"#5",value=rs['_speed_str'])
                self.tb.set(fila_sele,"#6",value=rs['_eta_str'])
                self.tb.set(fila_sele,"#7",value="Descargando")
            if rs['status']=='finished':
                self.tb.set(fila_sele,"#7",value="Finalizado")
                self.list_videos[fila]['stop']=True
            #print("\n-------\n"+str(rs)+"\n---------\n")
        if video_format_id!=-1:
            dl_opts={
                'format':str(video_format_id),
                'outtmpl':str(video_storage)+"/%(title)s_"+str(video_format_id)+".%(ext)s",
                'logger':MyLogger(),
                'progress_hooks':[my_hook],
                'ignoreerrors':True
            }
            self.tb.set(self.fila_sele,"#7",value="Iniciando")
            with YoutubeDL(dl_opts) as ydl:
                #self.btn_download['state']="disabled"
                ydl.download([str(video_url)])

    def stopDownload(self):
        try:
            self.fila_sele=self.tb.selection()[0]
            self.list_videos[int(self.fila_sele[1:])-1]['stop']=True
        except:
            messagebox.showinfo(message="Seleccione un video",title="Advertencia")

    def my_hook_temp(self,rs):
        Thread(target=self.my_hook,args=[rs,self.fila_sele]).start()

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
        self.caja_storage=Entry(self,font=("arial",12))
        self.caja_storage.grid(row=1,column=1)
        self.btn_storage=Button(self,text="Examinar",font=("arial",10),command=lambda:self.examinar())
        self.btn_storage.grid(row=1,column=2,sticky="w",padx=5,pady=5)

        # Url
        Label(self,text="URL: ",font=("arial",10)).grid(row=2,column=0,sticky="w",padx=5,pady=5)
        self.text_url=Label(self,text="",font=("arial",10))
        self.text_url.grid(row=2,column=1,columnspan=4,sticky="w")

        # Título
        Label(self,text="Título: ",font=("arial",10)).grid(row=3,column=0,sticky="w",padx=5,pady=5)
        self.text_title=Label(self,text="",font=("arial",10))
        self.text_title.grid(row=3,column=1,columnspan=4,sticky="w")

        # Duración
        Label(self,text="Duración: ",font=("arial",10)).grid(row=4,column=0,sticky="w",padx=5,pady=5)
        self.text_duration=Label(self,text="",font=("arial",10))
        self.text_duration.grid(row=4,column=1,columnspan=4,sticky="w")

        # Espacio
        Label(self,text="Espacio: ",font=("arial",10)).grid(row=5,column=0,sticky="w",padx=5,pady=5)
        self.text_size=Label(self,text="",font=("arial",10))
        self.text_size.grid(row=5,column=1,columnspan=4,sticky="w")

        # Canal
        Label(self,text="Canal: ",font=("arial",10)).grid(row=6,column=0,sticky="w",padx=5,pady=5)
        self.text_channel=Label(self,text="",font=("arial",10))
        self.text_channel.grid(row=6,column=1,columnspan=4,sticky="w")

        # Opciones de descarga
        self.caja_formats=ttk.Combobox(self,width=60,font=("arial",10),state="readonly")
        self.caja_formats.grid(row=7,column=0,columnspan=2,sticky="w",padx=5,pady=5)
        btn_add_video=Button(self,text="Agregar",font=("arial",10),command=lambda:Thread(self.add(btn_add_video)))
        btn_add_video.grid(row=7,column=2,sticky="w",padx=5,pady=5)
        btn_add_video_best=Button(self,text="Mejor (sólo video)",font=("arial",10),command=lambda:Thread(self.add(btn_add_video_best)))
        btn_add_video_best.grid(row=7,column=3,sticky="w",padx=5,pady=5)
        btn_add_audio_best=Button(self,text="Mejor (sólo audio)",font=("arial",10),command=lambda:Thread(self.add(btn_add_audio_best)))
        btn_add_audio_best.grid(row=7,column=4,sticky="w",padx=5,pady=5)
        btn_add_video_audio_best=Button(self,text="Mejor (video y audio)",font=("arial",10),command=lambda:Thread(self.add(btn_add_video_audio_best)))
        btn_add_video_audio_best.grid(row=7,column=5,sticky="w",padx=5,pady=5)

        # Descargar propiedades y tabla
        self.tb=ttk.Treeview(self,columns=("#1","#2","#3","#4","#5","#6","#7"))
        self.tb.grid(row=8,column=0,columnspan=8,padx=5,pady=5,sticky="w")
        self.tb.column("#0",width=150)
        self.tb.column("#1",width=500)
        self.tb.column("#2",width=70)
        self.tb.column("#3",width=120)
        self.tb.column("#4",width=100)
        self.tb.column("#5",width=100)
        self.tb.column("#6",width=50)
        self.tb.column("#7",width=100)
        self.tb.heading("#0",text="Canal")
        self.tb.heading("#1",text="Título")
        self.tb.heading("#2",text="Duración")
        self.tb.heading("#3",text="Descarga")
        self.tb.heading("#4",text="Porcentaje")
        self.tb.heading("#5",text="Velocidad")
        self.tb.heading("#6",text="Tiempo")
        self.tb.heading("#7",text="Estado")
        self.btn_properties=Button(self,text="Propiedades",font=("arial",10),command=lambda:Thread(target=propertiesVideo).start())
        self.btn_properties.grid(row=9,column=0,padx=5,pady=5,sticky="w")
        self.btn_delete=Button(self,text="Eliminar",font=("arial",10),command=self.deleteVideo)
        self.btn_delete.grid(row=9,column=4,padx=5,pady=5,sticky="e")
        self.btn_download_stop=Button(self,text="Detener / Pausar",font=("arial",10),command=self.stopDownload)
        self.btn_download_stop.grid(row=9,column=5,padx=5,pady=5,sticky="e")
        self.btn_download=Button(self,text="Descargar",font=("arial",10),command=self.seleVideo)
        self.btn_download.grid(row=9,column=6,padx=5,pady=5,sticky="e")

    # Variables
    caja_url=None
    btn_search=None
    caja_storage=None
    btn_storage=None
    text_url=None
    text_title=None
    text_duration=None
    text_size=None
    text_channel=None
    caja_formats=None
    tb=None
    btn_properties=None
    btn_delete=None
    btn_download=None
    btn_download_stop=None
    list_formats=[]
    list_videos=[]
    fila_sele=None
    connection=DB().main()

class MyLogger(object):
    def debug(self,msg):
        pass
    def warning(self,msg):
        pass
    def error(self,msg):
        messagebox.showinfo(message=msg,title="Error")

root=Tk()
root.title("Descarga videos")
root.resizable(False,False)
frame=Gui(root=root)
frame.mainloop()