from flask import Flask, render_template, request, redirect, url_for
import os
import time
import serial
from QboCmd import Controller

# Robot Setup
port = '/dev/serial0'
ser = serial.Serial(port, 115200)
QBO = Controller(ser)

app = Flask(__name__)

questions = [
    {
        "question": "What is the opposite of 'big'?",
        "choices": ["timing", "small", "long", "short"],
        "answer": "small"
    },
    {
        "question": "Which word describes a fast animal?",
        "choices": ["slow", "quick", "lazy", "sleepy"],
        "answer": "quick"
    },
    {
        "question": "What do you wear on your feet?",
        "choices": ["hat", "shirt", "shoes", "gloves"],
        "answer": "shoes"
    },
    {
        "question": "Which word means the same as 'happy'?",
        "choices": ["sad", "joyful", "angry", "bored"],
        "answer": "joyful"
    },
    {
        "question": "Which is a fruit?",
        "choices": ["carrot", "lettuce", "apple", "broccoli"],
        "answer": "apple"
    }
]

@app.route('/', methods=['GET', 'POST'])
def quiz():
    if request.method == "POST":
        answer = request.form['choice']
        question_num = int(request.form['question_num'])
        if questions[question_num]["answer"] == answer:
            # Correct Answer Action
            QBO.SetMouth(0x110E00)
            time.sleep(1)            
            QBO.SetServo(2, 380, 300)
            time.sleep(0.5)
            QBO.SetServo(2, 530, 300)  # Axis, Angle, Speed
            time.sleep(0.5)
            QBO.SetServo(1, 500, 300)
            time.sleep(0.5)
            QBO.SetMouth(0)            
            os.system("mpg123 -a hw:1,0 GoodJob.mp3")            
        else:
            # Wrong Answer Action
            QBO.SetNoseColor(1)
            time.sleep(1)
            QBO.SetServo(1, 210, 300)
            time.sleep(0.5)
            QBO.SetServo(1, 500, 300)
            time.sleep(0.5)
            QBO.SetServo(1, 725, 300)  # Axis, Angle, Speed
            time.sleep(0.5)
            QBO.SetServo(1, 500, 300)
            time.sleep(1)
            QBO.SetNoseColor(0)
            os.system("mpg123 -a hw:1,0 WrongAnswer.mp3")

        # Reset Action
        QBO.SetNoseColor(0)
        QBO.SetMouth(0)
        QBO.SetServo(1, 500, 100)
        time.sleep(1)
        
        if question_num == len(questions) - 1:
            return render_template('thankyou.html')
        
        question_num += 1
        return render_template('quiz.html', question=questions[question_num], question_num=question_num)
    else:
        return render_template('quiz.html', question=questions[0], question_num=0)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
