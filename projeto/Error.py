import * from os
from datetime import *

class Error():

    file = ""

    def addError(self, error, colector):
        self.file = "Error"+colector+".txt"
        temp = open(self.arquivo,"a+")
        temp.write(str(datetime.now()+"\n"+str(error)+"\n\n"))
        temp.close()

    def getError(self):
        if os.path.isfile(self.file):
            temp = open(self.arquivo,"a+")
            return temp.read()
        else:
            return "Error not found"