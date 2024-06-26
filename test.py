import cv2
import os
import math
import tkinter as tk
import pandas as pd
from tkinter import ttk,filedialog
from PIL import Image, ImageTk
from test2 import RectangleDrawer
# from rect import RectangleWithMovablePoints, MovablePoint

class ImageEditor:
    def __init__(self, master):
        
        self.master = master
        self.canvas = tk.Canvas(master, cursor="arrow")
        
        # self.RectangleWithMovablePoints = RectangleWithMovablePoints(self)
        # self.MovablePoint = MovablePoint(self)

        self.master.title("Pratyksh Image Editor")
        # self.master.iconbitmap('favicon.ico') 
        self.current_index = 0
        self.point1 = [0,0]
        self.current_index = 0
        self.point2 = [0,0]
        self.start_x = 0
        self.start_y = 0
        self.temp_line = 0
        self.line_counter = 0
        self.point_counter = 0
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
        draw_rect = tk.Button(self.button_frame, text="rectangle", command=self.rect)
        draw_rect.grid(row=0, column=5)
        download_button = tk.Button(self.button_frame, text="Download folder", command=self.download_json)
        download_button.grid(row=0, column=6)
        yolo_file = tk.Button(self.button_frame, text="yolo", command=self.yolo)
        yolo_file.grid(row=1, column=0)

        self.canvas.config(width = 640, height = 480)
        self.canvas.pack(fill="both", expand=True)

        self.label = tk.Label(self.button_frame, text="x1,y1:")
        self.label.grid(row=0, column=7)

        self.label1 = tk.Label(self.button_frame, text="None")
        self.label1.grid(row=0, column=8)
        self.data = pd.DataFrame(columns=['Sr. No.','Image Name', 'coordinates'])
        self.RectangleDrawer = RectangleDrawer(self.canvas,self.label,self.label1,self.data, self.current_index)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<Configure>", self.show_image)
        self.tree_frame = tk.Frame(master, width=200, height=200)
        self.tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.tree_frame, columns=['Sr. No.','Image Name','coordinates', 'annotate'], show='headings')
        self.tree.heading('Sr. No.', text='Sr. No.')
        self.tree.heading('Image Name', text='Image Name')
        self.tree.heading('coordinates', text='coordinates')
        self.tree.heading('annotate', text='annotate')
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def load_folder(self):
        folder_path = filedialog.askdirectory()
        self.folder_path = folder_path
        os.makedirs(f'{self.folder_path}/annotated', exist_ok=True)
        if folder_path:
            self.images = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(('png', 'jpg', 'jpeg'))]
            self.current_index = 0
            # self.show_image()
            image_path = self.images[self.current_index]
            self.img = cv2.imread(image_path)
            self.img = cv2.resize(self.img, (480,640))
            self.show_image()
    
    def yolo(self):
        file_path = filedialog.askopenfilename()
        print(file_path,type(file_path))

    def format(self,img):
        # if self.current_index ==0:
        #     return
        list = self.data.at[self.current_index, 'coordinates'][1:-1].split(',')
        if list == ['on']:
            return
        # print(list)

        start_x = float(list[0])
        start_y = float(list[1])
        end_x = float(list[2])
        end_y = float(list[3])
        height, width, _ = img.shape
        h = abs((start_y - end_y)/height)
        w = abs((start_x - end_y)/width)
        x = abs((start_x + end_x)/(2*width))
        y = abs((start_y + end_y)/(2*height))
        print(0, x, y, h, w)
        return [0, x, y, h, w]

    def next_image(self):
        if self.images and self.current_index < len(self.images) - 1:
            if self.label1.cget('text') != 'None':
                self.data.at[self.current_index, 'coordinates'] = self.label1.cget('text')
                print('hi',self.format(self.img),self.label1.cget('text'))
                self.data.at[self.current_index, 'annotate'] = str(self.format(self.img))
            # else:
            #     self.data.at[self.current_index, 'coordinates'] = self.data.at[self.current_index, 'coordinates']
            # print('1:',self.data.at[self.current_index, 'coordinates'])
            # print('2:',self.label1.cget('text'))
            
            self.current_index += 1
            self.zoom_level = 1.0
            image_path = self.images[self.current_index]
            self.img = cv2.imread(image_path)
            self.img = cv2.resize(self.img, (480,640))
            self.RectangleDrawer.rect = None
            self.label1.config(text = 'None')
            self.show_image()
            if self.data.at[self.current_index, 'coordinates'] != 'None':
                list = self.data.at[self.current_index, 'coordinates'][1:-1].split(',')
                # print(list)
                self.RectangleDrawer.start_x = float(list[0])
                self.RectangleDrawer.start_y = float(list[1])
                self.RectangleDrawer.end_x = float(list[2])
                self.RectangleDrawer.end_y = float(list[3])
                self.RectangleDrawer.circle1 = self.canvas.create_oval(self.RectangleDrawer.start_x-5, self.RectangleDrawer.start_y-5, self.RectangleDrawer.start_x+5, self.RectangleDrawer.start_y + 5, fill='red', outline="", tag = 'circle1')
                self.RectangleDrawer.circle2 = self.canvas.create_oval(self.RectangleDrawer.end_x-5, self.RectangleDrawer.end_y-5, self.RectangleDrawer.end_x+5, self.RectangleDrawer.end_y+5, fill='red', outline="", tag = 'circle2')
                self.RectangleDrawer.rect = self.canvas.create_rectangle(self.RectangleDrawer.start_x, self.RectangleDrawer.start_y, self.RectangleDrawer.end_x, self.RectangleDrawer.end_y, outline="black", tag="rectangle")
                self.RectangleDrawer.draw()

    def rect(self):
        self.canvas.bind("<ButtonRelease-1>", self.makepoint)#"<ButtonRelease-1>"



    def makepoint(self, event):
        self.RectangleDrawer.draw()
    
    
    def reset_image(self):
        self.zoom_level = 1.0
        image_path = self.images[self.current_index]
        self.img = cv2.imread(image_path)
        self.img = cv2.resize(self.img, (480,640))
        self.show_image()

        # self.show_image()

    def prev_image(self):
        if self.images and self.current_index > 0:
            # self.data.at[self.current_index, 'coordinates'] = self.label1.cget('text')
            if self.label1.cget('text') != 'None':
                self.data.at[self.current_index, 'coordinates'] = self.label1.cget('text')
                self.data.at[self.current_index, 'annotate'] = self.format(self.img)
            self.current_index -= 1
            self.zoom_level = 1.0
            image_path = self.images[self.current_index]
            self.img = cv2.imread(image_path)
            self.img = cv2.resize(self.img, (480,640))
            self.label1.config(text = 'None')
            self.show_image()
            if self.data.at[self.current_index, 'coordinates'] != 'None':
                list = self.data.at[self.current_index, 'coordinates'][1:-1].split(',')
                # print(list)
                self.RectangleDrawer.start_x = float(list[0])
                self.RectangleDrawer.start_y = float(list[1])
                self.RectangleDrawer.end_x = float(list[2])
                self.RectangleDrawer.end_y = float(list[3])
                self.RectangleDrawer.circle1 = self.canvas.create_oval(self.RectangleDrawer.start_x-5, self.RectangleDrawer.start_y-5, self.RectangleDrawer.start_x+5, self.RectangleDrawer.start_y + 5, fill='red', outline="", tag = 'circle1')
                self.RectangleDrawer.circle2 = self.canvas.create_oval(self.RectangleDrawer.end_x-5, self.RectangleDrawer.end_y-5, self.RectangleDrawer.end_x+5, self.RectangleDrawer.end_y+5, fill='red', outline="", tag = 'circle2')
                self.RectangleDrawer.rect = self.canvas.create_rectangle(self.RectangleDrawer.start_x, self.RectangleDrawer.start_y, self.RectangleDrawer.end_x, self.RectangleDrawer.end_y, outline="black", tag="rectangle")
                self.RectangleDrawer.draw()
    
    def download_json(self):
        filename =  filedialog.askdirectory()
        if filename:
            for index, row in self.data.iterrows():
                print('hi',row['Image Name'],filename)
                path = str(filename) + '/' + str(row['Image Name'].split('.')[:-1][0]) + '.text'
                path = "".join(path.split(","))
                print(path)
                with open(path, "w") as file:
                    file.write("".join((row['annotate'][1:-1]).split(",")))
            # self.data.to_json(filename, orient='records')
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
            img1 = Image.fromarray(img)
            self.tk_img = ImageTk.PhotoImage(img1)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
            # if self.current_index != 0:
                # self.format(img)
            if self.data.empty:
                self.data.loc[0] = [self.current_index,os.path.basename(self.images[self.current_index]),'None']
            else:
                if not self.data['Sr. No.'].eq(self.current_index).any():
                    self.data = self.data.append({'Sr. No.':self.current_index,'Image Name': os.path.basename(self.images[self.current_index]),'coordinates':'None', 'annotate': 'None'}, ignore_index=True)
            self.tree.delete(*self.tree.get_children())
            # print(os.path.basename(self.images[self.current_index]))
            
            for index, row in self.data.iterrows():
                self.tree.insert("", "end", values=[row['Sr. No.'],row['Image Name'],row['coordinates'],row['annotate']])

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
                # self.data.at[self.current_index, 'angle'] = angle
                self.canvas.create_text(10, 100, anchor='nw', text=str(angle), fill="red")
                # self.label.config(text = f'Angle: {angle}')
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
