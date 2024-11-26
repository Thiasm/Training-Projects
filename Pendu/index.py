from data import healthPoint, words
import random
import csv
import pandas as pd # type: ignore

def replaceLetter(selectedLetter, word, hashWord):
    for index, char in enumerate(word):
        if char == selectedLetter:
            hashWord = hashWord[:index] + char + hashWord[index + 1:]
    
    return hashWord

def selectLetter():
    while True:
        selectedLetter = input("Enter a letter: ")
        if len(selectedLetter) == 1 and selectedLetter.isalpha():
            return selectedLetter
        else:
            print("Enter only one letter please.")

def playAgain(playerName: str):
    print('Press R to retry or Q to quit')
    selectedLetter = selectLetter(playerName)

    if selectedLetter.lower() == 'r':
        gameBoucle()
    if selectedLetter.lower() == 'q':
        return 0
    else:
        selectedLetter = selectLetter()

def getHighscore(playerName: str):
    df = pd.read_csv("score.csv")
    if playerName in df['name'].values:
        score = df.loc[df['name'] == playerName, 'score'].values[0]
        return score
    return 0

def setHighScore(playerName: str, newScore: int):
    df = pd.read_csv("score.csv")
    if playerName in df['name'].values:
        currentScore = df.loc[df['name'] == playerName, 'score'].values[0]
        if currentScore < newScore:
            df.loc[df['name'] == playerName, 'score'] = newScore
        else:
            return 0
    else:
        df = df._append({'name': playerName.lower(), 'score': newScore}, ignore_index=True)
    df.to_csv("score.csv", index=False)
    print("You're new HighScore is " + str(newScore))
    return 0


def gameBoucle(playerName: str):
    life = healthPoint
    word = random.choice(words)
    hashWord = "".join(["#" for _ in word]) # Replace word characters with '#'

    while True:
        print(hashWord)
        selectedLetter = selectLetter()
        if selectedLetter in word:
            hashWord = replaceLetter(selectedLetter, word, hashWord)
            print('Good\n')
            if not '#' in hashWord: # Check win condition
                print('WIN\n')
                break
        else:
            life -= 1
            print('Incorrect, ' + str(life) + ' HP left\n')
            if life <= 0:
                print('LOSE\n')
                break
    setHighScore(playerName, life)
    playAgain(playerName)
    return 0

def getPlayerName():
    print('Enter your name:') 
    playerName = input()
    return playerName

def mainFunction():
    playerName = getPlayerName()
    highScore = getHighscore(playerName)
    
    print("Welcome " + playerName + ", you're Highscore is " + str(highScore))
    gameBoucle(playerName)             
    return 0

if __name__ == "__main__":
    mainFunction()