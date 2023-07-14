"""This is Langton's ant program
You can import it to use Ant class or just modify for your needs, comments will help you :D"""


# importing GUI modules
import tkinter as tk
import ctypes

# importing backend modules
import platform
import time
import random
from typing import Literal


# Windows right resolution setup
if platform.system() == 'Windows':
    ctypes.windll.shcore.SetProcessDpiAwareness(1)


# list that contains coordinates of black sells
black_sells = []


# Ant type definition
class Ant:
    def __init__(self, canvas: tk.Canvas, coords: tuple, image: tk.PhotoImage,
                  direction: Literal['up', 'down', 'right', 'left'],
                  unit: int = 30):
        """This is Langton's ant\n
        Movement rules reminder:\n
        a. If the ant is on a white cell, it turns 90 degrees to the right (clockwise), changes the cell color to black, and moves one unit forward.\n
        b. If the ant is on a black cell, it turns 90 degrees to the left (counter-clockwise), changes the cell color to white, and moves one unit forward.\n
        Parameters:\n
        canvas - tkinter.Canvas to draw on\n
        coords - first ant's coordinates\n
        image - ant image\n
        direction - first direction\n
        unit - size of one ant move(in pixels)
        """
        
        # ant logic variables
        self.x, self.y = coords
        self.unit = unit
        self.direction = direction
        print(self.direction)

        # direction changers
        self.turn_left = {'up':'left', 'left':'down', 'down':'right', 'right':'up'}
        self.turn_right = {'up':'right', 'right':'down', 'down':'left', 'left':'up'}

        self.canvas = canvas
        self.ant_image = image

        # ant canvas object
        self.id = self.canvas.create_image(self.x, self.y, image=self.ant_image, anchor='nw')

    # Method for ant movement
    def move(self):
        # ant coordinates
        coords = (self.x, self.y)

        # filling cell and getting new direction
        if black_sells and coords in black_sells:
            # removing black cell from list
            black_sells.remove(coords)
            # creating white cell instead
            self.canvas.create_rectangle(self.x, self.y, self.x+self.unit, self.y+self.unit, fill='white')
            # changing direction
            self.direction = self.turn_left[self.direction]
        else:
            # adding black cell to list
            black_sells.append(coords)
            # creating black cell
            self.canvas.create_rectangle(self.x, self.y, self.x+self.unit, self.y+self.unit, fill='black')
            # changing direction
            self.direction = self.turn_right[self.direction]

        # moving ant
        if self.direction == 'up':
            self.canvas.move(self.id, 0, self.unit*-1)
            self.y += self.unit*-1
        elif self.direction == 'down':
            self.canvas.move(self.id, 0, self.unit)
            self.y += self.unit
        elif self.direction == 'right':
            self.canvas.move(self.id, self.unit, 0)
            self.x += self.unit
        elif self.direction == 'left':
            self.canvas.move(self.id, self.unit*-1, 0)
            self.x += self.unit*-1

        # showing ant
        self.canvas.lift(self.id)


# RandomDirectinAnt type definition
class RandomDirectionAnt(Ant):
    def __init__(self, canvas: tk.Canvas, coords: tuple, image: tk.PhotoImage):
        """This is Langton's ant, but with random start direction
        Parameters are same except there's no 'direction' parameter"""
        super().__init__(canvas, coords, image, direction=random.choice(['up', 'down', 'right', 'left']))


# start program if file isn't imported but runned  
if __name__ == "__main__":

    # window instance
    win = tk.Tk()

    win.title("Langton's ant")

    # make window fullscreen
    win.wm_attributes('-fullscreen', True)

    # you can change canvas = tk.Canvas(win, background='white') to canvas = tk.Canvas(win)
    # and uncomment command bellow to make background transparent(looks like an ant that appears from nothing, tested only on Windows)
    #win.wm_attributes('-transparentcolor', win['bg'])

    # you can comment out win.wm_attributes('-fullscreen', True)
    # and uncomment command bellow to make window not fullscreen 
    #win.geometry("1000x800")

    # canvas instance
    canvas = tk.Canvas(win, background='white')
    canvas.pack(expand=True, fill='both')

    # update canvas to get its size and center
    canvas.update()
    width = canvas.winfo_width()
    height = canvas.winfo_height()

    # calculate coords
    x = width // 2 - 15
    y = height // 2 - 15

    # making ant image object
    i = tk.PhotoImage(file='ant.png')

    # Ant instance
    ant = Ant(canvas, (x, y), i, 'up')

    # you can comment out ant = Ant(canvas, (x, y), i, 'up') and
    # uncomment command bellow to make ant with random start direction as default
    #random_direction_ant = RandomDirectionAnt(canvas, (x, y), i)

    # count of iterations for ant movement cycle(at every iteration ant makes 1 move)
    times = 20000
    
    # ant movement cycle
    for t in range(times):
        # moving ant
        ant.move()

        # you can comment out ant = Ant(canvas, (x, y), i, 'up') and ant.move(),
        # and, then, uncomment command bellow to make RandomDirectionAnt moving
        #random_direction_ant.move()

        # delay for more smooth animation
        time.sleep(0.001)

        # updating window to see changes
        win.update()

    # stay window exsiting
    win.mainloop()