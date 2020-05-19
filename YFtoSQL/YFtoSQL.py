#Este programa descarga los datos desde YAHOO FINANCIAL a una BD en SQL SERVER
#Además obtiene los datos de las noticias en The Guardian
#
#
#

import pyodbc
import yfinance as yf
from datetime import datetime, timedelta
import pytz
import numpy as np
from io import open
import FileHandling
import DBHandling
import TkFinancialDataList
import TheGuardianData

#STEP 1: Get the list of tickets and create tkFinancialObjectList
ticketList = FileHandling.elementList()
financialObjectList = []


##Debug
#print(ticketList.Elements)

#STEP 2: Open DB
DBControl = DBHandling.DBHandle()

#STEP 3: Create,  if does not exist, the news table data.
DBControl.createNewsTable()

##STEP 4: Barrer elementos
for ticket in ticketList.Elements:
    tkDataList = TkFinancialDataList.FinDataList(ticket)
    #STEP 4.1: Verificar si existe o no existe la tabla
    if tkDataList.Symbol.find('^')!=-1:
        table = DBControl.DBName + ".dbo." + ticket.strip('^')
    else:
        table = DBControl.DBName + ".dbo." + ticket

    consulta = "SELECT Fecha FROM " + table + " ORDER BY Fecha desc"
    Result = DBControl.Consulta(consulta)
    if Result[0] == 0:
        #STEP 4.1.1: Si existe, buscamos la última fecha de carga de datos
        #auxDate = Result[1].type
        tkDataList.startDate = Result[1].strftime("%Y-%m-%d")
        
        ##Debug
        #tkDataList.getFinancialData()
        #DBControl.InsertData(table, tkDataList.DataList)
    else:       
        #STEP 4.1.2: Si no existe la tabla, se crea y se agrega la fila con los datos en la tabla general
        DBControl.createTable(ticket, table)
        tkDataList.startDate = "2010-01-01"
        tkDataList.getTicketInfo()
        DBControl.InsertDataONGeneralTable(tkDataList.DataInfo)

    tkDataList.getFinancialData()
    DBControl.InsertData(table, tkDataList.DataList)
    print("Ticket guardado", ticket)
    del tkDataList



#STEP 5: Cargar datos de noticias  --> Evaluar si no conviene descargar este listado desde el archivo.txt
sectionList = ("business", "world", "sport","environment", "science", "technology")
##sectionList = ("world","business")
for indexSection in range(0,len(sectionList)):
    section = sectionList[indexSection]
    #STEP 5.1: Revisar si existen datos en la sección
    if section == "world":
        consulta = "SELECT Fecha, Seccion FROM FinancialDB.dbo.NewsInfo WHERE Seccion = 'World news' ORDER BY Fecha desc"
    else:
        consulta = "SELECT Fecha, Seccion FROM FinancialDB.dbo.NewsInfo WHERE Seccion = '" +section +"' ORDER BY Fecha desc"

    
    Result = DBControl.Consulta(consulta)
    if Result[0] == 0:
        #STEP 5.1.1: Tenemos datos disponibles, por lo tanto buscamos la última fecha de la sección
        inicialDate = Result[1].strftime("%Y-%m-%d")
    else:
        inicialDate = "2010-01-01"
    try:
        ##Debug
        NewsData = TheGuardianData.TheGuardianNews()
        NewsData.getData(inicialDate, section)
        NewsData.transforData()
        ##print(NewsData.newsData[1])
        if len(NewsData.newsData) == 0:
            print("Section "+ section + " does not exist, please check")
        ##Debug
        #else:
        #    print(NewsData.newsData)
        ##print(NewsData.newsData[1][1])    
    except:
        print("Section "+ section + " does not exist, please check")
    
    try:
        DBControl.InsertDataONNewsTable(NewsData.newsData)
        
        print("Los datos de la sección " + section + " han sido cargados desde " + inicialDate + " hasta la fecha")
    except:
        
        print("Error al cargar los datos en la seccion " + section)
    del NewsData
#STEP 5: Close DB
DBControl.disconnect()