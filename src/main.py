import cv2
import time
from pyzbar import pyzbar
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class codeScanner:
    def __init__(self, window):
        self.window = window
        self.cap = None
        self.camera_idx = 0
        self.interval = 1000    #scan interval
        self.start_time = time.time()

        self.left_frame = tk.Frame(self.window)
        self.left_frame.pack(side="left",padx=5, pady=5, fill="y")

        self.right_frame = tk.Frame(self.window)
        self.right_frame.pack(side="right", padx=5, pady=5, fill="y")

        self.video = tk.Label(self.right_frame) #show camera video 
        self.video.pack(side="top",anchor="ne")
        self.video.image = None

        self.log_text = tk.Text(self.right_frame, font="微软雅黑", width=60, height=10,state="disabled")
        self.log_text.pack(side="bottom", anchor="se")

        self.clear_butn = tk.Button(self.right_frame, font="微软雅黑", text="clear log", command=self.clear_log)
        self.clear_butn.pack(side="bottom",anchor="sw")


        self.str_interval = tk.StringVar()
        self.str_interval.set(str(self.interval/1000))
        self.interval_label = tk.Label(self.left_frame, text="Scan interval:",font="微软雅黑")
        self.interval_entry = tk.Entry(self.left_frame, bd=5, font="微软雅黑", textvariable= self.str_interval)#interval submit entry
        self.interval_submit_butn = tk.Button(self.left_frame, text="submit", command=self.submit, font="微软雅黑", padx=5,pady=5)

        self.interval_label.grid(row=0, column=0,sticky=tk.NW)
        self.interval_entry.grid(row=0, column=1,sticky=tk.NW)
        self.interval_submit_butn.grid(row=0, column=2,sticky=tk.NW)

        self.combobox_label = tk.Label(self.left_frame, text="Select camera:", font="微软雅黑")
        self.combobox_label.grid(row=1, column=0, sticky=tk.W)

        self.camera_list = self.get_camera_list()
        self.camera_combobox = ttk.Combobox(self.left_frame, values=self.camera_list, font="微软雅黑",state="readonly")
        self.camera_combobox.current(0)
        self.camera_combobox.grid(row=1,column=1,sticky=tk.W)

        self.main_button = tk.Button(self.left_frame,text="open camera", command=self.combine_camera, font="微软雅黑",padx=5,pady=5)
        self.main_button.grid(row=1, column=2,sticky=tk.W)

        self.scan_code()

    def submit(self):
        self.interval = int(float(self.interval_entry.get())) * 1000

    def clear_log(self):
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")
    
    # get current device camera index
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

    # control camera switch by button 
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

    # read video and capture frame then used to decode
    def scan_code(self):

        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                self.video.image = ImageTk.PhotoImage(image)
                self.video.config(image=self.video.image)
                elapsed_time = time.time() - self.start_time

                if int(elapsed_time * 1000) >= self.interval:
                    self.start_time = time.time()
                    barcodes = pyzbar.decode(frame)
                    for barcode in barcodes:
                        barcode_data = barcode.data.decode("utf-8")
                        barcode_type = barcode.type
                    
                        self.code_data = str(barcode_data) +"\n" + str(barcode_type)
                        self.log_text.config(state="normal")
                        self.log_text.insert("end", self.code_data + "\n")
                        self.log_text.see("end")
                        self.log_text.config(state="disabled")
        
        self.window.after(1, self.scan_code)

if __name__ == "__main__":
    window = tk.Tk()
    window.title("barcode scanner")
    window.geometry("1500x800")
    app = codeScanner(window)
    window.mainloop()
