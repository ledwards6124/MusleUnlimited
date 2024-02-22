import csv

class artist:

    __slots__ = ['__name', '__age', '__genre', '__discography']

    def __init__(self, name, age, genre, discography):
        self.__name = name
        self.__age = age
        self.__genre = genre
        self.__discography = discography

    def getName(self):
        return self.__name
    
    def getAge(self):
        return self.__age
    
    def getGenre(self):
        return self.__genre
    
    def getDiscography(self):
        with open(self.__discography, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row != '###':
                    print(row)