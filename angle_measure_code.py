import cv2
import os
import math
import tkinter as tk
import pandas as pd
from tkinter import ttk,filedialog
from PIL import Image, ImageTk

class ImageEditor:
    def __init__(self, master):
        
        self.master = master
        self.master.title("Image Editor")
        # self.master.iconbitmap('favicon.ico') 
        self.current_index = 0
        self.start_x = 0
        self.start_y = 0
        self.temp_line = 0
        self.line_counter = 0
        self.images = []
        self.slopes = [0,0]
        self.zoom_level = 1.0  # Initial zoom level
        self.image_label = tk.Label(master)
        self.image_label.pack()
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # self.button_frame.pack(side ="left")
        self.load_folder_button = tk.Button(self.button_frame, text="Load Folder", command=self.load_folder)
        self.load_folder_button.grid(row=0, column=0)
        self.prev_button = tk.Button(self.button_frame, text="Previous", command=self.prev_image)
        self.prev_button.grid(row=0, column=1)
        self.next_button = tk.Button(self.button_frame, text="Next", command=self.next_image)
        self.next_button.grid(row=0, column=2)
        self.reset_button = tk.Button(self.button_frame, text="reset", command=self.reset_image)
        self.reset_button.grid(row=0, column=3)
        self.pan_button = tk.Button(self.button_frame, text="pan", command=self.pan)
        self.pan_button.grid(row=0, column=4)
        draw_button = tk.Button(self.button_frame, text="draw", command=self.draw_but)
        draw_button.grid(row=0, column=5)
        download_button = tk.Button(self.button_frame, text="Download JSON", command=self.download_json)
        download_button.grid(row=0, column=6)
        # self.magnify_button = tk.Button(master, text="Magnify", command=self.activate_magnify)
        # self.magnify_button.pack(side="left")
        self.canvas = tk.Canvas(master, cursor="arrow")
        self.canvas.config(width = 400, height = 400)
        self.canvas.pack(fill="both", expand=True)

        self.label = tk.Label(self.button_frame, text="Angle: None")
        self.label.grid(row=0, column=7)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<Configure>", self.show_image)

        self.data = pd.DataFrame(columns=['Sr. No.','Image Name', 'angle'])
        self.tree_frame = tk.Frame(master, width=200, height=200)
        self.tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.tree_frame, columns=['Sr. No.','Image Name','angle'], show='headings')
        self.tree.heading('Sr. No.', text='Sr. No.')
        self.tree.heading('Image Name', text='Image Name')
        self.tree.heading('angle', text='angle')
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def load_folder(self):
        folder_path = filedialog.askdirectory()
        self.folder_path = folder_path
        os.makedirs(f'{self.folder_path}/annotated', exist_ok=True)
        if folder_path:
            self.images = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(('png', 'jpg', 'jpeg'))]
            print(self.images)
            self.current_index = 0
            # self.show_image()
            image_path = self.images[self.current_index]
            self.img = cv2.imread(image_path)
            self.show_image()


    def next_image(self):
        if self.images and self.current_index < len(self.images) - 1:
            self.current_index += 1
            self.zoom_level = 1.0
            image_path = self.images[self.current_index]
            self.img = cv2.imread(image_path)
            self.show_image()
    
    def reset_image(self):
        self.zoom_level = 1.0
        image_path = self.images[self.current_index]
        self.img = cv2.imread(image_path)
        self.show_image()
        self.show_image()

    def prev_image(self):
        if self.images and self.current_index > 0:
            self.current_index -= 1
            self.zoom_level = 1.0
            image_path = self.images[self.current_index]
            self.img = cv2.imread(image_path)
            self.show_image()
    
    def download_json(self):
        # Prompt user for file save location
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=(("JSON files", "*.json"), ("All files", "*.*")))

        if filename:
            # Save DataFrame as JSON
            self.data.to_json(filename, orient='records')
    def pan(self):
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<Configure>", self.show_image)
    
    def activate_pan(self):
        self.canvas.config(cursor="fleur")

    def activate_magnify(self):
        self.canvas.config(cursor="tcross")

    def magnify_image(self, img):
        # Resize the image based on the zoom level
        height, width, _ = img.shape
        new_height = int(height * self.zoom_level)
        new_width = int(width * self.zoom_level)
        resized_img = cv2.resize(img, (new_width, new_height))
        return resized_img

    def show_image(self, event=None):
        if self.images:

            # img = cv2.resize(img,(self.canvas.winfo_reqwidth(),self.canvas.winfo_reqheight()))
            img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            img = self.magnify_image(img)
            img = Image.fromarray(img)
            self.tk_img = ImageTk.PhotoImage(img)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
            if self.data.empty:
                self.data.loc[0] = [self.current_index,os.path.basename(self.images[self.current_index]),'None']
            else:
                if not self.data['Sr. No.'].eq(self.current_index).any():
                    self.data = self.data.append({'Sr. No.':self.current_index,'Image Name': os.path.basename(self.images[self.current_index]),'angle':'None'}, ignore_index=True)
            self.tree.delete(*self.tree.get_children())
            # print(os.path.basename(self.images[self.current_index]))
            for index, row in self.data.iterrows():
                self.tree.insert("", "end", values=[row['Sr. No.'],row['Image Name'],row['angle']])

    def draw_but(self):
        self.line_counter = 0
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.track_mouse)
        self.canvas.bind("<ButtonRelease-1>", self.draw_line)

    def start_draw(self,event):
        # self.start_x, start_y, temp_line
        
        self.start_x, self.start_y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        self.temp_line = self.canvas.create_line(self.start_x, self.start_y, self.start_x, self.start_y, dash=(2, 2), fill='red')

    def track_mouse(self,event):
        if self.start_x is not None and self.start_y is not None:
            self.canvas.coords(self.temp_line, self.start_x, self.start_y, self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))

    def draw_line(self,event):
        # global start_x, start_y, line_counter
        if self.start_x is not None and self.start_y is not None and self.line_counter < 2:
            x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
            print('hi',self.start_x, self.start_y)
            # self.canvas.create_line(self.start_x, self.start_y, x, y,fill = 'red')
            cv2.line(self.img, (int(self.start_x*(1/self.zoom_level)), int(self.start_y*(1/self.zoom_level))),(int(x*(1/self.zoom_level)),int(y*(1/self.zoom_level))), (255,0,0), 3)
            # print(self.line_counter)
            self.slopes[self.line_counter] = (y -self.start_y)/(x -self.start_x+.0000000001)
            # add slope function _________________________________________________________________________
            
            self.start_x, self.start_y = None, None
            self.line_counter += 1
            if self.line_counter == 2:
                m1 = self.slopes[0]
                m2 = self.slopes[1]
                angle = math.degrees(math.atan(abs((m2 - m1) / (1 + m1 * m2))))
                # print(angle,m1,m2)
                self.data.at[self.current_index, 'angle'] = angle
                self.canvas.create_text(10, 100, anchor='nw', text=str(angle), fill="red")
                self.label.config(text = f'Angle: {angle}')
                # print(f'{self.folder_path}/annotated/{os.path.basename(self.images[self.current_index])}')
                cv2.putText(self.img, f'Angle: {angle}', (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                cv2.imwrite(f'{self.folder_path}/annotated/{os.path.basename(self.images[self.current_index])}',self.img)
                # self.slopes[self.line_counter] == (y -self.start_y)/(x -self.start_x)
            if self.line_counter >= 2:
                # draw_button.config(state=tk.DISABLED)
                self.canvas.unbind("<Button-1>")
                self.canvas.unbind("<B1-Motion>")
                self.canvas.unbind("<ButtonRelease-1>")
            self.show_image()


    def on_button_press(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def on_move_press(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        # self.canvas.scan_dragto(event.x, event.y)

    def on_mousewheel(self, event):
        if event.delta > 0:
            self.zoom_level *= 1.2  # Increase zoom level when mouse wheel moves up
        elif event.delta < 0:
            self.zoom_level /= 1.2  # Decrease zoom level when mouse wheel moves down
        # Limit zoom level to avoid excessive zooming
        self.zoom_level = max(0.2, min(self.zoom_level, 5.0))
        self.show_image()

    

def main():
    root = tk.Tk()
    editor = ImageEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()

#  self.root.bind('n', lambda event: self.next_image())
#         self.root.bind('p', lambda event: self.prev_image())
#         self.root.bind('r', lambda event: self.resize_image())