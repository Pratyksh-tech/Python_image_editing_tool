
class RectangleDrawer:
    def __init__(self, canvas,label,label1,data,current_index):
        # self.master = master
        self.data = data
        self.current_index = current_index
        self.canvas = canvas
        self.label = label
        self.label1 = label1
        # self.canvas.pack()
        self.radius = 5
        self.color = 'red'
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.x = None
        self.y = None
        

    def draw(self):
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        
    def on_press(self, event):
        if self.rect:
            self.x = self.canvas.canvasx(event.x)
            self.y = self.canvas.canvasy(event.y)
            # print(abs(self.x-self.start_x)+abs(self.y-self.start_y),abs(self.x-self.end_x)+abs(self.y-self.end_y))
            if (abs(self.x-self.start_x)+abs(self.y-self.start_y))<(abs(self.x-self.end_x)+abs(self.y-self.end_y)):
                self.canvas.delete("circle1")
                self.canvas.bind("<B1-Motion>", self.on_drag_1)
            else:
                self.canvas.delete("circle2")
                self.canvas.bind("<B1-Motion>", self.on_drag)
            # self.canvas.delete("rectangle","circle2","circle1")
            # self.canvas.delete("circle2")
        else:
            self.start_x = self.canvas.canvasx(event.x)
            self.start_y = self.canvas.canvasy(event.y)
            self.end_x = self.canvas.canvasx(event.x)
            self.end_y = self.canvas.canvasy(event.y)
            self.circle1 = self.canvas.create_oval(self.start_x-self.radius, self.start_y-self.radius, self.start_x+self.radius, self.start_y+self.radius, fill=self.color, outline="", tag = 'circle1')
            self.circle2 = self.canvas.create_oval(self.end_x-self.radius, self.end_y-self.radius, self.end_x+self.radius, self.end_y+self.radius, fill=self.color, outline="", tag = 'circle2')
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline="black", tag="rectangle")
            self.canvas.bind("<B1-Motion>", self.on_drag)
            self.label.config(text = f'X1,Y1:')
            self.label1.config(text = f'{self.start_x,self.start_y,self.end_x, self.end_y}')
            # self.data.at[self.current_index, 'coordinates'] = self.start_x, self.start_y, self.end_x, self.end_y
            
    def on_drag(self, event):
        if self.rect:
            self.end_x = self.canvas.canvasx(event.x)
            self.end_y = self.canvas.canvasy(event.y)
            self.canvas.delete("circle2")
            self.circle2 = self.canvas.create_oval(self.end_x-self.radius, self.end_y-self.radius, self.end_x+self.radius, self.end_y+self.radius, fill=self.color, outline="",tag = 'circle2')
            # self.canvas.coords(self.rect, self.start_x, self.start_y, self.end_x, self.end_y)
            self.canvas.delete("rectangle")
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline="black", tag="rectangle")
            self.label.config(text = f'X1,Y1:')
            self.label1.config(text = f'{self.start_x,self.start_y,self.end_x, self.end_y}')
            self.data.at[self.current_index, 'coordinates'] = self.start_x, self.start_y, self.end_x, self.end_y
            # print(self.data)
            # return 
    
    def on_drag_1(self, event):
        if self.rect:
            self.start_x = self.canvas.canvasx(event.x)
            self.start_y = self.canvas.canvasy(event.y)
            self.canvas.delete("circle1")
            self.circle1 = self.canvas.create_oval(self.start_x-self.radius, self.start_y-self.radius, self.start_x+self.radius, self.start_y+self.radius, fill=self.color, outline="",tag = 'circle1')
            self.canvas.delete("rectangle")
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline="black", tag="rectangle")
            self.label.config(text = f'X1,Y1:')
            self.label1.config(text = f'{self.start_x,self.start_y,self.end_x, self.end_y}')
            # self.data.at[self.current_index, 'coordinates'] = self.start_x, self.start_y, self.end_x, self.end_y
            # print(self.data)
    
    def on_release(self, event):
        pass

