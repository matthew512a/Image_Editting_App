import tkinter as tk
from tkinter import ttk
from matplotlib import pyplot as plt
from tkinter import messagebox as mBox
from PIL import Image, ImageTk
import subprocess
import cv2
from pylab import *
from matplotlib import path
import matplotlib.cm as cm
from matplotlib.widgets import Slider
from tkinter import filedialog
import numpy as np
from matplotlib.image import imread
from scipy import ndimage as ndi

from skimage.feature import peak_local_max

from skimage.transform import (hough_line, hough_line_peaks,
                               probabilistic_hough_line)
from skimage.feature import canny
from skimage import data

import matplotlib.pyplot as plt
from matplotlib import cm

import tkinter.scrolledtext as tkst
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib.path import Path
from matplotlib.widgets import LassoSelector
from collections import deque
import matplotlib.image as mpimg

### Functions
def OPEN():
    global Original_Image
    global Dimension_Number
    global Original_image_Size
    root1.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                filetypes=(("jpeg files", "*.jpg"),("png files", "*.png"),
                                                ("tif files", "*.TIF"), ("all files", "*.*")))
    Original_Image = Image.open(root1.filename)
    Original_Image=np.array(Original_Image)
    Original_image_Size = np.shape(Original_Image)
    print(len(Original_image_Size))


    a1 = np.shape(Original_Image)
    a1 = str(a1)
    tk.Label(root1, text='Dimensions: ').place(x=0,y=0)
    v_dim = tk.StringVar(root1, value=a1)
    e = tk.Entry(root1, textvariable=v_dim)
    e.place(x=70, y=0)



    if len(Original_image_Size) > 2:
        Dimension_Number = []
        Dimension_Number_int = []
        for x1 in range(Original_Image.shape[2]):
            Dimension_Number_int.append(x1 + 1)
            Dimension_Number.append(("Band ", x1 + 1))

    else:
        Dimension_Number = [("Band", 1)]

    def RGB_Show():
        root2 = tk.Toplevel()
        root2.geometry('600x600')

        def resize_image(event):
            new_width = event.width
            new_height = event.height
            image = copy_of_image.resize((new_width, new_height))
            photo = ImageTk.PhotoImage(image)
            label.config(image=photo)
            label.image = photo  # avoid garbage collection

        image = Original_Image
        image = Image.fromarray(image)
        copy_of_image = image.copy()
        photo = ImageTk.PhotoImage(image)
        label = ttk.Label(root2, image=photo)
        label.bind('<Configure>', resize_image)
        label.pack(fill=tk.BOTH, expand='YES')

        root2.mainloop()

    def ShowChoice():
        a = int(v1.get())
        root2 = tk.Toplevel()
        root2.geometry('600x600')

        def resize_image(event):
            new_width = event.width
            new_height = event.height
            image = copy_of_image.resize((new_width, new_height))
            photo = ImageTk.PhotoImage(image)
            label.config(image=photo)
            label.image = photo  # avoid garbage collection

        image = Original_Image[:, :, a]
        image = Image.fromarray(image)
        copy_of_image = image.copy()
        photo = ImageTk.PhotoImage(image)
        label = ttk.Label(root2, image=photo)
        label.bind('<Configure>', resize_image)
        label.pack(fill=tk.BOTH, expand='YES')

        root2.mainloop()

    def ShowChoiceOneBand():
        root2 = tk.Toplevel()
        root2.geometry('600x600')

        def resize_image(event):
            new_width = event.width
            new_height = event.height
            image = copy_of_image.resize((new_width, new_height))
            photo = ImageTk.PhotoImage(image)
            label.config(image=photo)
            label.image = photo  # avoid garbage collection

        image = Original_Image
        image = Image.fromarray(image)
        copy_of_image = image.copy()
        photo = ImageTk.PhotoImage(image)
        label = ttk.Label(root2, image=photo)
        label.bind('<Configure>', resize_image)
        label.pack(fill=tk.BOTH, expand='YES')

    tk.Label(root1, text="""Choose your favourite view:""", justify=tk.LEFT, padx=20).place(x=0,y=20)

    if len(Original_image_Size) > 2:
        v1 = tk.StringVar()
        v1.set("L")  # initialize
        z=20
        for val, Dimension_Number in enumerate(Dimension_Number):
            z=z+20
            b = tk.Radiobutton(root1, text=Dimension_Number, padx=20, variable=v1, value=val, command=ShowChoice)
            b.place(x=0,y=z)
        if Original_image_Size[2] == 3:
            RGB_btn = tk.Button(root1, bg='#000000', fg='#b7f731', text='   RGB   ', padx=20, bd='5', command=RGB_Show)
            RGB_btn.place(x=0,y=20+z)
    else:
        z=20
        b = tk.Radiobutton(root1, text="Band 1", padx=20, value=1, command=ShowChoiceOneBand)
        b.place(x=0,y=z+20)

    def Staticks():
        root3 = tk.Tk()
        if len(Original_image_Size) > 2:
            a_staticks = int(v1.get())
            img_staticks = Original_Image[:, :, a_staticks]

            Min = np.min(img_staticks)
            Min = str(Min)
            tk.Label(root3, text='Minimum: ').grid(row=0, column=0)
            v_min = tk.StringVar(root3, value=Min)
            e_min = tk.Entry(root3, textvariable=v_min)
            e_min.grid(row=0, column=1)

            Max = np.max(img_staticks)
            Max = str(Max)
            tk.Label(root3, text='Maximum: ').grid(row=1, column=0)
            v_Max = tk.StringVar(root3, value=Max)
            e_Max = tk.Entry(root3, textvariable=v_Max)
            e_Max.grid(row=1, column=1)

            Mean = np.mean(img_staticks)
            Mean = str(Mean)
            tk.Label(root3, text='Maximum: ').grid(row=2, column=0)
            v_Mean = tk.StringVar(root3, value=Mean)
            e_Mean = tk.Entry(root3, textvariable=v_Mean)
            e_Mean.grid(row=2, column=1)

            STD = np.std(img_staticks)
            STD = str(STD)
            tk.Label(root3, text='Standard Diversion: ').grid(row=3, column=0)
            v_STD = tk.StringVar(root3, value=STD)
            e_STD = tk.Entry(root3, textvariable=v_STD)
            e_STD.grid(row=3, column=1)

            SUM = np.sum(img_staticks)
            SUM = str(SUM)
            tk.Label(root3, text='Total: ').grid(row=4, column=0)
            v_SUM = tk.StringVar(root3, value=SUM)
            e_SUM = tk.Entry(root3, textvariable=v_SUM)
            e_SUM.grid(row=4, column=1)
        else:
            img_staticks = Original_Image

            Min = np.min(img_staticks)
            Min = str(Min)
            tk.Label(root3, text='Minimum: ').grid(row=0, column=0)
            v_min = tk.StringVar(root3, value=Min)
            e_min = tk.Entry(root3, textvariable=v_min)
            e_min.grid(row=0, column=1)

            Max = np.max(img_staticks)
            Max = str(Max)
            tk.Label(root3, text='Maximum: ').grid(row=1, column=0)
            v_Max = tk.StringVar(root3, value=Max)
            e_Max = tk.Entry(root3, textvariable=v_Max)
            e_Max.grid(row=1, column=1)

            Mean = np.mean(img_staticks)
            Mean = str(Mean)
            tk.Label(root3, text='Maximum: ').grid(row=2, column=0)
            v_Mean = tk.StringVar(root3, value=Mean)
            e_Mean = tk.Entry(root3, textvariable=v_Mean)
            e_Mean.grid(row=2, column=1)

            STD = np.std(img_staticks)
            STD = str(STD)
            tk.Label(root3, text='Standard Diversion: ').grid(row=3, column=0)
            v_STD = tk.StringVar(root3, value=STD)
            e_STD = tk.Entry(root3, textvariable=v_STD)
            e_STD.grid(row=3, column=1)

            SUM = np.sum(img_staticks)
            SUM = str(SUM)
            tk.Label(root3, text='Total: ').grid(row=4, column=0)
            v_SUM = tk.StringVar(root3, value=SUM)
            e_SUM = tk.Entry(root3, textvariable=v_SUM)
            e_SUM.grid(row=4, column=1)

        root3.mainloop()

    Quick_Staticks_btn = tk.Button(root1, bg='#000000', fg='#b7f731', text='Staticks', padx=20, bd='5',
                                   command=Staticks)
    Quick_Staticks_btn.place(x=0,y=z+50)

def Show_Histogram1():
    root4 = tk.Toplevel()
    root4.geometry("1800x900")
    root4.configure(background='white')
    root4.title("VNU - UET - GROUP 16 - NGUYEN KHAC KIEN, BUI DUC ANH, TRAN HOANG HUAN")

    frame1 = tk.Frame(
        master=root4,
        bg='#808000'
    )
    frame1.place(x=0, y=200)
    editArea = tkst.ScrolledText(
        master=frame1,
        wrap=tk.WORD,
        width=20,
        height=10
    )
    # Don't use widget.place(), use pack or grid instead, since
    # They behave better on scaling the window -- and you don't
    # have to calculate it manually!
    editArea.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    editArea.configure(font=('Franklin Gothic Demi Cond', 11))
    
    def Show_Histogram2():
        if len(Original_image_Size) > 2:
            a_Histogram = int(numberChosen1.get())
            img = Original_Image[:, :, a_Histogram - 1]
            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])

            fig = plt.Figure(figsize=(13, 7),facecolor='w')

            canvas = FigureCanvasTkAgg(fig, root4)
            canvas.get_tk_widget().place(x=200, y=0)

            toolbarFrame = tk.Frame(master=root4)
            toolbarFrame.place(x=720,y=600)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax1.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax1.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");
            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax1.set_facecolor("#2E2E2E")
            ax2.set_facecolor("#2E2E2E")

            fig.subplots_adjust(bottom=0.25)
            ax1.bar(range(256), hist_img.ravel(),color="#d1ae45",label="Band"+str(a_Histogram))
            ax2.plot(range(256), hist_img.ravel(),color="#d1ae45",label="Band"+str(a_Histogram))

            ax1.set_title("Band"+str(a_Histogram)+" Histogram", fontsize=12, color="#333533")
            ax2.set_title("Band" + str(a_Histogram) + " Histogram", fontsize=12, color="#333533")

            ax1.legend(loc='best')
            ax2.legend(loc='best')


            fig.canvas.draw_idle()




        else:
            img = Original_Image
            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])

            fig = plt.Figure(figsize=(13, 7), facecolor='w')

            canvas = FigureCanvasTkAgg(fig, root4)
            canvas.get_tk_widget().place(x=200, y=0)

            toolbarFrame = tk.Frame(master=root4)
            toolbarFrame.place(x=720, y=600)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax1.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax1.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");
            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax1.set_facecolor("#2E2E2E")
            ax2.set_facecolor("#2E2E2E")

            fig.subplots_adjust(bottom=0.25)
            ax1.bar(range(256), hist_img.ravel(), color="#d1ae45", label="Band" + str(1))
            ax2.plot(range(256), hist_img.ravel(), color="#d1ae45", label="Band" + str(1))

            ax1.set_title("Band" + str(1) + " Histogram", fontsize=12, color="#333533")
            ax2.set_title("Band" + str(1) + " Histogram", fontsize=12, color="#333533")

            ax1.legend(loc='best')
            ax2.legend(loc='best')

            fig.canvas.draw_idle()


    def ALL_BANDS():

        color = ('b', 'g', 'r')
        fig = plt.Figure(figsize=(13, 7))
        canvas = FigureCanvasTkAgg(fig, root4)
        canvas.get_tk_widget().place(x=200, y=0)

        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)

        ax1.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
        ax1.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");
        ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
        ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

        ax1.set_facecolor("#2E2E2E")
        ax2.set_facecolor("#2E2E2E")

        toolbarFrame = tk.Frame(master=root4)
        toolbarFrame.place(x=720, y=600)

        ax1.set_title("Histogram")
        ax2.set_title("Histogram")

        toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
        toolbar.update()

        def on_key_press(event):
            print("you pressed {}".format(event.key))
            key_press_handler(event, canvas, toolbar)

        canvas.mpl_connect("key_press_event", on_key_press)

        fig.subplots_adjust(bottom=0.25)
        k=0
        for i, col in enumerate(color):
            k=1+k
            hist_RGB = cv2.calcHist([Original_Image], [i], None, [256], [0, 256])
            ax1.bar(range(256), hist_RGB.ravel(), color=col,label="Band"+str(k))
            ax2.plot(range(256), hist_RGB.ravel(), color=col,label="Band"+str(k))

            ax1.legend(loc='best')
            ax2.legend(loc='best')

            fig.canvas.draw_idle()

    def CumulativeHistogram():
        if len(Original_image_Size) > 2:
            a_CumulativeHistogr = int(numberChosen1.get())
            img = Original_Image[:, :, a_CumulativeHistogr - 1]
            CumulativeHist = cv2.calcHist([img], [0], None, [256], [0, 256])
            CDF = CumulativeHist.cumsum()

            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root4)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax1.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533")
            ax1.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533")
            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533")
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533")

            ax1.set_facecolor("#2E2E2E")
            ax2.set_facecolor("#2E2E2E")

            toolbarFrame = tk.Frame(master=root4)
            toolbarFrame.place(x=720, y=600)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.bar(range(256), CDF.ravel(),color="gold",label="Band"+str(a_CumulativeHistogr)+"Commulative Histogram")
            ax1.bar(range(256), CumulativeHist.ravel(),color="magenta",label="Band"+str(a_CumulativeHistogr))
            ax2.plot(range(256), CDF.ravel(),color="gold",label="Band"+str(a_CumulativeHistogr)+"Commulative Histogram")
            ax2.plot(range(256), CumulativeHist.ravel(),color="magenta",label="Band"+str(a_CumulativeHistogr))

            ax1.legend(loc='best')
            ax2.legend(loc='best')

            ax1.set_title("Band" + str(a_CumulativeHistogr) + "Comulative Histogram", fontsize=12, color="#333533")
            ax2.set_title("Band" + str(a_CumulativeHistogr) + "Comulative Histogram", fontsize=12, color="#333533")

            fig.canvas.draw_idle()

        else:
            img = Original_Image
            CumulativeHist = cv2.calcHist([img], [0], None, [256], [0, 256])
            CDF = CumulativeHist.cumsum()

            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root4)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax1.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax1.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");
            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax1.set_facecolor("#2E2E2E")
            ax2.set_facecolor("#2E2E2E")

            toolbarFrame = tk.Frame(master=root4)
            toolbarFrame.place(x=720, y=600)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.bar(range(256), CDF.ravel(), color="gold", label="Band" + str(1))
            ax1.bar(range(256), CumulativeHist.ravel(), color="magenta", label="Band" + str(1))
            ax2.plot(range(256), CDF.ravel(), color="gold", label="Band" + str(1))
            ax2.plot(range(256), CumulativeHist.ravel(), color="magenta", label="Band" + str(1))

            ax1.legend(loc='best')
            ax2.legend(loc='best')

            ax1.set_title("Band" + str(1) + "Comulative Histogram", fontsize=12, color="#333533")
            ax2.set_title("Band" + str(1) + "Comulative Histogram", fontsize=12, color="#333533")

            fig.canvas.draw_idle()

    if len(Original_image_Size) > 2:

        Dimension_Number = []
        Dimension_Number_int = []
        for x1 in range(Original_Image.shape[2]):
            Dimension_Number_int.append(x1 + 1)
            Dimension_Number.append(("Band ", x1 + 1))

    else:
        Dimension_Number = [("Band", 1)]

    if len(Original_image_Size) > 2:
        ttk.Label(root4, text="Choose a band:").place(x=0,y=0)
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root4, width=12, textvariable=number1)
        numberChosen1['values'] = (Dimension_Number_int)
        numberChosen1.place(x=0, y=30)
        numberChosen1.current(0)
        if Original_image_Size[2] == 3:
            RGB_btn = tk.Button(root4, bg='#000000', fg='#b7f731', text='   show hist   ', padx=20, bd='5',
                                command=Show_Histogram2)
            RGB_btn.place(x=0, y=60)
            RGB_btn1 = tk.Button(root4, bg='#000000', fg='#b7f731', text='   All Bands   ', padx=20, bd='5',
                                 command=ALL_BANDS)
            RGB_btn1.place(x=0, y=90)
            Cumsum_btn = tk.Button(root4, bg='#000000', fg='#b7f731', text='Cumulative histogram', padx=20, bd='5',
                                   command=CumulativeHistogram)
            Cumsum_btn.place(x=0, y=120)

        def Quit():
           root4.quit()
           root4.destroy()



        button = tk.Button(master=root4, bg='#000000', fg='#b7f731', text='       Quit        ', padx=20,
                            bd='5', command=Quit)
        button.place(x=0, y=150)


    else:
        tk.Label(root4, text="Choose a band:").place(x=0,y=0)
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root4, width=12, textvariable=number1)
        numberChosen1['values'] = "1"
        numberChosen1.place(x=0, y=30)
        numberChosen1.current(0)
        btn1 = tk.Button(root4, bg='#000000', fg='#b7f731', text='   show hist   ', padx=20, bd='5',
                         command=Show_Histogram2)
        btn1.place(x=0, y=60)
        Cumsum_btn = tk.Button(root4, bg='#000000', fg='#b7f731', text='   Cumulative histogram   ', padx=20,
                               bd='5', command=CumulativeHistogram)
        Cumsum_btn.place(x=0, y=90)


        def Quit():
           root4.quit()
           root4.destroy()



        button = tk.Button(master=root4, bg='#000000', fg='#b7f731', text='       Quit        ', padx=20,
                            bd='5', command=Quit)
        button.place(x=0, y=120)

    root4.mainloop()

def Equalization():
    root4 = tk.Toplevel()
    root4.geometry("1800x900")
    root4.configure(background='white')
    root4.title("VNU - UET - GROUP 16 - NGUYEN KHAC KIEN, BUI DUC ANH, TRAN HOANG HUAN")

    frame1 = tk.Frame(
        master=root4,
        bg='#808000'
    )
    frame1.pack(anchor='w')
    editArea = tkst.ScrolledText(
        master=frame1,
        wrap=tk.WORD,
        width=20,
        height=10
    )
    

    def EqualizationOneBand():
        if len(Original_image_Size) > 2:
            a_Histogram = int(numberChosen1.get())
            img = Original_Image[:, :, a_Histogram - 1]
            img2 = cv2.equalizeHist(img)

            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root4)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(221)
            ax2 = fig.add_subplot(222)
            ax3 = fig.add_subplot(212)
            fig.subplots_adjust(bottom=0.25)

            ax3.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax3.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax3.set_facecolor("#2E2E2E")

            toolbarFrame = tk.Frame(master=root4)
            toolbarFrame.place(x=720, y=600)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)



            ax1.imshow(img, cmap='gray')
            ax2.imshow(img2, cmap='gray')
            ax1.grid(False)
            ax2.grid(False)

            a_Histogram = int(numberChosen1.get())
            img = Original_Image[:, :, a_Histogram - 1]
            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
            hist_img1 = cv2.calcHist([img2], [0], None, [256], [0, 256])

            ax3.plot(range(256), hist_img.ravel(), color="magenta", label="Band" + str(1)+"Histogram")
            ax3.plot(range(256), hist_img1.ravel(), color="gold", label="Band" + str(1)+"Equalized Histogram")

            ax3.legend(loc='best')


            ax3.set_title(" Histogram", fontsize=12, color="#333533")
            ax1.set_title(" Original Image", fontsize=12, color="#333533")
            ax2.set_title(" Equalized Image", fontsize=12, color="#333533")


            fig.canvas.draw_idle()

            def SaveI():
                f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                if f is None:
                    return

                filename = f.name

                cv2.imwrite(str(filename) + '.jpg', img2)
                f.close()

            btnw = tk.Button(root4, bg='#000000', fg='#b7f731', text='   Save Equalized Image   ', padx=20, bd='5',
                             command=SaveI)
            btnw.place(x=1000, y=0)


        else:
            img = Original_Image
            img2 = cv2.equalizeHist(img)

            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root4)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(221)
            ax2 = fig.add_subplot(222)
            ax3 = fig.add_subplot(212)
            fig.subplots_adjust(bottom=0.25)

            ax3.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax3.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax3.set_facecolor("#2E2E2E")

            toolbarFrame = tk.Frame(master=root4)
            toolbarFrame.place(x=720, y=600)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            ax1.imshow(img, cmap='gray')
            ax2.imshow(img2, cmap='gray')
            ax1.grid(False)
            ax2.grid(False)


            img = Original_Image
            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
            hist_img1 = cv2.calcHist([img2], [0], None, [256], [0, 256])

            ax3.plot(range(256), hist_img.ravel(), color="magenta", label="Band" + str(1) + "Histogram")
            ax3.plot(range(256), hist_img1.ravel(), color="gold", label="Band" + str(1) + "Equalized Histogram")

            ax3.legend(loc='best')

            ax3.set_title(" Histogram", fontsize=12, color="#333533")
            ax1.set_title(" Original Image", fontsize=12, color="#333533")
            ax2.set_title(" Equalized Image", fontsize=12, color="#333533")


            fig.canvas.draw_idle()

            def SaveI():
                f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))


                if f is None:
                    return

                filename = f.name



                cv2.imwrite(str(filename)+'.jpg',img2)
                f.close()
            btnw = tk.Button(root4, bg='#000000', fg='#b7f731', text='   Save Equalized Image   ', padx=20, bd='5',
                            command=SaveI)
            btnw.place(x=1000, y=0)

    if len(Original_image_Size) > 2:
        Dimension_Number = []
        Dimension_Number_int = []
        for x1 in range(Original_Image.shape[2]):
            Dimension_Number_int.append(x1 + 1)
            Dimension_Number.append(("Band ", x1 + 1))

    else:
        Dimension_Number = [("Band", 1)]

    if len(Original_image_Size) > 2:
        ttk.Label(root4, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root4, width=12, textvariable=number1)
        numberChosen1['values'] = (Dimension_Number_int)
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        btn = tk.Button(root4, bg='#000000', fg='#b7f731', text='   Equalize   ', padx=20, bd='5',
                        command=EqualizationOneBand)
        btn.pack(anchor='w')

    else:
        tk.Label(root4, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root4, width=12, textvariable=number1)
        numberChosen1['values'] = "1"
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        btn1 = tk.Button(root4, bg='#000000', fg='#b7f731', text='   Equalize   ', padx=20, bd='5',
                         command=EqualizationOneBand)
        btn1.pack(anchor='w')

    def Quit():
        root4.quit()
        root4.destroy()

    button = tk.Button(master=root4, bg='#000000', fg='#b7f731', text='       Quit        ', padx=20,
                       bd='5', command=Quit)
    button.pack(anchor='w')

    root4.mainloop()


def Brightness():
    root8 = tk.Toplevel()
    root8.geometry("1800x900")
    root8.configure(background='white')
    root8.title("VNU - UET - GROUP 16 - NGUYEN KHAC KIEN, BUI DUC ANH, TRAN HOANG HUAN")

    frame1 = tk.Frame(
        master=root8,
        bg='#808000'
    )
    frame1.pack(anchor='w')
    editArea = tkst.ScrolledText(
        master=frame1,
        wrap=tk.WORD,
        width=20,
        height=10
    )

    def Brightness1():

        if len(Original_image_Size) > 2:
            a_Brightness = int(numberChosen1.get())
            img = Original_Image[:, :, a_Brightness - 1]
            img = np.array(img)
            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            fig.subplots_adjust(bottom=0.25)

            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax2.set_facecolor("#2E2E2E")

            ax2.set_title(" HiBrightness", fontsize=12, color="#333533")
            ax1.set_title(" Original Image", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=720, y=650)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            ax1.imshow(img, cmap='gray')

            ax1_value = fig.add_axes([0.12, 0.1, 0.78, 0.03])
            s_time = Slider(ax1_value, 'Brightness:', 0, 255, valinit=0,color='red')

            def DrawPlot():
                E11 = float(E1.get())
                q = E11 + img

                for i in range(img.shape[0]):
                    for j in range(img.shape[1]):
                        if q[i, j] > 255:
                            q[i, j] = 255

                ax1.imshow(q, cmap='gray')
                ax1.set_title(" Processed Image", fontsize=12, color="#333533")
                y = E11 + x
                p = str(E11)
                ax2.plot(x, y, label=p)
                ax2.legend(loc='upper left', prop={'size': 7}, bbox_to_anchor=(1, 1))

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Processed Image   ', padx=20, bd='5',
                                 command=SaveI)
                btnw.place(x=500, y=0)

                fig.canvas.draw_idle()

            L1 = tk.Label(root8, text="Brightness:", bg='#000000', fg='#b7f731', bd=5)
            L1.place(x=260, y=650)
            E1 = tk.Entry(root8, bd=5)
            E1.place(x=330, y=650)
            btn1 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Apply   ', padx=20, bd='1',
                             command=DrawPlot)
            btn1.place(x=460, y=650)

            def update(val):

                pos = float(s_time.val)
                q = pos + img

                for i in range(img.shape[0]):
                    for j in range(img.shape[1]):
                        if q[i, j] > 255:
                            q[i, j] = 255
                ax1.imshow(q, cmap='gray')
                ax1.set_title(" Processed Image", fontsize=12, color="#333533")
                y = pos + x
                p = str(pos)
                ax2.plot(x, y, label=p)
                ax2.legend(loc='upper left', prop={'size': 7}, bbox_to_anchor=(1, 1))

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Processed Image   ', padx=20, bd='5',
                                 command=SaveI)
                btnw.place(x=500, y=0)

                fig.canvas.draw_idle()

            x = np.arange(0, 256, 1)
            y = x
            ax2.plot(x, y)
            ax2.plot(x, y, label="c={0}".format(s_time.val))
            ax2.legend(loc='upper left', prop={'size': 7}, bbox_to_anchor=(1, 1))
            s_time.on_changed(update)
        else:
            img = Original_Image
            img = np.array(img)
            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            fig.subplots_adjust(bottom=0.25)

            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax2.set_facecolor("#2E2E2E")

            ax2.set_title(" Brightness", fontsize=12, color="#333533")
            ax1.set_title(" Original Image", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=720, y=650)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            ax1.imshow(img, cmap='gray')

            ax1_value = fig.add_axes([0.12, 0.1, 0.78, 0.03])
            s_time = Slider(ax1_value, 'Brightness:', 0, 255, valinit=0, color='red')

            def DrawPlot():
                E11 = float(E1.get())
                q = E11 + img

                for i in range(img.shape[0]):
                    for j in range(img.shape[1]):
                        if q[i, j] > 255:
                            q[i, j] = 255

                ax1.imshow(q, cmap='gray')
                ax1.set_title(" Processed Image", fontsize=12, color="#333533")
                y = E11 + x
                p = str(E11)
                ax2.plot(x, y, label=p)
                ax2.legend(loc='upper left', prop={'size': 7}, bbox_to_anchor=(1, 1))

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Processed Image   ', padx=20, bd='5',
                                 command=SaveI)
                btnw.place(x=500, y=0)

                fig.canvas.draw_idle()

            L1 = tk.Label(root8, text="Brightness:", bg='#000000', fg='#b7f731', bd=5)
            L1.place(x=260, y=650)
            E1 = tk.Entry(root8, bd=5)
            E1.place(x=330, y=650)
            btn1 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Apply   ', padx=20, bd='1',
                             command=DrawPlot)
            btn1.place(x=460, y=650)

            def update(val):

                pos = float(s_time.val)
                q = pos + img

                for i in range(img.shape[0]):
                    for j in range(img.shape[1]):
                        if q[i, j] > 255:
                            q[i, j] = 255
                ax1.imshow(q, cmap='gray')
                ax1.set_title(" Processed Image", fontsize=12, color="#333533")
                y = pos + x
                p = str(pos)
                ax2.plot(x, y, label=p)
                ax2.legend(loc='upper left', prop={'size': 7}, bbox_to_anchor=(1, 1))

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Processed Image   ', padx=20, bd='5',
                                 command=SaveI)
                btnw.place(x=500, y=0)

                fig.canvas.draw_idle()

            x = np.arange(0, 256, 1)
            y = x
            ax2.plot(x, y)
            ax2.plot(x, y, label="c={0}".format(s_time.val))
            ax2.legend(loc='upper left', prop={'size': 7}, bbox_to_anchor=(1, 1))
            s_time.on_changed(update)

    if len(Original_image_Size) > 2:
        Dimension_Number = []
        Dimension_Number_int = []
        for x1 in range(Original_Image.shape[2]):
            Dimension_Number_int.append(x1 + 1)
            Dimension_Number.append(("Band ", x1 + 1))

    else:
        Dimension_Number = [("Band", 1)]

    if len(Original_image_Size) > 2:
        ttk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = (Dimension_Number_int)
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        btn = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5',
                        command=Brightness1)
        btn.pack(anchor='w')

    else:
        tk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = "1"
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        btn1 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5',
                         command=Brightness1)
        btn1.pack(anchor='w')


    def Quit():
        root8.quit()
        root8.destroy()

    button = tk.Button(master=root8, bg='#000000', fg='#b7f731', text='       Quit        ', padx=20,
                       bd='5', command=Quit)
    button.pack(anchor='w')

    root8.mainloop()


def Tresholding():
    root8 = tk.Toplevel()
    root8.geometry("1800x900")
    root8.configure(background='white')
    root8.title("VNU - UET - GROUP 16 - NGUYEN KHAC KIEN, BUI DUC ANH, TRAN HOANG HUAN")

    frame1 = tk.Frame(
        master=root8,
        bg='#808000'
    )
    frame1.pack(anchor='w')
    editArea = tkst.ScrolledText(
        master=frame1,
        wrap=tk.WORD,
        width=20,
        height=10
    )
    # Don't use widget.place(), use pack or grid instead, since
    # They behave better on scaling the window -- and you don't
    # have to calculate it manually!
    editArea.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    editArea.configure(font=('Franklin Gothic Demi Cond', 11))
    # Adding some text, to see if scroll is working as we expect it
    editArea.insert(tk.INSERT,
                    """\
this menu returns Tresholded image. for using this option on the application at first you should select your special band from the "list top of the page" and then press "Select Band" button then You can use slider to treshold your image. if you want to save output image use the "Save Tresholded Image" botton.

                    """)


    def Tresholding1():
        if len(Original_image_Size) > 2:
            global imgT
            a_Tresholding = int(numberChosen1.get())
            imgT = Original_Image[:, :, a_Tresholding - 1]

            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)


            ax2.set_title(" Histogram", fontsize=12, color="#333533")

            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax2.set_facecolor("#2E2E2E")

            ax2.set_title("Histogram", fontsize=12, color="#333533")
            ax1.set_title("Original Image", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=720, y=650)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(imgT, cmap='gray')

            hist_img = cv2.calcHist([imgT], [0], None, [256], [0, 256])
            ax2.bar(range(256), hist_img.ravel(),color="#d1ae45",label="Band"+str(a_Tresholding)+"Histogram")



            ax2.axvline(x=0,label="Treshold", color='r')
            ax2.legend(loc='best')


            fig.canvas.draw_idle()

            ax1_value = fig.add_axes([0.12, 0.1, 0.78, 0.03])
            s_time = Slider(ax1_value, 'Tresholding:', 0, 255, valinit=0,color='r')

            def update(val):
                ax2.cla()

                hist_img = cv2.calcHist([imgT], [0], None, [256], [0, 256])
                a_Tresholding = int(numberChosen1.get())
                ax2.bar(range(256), hist_img.ravel(),color="#d1ae45",label="Band"+str(a_Tresholding)+"Histogram")
                ax2.axvline(x=int(s_time.val),label="Treshold", color='r')


                img = Original_Image[:, :, a_Tresholding - 1]
                img = np.array(img)
                for i in range(img.shape[0]):
                    for j in range(img.shape[1]):
                        if img[i, j] > s_time.val:
                            img[i, j] = 255
                        else:
                            img[i, j] = 0
                img3 = img
                ax1.imshow(img3, cmap='gray')

                ax2.set_title("Histogram", fontsize=12, color="#333533")
                ax1.set_title("Tresholding Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")
                ax2.legend(loc='best')

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', img3)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Tresholded Image   ', padx=20, bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)


                fig.canvas.draw_idle()

            s_time.on_changed(update)
        else:

            imgT = Original_Image

            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax2.set_title(" Histogram", fontsize=12, color="#333533")

            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax2.set_facecolor("#2E2E2E")

            ax2.set_title("Histogram", fontsize=12, color="#333533")
            ax1.set_title("Original Image", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=720, y=650)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(imgT, cmap='gray')

            hist_img = cv2.calcHist([imgT], [0], None, [256], [0, 256])
            ax2.bar(range(256), hist_img.ravel(), color="#d1ae45", label="Band" + str(1) + "Histogram")

            ax2.axvline(x=0, label="Treshold", color='r')
            ax2.legend(loc='best')

            fig.canvas.draw_idle()

            ax1_value = fig.add_axes([0.12, 0.1, 0.78, 0.03])
            s_time = Slider(ax1_value, 'Tresholding:', 0, 255, valinit=0, color='r')

            def update(val):
                ax2.cla()

                hist_img = cv2.calcHist([imgT], [0], None, [256], [0, 256])

                ax2.bar(range(256), hist_img.ravel(), color="#d1ae45", label="Band" + str(1) + "Histogram")
                ax2.axvline(x=int(s_time.val), label="Treshold", color='r')

                img = Original_Image
                img = np.array(img)
                for i in range(img.shape[0]):
                    for j in range(img.shape[1]):
                        if img[i, j] > s_time.val:
                            img[i, j] = 255
                        else:
                            img[i, j] = 0
                img3 = img
                ax1.imshow(img3, cmap='gray')

                ax2.set_title("Histogram", fontsize=12, color="#333533")
                ax1.set_title("Tresholding Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")
                ax2.legend(loc='best')

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', img3)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Tresholded Image   ', padx=20, bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                fig.canvas.draw_idle()

            s_time.on_changed(update)

    if len(Original_image_Size) > 2:
        Dimension_Number = []
        Dimension_Number_int = []
        for x1 in range(Original_Image.shape[2]):
            Dimension_Number_int.append(x1 + 1)
            Dimension_Number.append(("Band ", x1 + 1))

    else:
        Dimension_Number = [("Band", 1)]

    if len(Original_image_Size) > 2:
        ttk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = (Dimension_Number_int)
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        btn = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5',
                        command=Tresholding1)
        btn.pack(anchor='w')

    else:
        tk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = "1"
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        btn1 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5',
                         command=Tresholding1)
        btn1.pack(anchor='w')


    def Quit():
        root8.quit()
        root8.destroy()

    button = tk.Button(master=root8, bg='#000000', fg='#b7f731', text='       Quit        ', padx=20,
                       bd='5', command=Quit)
    button.pack(anchor='w')

    root8.mainloop()

# Code here
def Robertz():
    root8 = tk.Toplevel()
    root8.geometry("1800x900")
    root8.configure(background='white')
    root8.title("VNU - UET - GROUP 16 - NGUYEN KHAC KIEN, BUI DUC ANH, TRAN HOANG HUAN")

    frame1 = tk.Frame(
        master=root8,
        bg='#808000'
    )
    frame1.pack(anchor='w')
    editArea = tkst.ScrolledText(
        master=frame1,
        wrap=tk.WORD,
        width=20,
        height=10
    )
    # Don't use widget.place(), use pack or grid instead, since
    # They behave better on scaling the window -- and you don't
    # have to calculate it manually!
    editArea.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    editArea.configure(font=('Franklin Gothic Demi Cond', 11))
    # Adding some text, to see if scroll is working as we expect it
    editArea.insert(tk.INSERT,
                    """\
this menu use for Robertz filtering. for using this option on the application at first you should select your special band from the "list top of the page" and then press "Select Band" button or select all bands by press "All Bands" Button then You can use two Button "Filter in X Direcion" and "Filter in Y Direction" for Robertz filtering. if you want to save output image use the "Save Filtered Image" botton.

                    """)

    def Robertz1():
        if len(Original_image_Size) > 2:
            a_AverageFiltering = int(numberChosen1.get())
            img = Original_Image[:, :, a_AverageFiltering - 1]
            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax2.set_facecolor("#2E2E2E")

            ax1.set_title("Original Image", fontsize=12, color="#333533")
            ax2.set_title("Histogram", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=1000, y=650)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')

            def Robertz2():
                ax2.cla()

                kernel_3 = np.array([[-1, 0], [0, 1]])

                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel() , color="gold", label="Band" + str(a_AverageFiltering) + "Histogram")


                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)


                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            def Robertz4():
                ax2.cla()

                kernel_3 = np.array([[0, -1], [1, 0]])

                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(a_AverageFiltering) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            btn2 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Filter In X Direction   ', padx=20,
                             bd='1', command=Robertz2)
            btn2.place(x=530, y=650)
            btn3 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Filter in Y direction   ', padx=20, bd='1',
                             command=Robertz4)
            btn3.place(x=720, y=650)

            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
            ax2.plot(range(256), hist_img.ravel() , color="gold", label="Band" + str(a_AverageFiltering) + "Histogram")
            ax2.legend(loc='best')


        else:
            img = Original_Image
            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax2.set_facecolor("#2E2E2E")

            ax1.set_title("Original Image", fontsize=12, color="#333533")
            ax2.set_title("Histogram", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=1000, y=650)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')

            def Robertz2():
                ax2.cla()

                kernel_3 = np.array([[-1, 0], [0, 1]])

                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(1) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            def Robertz4():
                ax2.cla()

                kernel_3 = np.array([[0, -1], [1, 0]])

                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(1) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            btn2 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Filter In X Direction   ', padx=20,
                             bd='1', command=Robertz2)
            btn2.place(x=530, y=650)
            btn3 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Filter in Y direction   ', padx=20, bd='1',
                             command=Robertz4)
            btn3.place(x=720, y=650)

            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
            ax2.plot(range(256), hist_img.ravel(), color="gold", label="Band" + str(1) + "Histogram")
            ax2.legend(loc='best')

    if len(Original_image_Size) > 2:
        Dimension_Number = []
        Dimension_Number_int = []
        for x1 in range(Original_Image.shape[2]):
            Dimension_Number_int.append(x1 + 1)
            Dimension_Number.append(("Band ", x1 + 1))

    else:
        Dimension_Number = [("Band", 1)]

    if len(Original_image_Size) > 2:
        ttk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = (Dimension_Number_int)
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        if len(Original_image_Size) == 3:
            def RGBRobertz():
                img = Original_Image
                fig = plt.Figure(figsize=(13, 7))
                canvas = FigureCanvasTkAgg(fig, root8)
                canvas.get_tk_widget().place(x=200, y=0)

                ax1 = fig.add_subplot(121)
                ax2 = fig.add_subplot(122)

                ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
                ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

                ax2.set_facecolor("#2E2E2E")

                ax1.set_title("Original Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                toolbarFrame = tk.Frame(master=root8)
                toolbarFrame.place(x=1000, y=650)

                toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
                toolbar.update()

                def on_key_press(event):
                    print("you pressed {}".format(event.key))
                    key_press_handler(event, canvas, toolbar)

                canvas.mpl_connect("key_press_event", on_key_press)

                fig.subplots_adjust(bottom=0.25)

                ax1.imshow(img, cmap='gray')

                def Robertz2():
                    ax2.cla()
                    kernel_3 = np.array([[-1, 0], [0, 1]])

                    q = cv2.filter2D(img, -1, kernel_3)
                    ax1.imshow(q, cmap='gray')

                    hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                    hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                    hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                    hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_q.ravel(), color="gold", label="Filtered Image Histogram")

                    ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                    ax2.set_title("Histogram", fontsize=12, color="#333533")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                     bd='5',
                                     command=SaveI)
                    btnw.place(x=400, y=0)

                    ax2.legend(loc='best')
                    fig.canvas.draw_idle()

                def Robertz4():
                    ax2.cla()

                    kernel_3 = np.array([[0, -1], [1, 0]])

                    q = cv2.filter2D(img, -1, kernel_3)
                    ax1.imshow(q, cmap='gray')
                    hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                    hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                    hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                    hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_q.ravel(), color="gold", label="Filtered Image Histogram")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                     bd='5',
                                     command=SaveI)
                    btnw.place(x=400, y=0)

                    ax2.legend(loc='best')
                    fig.canvas.draw_idle()


                btn2 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Filter In X Direction   ', padx=20,
                                 bd='1', command=Robertz2)
                btn2.place(x=530, y=650)
                btn3 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Filter in Y direction   ', padx=20, bd='1',
                                 command=Robertz4)
                btn3.place(x=720, y=650)

                hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            btn = tk.Button(root8, bg='#000000', fg='#b7f731', text='   All Band   ', padx=20, bd='5',
                            command=RGBRobertz)
            btn.pack(anchor='w')
        btn = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5',
                        command=Robertz1)
        btn.pack(anchor='w')

    else:
        tk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = "1"
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        btn1 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5',
                         command=Robertz1)
        btn1.pack(anchor='w')



    def Quit():
        root8.quit()
        root8.destroy()

    button = tk.Button(master=root8, bg='#000000', fg='#b7f731', text='       Quit        ', padx=20,
                       bd='5', command=Quit)
    button.pack(anchor='w')


    root8.mainloop()


def Prewitt():
    root8 = tk.Toplevel()
    root8.geometry("1800x900")
    root8.configure(background='white')
    root8.title("VNU - UET - GROUP 16 - NGUYEN KHAC KIEN, BUI DUC ANH, TRAN HOANG HUAN")

    frame1 = tk.Frame(
        master=root8,
        bg='#808000'
    )
    frame1.pack(anchor='w')
    editArea = tkst.ScrolledText(
        master=frame1,
        wrap=tk.WORD,
        width=20,
        height=10
    )
    # Don't use widget.place(), use pack or grid instead, since
    # They behave better on scaling the window -- and you don't
    # have to calculate it manually!
    editArea.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    editArea.configure(font=('Franklin Gothic Demi Cond', 11))
    # Adding some text, to see if scroll is working as we expect it
    editArea.insert(tk.INSERT,
                    """\
this menu use for Prewitt filtering. for using this option on the application at first you should select your special band from the "list top of the page" and then press "Select Band" button or select all bands by press "All Bands" Button then You can use four Button "Horizontal" ,"Vertical" , "NE" and "NW" for Prewitt filtering. if you want to save output image use the "Save Filtered Image" botton.

                    """)

    def Prewitt1():
        if len(Original_image_Size) > 2:
            a_AverageFiltering = int(numberChosen1.get())
            img = Original_Image[:, :, a_AverageFiltering - 1]
            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax2.set_facecolor("#2E2E2E")

            ax1.set_title("Original Image", fontsize=12, color="#333533")
            ax2.set_title("Histogram", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=1000, y=650)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')

            def Prewitt2():
                ax2.cla()
                kernel_3 = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(a_AverageFiltering) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            def Prewitt4():
                ax2.cla()
                kernel_3 = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(a_AverageFiltering) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            def Prewitt5():
                ax2.cla()
                kernel_3 = np.array([[0, 1, 1], [-1, 0, 1], [-1, -1, 0]])
                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(a_AverageFiltering) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            def Prewitt6():
                ax2.cla()
                kernel_3 = np.array([[-1, -1, 0], [-1, 0, 1], [0, 1, 1]])
                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(a_AverageFiltering) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            btn2 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Horizontal   ', padx=20, bd='1',
                             command=Prewitt2)
            btn2.place(x=530, y=650)
            btn3 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Vertical   ', padx=20, bd='1',
                             command=Prewitt4)
            btn3.place(x=630, y=650)
            btn21 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   NE   ', padx=20, bd='1', command=Prewitt5)
            btn21.place(x=530, y=700)
            btn31 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   NW   ', padx=20, bd='1', command=Prewitt6)
            btn31.place(x=630, y=700)

            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
            ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(a_AverageFiltering) + "Histogram")
            ax2.legend(loc='best')
            fig.canvas.draw_idle()


        else:
            img = Original_Image
            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax2.set_facecolor("#2E2E2E")

            ax1.set_title("Original Image", fontsize=12, color="#333533")
            ax2.set_title("Histogram", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=1000, y=650)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')

            def Prewitt2():
                ax2.cla()
                kernel_3 = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(1) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            def Prewitt4():
                ax2.cla()
                kernel_3 = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(1) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            def Prewitt5():
                ax2.cla()
                kernel_3 = np.array([[0, 1, 1], [-1, 0, 1], [-1, -1, 0]])
                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(1) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            def Prewitt6():
                ax2.cla()
                kernel_3 = np.array([[-1, -1, 0], [-1, 0, 1], [0, 1, 1]])
                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(1) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            btn2 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Horizontal   ', padx=20, bd='1',
                             command=Prewitt2)
            btn2.place(x=530, y=650)
            btn3 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Vertical   ', padx=20, bd='1',
                             command=Prewitt4)
            btn3.place(x=630, y=650)
            btn21 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   NE   ', padx=20, bd='1', command=Prewitt5)
            btn21.place(x=530, y=700)
            btn31 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   NW   ', padx=20, bd='1', command=Prewitt6)
            btn31.place(x=630, y=700)

            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
            ax2.plot(range(256), hist_img.ravel(), color="gold",
                     label="Band" + str(1) + "Histogram")
            ax2.legend(loc='best')
            fig.canvas.draw_idle()

    if len(Original_image_Size) > 2:
        Dimension_Number = []
        Dimension_Number_int = []
        for x1 in range(Original_Image.shape[2]):
            Dimension_Number_int.append(x1 + 1)
            Dimension_Number.append(("Band ", x1 + 1))

    else:
        Dimension_Number = [("Band", 1)]

    if len(Original_image_Size) > 2:
        ttk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = (Dimension_Number_int)
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        if len(Original_image_Size) == 3:
            def RGBPrewitt():
                img = Original_Image
                fig = plt.Figure(figsize=(13, 7))
                canvas = FigureCanvasTkAgg(fig, root8)
                canvas.get_tk_widget().place(x=200, y=0)

                ax1 = fig.add_subplot(121)
                ax2 = fig.add_subplot(122)

                ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
                ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

                ax2.set_facecolor("#2E2E2E")

                ax1.set_title("Original Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                toolbarFrame = tk.Frame(master=root8)
                toolbarFrame.place(x=1000, y=650)

                toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
                toolbar.update()

                def on_key_press(event):
                    print("you pressed {}".format(event.key))
                    key_press_handler(event, canvas, toolbar)

                canvas.mpl_connect("key_press_event", on_key_press)


                fig.subplots_adjust(bottom=0.25)

                ax1.imshow(img, cmap='gray')

                def Prewitt2():
                    ax2.cla()
                    kernel_3 = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
                    q = cv2.filter2D(img, -1, kernel_3)
                    ax1.imshow(q, cmap='gray')
                    hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                    hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                    hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                    hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_q.ravel(), color="gold", label="Filtered Image Histogram")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                     bd='5',
                                     command=SaveI)
                    btnw.place(x=400, y=0)

                    ax2.legend(loc='best')
                    fig.canvas.draw_idle()

                def Prewitt4():
                    ax2.cla()
                    kernel_3 = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
                    q = cv2.filter2D(img, -1, kernel_3)
                    ax1.imshow(q, cmap='gray')
                    hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                    hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                    hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                    hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_q.ravel(), color="gold", label="Filtered Image Histogram")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                     bd='5',
                                     command=SaveI)
                    btnw.place(x=400, y=0)

                    ax2.legend(loc='best')
                    fig.canvas.draw_idle()

                def Prewitt5():
                    ax2.cla()
                    kernel_3 = np.array([[0, 1, 1], [-1, 0, 1], [-1, -1, 0]])
                    q = cv2.filter2D(img, -1, kernel_3)
                    ax1.imshow(q, cmap='gray')
                    hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                    hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                    hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                    hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_q.ravel(), color="gold", label="Filtered Image Histogram")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                     bd='5',
                                     command=SaveI)
                    btnw.place(x=400, y=0)

                    ax2.legend(loc='best')
                    fig.canvas.draw_idle()

                def Prewitt6():
                    ax2.cla()
                    kernel_3 = np.array([[-1, -1, 0], [-1, 0, 1], [0, 1, 1]])
                    q = cv2.filter2D(img, -1, kernel_3)
                    ax1.imshow(q, cmap='gray')
                    hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                    hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                    hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                    hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_q.ravel(), color="gold", label="Filtered Image Histogram")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                     bd='5',
                                     command=SaveI)
                    btnw.place(x=400, y=0)

                    ax2.legend(loc='best')
                    fig.canvas.draw_idle()

                btn2 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Horizontal   ', padx=20, bd='1',
                                 command=Prewitt2)
                btn2.place(x=530, y=650)
                btn3 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Vertical   ', padx=20, bd='1',
                                 command=Prewitt4)
                btn3.place(x=630, y=650)
                btn21 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   NE   ', padx=20, bd='1',
                                  command=Prewitt5)
                btn21.place(x=530, y=700)
                btn31 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   NW   ', padx=20, bd='1',
                                  command=Prewitt6)
                btn31.place(x=630, y=700)

                hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            btn = tk.Button(root8, bg='#000000', fg='#b7f731', text='   All Band   ', padx=20, bd='5',
                            command=RGBPrewitt)
            btn.pack(anchor='w')
        btn = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5',
                        command=Prewitt1)
        btn.pack(anchor='w')

    else:
        tk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = "1"
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        btn1 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5',
                         command=Prewitt1)
        btn1.pack(anchor='w')



    def Quit():
        root8.quit()
        root8.destroy()

    button = tk.Button(master=root8, bg='#000000', fg='#b7f731', text='       Quit        ', padx=20,
                       bd='5', command=Quit)
    button.pack(anchor='w')

    root8.mainloop()


def Sobel():
    root8 = tk.Toplevel()
    root8.geometry("1800x900")
    root8.configure(background='white')
    root8.title("VNU - UET - GROUP 16 - NGUYEN KHAC KIEN, BUI DUC ANH, TRAN HOANG HUAN")

    frame1 = tk.Frame(
        master=root8,
        bg='#808000'
    )
    frame1.pack(anchor='w')
    editArea = tkst.ScrolledText(
        master=frame1,
        wrap=tk.WORD,
        width=20,
        height=10
    )
    # Don't use widget.place(), use pack or grid instead, since
    # They behave better on scaling the window -- and you don't
    # have to calculate it manually!
    editArea.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    editArea.configure(font=('Franklin Gothic Demi Cond', 11))
    # Adding some text, to see if scroll is working as we expect it
    editArea.insert(tk.INSERT,
                    """\
this menu use for Sobel filtering. for using this option on the application at first you should select your special band from the "list top of the page" and then press "Select Band" button or select all bands by press "All Bands" Button then You can use four Button "Horizontal" ,"Vertical" , "NE" and "NW" for Sobel filtering. if you want to save output image use the "Save Filtered Image" botton.

                    """)


    def Sobel1():
        if len(Original_image_Size) > 2:
            a_AverageFiltering = int(numberChosen1.get())
            img = Original_Image[:, :, a_AverageFiltering - 1]
            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax2.set_facecolor("#2E2E2E")

            ax1.set_title("Original Image", fontsize=12, color="#333533")
            ax2.set_title("Histogram", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=1000, y=650)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)


            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')

            def Sobel2():
                ax2.cla()

                kernel_3 = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(a_AverageFiltering) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            def Sobel4():
                ax2.cla()

                kernel_3 = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])

                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(a_AverageFiltering) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            def Sobel5():
                ax2.cla()

                kernel_3 = np.array([[0, 1, 2], [-1, 0, 1], [-2, -1, 0]])

                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(a_AverageFiltering) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            def Sobel6():
                ax2.cla()

                kernel_3 = np.array([[-2, -1, 0], [-1, 0, 1], [0, 1, 2]])

                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(a_AverageFiltering) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            btn2 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Horizontal   ', padx=20, bd='1',
                             command=Sobel2)
            btn2.place(x=530, y=650)
            btn3 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Vertical   ', padx=20, bd='1',
                             command=Sobel4)
            btn3.place(x=630, y=650)
            btn21 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   NE   ', padx=20, bd='1', command=Sobel5)
            btn21.place(x=530, y=700)
            btn31 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   NW   ', padx=20, bd='1', command=Sobel6)
            btn31.place(x=630, y=700)

            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
            ax2.plot(range(256), hist_img.ravel(), color="gold",
                     label="Band" + str(a_AverageFiltering) + "Histogram")

            ax2.legend(loc='best')
            fig.canvas.draw_idle()


        else:
            img = Original_Image
            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax2.set_facecolor("#2E2E2E")

            ax1.set_title("Original Image", fontsize=12, color="#333533")
            ax2.set_title("Histogram", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=1000, y=650)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')

            def Sobel2():
                ax2.cla()

                kernel_3 = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(1) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            def Sobel4():
                ax2.cla()

                kernel_3 = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])

                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(1) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            def Sobel5():
                ax2.cla()

                kernel_3 = np.array([[0, 1, 2], [-1, 0, 1], [-2, -1, 0]])

                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(1) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            def Sobel6():
                ax2.cla()

                kernel_3 = np.array([[-2, -1, 0], [-1, 0, 1], [0, 1, 2]])

                q = cv2.filter2D(img, -1, kernel_3)
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(1) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            btn2 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Horizontal   ', padx=20, bd='1',
                             command=Sobel2)
            btn2.place(x=530, y=650)
            btn3 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Vertical   ', padx=20, bd='1',
                             command=Sobel4)
            btn3.place(x=630, y=650)
            btn21 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   NE   ', padx=20, bd='1', command=Sobel5)
            btn21.place(x=530, y=700)
            btn31 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   NW   ', padx=20, bd='1', command=Sobel6)
            btn31.place(x=630, y=700)

            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
            ax2.plot(range(256), hist_img.ravel(), color="gold",
                     label="Band" + str(1) + "Histogram")

            ax2.legend(loc='best')
            fig.canvas.draw_idle()

    if len(Original_image_Size) > 2:
        Dimension_Number = []
        Dimension_Number_int = []
        for x1 in range(Original_Image.shape[2]):
            Dimension_Number_int.append(x1 + 1)
            Dimension_Number.append(("Band ", x1 + 1))

    else:
        Dimension_Number = [("Band", 1)]

    if len(Original_image_Size) > 2:
        ttk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = (Dimension_Number_int)
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        if len(Original_image_Size) == 3:
            def RGBSobel():
                img = Original_Image
                fig = plt.Figure(figsize=(13, 7))
                canvas = FigureCanvasTkAgg(fig, root8)
                canvas.get_tk_widget().place(x=200, y=0)

                ax1 = fig.add_subplot(121)
                ax2 = fig.add_subplot(122)

                ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
                ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

                ax2.set_facecolor("#2E2E2E")

                ax1.set_title("Original Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                toolbarFrame = tk.Frame(master=root8)
                toolbarFrame.place(x=1000, y=650)

                toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
                toolbar.update()

                def on_key_press(event):
                    print("you pressed {}".format(event.key))
                    key_press_handler(event, canvas, toolbar)

                canvas.mpl_connect("key_press_event", on_key_press)

                fig.subplots_adjust(bottom=0.25)

                ax1.imshow(img, cmap='gray')

                def Sobel2():
                    ax2.cla()

                    kernel_3 = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

                    q = cv2.filter2D(img, -1, kernel_3)
                    ax1.imshow(q, cmap='gray')
                    hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                    hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                    hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                    hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_q.ravel(), color="gold", label="Filtered Image Histogram")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                     bd='5',
                                     command=SaveI)
                    btnw.place(x=400, y=0)

                    ax2.legend(loc='best')
                    fig.canvas.draw_idle()

                def Sobel4():
                    ax2.cla()

                    kernel_3 = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])

                    q = cv2.filter2D(img, -1, kernel_3)
                    ax1.imshow(q, cmap='gray')
                    hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                    hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                    hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                    hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_q.ravel(), color="gold", label="Filtered Image Histogram")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                     bd='5',
                                     command=SaveI)
                    btnw.place(x=400, y=0)

                    ax2.legend(loc='best')
                    fig.canvas.draw_idle()

                def Sobel5():
                    ax2.cla()

                    kernel_3 = np.array([[0, 1, 2], [-1, 0, 1], [-2, -1, 0]])

                    q = cv2.filter2D(img, -1, kernel_3)
                    ax1.imshow(q, cmap='gray')
                    hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                    hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                    hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                    hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_q.ravel(), color="gold", label="Filtered Image Histogram")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                     bd='5',
                                     command=SaveI)
                    btnw.place(x=400, y=0)

                    ax2.legend(loc='best')
                    fig.canvas.draw_idle()

                def Sobel6():
                    ax2.cla()

                    kernel_3 = np.array([[-2, -1, 0], [-1, 0, 1], [0, 1, 2]])

                    q = cv2.filter2D(img, -1, kernel_3)
                    ax1.imshow(q, cmap='gray')
                    hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                    hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                    hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                    hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_q.ravel(), color="gold", label="Filtered Image Histogram")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                     bd='5',
                                     command=SaveI)
                    btnw.place(x=400, y=0)

                    ax2.legend(loc='best')
                    fig.canvas.draw_idle()

                btn2 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Horizontal   ', padx=20, bd='1',
                                 command=Sobel2)
                btn2.place(x=530, y=650)
                btn3 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Vertical   ', padx=20, bd='1',
                                 command=Sobel4)
                btn3.place(x=630, y=650)
                btn21 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   NE   ', padx=20, bd='1',
                                  command=Sobel5)
                btn21.place(x=530, y=700)
                btn31 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   NW   ', padx=20, bd='1',
                                  command=Sobel6)
                btn31.place(x=630, y=700)

                hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            btn = tk.Button(root8, bg='#000000', fg='#b7f731', text='   All Band   ', padx=20, bd='5',
                            command=RGBSobel)
            btn.pack(anchor='w')
        btn = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5',
                        command=Sobel1)
        btn.pack(anchor='w')

    else:
        tk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = "1"
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        btn1 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5',
                         command=Sobel1)
        btn1.pack(anchor='w')


    def Quit():
        root8.quit()
        root8.destroy()

    button = tk.Button(master=root8, bg='#000000', fg='#b7f731', text='       Quit        ', padx=20,
                       bd='5', command=Quit)
    button.pack(anchor='w')

    root8.mainloop()


def USM():
    root8 = tk.Toplevel()
    root8.geometry("1800x900")
    root8.configure(background='white')
    root8.title("VNU - UET - GROUP 16 - NGUYEN KHAC KIEN, BUI DUC ANH, TRAN HOANG HUAN")

    frame1 = tk.Frame(
        master=root8,
        bg='#808000'
    )
    frame1.pack(anchor='w')
    editArea = tkst.ScrolledText(
        master=frame1,
        wrap=tk.WORD,
        width=20,
        height=10
    )
    # Don't use widget.place(), use pack or grid instead, since
    # They behave better on scaling the window -- and you don't
    # have to calculate it manually!
    editArea.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    editArea.configure(font=('Franklin Gothic Demi Cond', 11))
    # Adding some text, to see if scroll is working as we expect it
    editArea.insert(tk.INSERT,
                    """\
this menu use for Unsharp masking. for using this option on the application at first you should select your special band from the "list top of the page" and then press "Select Band" button or select all bands by press "All Bands" Button then You should enter kernel size in entry box and press "Apply" then control parameters by sliders. if you want to save output image use the "Save Filtered Image" botton.

                    """)


    def USM1():
        if len(Original_image_Size) > 2:
            a_USM = int(numberChosen1.get())
            img = Original_Image[:, :, a_USM - 1]
            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax2.set_facecolor("#2E2E2E")

            ax1.set_title("Original Image", fontsize=12, color="#333533")
            ax2.set_title("Histogram", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=1000, y=720)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')

            ax1_value = fig.add_axes([0.12, 0.04, 0.78, 0.03])
            ax2_value = fig.add_axes([0.12, 0.08, 0.78, 0.03])
            ax3_value = fig.add_axes([0.12, 0.12, 0.78, 0.03])
            s_time1 = Slider(ax1_value, 'K', 0, 30, valinit=0,color='r')
            s_time2 = Slider(ax2_value, 'Sigma X', 0, 30, valinit=0,color='g')
            s_time3 = Slider(ax3_value, 'Sigma Y', 0, 30, valinit=0,color='b')

            def USM3():
                global t1
                t1 = int(E1.get())

            def USM2(val):
                ax2.cla()
                b = cv2.GaussianBlur(img, (t1, t1), s_time2.val, s_time3.val)
                K = int(s_time1.val)
                gmask = img - b
                q = img + K * gmask
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(a_USM) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            L1 = tk.Label(root8, text="Kernel Size(odd number):", bg='#000000', fg='#b7f731', bd=5)
            L1.place(x=320, y=720)
            E1 = tk.Entry(root8, bd=5)
            E1.place(x=480, y=720)

            btn2 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Apply   ', padx=20, bd='1', command=USM3)
            btn2.place(x=630, y=720)

            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
            ax2.plot(range(256), hist_img.ravel(), color="gold",
                     label="Band" + str(a_USM) + "Histogram")
            ax2.legend(loc='best')
            fig.canvas.draw_idle()

            s_time1.on_changed(USM2)
            s_time2.on_changed(USM2)
            s_time3.on_changed(USM2)


        else:
            img = Original_Image
            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax2.set_facecolor("#2E2E2E")

            ax1.set_title("Original Image", fontsize=12, color="#333533")
            ax2.set_title("Histogram", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=1000, y=720)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')

            ax1_value = fig.add_axes([0.12, 0.04, 0.78, 0.03])
            ax2_value = fig.add_axes([0.12, 0.08, 0.78, 0.03])
            ax3_value = fig.add_axes([0.12, 0.12, 0.78, 0.03])
            s_time1 = Slider(ax1_value, 'K', 0, 30, valinit=0, color='r')
            s_time2 = Slider(ax2_value, 'Sigma X', 0, 30, valinit=0, color='g')
            s_time3 = Slider(ax3_value, 'Sigma Y', 0, 30, valinit=0, color='b')

            def USM3():
                global t1
                t1 = int(E1.get())

            def USM2(val):
                ax2.cla()
                b = cv2.GaussianBlur(img, (t1, t1), s_time2.val, s_time3.val)
                K = int(s_time1.val)
                gmask = img - b
                q = img + K * gmask
                ax1.imshow(q, cmap='gray')
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img.ravel(), color="gold",
                         label="Band" + str(1) + "Histogram")

                hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_q.ravel(), color="magenta", label="Filtered image Histogram")

                ax1.set_title("Filtered Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

            L1 = tk.Label(root8, text="Kernel Size(odd number):", bg='#000000', fg='#b7f731', bd=5)
            L1.place(x=320, y=720)
            E1 = tk.Entry(root8, bd=5)
            E1.place(x=480, y=720)

            btn2 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Apply   ', padx=20, bd='1', command=USM3)
            btn2.place(x=630, y=720)

            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
            ax2.plot(range(256), hist_img.ravel(), color="gold",
                     label="Band" + str(1) + "Histogram")
            ax2.legend(loc='best')
            fig.canvas.draw_idle()

            s_time1.on_changed(USM2)
            s_time2.on_changed(USM2)
            s_time3.on_changed(USM2)

    if len(np.shape(Original_Image)) > 2:
        Dimension_Number = []
        Dimension_Number_int = []
        for x1 in range(Original_Image.shape[2]):
            Dimension_Number_int.append(x1 + 1)
            Dimension_Number.append(("Band ", x1 + 1))

    else:
        Dimension_Number = [("Band", 1)]

    if len(Original_image_Size) > 2:
        ttk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = (Dimension_Number_int)
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        if len(Original_image_Size) == 3:
            def RGBUSM():
                img = Original_Image
                fig = plt.Figure(figsize=(13, 7))
                canvas = FigureCanvasTkAgg(fig, root8)
                canvas.get_tk_widget().place(x=200, y=0)

                ax1 = fig.add_subplot(121)
                ax2 = fig.add_subplot(122)

                ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
                ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

                ax2.set_facecolor("#2E2E2E")

                ax1.set_title("Original Image", fontsize=12, color="#333533")
                ax2.set_title("Histogram", fontsize=12, color="#333533")

                toolbarFrame = tk.Frame(master=root8)
                toolbarFrame.place(x=1000, y=720)

                toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
                toolbar.update()

                def on_key_press(event):
                    print("you pressed {}".format(event.key))
                    key_press_handler(event, canvas, toolbar)

                canvas.mpl_connect("key_press_event", on_key_press)


                fig.subplots_adjust(bottom=0.25)

                ax1.imshow(img, cmap='gray')

                ax1_value = fig.add_axes([0.12, 0.04, 0.78, 0.03])
                ax2_value = fig.add_axes([0.12, 0.08, 0.78, 0.03])
                ax3_value = fig.add_axes([0.12, 0.12, 0.78, 0.03])
                s_time1 = Slider(ax1_value, 'K', 0, 30, valinit=0, color='r')
                s_time2 = Slider(ax2_value, 'Sigma X', 0, 30, valinit=0, color='g')
                s_time3 = Slider(ax3_value, 'Sigma Y', 0, 30, valinit=0, color='b')

                def USM3():
                    global t1
                    t1 = int(E1.get())

                def USM2(val):
                    ax2.cla()
                    b = cv2.GaussianBlur(img, (t1, t1), s_time2.val, s_time3.val)
                    K = int(s_time1.val)
                    gmask = img - b
                    q = img + K * gmask
                    ax1.imshow(q, cmap='gray')
                    hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                    hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                    hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                    ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                    hist_q = cv2.calcHist([q], [0], None, [256], [0, 256])
                    ax2.plot(range(256), hist_q.ravel(), color="gold", label="Filtered Image Histogram")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Filtered Image   ', padx=20,
                                     bd='5',
                                     command=SaveI)
                    btnw.place(x=400, y=0)

                    ax2.legend(loc='best')
                    fig.canvas.draw_idle()

                L1 = tk.Label(root8, text="Kernel Size(odd number):", bg='#000000', fg='#b7f731', bd=5)
                L1.place(x=320, y=720)
                E1 = tk.Entry(root8, bd=5)
                E1.place(x=480, y=720)

                btn2 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Apply   ', padx=20, bd='1', command=USM3)
                btn2.place(x=630, y=720)

                hist_img0 = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.plot(range(256), hist_img0.ravel(), color="r", label="Band" + str(1) + "Histogram")
                hist_img1 = cv2.calcHist([img], [1], None, [256], [0, 256])
                ax2.plot(range(256), hist_img1.ravel(), color="g", label="Band" + str(2) + "Histogram")
                hist_img2 = cv2.calcHist([img], [2], None, [256], [0, 256])
                ax2.plot(range(256), hist_img2.ravel(), color="b", label="Band" + str(3) + "Histogram")

                ax2.legend(loc='best')
                fig.canvas.draw_idle()

                s_time1.on_changed(USM2)
                s_time2.on_changed(USM2)
                s_time3.on_changed(USM2)

            btn = tk.Button(root8, bg='#000000', fg='#b7f731', text='   All Band   ', padx=20, bd='5',
                            command=RGBUSM)
            btn.pack(anchor='w')
        btn = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5', command=USM1)
        btn.pack(anchor='w')

    else:
        tk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = "1"
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        btn1 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5', command=USM1)
        btn1.pack(anchor='w')


    def Quit():
        root8.quit()
        root8.destroy()

    button = tk.Button(master=root8, bg='#000000', fg='#b7f731', text='       Quit        ', padx=20,
                       bd='5', command=Quit)
    button.pack(anchor='w')

    root8.mainloop()


def SAP():
    root8 = tk.Toplevel()
    root8.geometry("1800x900")
    root8.configure(background='white')
    root8.title("VNU - UET - GROUP 16 - NGUYEN KHAC KIEN, BUI DUC ANH, TRAN HOANG HUAN")

    frame1 = tk.Frame(
        master=root8,
        bg='#808000'
    )
    frame1.pack(anchor='w')
    editArea = tkst.ScrolledText(
        master=frame1,
        wrap=tk.WORD,
        width=20,
        height=10
    )
    # Don't use widget.place(), use pack or grid instead, since
    # They behave better on scaling the window -- and you don't
    # have to calculate it manually!
    editArea.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    editArea.configure(font=('Franklin Gothic Demi Cond', 11))
    # Adding some text, to see if scroll is working as we expect it
    editArea.insert(tk.INSERT,
                    """\
this menu use for add nise to image. for using this option on the application at first you should select your special band from the "list top of the page" and then press "Select Band" button then You can control salt and pepper by slider. if you want to save noisy image you can use "save noisy image"
                    """)


    def SAP1():
        if len(Original_image_Size) > 2:
            a_SAP = int(numberChosen1.get())
            img = Original_Image[:, :, a_SAP - 1]
            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)



            ax1.set_title("Original Image", fontsize=12, color="#333533")
            ax2.set_title("Original Image", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=800, y=650)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')
            ax2.imshow(img,cmap='gray')


            ax1_value = fig.add_axes([0.12, 0.1, 0.78, 0.03])
            s_time1 = Slider(ax1_value, 'Salt:', 0, 1, valinit=0,color='r')

            channel_2 = np.atleast_1d(img)
            noisy = np.zeros_like(channel_2)

            def update(val):

                s_and_p = np.random.rand(img.shape[0], img.shape[1])
                salt = s_and_p > s_time1.val
                pepper = s_and_p < 1 - s_time1.val
                for i in range(channel_2.shape[0] * channel_2.shape[1]):
                    if salt.ravel()[i] == 1:
                        noisy.ravel()[i] = 255
                    elif pepper.ravel()[i] == 1:
                        noisy.ravel()[i] = 0
                    else:
                        noisy.ravel()[i] = channel_2.ravel()[i]

                ax2.imshow(noisy, cmap='gray')

                S = s_time1.val
                P = 1 - s_time1.val
                ax1.set_title("Original Image", fontsize=12, color="#333533")
                ax2.set_title("Noisy Image(Salt="+str(S)+",Pepper="+str(P), fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', noisy)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Noisy Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=1000, y=0)

                fig.canvas.draw_idle()

            s_time1.on_changed(update)


        else:
            img = Original_Image
            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax1.set_title("Original Image", fontsize=12, color="#333533")
            ax2.set_title("Original Image", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=800, y=650)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')
            ax2.imshow(img, cmap='gray')

            ax1_value = fig.add_axes([0.12, 0.1, 0.78, 0.03])
            s_time1 = Slider(ax1_value, 'Salt:', 0, 1, valinit=0, color='r')

            channel_2 = np.atleast_1d(img)
            noisy = np.zeros_like(channel_2)

            def update(val):

                s_and_p = np.random.rand(img.shape[0], img.shape[1])
                salt = s_and_p > s_time1.val
                pepper = s_and_p < 1 - s_time1.val
                for i in range(channel_2.shape[0] * channel_2.shape[1]):
                    if salt.ravel()[i] == 1:
                        noisy.ravel()[i] = 255
                    elif pepper.ravel()[i] == 1:
                        noisy.ravel()[i] = 0
                    else:
                        noisy.ravel()[i] = channel_2.ravel()[i]

                ax2.imshow(noisy, cmap='gray')

                S = s_time1.val
                P = 1 - s_time1.val
                ax1.set_title("Original Image", fontsize=12, color="#333533")
                ax2.set_title("Noisy Image(Salt=" + str(S) + ",Pepper=" + str(P), fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', noisy)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Noisy Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=1000, y=0)

                fig.canvas.draw_idle()

            s_time1.on_changed(update)

    if len(Original_image_Size) > 2:
        Dimension_Number = []
        Dimension_Number_int = []
        for x1 in range(Original_Image.shape[2]):
            Dimension_Number_int.append(x1 + 1)
            Dimension_Number.append(("Band ", x1 + 1))

    else:
        Dimension_Number = [("Band", 1)]

    if len(Original_image_Size) > 2:
        ttk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = (Dimension_Number_int)
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)

        btn = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5', command=SAP1)
        btn.pack(anchor='w')

    else:
        tk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = "1"
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        btn1 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5', command=SAP1)
        btn1.pack(anchor='w')





    def Quit():
        root8.quit()
        root8.destroy()

    button = tk.Button(master=root8, bg='#000000', fg='#b7f731', text='       Quit        ', padx=20,
                       bd='5', command=Quit)
    button.pack(anchor='w')

    root8.mainloop()


def GNoise():
    root8 = tk.Toplevel()
    root8.geometry("1800x900")
    root8.configure(background='white')
    root8.title("VNU - UET - GROUP 16 - NGUYEN KHAC KIEN, BUI DUC ANH, TRAN HOANG HUAN")

    frame1 = tk.Frame(
        master=root8,
        bg='#808000'
    )
    frame1.pack(anchor='w')
    editArea = tkst.ScrolledText(
        master=frame1,
        wrap=tk.WORD,
        width=20,
        height=10
    )
    # Don't use widget.place(), use pack or grid instead, since
    # They behave better on scaling the window -- and you don't
    # have to calculate it manually!
    editArea.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    editArea.configure(font=('Franklin Gothic Demi Cond', 11))
    # Adding some text, to see if scroll is working as we expect it
    editArea.insert(tk.INSERT,
                    """\
this menu use for add nise to image. for using this option on the application at first you should select your special band from the "list top of the page" and then press "Select Band" button then You can control gaussian noise parameters by sliders. if you want to save noisy image you can use "save noisy image"
                    """)

    def GNoise1():
        if len(Original_image_Size) > 2:
            a_GNoise = int(numberChosen1.get())
            img = Original_Image[:, :, a_GNoise - 1]
            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax1.set_title("Original Image", fontsize=12, color="#333533")
            ax2.set_title("Original Image", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=800, y=720)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)


            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')
            ax2.imshow(img, cmap='gray')

            ax1_value = fig.add_axes([0.12, 0.1, 0.78, 0.03])
            s_time1 = Slider(ax1_value, 'Mean:', 0, 200, valinit=0,color='r')

            ax2_value = fig.add_axes([0.12, 0.05, 0.78, 0.03])
            s_time2 = Slider(ax2_value, 'Sigma:', 0, 200, valinit=0,color='g')

            def update(val):

                gauss_noise = np.random.normal(s_time1.val, s_time2.val, (img.shape[0], img.shape[1]))

                g_noisy = img + gauss_noise

                ax2.imshow(g_noisy, cmap='gray')

                ax1.set_title("Original Image", fontsize=12, color="#333533")
                ax2.set_title("Noisy Image", fontsize=12, color="#333533")


                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', g_noisy)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Noisy   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=1000, y=0)

                fig.canvas.draw_idle()

            s_time1.on_changed(update)
            s_time2.on_changed(update)


        else:
            img = Original_Image
            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax1.set_title("Original Image", fontsize=12, color="#333533")
            ax2.set_title("Original Image", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=800, y=720)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')
            ax2.imshow(img, cmap='gray')

            ax1_value = fig.add_axes([0.12, 0.1, 0.78, 0.03])
            s_time1 = Slider(ax1_value, 'Mean:', 0, 200, valinit=0, color='r')

            ax2_value = fig.add_axes([0.12, 0.05, 0.78, 0.03])
            s_time2 = Slider(ax2_value, 'Sigma:', 0, 200, valinit=0, color='g')

            def update(val):

                gauss_noise = np.random.normal(s_time1.val, s_time2.val, (img.shape[0], img.shape[1]))

                g_noisy = img + gauss_noise

                ax2.imshow(g_noisy, cmap='gray')

                ax1.set_title("Original Image", fontsize=12, color="#333533")
                ax2.set_title("Noisy Image", fontsize=12, color="#333533")

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', g_noisy)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Noisy Image   ', padx=20,
                                 bd='5',
                                 command=SaveI)
                btnw.place(x=1000, y=0)

                fig.canvas.draw_idle()

            s_time1.on_changed(update)
            s_time2.on_changed(update)

    if len(Original_image_Size) > 2:
        Dimension_Number = []
        Dimension_Number_int = []
        for x1 in range(Original_Image.shape[2]):
            Dimension_Number_int.append(x1 + 1)
            Dimension_Number.append(("Band ", x1 + 1))

    else:
        Dimension_Number = [("Band", 1)]

    if len(Original_image_Size) > 2:
        ttk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = (Dimension_Number_int)
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        btn = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5',
                        command=GNoise1)
        btn.pack(anchor='w')

    else:
        tk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = "1"
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        btn1 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5',
                         command=GNoise1)
        btn1.pack(anchor='w')


    def Quit():
        root8.quit()
        root8.destroy()

    button = tk.Button(master=root8, bg='#000000', fg='#b7f731', text='       Quit        ', padx=20,
                       bd='5', command=Quit)
    button.pack(anchor='w')

    root8.mainloop()

#Code here
def Canny():
    root8 = tk.Toplevel()
    root8.geometry("1800x900")
    root8.configure(background='white')
    root8.title("VNU - UET - GROUP 16 - NGUYEN KHAC KIEN, BUI DUC ANH, TRAN HOANG HUAN")

    frame1 = tk.Frame(
        master=root8,
        bg='#808000'
    )
    frame1.pack(anchor='w')
    editArea = tkst.ScrolledText(
        master=frame1,
        wrap=tk.WORD,
        width=20,
        height=10
    )
    # Don't use widget.place(), use pack or grid instead, since
    # They behave better on scaling the window -- and you don't
    # have to calculate it manually!
    editArea.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    editArea.configure(font=('Franklin Gothic Demi Cond', 11))
    # Adding some text, to see if scroll is working as we expect it
    editArea.insert(tk.INSERT,
                    """\
this menu use for Image segmantation. for using this option on the application at first you should select your special band from the "list top of the page" and then press "Select Band" button then you can control Canny Parametrs by sliders. if you want to save output image you can use "save  Segmented Image" button.
                    """)



    def Canny1():
        if len(Original_image_Size) > 2:
            a_Canny = int(numberChosen1.get())
            img = Original_Image[:, :, a_Canny - 1]
            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)



            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax2.set_facecolor("#2E2E2E")

            ax2.set_title("Histogram", fontsize=12, color="#333533")
            ax1.set_title("Original Image", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=720, y=670)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)


            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')

            ax1_value = fig.add_axes([0.12, 0.1, 0.78, 0.03])
            ax2_value = fig.add_axes([0.12, 0.05, 0.78, 0.03])

            s_time1 = Slider(ax1_value, 'Minimum Value', 0, np.max(img), valinit=0, color='r')
            s_time2 = Slider(ax2_value, 'Maximum Value', 0, np.max(img), valinit=0, color='g')



            def Canny2(val):
                ax2.cla()
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.bar(range(256), hist_img.ravel(),color="#d1ae45",label="Band"+str(a_Canny)+"Histogram")

                ax2.axvline(x=int(s_time1.val), color='r',label="Minimum")
                ax2.axvline(x=int(s_time2.val), color='g',label="Maximum")

                ax2.legend(loc='best')

                q = cv2.Canny(img, int(s_time1.val), int(s_time2.val))
                ax1.imshow(q, cmap='gray')





                ax2.set_title("Histogram", fontsize=12, color="#333533")
                ax1.set_title("Segmented Image", fontsize=12, color="#333533")

                fig.canvas.draw_idle()

            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
            ax2.bar(range(256), hist_img.ravel(),color="#d1ae45",label="Band"+str(a_Canny)+"Histogram")

            ax2.legend(loc='best')

            def SaveI():
                f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                if f is None:
                    return

                filename = f.name

                cv2.imwrite(str(filename) + '.jpg', q)
                f.close()

            btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Segmented Image   ', padx=20, bd='5',
                             command=SaveI)
            btnw.place(x=400, y=0)

            s_time1.on_changed(Canny2)
            s_time2.on_changed(Canny2)



        else:
            img = Original_Image
            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax2.set_facecolor("#2E2E2E")

            ax2.set_title("Histogram", fontsize=12, color="#333533")
            ax1.set_title("Original Image", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=720, y=670)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')

            ax1_value = fig.add_axes([0.12, 0.1, 0.78, 0.03])
            ax2_value = fig.add_axes([0.12, 0.05, 0.78, 0.03])

            s_time1 = Slider(ax1_value, 'Minimum Value', 0, np.max(img), valinit=0, color='r')
            s_time2 = Slider(ax2_value, 'Maximum Value', 0, np.max(img), valinit=0, color='g')

            def Canny2(val):
                ax2.cla()
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.bar(range(256), hist_img.ravel(), color="#d1ae45", label="Band" + str(1) + "Histogram")

                ax2.axvline(x=int(s_time1.val), color='r', label="Minimum")
                ax2.axvline(x=int(s_time2.val), color='g', label="Maximum")

                ax2.legend(loc='best')

                q = cv2.Canny(img, int(s_time1.val), int(s_time2.val))
                ax1.imshow(q, cmap='gray')
                global q1
                q1=q

                ax2.set_title("Histogram", fontsize=12, color="#333533")
                ax1.set_title("Segmented Image", fontsize=12, color="#333533")

                fig.canvas.draw_idle()

            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
            ax2.bar(range(256), hist_img.ravel(), color="#d1ae45", label="Band" + str(1) + "Histogram")

            ax2.legend(loc='best')

            def SaveI():
                f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                if f is None:
                    return

                filename = f.name

                cv2.imwrite(str(filename) + '.jpg', q1)
                f.close()

            btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Segmented Image   ', padx=20, bd='5',
                             command=SaveI)
            btnw.place(x=400, y=0)

            s_time1.on_changed(Canny2)
            s_time2.on_changed(Canny2)

    if len(Original_image_Size) > 2:
        Dimension_Number = []
        Dimension_Number_int = []
        for x1 in range(Original_Image.shape[2]):
            Dimension_Number_int.append(x1 + 1)
            Dimension_Number.append(("Band ", x1 + 1))

    else:
        Dimension_Number = [("Band", 1)]

    if len(Original_image_Size) > 2:
        ttk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = (Dimension_Number_int)
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)

        btn = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5',
                        command=Canny1)
        btn.pack(anchor='w')

    else:
        tk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = "1"
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        btn1 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5',
                         command=Canny1)
        btn1.pack(anchor='w')

    def Quit():
        root8.quit()
        root8.destroy()

    button = tk.Button(master=root8, bg='#000000', fg='#b7f731', text='       Quit        ', padx=20,
                       bd='5', command=Quit)
    button.pack(anchor='w')

    root8.mainloop()


def AT():
    root8 = tk.Toplevel()
    root8.geometry("1800x900")
    root8.configure(background='white')
    root8.title("VNU - UET - GROUP 16 - NGUYEN KHAC KIEN, BUI DUC ANH, TRAN HOANG HUAN")

    frame1 = tk.Frame(
        master=root8,
        bg='#808000'
    )
    frame1.pack(anchor='w')
    editArea = tkst.ScrolledText(
        master=frame1,
        wrap=tk.WORD,
        width=20,
        height=10
    )
    # Don't use widget.place(), use pack or grid instead, since
    # They behave better on scaling the window -- and you don't
    # have to calculate it manually!
    editArea.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    editArea.configure(font=('Franklin Gothic Demi Cond', 11))
    # Adding some text, to see if scroll is working as we expect it
    editArea.insert(tk.INSERT,
                    """\
this menu use for image segmentation. for using this option on the application at first you should select your special band from the "list top of the page" and then press "Select Band" button then appears two buttons that specific that kind of tresholding select one of them and enter block size and then you can control tresholding parameters ny sliders. if you want to save output image you can use "save  segmented Image" button.
                    """)



    def AT1():
        if len(Original_image_Size) > 2:
            a_AT = int(numberChosen1.get())
            img = Original_Image[:, :, a_AT - 1]

            def BT():
                fig = plt.Figure(figsize=(13, 7))
                canvas = FigureCanvasTkAgg(fig, root8)
                canvas.get_tk_widget().place(x=200, y=0)

                ax1 = fig.add_subplot(121)
                ax2 = fig.add_subplot(122)

                ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
                ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

                ax2.set_facecolor("#2E2E2E")

                ax2.set_title("Histogram", fontsize=12, color="#333533")
                ax1.set_title("Original Image", fontsize=12, color="#333533")

                toolbarFrame = tk.Frame(master=root8)
                toolbarFrame.place(x=720, y=700)

                toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
                toolbar.update()

                def on_key_press(event):
                    print("you pressed {}".format(event.key))
                    key_press_handler(event, canvas, toolbar)

                canvas.mpl_connect("key_press_event", on_key_press)

                fig.subplots_adjust(bottom=0.25)

                ax1.imshow(img, cmap='gray')

                ax1_value = fig.add_axes([0.12, 0.1, 0.78, 0.03])
                ax2_value = fig.add_axes([0.12, 0.05, 0.78, 0.03])

                s_time1 = Slider(ax1_value, 'Constant', 0, 20, valinit=1,color='r')
                s_time2 = Slider(ax2_value, 'Maximum Value', 0, np.max(img), valinit=0,color='g')

                def Canny2(val):
                    ax2.cla()
                    hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.bar(range(256), hist_img.ravel(), color="#d1ae45",
                            label="Band" + str(a_AT) + "Histogram")
                    ax2.axvline(x=int(s_time2.val), color='r',label="Maximum")
                    ax2.legend(loc='best')

                    q = cv2.adaptiveThreshold(img, int(s_time2.val), cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,
                                              int(E1.get()), int(s_time1.val))
                    ax1.imshow(q, cmap='gray')
                    ax1.set_title("Segmented Image")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Segmented Image   ', padx=20, bd='5',
                                     command=SaveI)
                    btnw.place(x=400, y=0)

                    fig.canvas.draw_idle()

                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.bar(range(256), hist_img.ravel(), color="#d1ae45",
                        label="Band" + str(a_AT) + "Histogram")

                L1 = tk.Label(root8, text="Block Size(Odd Number):", bg='#000000', fg='#b7f731', bd=5)
                L1.place(x=230, y=700)
                E1 = tk.Entry(root8, bd=5)
                E1.place(x=360, y=700)

                s_time1.on_changed(Canny2)
                s_time2.on_changed(Canny2)

            def BTI():
                fig = plt.Figure(figsize=(13, 7))
                canvas = FigureCanvasTkAgg(fig, root8)
                canvas.get_tk_widget().place(x=200, y=0)

                ax1 = fig.add_subplot(121)
                ax2 = fig.add_subplot(122)

                ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
                ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

                ax2.set_facecolor("#2E2E2E")

                ax2.set_title("Histogram", fontsize=12, color="#333533")
                ax1.set_title("Original Image", fontsize=12, color="#333533")

                toolbarFrame = tk.Frame(master=root8)
                toolbarFrame.place(x=720, y=700)

                toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
                toolbar.update()

                def on_key_press(event):
                    print("you pressed {}".format(event.key))
                    key_press_handler(event, canvas, toolbar)

                canvas.mpl_connect("key_press_event", on_key_press)

                fig.subplots_adjust(bottom=0.25)

                ax1.imshow(img, cmap='gray')

                ax1_value = fig.add_axes([0.12, 0.1, 0.78, 0.03])
                ax2_value = fig.add_axes([0.12, 0.05, 0.78, 0.03])

                s_time1 = Slider(ax1_value, 'Constant', 0, 20, valinit=1, color='r')
                s_time2 = Slider(ax2_value, 'Maximum Value', 0, np.max(img), valinit=0, color='g')


                def Canny2(val):
                    ax2.cla()
                    hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.bar(range(256), hist_img.ravel(), color="#d1ae45",
                            label="Band" + str(a_AT) + "Histogram")
                    ax2.axvline(x=int(s_time2.val), color='r', label="Maximum")
                    ax2.legend(loc='best')

                    q = cv2.adaptiveThreshold(img, int(s_time2.val), cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                              cv2.THRESH_BINARY, int(E1.get()), int(s_time1.val))
                    ax1.imshow(q, cmap='gray')
                    ax1.set_title("Segmented Image")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Segmented Image   ', padx=20,
                                     bd='5',
                                     command=SaveI)
                    btnw.place(x=400, y=0)


                    fig.canvas.draw_idle()

                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.bar(range(256), hist_img.ravel(), color="#d1ae45",
                        label="Band" + str(a_AT) + "Histogram")

                L1 = tk.Label(root8, text="Block Size(Odd Number):", bg='#000000', fg='#b7f731', bd=5)
                L1.place(x=230, y=700)
                E1 = tk.Entry(root8, bd=5)
                E1.place(x=360, y=700)

                s_time1.on_changed(Canny2)
                s_time2.on_changed(Canny2)

            btn5 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Mean Treshold Adaptive   ', padx=20,
                             bd='5', command=BT)
            btn5.place(x=0, y=100)
            btn6 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Gaussian Treshold Adaptive   ', padx=20,
                             bd='5', command=BTI)
            btn6.place(x=0, y=130)


        else:
            img = Original_Image

            def BT():
                fig = plt.Figure(figsize=(13, 7))
                canvas = FigureCanvasTkAgg(fig, root8)
                canvas.get_tk_widget().place(x=200, y=0)

                ax1 = fig.add_subplot(121)
                ax2 = fig.add_subplot(122)

                ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
                ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

                ax2.set_facecolor("#2E2E2E")

                ax2.set_title("Histogram", fontsize=12, color="#333533")
                ax1.set_title("Original Image", fontsize=12, color="#333533")

                toolbarFrame = tk.Frame(master=root8)
                toolbarFrame.place(x=720, y=700)

                toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
                toolbar.update()

                def on_key_press(event):
                    print("you pressed {}".format(event.key))
                    key_press_handler(event, canvas, toolbar)

                canvas.mpl_connect("key_press_event", on_key_press)

                fig.subplots_adjust(bottom=0.25)

                ax1.imshow(img, cmap='gray')

                ax1_value = fig.add_axes([0.12, 0.1, 0.78, 0.03])
                ax2_value = fig.add_axes([0.12, 0.05, 0.78, 0.03])

                s_time1 = Slider(ax1_value, 'Constant', 0, 20, valinit=1, color='r')
                s_time2 = Slider(ax2_value, 'Maximum Value', 0, np.max(img), valinit=0, color='g')

                def Canny2(val):
                    ax2.cla()
                    hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.bar(range(256), hist_img.ravel(), color="#d1ae45",
                            label="Band" + str(1) + "Histogram")
                    ax2.axvline(x=int(s_time2.val), color='r', label="Maximum")
                    ax2.legend(loc='best')

                    q = cv2.adaptiveThreshold(img, int(s_time2.val), cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,
                                              int(E1.get()), int(s_time1.val))
                    ax1.imshow(q, cmap='gray')
                    ax1.set_title("Segmented Image")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Segmented Image   ', padx=20,
                                     bd='5',
                                     command=SaveI)
                    btnw.place(x=400, y=0)

                    fig.canvas.draw_idle()

                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.bar(range(256), hist_img.ravel(), color="#d1ae45",
                        label="Band" + str(1) + "Histogram")

                L1 = tk.Label(root8, text="Block Size(Odd Number):", bg='#000000', fg='#b7f731', bd=5)
                L1.place(x=230, y=700)
                E1 = tk.Entry(root8, bd=5)
                E1.place(x=360, y=700)

                s_time1.on_changed(Canny2)
                s_time2.on_changed(Canny2)

            def BTI():
                fig = plt.Figure(figsize=(13, 7))
                canvas = FigureCanvasTkAgg(fig, root8)
                canvas.get_tk_widget().place(x=200, y=0)

                ax1 = fig.add_subplot(121)
                ax2 = fig.add_subplot(122)

                ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
                ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

                ax2.set_facecolor("#2E2E2E")

                ax2.set_title("Histogram", fontsize=12, color="#333533")
                ax1.set_title("Original Image", fontsize=12, color="#333533")

                toolbarFrame = tk.Frame(master=root8)
                toolbarFrame.place(x=720, y=700)

                toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
                toolbar.update()

                def on_key_press(event):
                    print("you pressed {}".format(event.key))
                    key_press_handler(event, canvas, toolbar)

                canvas.mpl_connect("key_press_event", on_key_press)

                fig.subplots_adjust(bottom=0.25)

                ax1.imshow(img, cmap='gray')

                ax1_value = fig.add_axes([0.12, 0.1, 0.78, 0.03])
                ax2_value = fig.add_axes([0.12, 0.05, 0.78, 0.03])

                s_time1 = Slider(ax1_value, 'Constant', 0, 20, valinit=1, color='r')
                s_time2 = Slider(ax2_value, 'Maximum Value', 0, np.max(img), valinit=0, color='g')

                def Canny2(val):
                    ax2.cla()
                    hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                    ax2.bar(range(256), hist_img.ravel(), color="#d1ae45",
                            label="Band" + str(1) + "Histogram")
                    ax2.axvline(x=int(s_time2.val), color='r', label="Maximum")
                    ax2.legend(loc='best')

                    q = cv2.adaptiveThreshold(img, int(s_time2.val), cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                              cv2.THRESH_BINARY, int(E1.get()), int(s_time1.val))
                    ax1.imshow(q, cmap='gray')
                    ax1.set_title("Segmented Image")

                    def SaveI():
                        f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                        if f is None:
                            return

                        filename = f.name

                        cv2.imwrite(str(filename) + '.jpg', q)
                        f.close()

                    btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Segmented Image   ', padx=20,
                                     bd='5',
                                     command=SaveI)
                    btnw.place(x=400, y=0)

                    fig.canvas.draw_idle()

                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.bar(range(256), hist_img.ravel(), color="#d1ae45",
                        label="Band" + str(1) + "Histogram")

                L1 = tk.Label(root8, text="Block Size(Odd Number):", bg='#000000', fg='#b7f731', bd=5)
                L1.place(x=230, y=700)
                E1 = tk.Entry(root8, bd=5)
                E1.place(x=360, y=700)

                s_time1.on_changed(Canny2)
                s_time2.on_changed(Canny2)

            btn5 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Mean Treshold Adaptive   ', padx=20,
                             bd='5', command=BT)
            btn5.place(x=0, y=100)
            btn6 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Gaussian Treshold Adaptive   ', padx=20,
                             bd='5', command=BTI)
            btn6.place(x=0, y=130)

    if len(Original_image_Size) > 2:
        Dimension_Number = []
        Dimension_Number_int = []
        for x1 in range(Original_Image.shape[2]):
            Dimension_Number_int.append(x1 + 1)
            Dimension_Number.append(("Band ", x1 + 1))

    else:
        Dimension_Number = [("Band", 1)]

    if len(Original_image_Size) > 2:
        ttk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = (Dimension_Number_int)
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)

        btn = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5', command=AT1)
        btn.pack(anchor='w')

    else:
        tk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = "1"
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        btn1 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5', command=AT1)
        btn1.pack(anchor='w')



    def Quit():
        root8.quit()
        root8.destroy()

    button = tk.Button(master=root8, bg='#000000', fg='#b7f731', text='       Quit        ', padx=20,
                       bd='5', command=Quit)
    button.pack(anchor='w')


    root8.mainloop()


def OT():
    root8 = tk.Toplevel()
    root8.geometry("1800x900")
    root8.configure(background='white')
    root8.title("VNU - UET - GROUP 16 - NGUYEN KHAC KIEN, BUI DUC ANH, TRAN HOANG HUAN")

    frame1 = tk.Frame(
        master=root8,
        bg='#808000'
    )
    frame1.pack(anchor='w')
    editArea = tkst.ScrolledText(
        master=frame1,
        wrap=tk.WORD,
        width=20,
        height=10
    )
    # Don't use widget.place(), use pack or grid instead, since
    # They behave better on scaling the window -- and you don't
    # have to calculate it manually!
    editArea.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    editArea.configure(font=('Franklin Gothic Demi Cond', 11))
    # Adding some text, to see if scroll is working as we expect it
    editArea.insert(tk.INSERT,
                    """\
this menu use for image segmentation. for using this option on the application at first you should select your special band from the "list top of the page" and then press "Select Band" button then enter block size and then you can control tresholding parameters by sliders. if you want to save output image you can use "save  segmented Image" button.
                    """)



    def OT1():
        if len(Original_image_Size) > 2:
            a_OT = int(numberChosen1.get())
            img = Original_Image[:, :, a_OT - 1]

            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

            ax2.set_facecolor("#2E2E2E")

            ax2.set_title("Histogram", fontsize=12, color="#333533")
            ax1.set_title("Original Image", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=720, y=720)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)


            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')

            ax1_value = fig.add_axes([0.12, 0.1, 0.78, 0.03])
            ax2_value = fig.add_axes([0.12, 0.05, 0.78, 0.03])

            s_time1 = Slider(ax1_value, 'Minimum Value', 0, np.max(img), valinit=0,color='r')
            s_time2 = Slider(ax2_value, 'Maximum Value', 0, np.max(img), valinit=0,color='g')

            def Canny2(val):
                ax2.cla()
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.bar(range(256), hist_img.ravel(),color="#d1ae45",label="Band"+str(a_OT)+"Histogram")
                ax2.axvline(x=int(s_time2.val), color='g',label="Maximum")
                ax2.axvline(x=int(s_time1.val), color='r', label="Minimum")

                blur = cv2.GaussianBlur(img, (int(E1.get()), int(E1.get())), 0)
                ret3, q = cv2.threshold(blur, int(s_time1.val), int(s_time2.val),
                                        cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                ax2.set_title("Histogram", fontsize=12, color="#333533")
                ax1.set_title("Treshhold Image", fontsize=12, color="#333533")

                ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
                ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

                ax1.imshow(q, cmap='gray')

                ax2.legend(loc='best')

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Invert Image   ', padx=20, bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                fig.canvas.draw_idle()

            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
            ax2.bar(range(256), hist_img.ravel(),color="#d1ae45",label="Band"+str(a_OT)+"Histogram")
            ax2.legend(loc='best')


            L1 = tk.Label(root8, text="Block Size(Odd Number):", bg='#000000', fg='#b7f731', bd=5)
            L1.place(x=200, y=720)
            E1 = tk.Entry(root8, bd=5)
            E1.place(x=330, y=720)

            s_time1.on_changed(Canny2)
            s_time2.on_changed(Canny2)




        else:
            img = Original_Image

            fig = plt.Figure(figsize=(13, 7))
            canvas = FigureCanvasTkAgg(fig, root8)
            canvas.get_tk_widget().place(x=200, y=0)

            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533")
            ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533")

            ax2.set_facecolor("#2E2E2E")

            ax2.set_title("Histogram", fontsize=12, color="#333533")
            ax1.set_title("Original Image", fontsize=12, color="#333533")

            toolbarFrame = tk.Frame(master=root8)
            toolbarFrame.place(x=720, y=720)

            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

            def on_key_press(event):
                print("you pressed {}".format(event.key))
                key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect("key_press_event", on_key_press)

            fig.subplots_adjust(bottom=0.25)

            ax1.imshow(img, cmap='gray')

            ax1_value = fig.add_axes([0.12, 0.1, 0.78, 0.03])
            ax2_value = fig.add_axes([0.12, 0.05, 0.78, 0.03])

            s_time1 = Slider(ax1_value, 'Minimum Value', 0, np.max(img), valinit=0, color='r')
            s_time2 = Slider(ax2_value, 'Maximum Value', 0, np.max(img), valinit=0, color='g')

            def Canny2(val):
                ax2.cla()
                hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
                ax2.bar(range(256), hist_img.ravel(), color="#d1ae45", label="Band" + str(1) + "Histogram")
                ax2.axvline(x=int(s_time2.val), color='g', label="Maximum")
                ax2.axvline(x=int(s_time1.val), color='r', label="Minimum")

                blur = cv2.GaussianBlur(img, (int(E1.get()), int(E1.get())), 0)
                ret3, q = cv2.threshold(blur, int(s_time1.val), int(s_time2.val),
                                        cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                ax2.set_title("Histogram", fontsize=12, color="#333533")
                ax1.set_title("Treshhold Image", fontsize=12, color="#333533")

                ax2.set_xlabel("Value", labelpad=15, fontsize=12, color="#333533");
                ax2.set_ylabel("Frequency", labelpad=15, fontsize=12, color="#333533");

                ax1.imshow(q, cmap='gray')

                ax2.legend(loc='best')

                def SaveI():
                    f = filedialog.asksaveasfile(filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

                    if f is None:
                        return

                    filename = f.name

                    cv2.imwrite(str(filename) + '.jpg', q)
                    f.close()

                btnw = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Save Invert Image   ', padx=20, bd='5',
                                 command=SaveI)
                btnw.place(x=400, y=0)

                fig.canvas.draw_idle()

            hist_img = cv2.calcHist([img], [0], None, [256], [0, 256])
            ax2.bar(range(256), hist_img.ravel(), color="#d1ae45", label="Band" + str(1) + "Histogram")
            ax2.legend(loc='best')

            L1 = tk.Label(root8, text="Block Size(Odd Number):", bg='#000000', fg='#b7f731', bd=5)
            L1.place(x=200, y=720)
            E1 = tk.Entry(root8, bd=5)
            E1.place(x=330, y=720)

            s_time1.on_changed(Canny2)
            s_time2.on_changed(Canny2)

    if len(Original_image_Size) > 2:
        Dimension_Number = []
        Dimension_Number_int = []
        for x1 in range(Original_Image.shape[2]):
            Dimension_Number_int.append(x1 + 1)
            Dimension_Number.append(("Band ", x1 + 1))

    else:
        Dimension_Number = [("Band", 1)]

    if len(Original_image_Size) > 2:
        ttk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = (Dimension_Number_int)
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)

        btn = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5', command=OT1)
        btn.place(x=0, y=60)

    else:
        tk.Label(root8, text="Choose a band:").pack(anchor='w')
        number1 = tk.StringVar()
        numberChosen1 = ttk.Combobox(root8, width=12, textvariable=number1)
        numberChosen1['values'] = "1"
        numberChosen1.pack(anchor='w')
        numberChosen1.current(0)
        btn1 = tk.Button(root8, bg='#000000', fg='#b7f731', text='   Select Band   ', padx=20, bd='5', command=OT1)
        btn1.pack(anchor='w')



    def Quit():
        root8.quit()
        root8.destroy()

    button = tk.Button(master=root8, bg='#000000', fg='#b7f731', text='       Quit        ', padx=20,
                       bd='5', command=Quit)
    button.pack(anchor='w')

    root8.mainloop()

# Định nghĩa hàm mở trình chỉnh sửa hình ảnh
def open_image_editor():
    subprocess.run(["python", "Image_Editing.py"])

# Tạo cửa sổ chính của ứng dụng với kích thước 1920x1080
root1 = tk.Tk()
root1.geometry("1920x1080")
# Đặt ảnh biểu tượng cho cửa sổ
img = ImageTk.PhotoImage(file='logo.png')
root1.tk.call('wm', 'iconphoto', root1._w, img)

# Định nghĩa hàm để thay đổi kích thước hình ảnh khi cửa sổ thay đổi kích thước
def resize_image(event):
    new_width = event.width
    new_height = event.height
    image = copy_of_image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(image)
    label.config(image = photo)
    label.image = photo #avoid garbage collection

# Mở ảnh ban đầu và sao chép nó
image = Image.open('Title.jpg')
copy_of_image = image.copy()
photo = ImageTk.PhotoImage(image)
# Gắn ảnh vào nhãn và thay đổi kích thước khi cửa sổ thay đổi
label = ttk.Label(root1, image = photo)
label.bind('<Configure>', resize_image)
label.pack(fill=tk.BOTH, expand = 'YES')

# Đặt tiêu đề cho cửa sổ
root1.title("VNU-UET - Group 16 - Image Processing Programme")

# Tạo thanh menu cho cửa sổ
menubar1 = tk.Menu(root1)


# Menu File với các lệnh liên quan đến file
filemenu = tk.Menu(menubar1, tearoff=0,activeborderwidth=4,activeforeground='red2',fg='blue',bg='thistle4',font=('Franklin Gothic Demi Cond', 11))
filemenu.add_command(label="New", command=OPEN)
filemenu.add_command(label="Open", command=OPEN)
filemenu.add_command(label="Save", command=OPEN)
filemenu.add_command(label="Save as...", command=OPEN)
filemenu.add_command(label="Close", command=OPEN)

# Thêm dấu phân cách và lệnh thoát
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root1.quit)
menubar1.add_cascade(label="File", menu=filemenu)

# Menu chỉnh sửa hình ảnh
image_editing_menu = tk.Menu(menubar1, tearoff=0)
image_editing_menu.add_command(label="Open Image Editor", command=open_image_editor)
menubar1.add_cascade(label="Image Editing", menu=image_editing_menu)

# Menu Histogram với các lệnh liên quan đến xử lý Histogram
Histogrammenu = tk.Menu(menubar1, tearoff=0,activeborderwidth=4,activeforeground='red2',fg='blue',bg='thistle4',font=('Franklin Gothic Demi Cond', 11))

Histogrammenu.add_command(label="Show Histogram", command=Show_Histogram1)
Histogrammenu.add_command(label="Histogram Equalization", command=Equalization)
Histogrammenu.add_command(label="Brightness", command=Brightness)

menubar1.add_cascade(label="Histogram", menu=Histogrammenu)

# Menu Segmentation với các lệnh liên quan đến phân đoạn ảnh
segmenu = tk.Menu(menubar1, tearoff=0, activeborderwidth=4, activeforeground='red2', fg='blue', bg='thistle4', font=('Franklin Gothic Demi Cond', 11))

# Menu Edge Detection với các phương pháp phát hiện cạnh
Edge = tk.Menu(menubar1, tearoff=0, activeborderwidth=4, activeforeground='red2', fg='blue', bg='thistle4', font=('Franklin Gothic Demi Cond', 11))
segmenu.add_cascade(label="Edge Detection", menu=Edge)
Edge.add_command(label="Robertz", command=Robertz)
Edge.add_command(label="Prewitt", command=Prewitt)
Edge.add_command(label="Sobel", command=Sobel)
Edge.add_command(label="Canny", command=Canny)

# Menu Tresholding với các phương pháp ngưỡng hóa
trmenu = tk.Menu(menubar1, tearoff=0, activeborderwidth=4, activeforeground='red2', fg='blue', bg='thistle4', font=('Franklin Gothic Demi Cond', 11))
segmenu.add_cascade(label="Tresholding", menu=trmenu)
trmenu.add_command(label="Simple Tresholding", command=Tresholding)
trmenu.add_command(label="Adaptive Tresholding", command=AT)
trmenu.add_command(label="Otsu's Thresholding", command=OT)


menubar1.add_cascade(label="Segmentation", menu=segmenu)


# Menu Edit với các lệnh chỉnh sửa cơ bản
editmenu = tk.Menu(menubar1, tearoff=0,activeborderwidth=4, activeforeground='red2', fg='blue', bg='thistle4', font=('Franklin Gothic Demi Cond', 11))
editmenu.add_command(label="Undo", command=OPEN)

# Thêm dấu phân cách và các lệnh cắt, sao chép, dán, xóa
editmenu.add_separator()

editmenu.add_command(label="Cut", command=OPEN)
editmenu.add_command(label="Copy", command=OPEN)
editmenu.add_command(label="Paste", command=OPEN)
editmenu.add_command(label="Delete", command=OPEN)
editmenu.add_command(label="Select All", command=OPEN)

menubar1.add_cascade(label="Edit", menu=editmenu)

# Menu Help với các lệnh trợ giúp
helpmenu = tk.Menu(menubar1, tearoff=0, activeborderwidth=4, activeforeground='red2', fg='blue', bg='thistle4', font=('Franklin Gothic Demi Cond', 11))
helpmenu.add_command(label="Help Index", command=OPEN)

helpmenu.add_command(label="About...", command=OPEN)
menubar1.add_cascade(label="Help", menu=helpmenu)

# Thiết lập thanh menu cho cửa sổ
root1.config(menu=menubar1)

# Bắt đầu vòng lặp giao diện
root1.mainloop()

