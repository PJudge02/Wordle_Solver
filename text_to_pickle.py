import pickle

def main():
    pickle_file = open("Words.pkl",'wb')
    words = open("All_Wordle_KeyWords.txt",'r')
    text = words.read()
    pickle.dump(pickle_file,text)
    pickle.dump()

    words.close()
    pickle_file.close()
    print("Task Complete")

main()