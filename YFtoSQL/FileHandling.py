from io import open

class elementList:
    Elements = []

    def __init__(self):
        #STEP 1: Open file with info
        file_text = open("Elementos.txt")

        #STEP 2: Read data an create a list of elements
        data_readed = file_text.read()
        prelim_list = data_readed.split('\n')
        file_text.close()

        #STEP 3: Format list
        for item in prelim_list:
            if item != "[Elementos]":
                if item != "":
                    self.Elements.append(item)
        

    
