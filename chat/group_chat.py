from turtle import width
from vpython import *
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time 

cred = credentials.Certificate("robo-chat-5f556-firebase-adminsdk-32vsc-664615fd98.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://robo-chat-5f556-default-rtdb.europe-west1.firebasedatabase.app/'}
)

groupName = input( 'Which Chat Group would you like to join? ') #rinatch-group
Name = input( 'Okay. What is your name? ') #rinat
def T(s):
    ref.set(Name + ' : ' + s.text)
input = winput(bind=T, width=300)
ref = db.reference('app/chats/' + groupName)
textarea = wtext(text='')


def callback_print_msg(db_event):
    msg = str(db_event.data)
    name = msg.split(' ')[0]
    if(name == Name):
        textarea.text+='\n  <p style="color:green">' + msg + '</p>'
    else:
        textarea.text+='\n' + msg
    input.text = '' 


ref.set('\n' + Name + ' has joined to ' + groupName)
ref.listen(callback_print_msg)

counter = 0
counter_after_10 = 0
data_to_db_counter_ref = db.reference('app/' + 'count')
data_to_db_counter10_ref = db.reference('app/' + 'count_after_10')
flag = 0
t0 = time.perf_counter()
while True:
    rate(1)
    while True:
        counter +=1
        data_to_db_counter_ref.set(counter)
        t1 = time.perf_counter()
        # print("t0 is:{} ".format(t0))
        # print("t1 is:{} ".format(t1))
        if((t1-t0)>10 and flag==0):
            counter_after_10 = counter
            data_to_db_counter10_ref.set(counter_after_10)
            flag=1
            break

