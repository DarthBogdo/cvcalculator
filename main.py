import cv2
from cvzone.HandTrackingModule import HandDetector
import sys


# Define button class
class Button:
    def __init__(self, p, w, h, val):
        self.p = p
        self.w = w
        self.h = h
        self.val = val

# Define how the grid is drawn
    def draw(self, img):
        cv2.rectangle(img, self.p, (self.p[0] + self.w, self.p[1] + self.h),
                      (225, 225, 225), cv2.FILLED)  # x1,y1,x2,y2
        cv2.rectangle(img, self.p, (self.p[0] + self.w, self.p[1] + self.h),
                      (50, 50, 50), 3)

        cv2.putText(img, self.val, (self.p[0] + 30, self.p[1] + 70), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (50, 50, 50), 2)  # text, position, font, scale of the font, color, thickness

# Checks if the button was clicked and returns True or False
    def Click(self, x,y):
        if self.p[0]< x <self.p[0] + self.w and \
                self.p[1] < y < self.p[1] + self.h:
            cv2.rectangle(img, self.p, (self.p[0] + self.w, self.p[1] + self.h),
                          (255, 255, 255), cv2.FILLED)  # x1,y1,x2,y2
            cv2.rectangle(img, self.p, (self.p[0] + self.w, self.p[1] + self.h),
                          (50, 50, 50), 3)

            cv2.putText(img, self.val, (self.p[0] + 30, self.p[1] + 70), cv2.FONT_HERSHEY_SIMPLEX,
                        2, (0, 0, 0), 2)
            return True
        else:
            return False


vid = cv2.VideoCapture(0)  # Taking feed from a webcam

det = HandDetector(detectionCon=0.8, maxHands=1)  # hand detection confidence
buttonlval = [['1', '2', '3', '+'],
              ['4', '5', '6', '-'],
              ['7', '8', '9', '*'],
              ['.', '0', '/', '=']]
buttonl = []
for x in range(4):
    for y in range(4):
        xpos = x*100 + 800
        ypos = y*100+150
        buttonl.append(Button((xpos, ypos), 100, 100, buttonlval[y][x]))
        print(f'x = {x}, y= {y}')

equation = ''
delay_count = 0

while True:
    condition, img = vid.read()  # tells if the image was received and gets it
    img = cv2.flip(img, 1)  # flips (0-vertically, 1 - horizontally)
    img = cv2.resize(img, (1280, 720))
    hands, img = det.findHands(img)  # sends the list of points of the hands

    cv2.rectangle(img, (800,60), (800 + 400, 60+100),
                  (225, 225, 225), cv2.FILLED)  # x1,y1,x2,y2
    cv2.rectangle(img, (800,60), (800 + 400, 60+100),
                  (50, 50, 50), 3)
    for b in buttonl:
        b.draw(img)


    if hands:
        lmList = hands[0]['lmList']
        length, _, img = det.findDistance(lmList[8][0:2], lmList[12][0:2], img)
        x, y = lmList[8][0:2]
        if length < 50:  # defines the threshold distance at which the button click is registered
            for i, b in enumerate(buttonl):
                if b.Click(x, y) and delay_count == 0:
                    c_val = buttonlval[int(i % 4)][int(i/4)]
                    if c_val == '=':
                        equation = str(eval(equation))
                    else:
                        equation += c_val
                    delay_count = 1

# Delays the input to avoid double clicks
    if delay_count != 0:
        delay_count += 1
        if delay_count > 10:
            delay_count = 0

    cv2.putText(img, equation, (810, 130), cv2.FONT_HERSHEY_SIMPLEX,
                2, (50, 50, 50), 2)
    # Display of the video
    cv2.imshow('Display', img)
    key = cv2.waitKey(1)

# Reset and escape buttons
    if key == ord('c'):
        equation = ''
    if key == ord('e'):
        sys.exit()





