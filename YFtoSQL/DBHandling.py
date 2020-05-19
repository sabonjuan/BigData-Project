import pyodbc
import yfinance as yf
from datetime import datetime, timedelta
import pytz
import numpy as np

class DBHandle:
    DBName = "FinancialDB"
    
    conn = []
    
    #Constructor que se conecta a la BD
    def __init__(self):
        ##Conectarse a BD
        try:
            self.conn = pyodbc.connect('Driver={SQL Server};'
                                       'Server=JMA-LAPTOP\MSSQLSERVER01;'
                                       'Database='+ self.DBName + ';'
                                       'Trusted_Connection=yes;')
            
        except:
            print("Error en la conexión")
        self.CreateGeneralInfoTable()

    #Crear una tabla con la información de los instrumentos
    def CreateGeneralInfoTable(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                            IF OBJECT_ID('TicketInfo') IS NOT NULL
                            BEGIN
                                SELECT * FROM FinancialDB.dbo.TicketInfo
                            END
                            ELSE
                            BEGIN
    
                                CREATE TABLE FinancialDB.dbo.TicketInfo (
                                    Id int IDENTITY(1,1) PRIMARY KEY,
                                    Simbolo  varchar(30) NOT NULL,
                                    Descripcion  varchar(100),
                                    Tipo varchar(100),
                                    Sector  varchar(100),
                                    InicioSeguim  smalldatetime
                                )
                            END
                        """)
        except:
            print("Error al crear la tabla General")
    
    #Realiza consultas simples, básicamente se usa para comprobar que exista la tabla
    def Consulta(self, query):
        cursor = self.conn.cursor()
        try: 
            cursor.execute(query)
            return 0, cursor.fetchone()[0]
        except:
            return 1, "01-01-1900"
    
    #Insertamos datos en las tablas de elementos
    def InsertData(self, tableName, dataList):
        cursor = self.conn.cursor()
        
        #Guardamos elemento por elemento
        for i in range(0, len(dataList)):
            cursor.execute("SELECT * FROM " + tableName +" WHERE Fecha = ? ", dataList[i][0])
            if cursor.rowcount != -1:
                cursor.execute("INSERT INTO " + tableName +""" (Fecha, Apertura, MaxVal, Cierre, AdjClose, Volume)
                        VALUES( ?, ?, ?, ?, ?, ?)""", dataList[i][0], dataList[i][1],dataList[i][2], dataList[i][4],dataList[i][4],dataList[i][5] )
        

        cursor.commit()
    

    #Insertamos datos en las tablas de información general
    def InsertDataONGeneralTable(self, dataList):
        cursor = self.conn.cursor()
        
        #Guardamos elemento por elemento
        cursor.execute("SELECT * FROM FinancialDB.dbo.TicketInfo WHERE Simbolo = ? ", dataList[0])
        if cursor.rowcount != -1:
            cursor.execute("""INSERT INTO FinancialDB.dbo.TicketInfo (Simbolo, Descripcion, Tipo, Sector, InicioSeguim )
                        VALUES( ?, ?, ?, ?, ?)""", dataList[0], dataList[1],dataList[2], dataList[3],dataList[4] )
        
            cursor.commit()



    #Creamos nueva tabla
    def createTable(self, ticket, tableName):
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
                            IF OBJECT_ID(""" + "'" + ticket + "'"+   """) IS NOT NULL
                            BEGIN
                                SELECT * FROM """ + tableName + """
                            END
                            ELSE
                            BEGIN
    
                                CREATE TABLE """ + tableName + """ (
                                    Id int IDENTITY(1,1) PRIMARY KEY,
                                    Fecha  smalldatetime,
                                    Apertura  float,
                                    MaxVal  float,
                                    Cierre  float,
                                    AdjClose  float,
                                    Volume  decimal
                                )
                            END
                        """)
            cursor.commit()
        except:
            print("No se mpudo crear la tabla ", tableName)

    ##Create News Table
    def createNewsTable(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                            IF OBJECT_ID('NewsInfo') IS NOT NULL
                            BEGIN
                                SELECT * FROM FinancialDB.dbo.NewsInfo
                            END
                            ELSE
                            BEGIN
                                CREATE TABLE FinancialDB.dbo.NewsInfo (
                                Id int IDENTITY(1,1) PRIMARY KEY,
                                Fecha  smalldatetime NOT NULL,
                                Seccion  varchar(100),
                                Encabezado varchar(500),
                                Web  varchar(500)
                                )
                            END
                        """)
            cursor.commit()
        except:
            print("Error al crear la tabla de noticias")


    #Insertamos datos en las tablas de información general
    def InsertDataONNewsTable(self, dataList):
        cursor = self.conn.cursor()
        
        #Guardamos elemento por elemento
        
        for i in range(0, len(dataList)):
            for j in range(0, len(dataList[i])):
                cursor.execute("SELECT * FROM FinancialDB.dbo.NewsInfo WHERE Encabezado = ? ", dataList[i][j][2])
                if cursor.rowcount != -1:
                    cursor.execute("""INSERT INTO FinancialDB.dbo.NewsInfo (Fecha, Seccion, Encabezado, Web)
                                          VALUES( ?, ?, ?, ?)""", dataList[i][j][0], dataList[i][j][1],dataList[i][j][2], dataList[i][j][3] )
        
                    cursor.commit()


    ##Desconectarse a BD
    def disconnect(self):
        cursor = self.conn.cursor()
        cursor.close()