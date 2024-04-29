import tkinter as tk

class MovablePoint:
    def __init__(self, canvas, x, y, label, radius=5, color="red"):
        self.canvas = canvas
        self.radius = radius
        self.color = color
        self.label = label
        self.circle = self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color, outline="")

        self.canvas.tag_bind(self.circle, "<ButtonPress-1>", self.start_drag)
        self.canvas.tag_bind(self.circle, "<ButtonRelease-1>", self.stop_drag)
        self.canvas.tag_bind(self.circle, "<B1-Motion>", self.drag)

        self.dragging = False
        self.prev_x = 0
        self.prev_y = 0
        


    def start_drag(self, event):
        self.dragging = True
        self.prev_x = self.canvas.canvasx(event.x)
        self.prev_y = self.canvas.canvasy(event.y)
        self.label.config(text = f'x, y: {self.prev_x,self.prev_y}')

    def stop_drag(self, event):
        self.dragging = False

    def drag(self, event):
        if self.dragging:
            dx = self.canvas.canvasx(event.x) - self.prev_x
            dy = self.canvas.canvasy(event.y) - self.prev_y
            self.canvas.move(self.circle, dx, dy)
            self.prev_x = self.canvas.canvasx(event.x)
            self.prev_y = self.canvas.canvasy(event.y)
            self.label.config(text = f'x, y: {self.prev_x,self.prev_y}')


class RectangleWithMovablePoints:
    def __init__(self, canvas, point1, point2):
        self.canvas = canvas
        self.point1 = point1
        self.point2 = point2

        # self.reset_button = tk.Button(self.button_frame, text="reset", command=self.reset_image)
        # self.reset_button.grid(row=0, column=3)

        self.canvas.bind("<B1-Motion>", self.update_rectangle)

    def update_rectangle(self, event):
        x1, y1 = self.point1.prev_x, self.point1.prev_y#self.canvas.coords(self.point1.circle)[0:2]
        x2, y2 = self.point2.prev_x, self.point2.prev_y#self.canvas.coords(self.point2.circle)[0:2]

        self.canvas.coords(self.rectangle, x1, y1, x2, y2)

    def draw_rectangle(self):
        x1, y1 = self.canvas.coords(self.point1.circle)[0:2]
        x2, y2 = self.canvas.coords(self.point2.circle)[0:2]
        # print(self.point1.prev_x)

        self.rectangle = self.canvas.create_rectangle(x1, y1, x2, y2, fill='', outline='black')

def main():
    root = tk.Tk()
    root.title("Rectangle with Two Movable Points")

    canvas = tk.Canvas(root, width=400, height=400, bg="white")
    canvas.pack()
    point1 = MovablePoint(canvas, 50, 50)
    point2 = MovablePoint(canvas, 200, 200)

    rectangle = RectangleWithMovablePoints(canvas, point1, point2)
    rectangle.draw_rectangle()

    root.mainloop()

if __name__ == "__main__":
    main()
