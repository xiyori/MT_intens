import cv2
from screeninfo import get_monitors
import numpy as np
import math
from scipy.spatial.transform import Rotation


import ctypes  # An included library with Python install.
def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

message = "    To highlight a point, press it with a double click.\n    Once you select a point, click next to the background to compare the intensity for it.\n    You can select several points. Do not forget for all of them to select a pair with background immediately.\n    After you have selected all the points, press the Enter for further processing."
# Mbox('Program usage rules', message, 1)

SELECT = 0
screen = get_monitors()
# print(screen[0].height)


for monitor in get_monitors():
    work_area = [monitor.width, monitor.height - 100]

    print(str(work_area[0]) + 'x' + str(work_area[1]))

crds = np.array([])
i=1

def mouse_action(event, x, y, flags, param):
    global crds, img, selected_img, union_img, img_ori, SELECT, I, i

    if event == cv2.EVENT_LBUTTONDBLCLK:
        if crds.shape[0] == 2:
            crds = np.append(crds, [x, y])
            print("crds", crds)
            x3, y3, x4, y4, ang, M = get_crds(crds)
            print("x, y", x3, y3, x4, y4)
            img = cv2.warpAffine(img, M, (img_ori_w, img_ori_h))
            # cv2.imshow("Rotated by 45 Degrees", rotated)
            selected_img = img[y3:y4, x3:x4].copy()

            cv2.rectangle(img, (x3, y3), (x4, y4), (255, 255, 0), 1)#draw rectangle on full img

            #copy selected area with extension so that the frame does not overlap data
            cv2.imshow("Selected Image "+ str(i), selected_img)
            i+=1
            # cv2.rectangle(selected_img, (0, 0), (8, 8), (255, 255, 255), 1)
            I = np.append(I, calculate_I(selected_img))
            print("III", I)
            crds = np.array([])
            print("cc", crds)

        else:
            crds = np.append(crds, [x, y])  # save click coordinates
            print("crds", crds)
    cv2.imshow("Z project", img)

def calculate_I(sel_img):
    Intens = 0
    for i in range(sel_img.shape[0]):
        for j in range(sel_img.shape[1]):
            Intens += 0.299 * sel_img[i, j, 2] + 0.587 * sel_img[i, j, 1] + 0.114 * sel_img[i, j, 0]
    print("sel img shape", sel_img.shape)
    return round(Intens / sel_img.shape[1])

def get_crds(crds):
    x1, y1, x2, y2 = crds
    l = math.sqrt((x1-x2)**2 + (y1-y2)**2)

    # for i in range(3):
    #     x3 = int(round(x1 - i / math.sqrt(1 + 1 / (a * a))))
    #     y3 = int(round(-x3 / a + x1 / a + y1))
    #
    #     x4 = int(round(x2 - i / math.sqrt(1 + 1 / (a * a))))
    #     y4 = int(round(-x4 / a + x2 / a + y2))
    #
    #     lines = np.append(lines, [x3, y3, x4, y4])

    ang = math.atan((y2-y1)/(x2-x1)) * 180 / math.pi
    M = cv2.getRotationMatrix2D((x1, y1), ang, 1.0)

    # old = np.array([x1, y1, 1])
    # new = np.matmul(M, old)
    # x1_new = new[0]
    # y1_new = new[1]
    x2_new = x1 + l
    y2_new = y1

    return int(x1), int(y1-3), int(x2_new), int(y2_new+3), ang, M




#------------change file name
img_ori = cv2.imread("pics/1.jpg")

cv2.namedWindow('Z project', cv2.WINDOW_FULLSCREEN)
cv2.moveWindow('Z project', int(0.1 * work_area[0]), int(0.1 * work_area[1]))
win = cv2.getWindowImageRect("Z project")



img_ori_h, img_ori_w = img_ori.shape[0:2] # original image width and height
img = img_ori.copy()
selected_img = []
union_img = []
cv2.imshow("Z project", img)
I = np.array([])


cv2.setMouseCallback('Z project', mouse_action)
