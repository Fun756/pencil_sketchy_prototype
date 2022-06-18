import cv2
import numpy as np
from tkinter import *

#GUI -------------------------
import tkinter as tk
from tkinter import ttk
# import filedialog module
from tkinter import filedialog
# Function for opening the
# file explorer window

# search for the input file 
def browseFiles():
    filename = filedialog.askopenfilename(title = "Select a File",filetypes = (("jpg files","*.jpg*"),("all files","*.*")))
    tPath.delete(0, tk.END) # delete the current text input
    tPath.insert(tk.END, filename) # replace that text input with new file path

# this is a function to get the user input from the text input box
def getFilePath():
	userPath = tPath.get()
	return userPath

# this is a function to get the user input from the text input box
def getDenoiseValue():
	userInput = tDenoise.get()
	return userInput

# this is a function to get the selected radio button value
def getBrightnessValue():
	buttonSelected = tBrightness.get()
	return buttonSelected

# this is a function to get the selected radio button value
def getSobelValue():
	buttonSelected = sobelSize.get()
	return buttonSelected

# this is a function to get the selected radio button value
def getGaussianValue():
	buttonSelected = gaussianSize.get()
	return buttonSelected

# this is the function called when the button is clicked
def btnClickFunction():
    sketchStart(getFilePath(),int(getDenoiseValue()),int(getBrightnessValue()) + 1,int(getSobelValue()),int(getGaussianValue()), int(getCheckboxValue()))

# this is a function to check the status of the checkbox (1 means checked, and 0 means unchecked)
def getCheckboxValue():
	checkedOrNot = Is_CVsketch.get()
	return checkedOrNot



#Sketch Part ------------------------------------

#other functions
# Automatic brightness and contrast optimization with optional histogram clipping
def automatic_brightness_and_contrast(image, clip_hist_percent):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate grayscale histogram
    hist = cv2.calcHist([gray],[0],None,[256],[0,256])
    hist_size = len(hist)

    # Calculate cumulative distribution from the histogram
    accumulator = []
    accumulator.append(float(hist[0]))
    for index in range(1, hist_size):
        accumulator.append(accumulator[index -1] + float(hist[index]))

    # Locate points to clip
    maximum = accumulator[-1]
    clip_hist_percent *= (maximum/100.0)
    clip_hist_percent /= 2.0

    # Locate left cut
    minimum_gray = 0
    while accumulator[minimum_gray] < clip_hist_percent:
        minimum_gray += 1

    # Locate right cut
    maximum_gray = hist_size -1
    while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
        maximum_gray -= 1

    # Calculate alpha and beta values
    alpha = 255 / (maximum_gray - minimum_gray)
    beta = -minimum_gray * alpha

    auto_result = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return (auto_result, alpha, beta)

#main function
def sketchStart(filePath, denoise_value, brightness_value, sobel_mask, gaussian_size, is_cvsketch):
    
    #input -----------------------
    image = cv2.imread(filePath)
    cv2.imshow('original', image)

    #texture removal --- denoise

    image_de = cv2.fastNlMeansDenoisingColored(image,None,denoise_value,denoise_value,7,21) # อธิบาย 7, 21 ในรายงาน


    #image enhancement -----------------------

    #edge detection --- sobel
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    x = cv2.Sobel(gray, cv2.CV_64F, 1,0, ksize=sobel_mask, scale=1)
    y = cv2.Sobel(gray, cv2.CV_64F, 0,1, ksize=sobel_mask, scale=1)
    absx= cv2.convertScaleAbs(x)
    absy = cv2.convertScaleAbs(y)
    edge = cv2.addWeighted(absx, 0.5, absy, 0.5,0)
    #cv2.imshow('edge', edge)
    edge_inv = 255 - edge

    #cv2.imshow('edge_inv', edge_inv)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    #auto contrast ---------------------------
    #image2 = cv2.imread('example4.jpg')
    auto_result, alpha, beta = automatic_brightness_and_contrast(image_de,brightness_value)

    #cv2.imshow('auto_result', auto_result)
    #cv2.imshow('ori', image_de)
    #cv2.waitKey()

    #making sketch ---------------------------

    #cv2 pencilSketch
    dst_gray, dst_color = cv2.pencilSketch(image_de, sigma_s=60, sigma_r=0.07, shade_factor=0.09)

    #main function
    gray_image = cv2.cvtColor(auto_result, cv2.COLOR_BGR2GRAY)

    #cv2.imwrite("gray.png", gray_image)
    inverted_image = 255 - gray_image
    #cv2.imwrite("inv.png", inverted_image)
    blurred = cv2.GaussianBlur(inverted_image, (gaussian_size, gaussian_size), 0)
    #cv2.imwrite("blur.png", blurred)
    inverted_blurred = 255 - blurred
    #cv2.imwrite("invblur.png", inverted_blurred)
    pencil_sketch = cv2.divide(gray_image, inverted_blurred, scale=256.0)
    #cv2.imwrite("Sketch.png", pencil_sketch)

    #result_divide = cv2.divide(pencil_sketch, edge_inv, scale=256.0)
    #result = cv2.addWeighted(pencil_sketch, 0.8, edge_inv, 0.2,0)
    #result_both = cv2.addWeighted(result_divide, 0.5, result, 0.5,0)

    #result_cv = cv2.addWeighted(result, 0.9, dst_gray, 0.1, 0)
    #result_cv_both = cv2.addWeighted(result_both, 0.5, result_cv, 0.5, 0)
    #result_cv_both_divide = cv2.divide(result_both, result_cv, scale=256.0)

    if(is_cvsketch == 1):
        #print('Yes')
        result = cv2.addWeighted(pencil_sketch, 0.8, edge_inv, 0.2,0)
        result = cv2.addWeighted(result, 0.85, dst_gray, 0.15, 0)
        cv2.imshow("Result : CVSketch Applied", result)
    
    else:
        #print('No')
        result = cv2.addWeighted(pencil_sketch, 0.8, edge_inv, 0.2,0)
        cv2.imshow("Result : Default", result)


#output ---------------------------------------------------------------------------

    #cv2.imshow("no pencil", result)
    #cv2.imshow("pencil ", pencil_sketch)
    #cv2.imshow("pencil cv", result_cv)
    #cv2.imshow("output", result_cv_both)
    #cv2.imshow("cv", dst_gray)
    #cv2.imshow("pencil cv all divide", result_cv_both_divide)
    #cv2.imshow("result_divide", result_divide)
    
    #before dividing
    #cv2.imshow("gray_image", gray_image)
    #cv2.imshow("inverted_blurred", inverted_blurred)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imwrite("output.jpg", result)

#----------------------------------------------------------------

# root - main window to call put labels, text, etc in it --------------------
root = Tk()


#declaration of the variable associated with the radio button group --- from string to int
tBrightness = tk.IntVar()

sobelSize = tk.IntVar()

gaussianSize = tk.IntVar()

#this is the declaration of the variable associated with the checkbox --- from string to int

Is_CVsketch = tk.IntVar()

# initial set up main window --------------------------------------------------
# This is the section of code which creates the main window
root.geometry('470x512')
root.configure(background='#F0F8FF')
root.title('Pencil Sketch')

# Upload the Photo -------------------------------------------------------------------------------------------
# This is the section of code which creates the a label
Label(root, text='Upload Your Photo Here!', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=14, y=8)

# This is the section of code which creates a text input box
tPath=Entry(root)
tPath.place(x=14, y=28)

# This is the section of code which put the path of the file to tPath
button_explore = Button(root, text = "Browse Files", font=('arial', 10, 'normal'), command = browseFiles).place(x=154, y=28)

# Denoising -------------------------------------------------------------------------------------------
# This is the section of code which creates the a label
Label(root, text='Denoising Value', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=14, y=68)
Label(root, text='ค่าที่เอาไว้ลบเนื้อภาพ เพื่อช่วยลบ Noise (Default: 5)', bg='#F0F8FF', font=('arial', 10, 'normal')).place(x=14, y=88)

# This is the section of code which creates a text input box
tDenoise=Entry(root)
tDenoise.place(x=14, y=108)

# Histrogram Clipping -------------------------------------------------------------------------------------------
# This is the section of code which creates the a label
Label(root, text='Histogram Clipping', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=14, y=138)
Label(root, text='ตัดส่วนสีที่เกินเกณฑ์ใน Hist.ภาพ ใช้กับ Auto Brightness(Default: 1)', bg='#F0F8FF', font=('arial', 10, 'normal')).place(x=14, y=158)

# This is the section of code which creates a text input box
tBrightness=Entry(root)
tBrightness.place(x=14, y=178)

# Sobel -------------------------------------------------------------------------------------------
# This is the section of code which creates the a label
Label(root, text='Sobel Size', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=14, y=218)
Label(root, text='ขนาด Mask ของ Sobel Filter (Default: 3)', bg='#F0F8FF', font=('arial', 10, 'normal')).place(x=14, y=238)

# This is the section of code which creates a group of radio buttons
frame=Frame(root, width=0, height=0, bg='#F0F8FF')
frame.place(x=14, y=258)
ARBEES=[
('3', '3'), 
('5', '5'), 
('7', '7'), 
]
for text, mode in ARBEES:
	rbSobel=Radiobutton(frame, text=text, variable=sobelSize, value=mode, bg='#F0F8FF', font=('arial', 12, 'normal')).pack(side='left', anchor = 'w')

# Gaussian -------------------------------------------------------------------------------------------
# This is the section of code which creates the a label
Label(root, text='Gaussian Size', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=14, y=298)
Label(root, text='ขนาดของ Blur เพื่อไปใช้ในสูตร (เกี่ยวข้องกับขอบดินสอร่าง) (Default:15)', bg='#F0F8FF', font=('arial', 10, 'normal')).place(x=14, y=318)

# This is the section of code which creates a group of radio buttons
frame=Frame(root, width=0, height=0, bg='#F0F8FF')
frame.place(x=14, y=338)
ARBEES=[
('9', '9'), 
('11', '11'), 
('13', '13'), 
('15', '15'), 
('17', '17'), 
('19', '19'), 
('21', '21'), 
]
for text, mode in ARBEES:
	rbGaussian=Radiobutton(frame, text=text, variable=gaussianSize, value=mode, bg='#F0F8FF', font=('arial', 12, 'normal')).pack(side='left', anchor = 'w')

# CVSketch -------------------------------------------------------------------------------------------
# This is the section of code which creates the a label
Label(root, text='CV Pencil Sketch', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=14, y=378)
Label(root, text='เปิดใช้งานอัลกอริทึม ร่างภาพ นอกเหนือจากตัวหลัก เพื่อเสริมรายละเอียดภาพ (Default: No)', bg='#F0F8FF', font=('arial', 10, 'normal')).place(x=14, y=398)

# This is the section of code which creates a checkbox
CVSketch=Checkbutton(root, text='คลิกเพื่อเปิดใช้งาน', variable=Is_CVsketch, bg='#F0F8FF', font=('arial', 12, 'normal'))
CVSketch.place(x=14, y=418)

# input ---------------------------------------------------------------------------------------------
# This is the section of code which creates a text input box
tDenoise=Entry(root)
tDenoise.place(x=14, y=108)


# Sketch! -------------------------------------------------------------------------------------------
# This is the section of code which creates a button
Button(root, text='Sketch!', bg='#FFF8DC', font=('arial', 14, 'normal'), command=btnClickFunction).place(x=190, y=458)

root.mainloop()