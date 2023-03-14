

from msilib.schema import RadioButton
from xml.etree.ElementTree import PI
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from vpython import *
from math import cos, exp, pi



#Connection with firebase
cred = credentials.Certificate("educational-robot-8140d-firebase-adminsdk-9spnz-8714c75dff.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://educational-robot-8140d-default-rtdb.europe-west1.firebasedatabase.app/'}
)
Lmotor = db.reference('Robophone/db/Lmotor/leftAngle')
Rmotor = db.reference('Robophone/db/Rmotor/rightAngle')
leftAngleVelocity = db.reference('Robophone/db/Lmotor/leftAngleVelocity')
rightAngleVelocity = db.reference('Robophone/db/Rmotor/rightAngleVelocity')
timeDiff = db.reference('Robophone/db/timeDiff')


#Global variables
rod=cylinder()
rod.visible = False
new_road_pos=0
pointer=arrow()
pointer.visible = False
#counters
counter1=counter2=counter3=1
left_wheel_angle=0
right_wheel_angle=0

road=box()
road.visible = False
#delta t
dt=0
#piviting angle of wheels
teta=0




scene.autoscale = False

bg=sphere(pos=vector(0,0,0), radius=750, shinness=0, color=vector(0,1,1))
scene.x= 50
scene.y = 50




#Functions
def create_wheel_rod(pos_rod, angle_rod, axis_rod, rad, length,color1):
    global rod, pointer
    #create cylinder
   
    rod = cylinder(pos=pos_rod, radius=rad, axis=length,color=color1)
    
    rod.rotate(angle=angle_rod, axis=axis_rod) 

    return rod

# Robot:
# create robot's wheels using create_wheel function:

# create right wheels
frontRightWheel=create_wheel_rod(vector(0,1.75,17),pi/2,vector(0,1,0),2.75, vector(1.5,0,0),vector(1,0,0))
rearRightWheel=create_wheel_rod(vector(-12,1.75,17),pi/2,vector(0,1,0),2.75, vector(1.5,0,0),vector(1,0,0))



# create left wheels 
frontLeftWheel=create_wheel_rod(vector(0,1.75,3),pi/2,vector(0,2,0),2.75, vector(-1.5,0,0),vector(0,1,0))
rearLeftWheel=create_wheel_rod(vector(-12,1.75,3),pi/2,vector(0,2,0),2.75, vector(-1.5,0,0),vector(0,1,0))


#create car structural parts
frontConnector=create_wheel_rod(vector(0,1.75,17),pi/2,vector(0,2,0),0.3, vector(14,0,0),vector(1,1,0))
rearConnector=create_wheel_rod(vector(-12,1.75,17),pi/2,vector(0,2,0),0.3, vector(14,0,0),vector(1,1,0))
carfloor=box(pos=vector(-6,1.75,10),length=20,hight=1.5,width=10, color=vector(0,0,1))
carBody=compound([frontConnector,rearConnector,carfloor])


#create enviromental objects
#pyramids:
geza1=pyramid(pos=vector(400,1.5,-400), size=vector(120,90,90),color=vector(0.5,0.5,0))
geza2=pyramid(pos=vector(300,1.5,-400), size=vector(90,60,60),color=vector(0.5,0.5,0))
geza3=pyramid(pos=vector(420,1.5,-300), size=vector(60,50,50),color=vector(0.5,0.5,0))
geza1.rotate(angle=pi/2,axis=vector(0,0,1))
geza2.rotate(angle=pi/2,axis=vector(0,0,1))
geza3.rotate(angle=pi/2,axis=vector(0,0,1))
pyramids=compound([geza1,geza2,geza3])
#sun:
sun = local_light(pos=vector(400,400,-400),
                      color=color.white)

#initial speeds for wheels
carBody.p = vector(0,0,0)


# Enviroment function (road, sky, stc)
def create_road(position):
    
    street = box(pos=position, length=2000, hight=0, width=80,color=vector(0.5,0.5,0.5))
    desertLeft= box(pos=position+vector(0,0,540),length=2000,hight=0,width=1000,color=vector(1,1,0))
    desertRight= box(pos=position-vector(0,0,540),length=2000,hight=0,width=1000,color=vector(1,1,0))

    
   

#label function

Rlabl=label(pos=vector(-30,10,-10),text="Radius:")
LVlabl=label(pos=vector(-30,20,-10),text="Left Wheel V:")
RVlabl=label(pos=vector(-30,30,-10),text="Right Wheel V:")

    


    



# Enviroment (road, sky, stc)
create_road(vector(0,-1.5,0))


def move_right_wheel(rightVelocity,teta,w):
    #radius from carbody's center to wheels
    r=sqrt(85)
    #initial angle
    fe=asin(6/r)
    
    frontRightWheel.pos = carBody.pos + r*vector(sin(fe+teta),0,cos(fe+teta))
    rearRightWheel.pos = carBody.pos + r*vector(-sin(fe-teta),0,cos(fe-teta))
    frontRightWheel.rotate(angle=rightVelocity*dt,axis=vector(sin(teta),0,cos(teta)))
    rearRightWheel.rotate(angle=rightVelocity*dt,axis=vector(sin(teta),0,cos(teta)))
    frontRightWheel.rotate(angle=w*dt,axis=vector(0,1,0))
    rearRightWheel.rotate(angle=w*dt,axis=vector(0,1,0))
 


def move_left_wheel(leftVelocity,teta,w):
    #radius from carbody's center to wheels
    r=sqrt(85)
    #initial angle
    fe=asin(6/r)
     
    frontLeftWheel.pos = carBody.pos + r*vector(sin(fe-teta),0,-cos(fe-teta)) 
    rearLeftWheel.pos = carBody.pos + r*vector(-sin(fe+teta),0,-cos(fe+teta))
    frontLeftWheel.rotate(angle=leftVelocity*dt,axis=vector(sin(teta),0,cos(teta)))
    rearLeftWheel.rotate(angle=leftVelocity*dt,axis=vector(sin(teta),0,cos(teta)))
    frontLeftWheel.rotate(angle=w*dt,axis=vector(0,1,0))
    rearLeftWheel.rotate(angle=w*dt,axis=vector(0,1,0))


def f():
    return carBody.pos
   

def move_carBody(leftVelocity,rightVelocity,teta,w):
   #wheels radius
    r=2.75
    #gap between wheels
    b=14
    #wheel width
    h=1
    #right wheel velocity
    Vr=(rightVelocity*r)/(2*pi)
    
   
    #left wheel velocity
    Vl=(leftVelocity*r)/(2*pi)
    #angular velocity of circular movment
    #w=(Vr-Vl)/b
 
    if(Vr==Vl):
        carBody.p=Vl*vector(cos(teta),0,-sin(teta))  
        carBody.pos = carBody.pos + (carBody.p)*(dt)
        carBody.rotate(angle=w*dt,axis=vector(0,1,0))

    
    
    if(Vr!=Vl):
        #distance from circle center to car center  
        R=((b/2)*(Vr+Vl)/(Vr-Vl))
        #velocity
        V=((Vr+Vl)/2)
        
        Rlabl.text = "Radius:" + str(abs(float(R)))
        Rlabl.pos=Rlabl.pos+(carBody.p)*(dt)
        LVlabl.text="Left Wheel V:" + str(float(2*Vl))
        LVlabl.pos=LVlabl.pos+(carBody.p)*(dt)
        RVlabl.text="Right Wheel V:" + str(float(2*Vr))
        RVlabl.pos=RVlabl.pos+(carBody.p)*(dt)


        
    
       
    
        carBody.p=V*vector(cos(teta),0,-sin(teta))  
        carBody.pos = carBody.pos + (carBody.p)*(dt)
        carBody.rotate(angle=w*dt,axis=vector(0,1,0))


    


# Rotate & advance wheels
while(1):

    rate(50)
    

    if(counter3%20==1):
        dt=timeDiff.get()

    if(counter2%15==1):
        right_angle_velocity = rightAngleVelocity.get()*(pi/180)*0.5
        
     
    if(counter2%15==1):
        
        left_angle_velocity = leftAngleVelocity.get()*(pi/180)*0.5
        
       
        

    
   
    counter1=counter1+2
    counter2=counter2+1
    counter3=counter3+1
    
   
    
    
    #duplicating enviroment as the car moves
    if (99>carBody.pos.x%100>95):
        new_road_pos=new_road_pos+1000
        create_road(vector(new_road_pos,-1.5,0))
        

    
    #angular velocity of car
    w=2.75*(right_angle_velocity-left_angle_velocity)/(14*2*pi)
    #pivit angle of car
    teta=teta+w*dt
    move_carBody(left_angle_velocity,right_angle_velocity,teta,w)
    move_right_wheel(right_angle_velocity,teta,w)
    move_left_wheel(left_angle_velocity,teta,w)
    bg.pos=carBody.pos
    scene.camera.follow(f)
    
    
    
    
    