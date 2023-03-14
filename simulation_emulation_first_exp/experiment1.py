import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from vpython import *
import time


#Connection with firebase
cred = credentials.Certificate("educational-robot-8140d-firebase-adminsdk-9spnz-8714c75dff.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://educational-robot-8140d-default-rtdb.europe-west1.firebasedatabase.app/'})
LmotorAngle = db.reference('Robophone/db/Lmotor/leftAngle')
leftAngleVelocity = db.reference('Robophone/db/Lmotor/leftAngleVelocity')
timeDiff = db.reference('Robophone/db/timeDiff')
leftPower=  db.reference('Robophone/db/Lmotor/leftPower')
leftAngleControl=db.reference('Robophone/db/Lmotor/leftAngleControl')


#Global variables
rod=cylinder()
rod.visible = False

pointer=arrow()
pointer.visible = False

road=box()
road.visible = False

left_wheel_angle=0

left_wheel_pos=0
left_motor_power=0

counter1=counter2=1
#wheel radius
r=2.75

#delta t
dt=0

angle=0

road_len=0

scene.autoscale = False
bg=sphere(pos=vector(0,0,0), radius=100, shinness=0)
scene.x= 50
scene.y = 50




#Functions
def create_wheel_rod(pos_rod, angle_rod, axis_rod, rad, length):
    global rod, pointer
    #create cylinder
    #rod = cylinder(pos=pos_rod,texture={'file':'wheel.jpg', 'place':['right', 'left']})
    rod = cylinder(pos=pos_rod, radius=rad, axis=length)
    rod.color = vector(0,0,1)
    rod.rotate(angle=angle_rod, axis=axis_rod) 

    return rod

# Robot:
# create robot's wheels using create_wheel function:

# create first wheel
leftWheel=create_wheel_rod(vector(0,1.75,8),pi/2,vector(0,1,0),2.75, vector(1,0,0))
leftWheel.color=vector(0,0,1)

#create arrow
pointer=arrow(pos=vector(0,1.75,8),length=2.75)
pointer.rotate(angle=pi/2,axis=vector(1,0,0))
#connecting parts
leftWheel=compound([leftWheel,pointer])
leftWheel.axis=vector(1,0,0)

#initial speeds for wheels
leftWheel.p= vector(0,0,0)

def create_road(x,y,z):
    
    road = box(pos=vector(x,y,z), length=200, hight=0, width=10)
    return road


def move_left_wheel(leftvel,leftPos,dt):
    leftWheel.pos = leftWheel.pos + leftPos*vector(1,0,0)
    leftWheel.rotate(angle=-leftvel*dt, axis=vector(0,0,1))


def f():
    return leftWheel.pos

# Enviroment (road, sky, etc)
road1=create_road(0,-1.5,1.6)
road2=create_road(0,-1.5,11.6)
road3=create_road(0,-1.5,21.6)

def powerControl(s):
    leftPower.set(int(xs.value))
    xs_caption.text='motor Power='+'{:1.0f}'.format(int(xs.value))
xs=slider( bind=powerControl ,min=-100, max=100, value=0)
xs_caption=wtext(text='motor Power='+'{:1.0f}'.format(int(xs.value)))

def angleControl(s):
    leftAngleControl.set(int(ys.value))
    ys_caption.text='motor angle='+'{:1.0f}'.format(int(ys.value))
ys=slider( bind=angleControl ,min=0, max=360, value=0)
ys_caption=wtext(text='motor angle='+'{:1.0f}'.format(int(ys.value)))



# Rotate & advance wheels
while(1):
    rate(40)
   
   
    if(counter2%6==1):
        dt=timeDiff.get()

    if(counter1%3==1):
       
        left_wheel_angle_velocity=(leftAngleVelocity.get())*(pi/180)
        left_angle=LmotorAngle.get()*(pi/180)
        left_wheel_pos=left_wheel_angle_velocity*r*dt/2*pi

        print("angleVel:",left_wheel_angle_velocity)
        print("position:",left_wheel_pos)
        print("angle:",angle)
        

    counter1=counter1+1
    counter2=counter2+1

    if (leftWheel.pos.x%20>19):
        road_len=road_len+200
        road1=create_road(road_len,-1.5,1.6)
        road2=create_road(road_len,-1.5,11.6)
        road3=create_road(road_len,-1.5,21.6)
    if(angle<LmotorAngle.get()*(pi/180)):
        move_left_wheel(left_wheel_angle_velocity,left_wheel_pos,dt)
        angle=angle+left_wheel_angle_velocity*dt
    scene.camera.follow(f)
    