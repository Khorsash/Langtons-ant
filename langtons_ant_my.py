"""This is Langton's ant program
You can import it to use Ant class or just modify for your needs, comments will help you :D"""


# importing GUI modules
import tkinter as tk
import ctypes

# importing backend modules
import platform
import sys
import time
import random


# Windows right resolution setup
if platform.system() == 'Windows':
    ctypes.windll.shcore.SetProcessDpiAwareness(1)


# dicts that contain coordinates of black and white sells
black_sells = {}
white_cells = {}


# Ant type definition
class Ant:
    def __init__(self, canvas: tk.Canvas, coords: tuple, image: tk.PhotoImage,
                  direction: str,
                  unit: int = 30):
        """This is Langton's ant\n
        Movement rules reminder:\n
        a. If the ant is on a white cell, it turns 90 degrees to the right (clockwise), changes the cell color to black, and moves one unit forward.\n
        b. If the ant is on a black cell, it turns 90 degrees to the left (counter-clockwise), changes the cell color to white, and moves one unit forward.\n
        Parameters:\n
        canvas - tkinter.Canvas to draw on\n
        coords - first ant's coordinates\n
        image - ant image(tkinter.PhotoImage)\n
        direction - first direction\n
        unit - size of one ant move(in pixels)
        """

        # ant logic variables
        self.x, self.y = coords
        self.unit = unit
        self.direction = direction
        #print(self.direction)

        # direction changers
        self.turn_left = {'up':'left', 'left':'down', 'down':'right', 'right':'up'}
        self.turn_right = {'up':'right', 'right':'down', 'down':'left', 'left':'up'}

        self.canvas = canvas
        self.ant_image = image

        # ant canvas object
        self.id = self.canvas.create_image(self.x, self.y, image=self.ant_image, anchor='nw')
        #self.id = self.canvas.create_rectangle(self.x, self.y, self.x+self.unit, self.y+self.unit, fill='red')

    # Method for ant movement
    def move(self):
        # ant coordinates
        coords = (self.x, self.y)

        # filling cell and getting new direction
        if coords in list(black_sells.values()):

            # if ant on black sell
            # we're trying to find id of it
            for id in black_sells:
                if black_sells[id] == coords:

                    # filling black cell with white
                    self.canvas.itemconfig(id, fill='white')

                    # deleting that cell from black_sells
                    del black_sells[id]

                    # adding that cell to white_sells
                    white_cells[id] = coords

                    # turning ant left
                    self.direction = self.turn_left[self.direction]

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
                    return
                
        elif coords in white_cells.values():

            # if ant on white sell
            # we're trying to find id of it
            for id in white_cells:
                if white_cells[id] == coords:

                    # filling white cell with black
                    self.canvas.itemconfig(id, fill='black')

                    # deleting that cell from white_sells
                    del white_cells[id]

                    # adding that cell to black_sells
                    black_sells[id] = coords

                    # turning ant right
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
                    return

        else:
            # creating black cell
            id = self.canvas.create_rectangle(self.x, self.y, self.x+self.unit, self.y+self.unit, fill='black')

            # adding that cell to black_sells
            black_sells[id] = coords

            # turning ant right
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
    #win.wm_attributes('-fullscreen', True)

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

    canvas.bind_all('<Up>', lambda event: canvas.yview_scroll(-1, 'units'))
    canvas.bind_all('<Down>', lambda event: canvas.yview_scroll(1, 'units'))
    canvas.bind_all('<Right>', lambda event: canvas.xview_scroll(1, 'units'))
    canvas.bind_all('<Left>', lambda event: canvas.xview_scroll(-1, 'units'))

    # making ant image object
    i = tk.PhotoImage(file='ant.png')

    win.iconphoto(False, i)

    # Ant instance
    ant = Ant(canvas, (x, y), i, 'up')

    iterations = 0

    def make_step():
        global iterations
        # moving ant
        ant.move()

        # adding iteration
        iterations += 1

        # updating window to see changes
        win.update()


    # function that starts animation
    def start(event):
        # set 'running' as True globally
        global running
        running = True

        # binding 'space' key to 'stop' function
        win.bind('<space>', stop)

        # starting ant movement cycle
        while running:

            # moving ant
            make_step()
            
            # delay for more smooth animation
            time.sleep(0.001)


    # function that starts animation
    def stop(event):
        # set 'running' as False globally(that stops animation, 'cause movement cycle is 'while running:')
        global running 
        running = False

        # binding 'space' key to 'make_step' function to make possibility of step-by-step animation by clicking 'space' key
        win.bind('<space>', lambda event: make_step())

    # start bindings
    win.bind('<Return>', start)
    win.bind('<space>', stop)
    win.bind('<Escape>', lambda event: sys.exit())

    # stay window exsiting
    win.mainloop()
