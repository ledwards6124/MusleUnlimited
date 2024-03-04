from spotifyCaller import *
from time import sleep

class MusleCLI:

    __slots__ = ['__caller', '_currentArtist'] #add game slot later

    def __init__(self):
        try:
            self.__caller = SpotifyCaller()
            print('Welcome to the Musle CLI!!')
        except:
            print('Unable to connect to the Spotify API, please try again...')
            quit()

    def searchArtist(self):
        try:
            artist = input("Enter your favorite artist's name below!\n")
            possibleArtists = self.__caller.searchForArtist(artist)
            return possibleArtists
        except:
            print('Unable to search via the Spotify API, please try again...')
            quit()
    
    def selectArtist(self):
        possibleArtists = self.searchArtist()
        count = 1
        for a in possibleArtists:
            print(f'{count}: {a.getName()}')
            count += 1
        artistChoice = input('\nEnter what number artist you want to choose and I can show you some of their songs just to make sure!\nYour Choice: ')
        tracks = self.__caller.returnPopularTracks(possibleArtists[int(artistChoice) - 1].getID())
        print(f"Showing you {possibleArtists[int(artistChoice) - 1].getName()}'s most popular songs!")
        for t in tracks:
            print(t.getName())
        print('Do these look familiar? (Y|N)')
        choice = input()
        choice = choice.strip().upper()
        if choice == 'Y':
            pass #play game with chosen artist
        elif choice == 'N':
            print('Do you want to choose another artist? (Y|N)')
            if choice == 'Y':
                self.selectArtist()
            else:
                quit()
        else:
            self.searchArtist()

def main():
    cli = MusleCLI()
    cli.selectArtist()

main()


    

    