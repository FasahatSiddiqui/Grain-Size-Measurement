import cv2
import numpy as np

def pixel_value(img):
    global ix, iy, fx, fy, drawing, scale
    img1 = img.copy()
    img2 = img.copy()
    scale = 0
    drawing = False
    ix, iy = -1, -1
    fx, fy = -1, -1

    # mouse callback function
    def mouse_crop(event, x, y, flags, params):
        global ix, iy, fx, fy, drawing, scale   
        overlay = img2.copy()
        output = img2.copy()
        alpha = 0.5

        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            ix, iy = x, y        
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing == True:
                overlay = img2.copy()
                cv2.line(overlay, (ix, iy), (x, y), (0, 0, 255), 2)
                cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, img1)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            fx, fy = x, y
            cv2.line(overlay, (ix, iy), (fx, fy), (0, 0, 255), 2)
            cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, img1)
            if ix > 0 and fx > 0:
                scale = int((((ix-fx )**2) + ((iy-fy)**2))**0.5)
                
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', mouse_crop)
    while(1):
        cv2.imshow('image', img1)
        if cv2.waitKey(20) & 0xFF==13:
            break
    cv2.destroyAllWindows()
    
    return scale


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

    pixel_value(img)
    print(scale)