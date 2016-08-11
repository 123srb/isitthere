from PIL import Image as PILImage
import VideoCapture as VC
import time
import smtplib
import os.path
import math

# Here are the email package modules we'll need
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#Logic for the main Process
def process():
    #Checks if the config file is there, so if it checked the default color
    if os.path.exists('config.txt'):

        img = capture_picture() # grab a pic

        new_color = average_pixels(img) #find average pixels in new pic
        saved_color = load_color() #load saved color from config file


        print(new_color)
        print(saved_color)
        distance = compare_colors(saved_color,new_color)
        if(distance > 20): #check how big the euclidean distance between two rgb colors
            SendMail(distance) # sends mail to whoever
            print('this shit worked')
        else:
           print('looks the same')
    else:
        #if the config file doesn't exist, then take a picture and create one
        config_default_color()
        print('this shit configged')

def save_color(color, filename='config.txt'):
     with open(filename, 'w') as f:
        for item in color:
            f.write(str(item) + '\n')

def load_color(filename='config.txt'):
    with open(filename, 'r') as f:
        my_list = [line.rstrip('\n') for line in f]
    for item in my_list:
        item = int(item)

    return my_list

def capture_picture():
    cam = VC.Device(0)  # initialize the webcam
    img = cam.getImage()  # in my testing the first getImage stays black.
    time.sleep(2)  # give sometime for the device to come up
    img = cam.getImage()  # capture the current image
    del cam  # no longer need the cam. uninitialize

########################IMAGE LOCATION##################################
    img.save("C:/directory/mail.jpg","jpeg")
###############################################################################
    return img

def config_default_color():
    img = capture_picture()
    avg_px = average_pixels(img)
    save_color(avg_px)


def SendMail(distance):
    #writes email
    COMMASPACE = ', '

    msg = MIMEMultipart()

#############################STUFF TO EDIT############################################
    me = 'email address to send from'
    password = "passwordhere"
    emails = ['email1@gmail.com', 'email2.com']

    msg['Subject'] = 'Thing has changed'
    msg['From'] = me
    msg['To'] = COMMASPACE.join(emails)
    text = 'Image difference =' + str(distance)
#######################################################################################

    #attaches image
    with open('mail.jpg', 'rb') as fp:
        img = MIMEImage(fp.read())

    message = MIMEText(text, 'plain')
    msg.attach(img)
    msg.attach(message)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(me, password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()


def average_pixels(img):
    size = 1, 1
    img.thumbnail(size, PILImage.ANTIALIAS) # makes a really small thumbnail, 1x1 pixel to find the ave. image
    px = img.load()
    #print(list(px[0, 0]))
    return list(px[0, 0])

def compare_colors(s,n):
    #takes the euclidean distance for the colors, I know there are better methods, and I've used them
    #but this was the easiest and fastest
    old = []
    new = []

    #convert string to ints
    for item in s:
        old.append(int(item))
    for item in n:
        new.append(int(item))

    #Euclidean distance
    distance = math.sqrt((old[0]-new[0])**2+(old[1]-new[1])**2+(old[2]-new[2])**2)
    print(distance)
    return distance


if __name__=="__main__":
  process()
