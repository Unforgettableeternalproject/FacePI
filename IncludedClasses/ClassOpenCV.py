import os
import time
import IncludedClasses.ClassConfig
from PIL import Image, ImageDraw, ImageFont, ImageTk
import cv2
import numpy as np

config = IncludedClasses.ClassConfig.Config()

def getTakePicturePath(personGroupId):
    basepath = os.path.dirname(os.path.realpath(__file__))

    jpgimagepath = os.path.join(
        basepath, 'takepictures', personGroupId + "_" +
        time.strftime("%Y%m%d_%H%M%S", time.localtime()) + ".jpg")

    if not os.path.exists(os.path.dirname(jpgimagepath)):
        os.makedirs(os.path.dirname(jpgimagepath))
    return jpgimagepath


def show_opencv(hint='', mirror=True):

    #cam = cv2.VideoCapture(config['videoid'])
    print('opening camara')
    cam = cv2.VideoCapture(0)
    print('cam opened')
    cam.set(3, 1280)  # resolution width
    cam.set(4, 1280 // 16 * 9)  # resolution height
    print('WIDTH', cam.get(3), 'HEIGHT', cam.get(4))

    while True:
        ret_val, img = cam.read()
        if mirror:
            img = cv2.flip(img, 1)

        H, W = img.shape[:2]

        cv2_im = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 
        pil_im = Image.fromarray(cv2_im)
        draw = ImageDraw.Draw(pil_im)  #

        ttf = "C:/Windows.old/Windows/Fonts/msjhbd.ttc"

        ##font = ImageFont.truetype(ttf, 40, encoding="utf-8")
        hintfont = ImageFont.truetype(ttf, 24, encoding="utf-8")

        hints = "Press Enter to capture." + hint
        w, h = draw.textsize(hints, font=hintfont)
        draw.rectangle(
            ((W / 2 - w / 2 - 5, H - h), (W / 2 + w / 2 + 5, H)), fill="blue")
        hintlocation = (W / 2 - w / 2, H - h)
        #textlocation = (0,0)
        draw.text(
            hintlocation, hints, (0, 255, 255),
            font=hintfont)  #

        cv2_text_im = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)

        # if ClassUtils.isWindows():
        cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN,
                              cv2.WINDOW_FULLSCREEN)

        cv2.imshow("window", cv2_text_im)
        #cv2.imshow("window", img)

        key = cv2.waitKey(1)
        if key == ord(' ') or key == 3 or key == 13:  # space or enter
            picturepath = getTakePicturePath(
                config.readConfig()['personGroupId'])
            ret_val, img = cam.read()
            cv2.imwrite(picturepath, img)
            cv2.destroyAllWindows()
            cv2.VideoCapture(0).release()
            return picturepath
        elif key == 27:  # esc to quit
            cv2.destroyAllWindows()
            cv2.VideoCapture(0).release()
            raise print("Press ESC to quit.")
        else:
            if key != -1:
                print('key=', key)
