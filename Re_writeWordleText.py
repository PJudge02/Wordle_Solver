#just transfered all the the words from "Wordle_Words.txt" to "All_Wordle_Words"
#but without any quotation marks
def main():
    input = open("Wordle_KeyWords.txt", 'r')
    writeOut = open("All_Wordle_KeyWords.txt",'w')

    entireFile = str(input.read())
    entireFile = entireFile.replace("\"","")
    writeOut.write(entireFile)

    writeOut.close()
    input.close()
    print("Job Complete")
    

main()