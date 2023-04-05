import cv2
from pyzbar import pyzbar
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class CameraApp:
    def __init__(self, window):
        self.window = window
        self.cap = None
        self.camera_idx = 0

        self.label = tk.Label(self.window)
        self.label.pack(side="left")

        

        self.select_label = tk.Label(self.window, text="Select camera:")
        self.select_label.pack()

        self.camera_list = self.get_camera_list()
        # self.camera_list = list (map(str, self.get_camera_indexes()))
        self.camera_combobox = ttk.Combobox(self.window, values=self.camera_list)
        self.camera_combobox.current(0)
        self.camera_combobox.pack()

        self.main_button = tk.Button(self.window,text="open camera", command=self.combine_camera)
        self.main_button.pack()


        self.update_video()

    def get_camera_list(self):
        index = 0
        camera_list = []
        while True:
            cap = cv2.VideoCapture(index)
            if not cap.isOpened():
                break
            else:
                camera_list.append("Camera {}".format(index))
            cap.release()
            index += 1
        return camera_list


    def combine_camera(self):
        if self.cap == None:
            self.open_camera()
            
        else:
            self.close_camera()
            


    def open_camera(self):
        self.camera_idx = self.camera_combobox.current()
        self.cap = cv2.VideoCapture(self.camera_idx)
        if self.cap.isOpened():
            self.main_button.config(text="close camera")
            

    def close_camera(self):
        self.cap.release()
        self.cap = None
        self.main_button.config(text="open camera")

    def update_video(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                barcodes = pyzbar.decode(frame)
                for barcode in barcodes:
                    barcode_data = barcode.data.decode("utf-8")
                    barcode_type = barcode.type
                    code_data = tk.StringVar()
                    code_type = tk.StringVar()
                    self.barcode_data = tk.Label(self.window,bg="black",fg="white", textvariable=code_data)
                    self.barcode_type = tk.Label(self.window,bg="black",fg="white", textvariable=code_type)
                    code_data.set("barcode date: "+str(barcode_data))
                    code_type.set("barcode type: "+str(barcode_type))
                    self.barcode_data.pack()
                    self.barcode_type.pack()
                    
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                photo = ImageTk.PhotoImage(image)
                
                self.label.config(image=photo)
                self.label.image = photo
        self.window.after(1000, self.update_video)

if __name__ == "__main__":
    window = tk.Tk()
    window.title("barcode scanner")
    window.geometry("900x600")
    app = CameraApp(window)
    window.mainloop()
