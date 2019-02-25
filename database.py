import sqlite3
import string

def insert():
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    array = ["zero"]

    with open("bank.txt", "r") as ins:
        
        for line in ins:
            array.append(line.strip())
    
    length = len(array)
    inc = 1

    while (inc < length):
        cursor.execute("INSERT INTO ques_and_ans VALUES (NULL, '" + array[inc] + "', '" + array[inc + 1] + "')")
        inc = inc + 3

    conn.commit()
    conn.close()


def select_questions():
    questionList = []
    
    translator = str.maketrans('', '', string.punctuation)
    
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    
    cursor.execute("SELECT question FROM ques_and_ans")
    questions = cursor.fetchall()
    for q in questions:  
        curr_q = q[0].translate(translator).lower()
        questionList.append(curr_q)
    conn.close()
    return questionList



def select_answers():
    answerList = []
    
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()

    cursor.execute("SELECT answer FROM ques_and_ans")
    answers = cursor.fetchall()
    for a in answers:  
        answerList.append(a[0])
    conn.close()
    return answerList
