#
#                Quiz
#

from random import randint

FILE_NAME_Q = "questions.txt"
FILE_NAME_A = "answers.txt"
SEPARATOR = "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
CORRECT_ANSWER_CHAR = "~"

STAGE_OPTIONS = [
        ["Edit answers/questions", "Edit participant list", "Start the game", "Leave the program"], 
        ["View questions", "View answers", "Add question & answer", "Delete question & answer", "Go back"],
        ["View participants", "Add a participant", "Remove a participant", "Go back"], ["Ask questions", "Show score", "Change participant\'s score", "End the game"]]

stage=0
participants = []
questions = []
answers = []
scores = []

def display(options, question=None):
    print("╭=====================================================╮")
    print("|                                                     |")
    if question != None:
        print(f"|             {question}")
    if len(options) == 0:
        print("|             Current list is empty.")
    else:
        for count, option in enumerate(options):
            print(f"|             {count+1} - {str(option).replace(CORRECT_ANSWER_CHAR, '').replace('[', '').replace(']', '')}")
    print("|                                                     |")
    print("╰=====================================================╯\n")

def choose(options):
    answer = input()
    print(SEPARATOR)
    try:
        if int(answer) > 0 and int(answer) <= len(options):
            return int(answer)
        else:
            error(answer)
    except:
        error(answer)

def edit(array, num=0):
    print("╭=====================================================╮")
    print("|                                                     |")
    reply = input("|             ~: ")
    if num != 0:
        array[num] = reply
    else:
        array.append(reply)
    print("|                                                     |")
    print("╰=====================================================╯\n")
    print(SEPARATOR)

def addQuestion():
    print("╭=====================================================╮")
    print("|                                                     |")
    print("|             Enter your question:")
    reply = input("|             ~: ")
    questions.append(reply)
    print("|                                                     |")
    print("╰=====================================================╯\n")
    print(SEPARATOR)

def addAnswers():
    print("╭=====================================================╮")
    print("|                                                     |")
    print("|             Enter the possible answers:")
    x = []
    for i in range(1,4):
        reply = input(f"|             {i}: ")
        x.append(reply)
    answers.append(x)
    print("|                                                     |")
    print("╰=====================================================╯\n")
    display(x, "Enter a number of the right answer:")
    reply = choose(x)
    if reply != None:
        x[reply-1] += CORRECT_ANSWER_CHAR
        print(x)

def remove(array):
    display(array, "Enter number of a participant to delete:")
    reply = choose(array)

    if reply != None: 
        print(str(array[reply-1]) + " has been successfully removed from the participants list.") 
        del array[reply-1]



def error(answer):
    print("╭=====================================================╮")
    print("|                                                     |")
    print("|  !!! Error: " + answer + " is not an option. !!!")
    print("|                                                     |")
    print("╰=====================================================╯")

def getQuestions():
    r = []
    with open(FILE_NAME_Q, "r") as file:
        for el in file.readlines(): 
            r.append(el.replace("\n", ""))
        file.close()
    return r

def getAnswers():
    r = []
    with open(FILE_NAME_A, "r") as file:
        for el in file.readlines(): 
            r.append(el.replace("\n", "").split(';'))
        file.close()
    return r



if __name__ == "__main__":

    # Get questions and answers from the files
    questions = getQuestions()
    answers = getAnswers()

    # Main loop
    while True:

        # List starting options
        display(STAGE_OPTIONS[stage])
        answer = choose(STAGE_OPTIONS[stage])

        # Checks whether the answer was appropriate
        if answer != None:

            # Leaves the program or moves back to the starting menu
            if answer == len(STAGE_OPTIONS[stage]):
                if stage == 0:
                    print("Leaving the program")
                    break
                else:
                    stage = 0

            # Startup
            elif stage == 0:
                stage = int(answer)

            # Q/A
            elif stage == 1:

                # Display questions
                if answer == 1:
                    display(questions)

                # Display answers
                elif answer == 2:
                    display(answers)

                # Add q&a
                elif answer == 3:
                    addQuestion()
                    addAnswers()

                # Delete q&a
                elif answer == 4:
                    remove(questions)
                    remove(answers)

            # Participants
            elif stage == 2:

                # Show all the participants
                if answer == 1:
                    display(participants)

                # Add a participant
                elif answer == 2:
                    edit(participants)

                # Delete a participant
                elif answer == 3:
                    remove(participants)

                # Move back to the initial stage
                elif answer == 4:
                    stage = 0

            # Game
            elif stage == 3:
                if len(participants) == 0:
                    print(SEPARATOR)
                    print("No participants in this game. Add the participants first to play the quiz.")
                    print(SEPARATOR)
                    stage = 2
                elif len(questions) < 3*len(participants):
                    print("Not enough questions for all the participants. Add more questions and answers first.")
                    stage = 1
                for i in range(len(participants)):
                    scores.append(0)

                #Ask questions
                if answer == 1:
                    display([participants[i] + " = " + scores[i] for i in range(len(scores))], "Enter the number of a participant, whom you're going to ask questions:")
                    answer = choose(participants)

                    if answer != None:
                        for i in range(3):
                            r_var = randint(0, len(questions)-1)
                            display(answers[r_var], questions[r_var])
                            reply = choose(answers[r_var])

                            if reply != None:
                                if CORRECT_ANSWER_CHAR in answers[r_var][reply-1]:
                                    scores[answer-1] += 1
                                    print("Correct!")
                                else:
                                    print("Wrong. The correct answer is " + str([(i) for i in answers[r_var] if CORRECT_ANSWER_CHAR in i]).replace(CORRECT_ANSWER_CHAR, '').replace('[', '').replace(']', ''))
                                del questions[r_var]
                                del answers[r_var]
                        print(SEPARATOR)
                        print(participants[answer-1] + " now has " + str(scores[answer-1]) + " points.")
                        print(SEPARATOR)

                # Show score
                elif answer == 2:
                    display([participants[i] + " = " + scores[i] for i in range(len(scores))])

                # Edit participants score
                elif answer == 3:
                    display([participants[i] + " = " + scores[i] for i in range(len(scores))], "Enter the number of a participant, whose score you want to change:")
                    answer = choose(participants)

                    if answer != None:
                        edit(scores, answer-1)
