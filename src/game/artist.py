import csv
import sys
import re

from song import *

sys.path.append('src/api/')

from caller import *


class Artist:

    __slots__ = ['__name', '__id','__genre']

    def __init__(self, name, genre):
        self.__name = name
        self.__genre = genre

    def getName(self):
        return self.__name

    def getGenre(self):
        return self.__genre
    



def main():
    c = Caller()
    print(c.getSong('6G9aDedv5hYaTgNYDuduqk'))

main()
    