import os
import cv2
import time
import threading

sleep = 0
screenshot_counter = 0

# Get the path of the this script
CURRENT_FILE_PATH = os.path.dirname(__file__)

# Load the haar-like features
FACE_CASCADE = cv2.CascadeClassifier(os.path.join(
    CURRENT_FILE_PATH, 'haarcascade_frontalface_default.xml'))

SMILE_CASCADE = cv2.CascadeClassifier(
    os.path.join(CURRENT_FILE_PATH, 'haarcascade_smile.xml'))


# Detect smile and draw stuff onto screen
def face_detection(bw_img, orig_img):

    global sleep
    global screenshot_counter
    
    faces = FACE_CASCADE.detectMultiScale(bw_img, 1.3, 5)

    for fx, fy, fw, fh in faces:
        region_of_interest_bw = bw_img[fy:fy+fh, fx:fx+fw]
        region_of_interest_color = orig_img[fy:fy+fh, fx:fx+fw]

        smiles = SMILE_CASCADE.detectMultiScale(region_of_interest_bw, 5, 30)
        for sx, sy, sw, sh in smiles:
            cv2.rectangle(region_of_interest_color, (sx, sy),
                          (sx+sw, sy+sh), (0, 0, 255), 2)
            if sleep == 0:
                dispense(orig_img, screenshot_counter)
                screenshot_counter += 1
                print(screenshot_counter)
                sleep = 1

    return orig_img 

# Take a screenshot and save onto local folder
def screenshot(img, counter):
    img_path = os.path.join(CURRENT_FILE_PATH, 'faces')

    if not os.path.exists(img_path):
        os.makedirs(img_path)
    cv2.imwrite(os.path.join(
        img_path, 'screenshot-{0}.jpeg'.format(counter)), img)\

# Run GPIO pin to trigger motor
def dispense(orig_img, screenshot_counter):
    print("Dispense")
    screenshot(orig_img, screenshot_counter)
    
# Wake up from cooldown and ready for next smile
def wakeup():
    threading.Timer(5.0, wakeup).start()
    global sleep

    if sleep == 1:
       print("Wake Up") 
       sleep = 0

# Init OpenCV camera here
def start_video_capturing(video_capture):
    wakeup()

    while True:
        _, img = video_capture.read()
        bw_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        canvas = face_detection(bw_img, img)
        cv2.imshow('Video', canvas)
        k = cv2.waitKey(1)
        if k == 27:
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':

     # 0 = internal webcam, 1 = external webcam
    VIDEO_CAPTURE = cv2.VideoCapture(0)
    start_video_capturing(VIDEO_CAPTURE)



   

   
