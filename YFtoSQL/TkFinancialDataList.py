#
#
#
#
#

import pyodbc
import yfinance as yf
from datetime import datetime, timedelta
import pytz
import numpy as np
import time

class FinDataList:
    #Symbol = ""
    #DataList = []
    #DataInfo = []
    #startDate = ""


    def __init__(self, ticket):
        self.Symbol = ticket
        self.DataList = []
        self.DataInfo = []
        self.startDate = ""
        

    def getFinancialData(self):
        #Get financial information of one ticket
        tkData = yf.Ticker(self.Symbol)
        endDate = time.strftime('%Y-%m-%d')
        finData = tkData.history(period='1d', start=self.startDate, end=endDate )

        #Conver date formats
        dateAux = finData.index.values
        dateNewTipe = np.array(dateAux).astype('M8[D]')
        dateString = np.datetime_as_string(dateNewTipe)

        for i in range(0, len(finData.values)):
            element = ['%.02f' %member for member in finData.values[i]]
            element.insert(0, dateString[i])
            self.DataList.append(element)


    #Obtiene la información del Ticket 
    def getTicketInfo(self):
        self.DataInfo.append(self.Symbol)
        tkData = yf.Ticker(self.Symbol)
        info = tkData.info
       
        self.DataInfo.append(info['shortName'])
        sector = ""
        type = ""
        try:
            sector = info['sector']
            type = "Acciones"
        except:
            sector = ""
            if self.Symbol.find('^') == -1:
                if self.Symbol.find('.') == -1:
                    if self.Symbol.find('=X') == -1:
                        if self.Symbol.find('=F') == -1:
                            type = "Indefinido"
                        else:
                            type = "Materia Prima"
                    else:
                        type = "Cruce de monedas"
                else:
                    type = "Indice"
            else:
                type = "Indice"
        StartFollow = time.strftime('%Y-%m-%d')
        self.DataInfo.append(type)
        self.DataInfo.append(sector)
        self.DataInfo.append(StartFollow)
        ##Debug
        #print("Ticket INFO: ", self.Symbol)
        #print(self.DataList):

    def __del__(self):
        self.Symbol = ""
        self.DataList = []
        self.DataInfo = []
        self.startDate = ""