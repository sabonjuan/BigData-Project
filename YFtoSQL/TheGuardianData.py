#Esta librería se encarga de obtener los datos de TheGuardian
#
#
#

from theguardian import theguardian_content


class TheGuardianNews:

    def __init__(self):
        self.content = []
        self.headers = []
        self.result = []
        self.newsData = []
        self.mainHeader = []

    def getData(self, fromDate, section):

        # create content
        self.content = theguardian_content.Content(api='test')


        # create content with filters
        # for more filters refer
        # http://open-platform.theguardian.com/documentation/search

        self.mainHeader = {
            "section": section,
            "from-date": fromDate,
            "order-by": "oldest",
            "page-size": 200,
            "show-fields": "sectionName,webTitle,webUrl,short-url",
        }
        headers = self.mainHeader
        self.content = theguardian_content.Content(api='test', **headers)

        #res = self.content.get_content_response()
        #self.result = self.content.get_results(res)

    def transforData(self):
        #STEP 1: Obtener el número de páginas
        auxContent = self.content.response_headers()
        totalPages = auxContent['pages']
        headers = self.mainHeader        
        anotherContent = theguardian_content.Content(api='test', **headers)

        #STEP 2: Barrer página por página
        for page in range(1, totalPages + 1):
            res = anotherContent.get_content_response(headers={'pages': page})
            self.result = anotherContent.get_results(res)
            pageData = []
            for i in range (0, len(self.result)):
                element = []
                refDate = self.result[i]['webPublicationDate']
                newString = ""  
                for x in refDate:
                    if x != 'T':
                        newString = newString + x
                    else:
                        break
            
                sectionName = self.result[i]['sectionName']
                webTitle = self.result[i]['webTitle']
                webUrl = self.result[i]['webUrl']
                element.insert(0, refDate)
                element.insert(1, sectionName)
                element.insert(2, webTitle)
                element.insert(3, webUrl)
                pageData.append(element)
            self.newsData.append(pageData)
            ###print(page)



    def __del__(self):
        self.content = []
        self.headers = []
        self.result = []
        self.newsData = []
