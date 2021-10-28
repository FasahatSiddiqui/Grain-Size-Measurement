import cv2
import numpy as np

def crop_ROI(img):
    global ix, iy, fx, fy, drawing, region
    img1 = img.copy()
    img2 = img.copy()
    region=[]
    drawing = False
    ix, iy = -1, -1
    fx, fy = -1, -1

    # mouse callback function
    def mouse_crop(event, x, y, flags, params):
        global ix, iy, fx, fy, drawing, region               #overlay, output, alpha
        overlay = img2.copy()
        output = img2.copy()
        alpha = 0.5

        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            ix, iy = x, y        
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing == True:
                overlay = img2.copy()
                cv2.rectangle(overlay, (ix, iy), (x, y), (0, 0, 255), 2)
                cv2.putText(overlay, 'Cropped Region', (ix, iy-10), cv2.FONT_HERSHEY_PLAIN, 0.9, (255,0,0), 2)
                cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, img1)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            fx, fy = x, y
            cv2.rectangle(overlay, (ix, iy), (fx, fy), (0, 0, 255), 2)
            cv2.putText(overlay, 'Cropped Region', (ix, iy-10), cv2.FONT_HERSHEY_PLAIN, 0.9, (255,0,0), 2)
            cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, img1)

    cv2.namedWindow('image')
    cv2.setMouseCallback('image', mouse_crop)
    while(1):
        cv2.imshow('image', img1)
        if cv2.waitKey(20) & 0xFF==13:
            break
    cv2.destroyAllWindows()
    
    if fx > 0:
        region = img2[iy:fy, ix:fx]
    return region


if __name__ =="__main__":
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    file_path =  filedialog.askopenfilename(initialdir = "/home/fasahat/pCloudDrive/MyPictures/",title = "Select file",filetypes = [("picture","*.jpg .png .tif .bmp .gif")])
    root.destroy()

    img = cv2.imread(file_path,1)
    img_height = 1000
    size_ratio = (img_height / float(img.shape[1]))
    img_width = int((float(img.shape[0]) * float(size_ratio)))
    img = cv2.resize(img, (img_height, img_width), interpolation=cv2.INTER_AREA)

    crop_ROI(img)
    print(region.shape)
    #filename='savedImage.jpg'
    #cv2.imwrite(filename, region)
    cv2.imshow('ROI', region)
    cv2.waitKey(0)
    cv2.destroyAllWindows()