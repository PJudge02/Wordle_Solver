#runs the main loop through user input
from colorama import Fore, Style
#pickle file!!!!!

def main():
    file = open('All_Wordle_KeyWords.txt','r')
    text = file.read()
    incorrectLetters = ""
    misplacedLetters = [""] * 5
    correctLetters = [""] * 5

    word = ""
    suggestedWord = ""
    print(Fore.GREEN + 
            "\n -Directly follow each letters with one of the follow:" +
            "\n\t -'.' for correct letter" + 
            "\n\t -'?' for correct letter wrong spot" + 
            "\n\t -'!' for incorrect letter" + 
            "\n Type 'complete' to terminate program\n" + Style.RESET_ALL)
    while(True):
        word = input(Fore.GREEN + "What word would you like to guess?\n" + Style.RESET_ALL)
        if(word.lower() == "complete"):
            if(input(Fore.GREEN + "Would you like to go again? (Y/N)" + Style.RESET_ALL).lower() == "y"):
                file = open('All_Wordle_KeyWords.txt','r')
                text = file.read()
                incorrectLetters = ""
                misplacedLetters = [""] * 5
                correctLetters = [""] * 5
                suggestedWord = ""
            else:
                break
        elif(validInput(word)):
            incorrectLetters += proccessWordParameters(word, incorrectLetters, misplacedLetters, correctLetters)
            # printWordInfo(incorrectLetters, misplacedLetters, correctLetters)
            text = SearchForWord(text, incorrectLetters, misplacedLetters, correctLetters)
            print(f"List of all possible words: {Fore.YELLOW + text + Style.RESET_ALL}")
            # printWordInfo(incorrectLetters,misplacedLetters,correctLetters)
            suggestedWord = weightWord(text)
            print(f"Suggested word is {Fore.RED + suggestedWord + Style.RESET_ALL}")
        else:
            word = ""
            print("You're input was invalid")

    

    file.close()
    print("Program End")

### takes in the words and puts the word parameters into the letter storage variables
def proccessWordParameters(word, incorrect_L, misplaced_L, correct_L):
    local_incorrect = "" # 
    # print("\'" + word + "\'")
    for i in range(1,10,2):
        if(word[i] == "."):
            #(int)(i/2) gets the corresponding position from 'word' of 0-4
            correct_L[(int)(i/2)] = word[i-1] 
        elif(word[i] == "!"):
            if(str(incorrect_L).find(word[i-1]) == -1):
                local_incorrect += word[i-1] #strings are primative
        else:
            #gets the string of letters that don't belong and checks to see if the (i-1) letter is one of them
            if(str(misplaced_L[(int)(i/2)]).find(word[i-1])): 
                misplaced_L[(int)(i/2)] = misplaced_L[(int)(i/2)] + word[i-1]
    
    # print("Process Word Perameters Complete")
    return local_incorrect

def SearchForWord(text, incorrect_L, misplaced_L, correct_L):
    #converts the string into an array
    arrText = text.split(',')
    # print(arrText)
    newArr = []
    #process through each word based on the parameters
    for word in arrText: 
        SkipWord = False
        #iterates through incorrect letters to make sure they're not in the word
        for badLetter in incorrect_L:
            if(word.find(badLetter) != -1 
                and not(badLetter in correct_L)
                and not(checkLetters(misplaced_L, badLetter, False))):
                SkipWord = True
                break
        #chckes for check letters then misplaced letters
        for i in range(5):
            if(SkipWord == True):
                break
            if(correct_L[i] != "" and word[i] != correct_L[i]):
                SkipWord = True
                break
            if(misplaced_L[i].find(word[i]) != -1 or not(checkLetters(misplaced_L, word, True))):
                SkipWord = True
                break
        if(SkipWord):
            SkipWord = False
        else:
            newArr.append(word)

    #returns string
    return ",".join(newArr)

#checks to make sure that all letters in misplaced letters show up in the word 
#(also used to check incorrect letters)
def checkLetters(misplaced_L, word, usedForMisplacedLBool):
    strMisplaced_L = "".join(misplaced_L)
    if(strMisplaced_L == "" and usedForMisplacedLBool == False):
        return False
    for letter in strMisplaced_L:
        if(word.find(letter) == -1):
            return False
    return True

#takes in the word tested & checks to see if the word is valid input for processing
def validInput(word):
    valid = True
    if(len(word) == 10):
        # print("There are enough characters")
        for i in range(10):
            if(i % 2 == 0 and str(word[i]).isalpha() == False):
                # print(str(word[i]))
                valid = False
                break
            elif(i % 2 == 1 and (word[i] != "." and word[i] != "?" and word[i] != "!")):
                # print(word[i])
                valid = False
                break
    else:
        valid = False
    return valid

#weight all the words and gets the best word
def weightWord(text):
    #arr of alpha
    alpha = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    #arr of num of letter 
    letterVals = []
    #converts string text into array
    arrText = text.split(',')

    for letterPos in range(26):
        counter = 0
        for word in arrText:
            if(alpha[letterPos] in word):
                counter +=1
        letterVals.append(counter)
        # letterVals.append(text.count(alpha[letterPos]))
    
    #initialize arr for value of words
    wordVals = []

    #sort through each word (double for loop) and weight the words
    for word in arrText:
        wordVal = 0
        for letter in word:
            #this first if statement handles word with multiple letters
            if(word.count(letter) > 1):
                wordVal += 1/(letterVals[alpha.index(letter)])
                if(min(letterVals) != 0):
                    wordVal += (word.count(letter) - 1)/min(letterVals)
                else:
                    wordVal += (word.count(letter) - 1)
            else:
                wordVal += 1/letterVals[alpha.index(letter)]
        wordVals.append(wordVal)

    #lowest value word is ideal
    return arrText[wordVals.index(min(wordVals))]

#Prints out the three parameters
def printWordInfo(incorrect_L, misplaced_L, correct_L):
    print("Misplaced Letters:")
    print(misplaced_L)
    print("Incorrect Letters: ")
    print(incorrect_L)
    print("Correct Letters: ")
    print(correct_L)

main()

