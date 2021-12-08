import sqlite3

class DB:

    #Base de datos
    def main(self):
        connection=sqlite3.connect('database.db')
        rs=connection.cursor()
        rs.execute("CREATE TABLE IF NOT EXISTS config(ruta_destino TEXT NOT NULL)")
        rs.execute("CREATE TABLE IF NOT EXISTS videos(id int(10) NOT NULL,"+
                                                "url TEXT NOT NULL,"+
                                                "title TEXT NOT NULL,"+
                                                "duration TEXT NOT NULL,"+
                                                "espacio TEXT NOT NULL,"+
                                                "canal TEXT NOT NULL,"+
                                                "format_id TEXT NOT NULL,"+
                                                "destino TEXT NOT NULL)")
        connection.commit()
        return connection

    def addVideo(self,connection,url,title,duration,espacio,canal,format_id,destino):
        sql="INSERT INTO videos VALUES ("+str(DB().getId(connection))+",'"+url+"','"+title+"','"+duration+"','"+espacio+"','"+canal+"','"+format_id+"','"+destino+"')"
        connection.cursor().execute(sql)
        connection.commit()

    def getId(self,connection):
        id=0
        for fila in connection.cursor().execute("SELECT * FROM videos ORDER BY id ASC"):
            id=int(fila[0])+1
        return int(id)

    def getVideos(self,connection):
        filas={}
        conta=0
        for fila in connection.cursor().execute("SELECT * FROM videos ORDER BY id DESC"):
            filas[conta]=fila
            conta=conta+1
        return filas