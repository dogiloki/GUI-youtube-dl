import sqlite3

class DB:

    #Base de datos
    def main(self):
        connection=sqlite3.connect('database.db',check_same_thread=False)
        rs=connection.cursor()
        rs.execute("CREATE TABLE IF NOT EXISTS config(storage TEXT NOT NULL)")
        rs.execute("CREATE TABLE IF NOT EXISTS videos(id int(10) NOT NULL,"+
                                                "url TEXT NOT NULL,"+
                                                "title TEXT NOT NULL,"+
                                                "duration TEXT NOT NULL,"+
                                                "size TEXT NOT NULL,"+
                                                "channel TEXT NOT NULL,"+
                                                "format_id TEXT NOT NULL,"+
                                                "storage TEXT NOT NULL,"+
                                                "filename TEXT NOT NULL,"+
                                                "data_register VARCHAR(50) NOT NULL)")
        connection.cursor().execute("INSERT INTO config VALUES ('')")
        connection.commit()
        return connection

    def changeStorage(self,connection,path):
        connection.cursor().execute("UPDATE config SET storage='"+str(path)+"'")
        connection.commit()

    def getStorage(self,connection):
        for fila in connection.cursor().execute("SELECT * FROM config"):
            return fila[0]
        return ""

    def addVideo(self,connection,url,title,duration,size,channel,format_id,storage):
        connection.cursor().execute("INSERT INTO videos VALUES ("+str(DB().getId(connection))+",'"+url+"','"+title+"','"+duration+"','"+size+"','"+channel+"','"+format_id+"','"+storage+"','',strftime('%Y/%m/%d %H:%M:%f','now'))")
        connection.commit()

    def deleteVideo(self,connection,id):
        for fila in connection.cursor().execute("SELECT * FROM videos WHERE id='"+str(id)+"'"):
            connection.cursor().execute("DELETE FROM videos WHERE id='"+str(id)+"'")
            connection.commit()
            return True
        return False

    def changeVideo(self,connection,id,filename):
        connection.cursor().execute("UPDATE videos SET filename='"+str(filename)+"' WHERE id='"+str(id)+"'")
        connection.commit()

    def getId(self,connection):
        id=0
        for fila in connection.cursor().execute("SELECT * FROM videos ORDER BY id ASC"):
            id=int(fila[0])+1
        return int(id)

    def getVideos(self,connection):
        filas={}
        conta=0
        for fila in connection.cursor().execute("SELECT * FROM videos ORDER BY id ASC"):
            filas[conta]=fila
            conta=conta+1
        return filas