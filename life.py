#Author: github.com/kjgorman
#The classic mathematical game of life, written in python for the
#curses augmented terminal. Because it relies on curses it is 
#unavailable for windows at this point.
import curses
import time
import math
from sys import argv


class Life:

   

    def __init__(self, width, height):
        self.ux = 0
        self.uy = 0
        self.width, self.height = self.setupWindowSize(width, height)
        
    def run(self):
        self.stdscr = curses.initscr()
        self.startup()
        self.cells = []
        self.generation = 0
        self.nodelay = 0
        while 1:
            self.background(self.generation, self.nodelay)
            self.fillCells(self.cells)
            self.mv_term_cursor(self.ux, self.uy)
            #by default a blocking function
            #when [r] is pressed we move to
            #a timeout period of a tenth of 
            #a second for animation. 
            self.c = self.stdscr.getch()

            if self.c == ord('s') or self.nodelay:
                self.cells = self.step(self.cells)
                self.generation = self.generation+1
            if self.c == ord('r'):
                if self.nodelay: self.stdscr.timeout(-1) 
                else:            self.stdscr.timeout(75)
                self.nodelay = self.nodelay ^ 1
            elif self.c == ord('n'):         self.cells = self.addCell(self.ux, self.uy, self.cells)
            elif self.c == ord('d'):         self.cells = self.delCell(self.ux, self.uy, self.cells)
            elif self.c == curses.KEY_RIGHT: self.ux = self.ux + 1 if self.ux < self.width-1 else self.ux
            elif self.c == curses.KEY_LEFT:  self.ux = self.ux - 1 if self.ux > 0 else self.ux
            elif self.c == curses.KEY_UP:    self.uy = self.uy - 1 if self.uy > 0 else self.uy
            elif self.c == curses.KEY_DOWN:  self.uy = self.uy + 1 if self.uy < self.height-1 else self.uy
            elif self.c == ord('q'):
                break
        self.shutdown()

    #Sets up the curses window
    def startup(self):
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)
    #Destructs the curses window and reverts key settings
    def shutdown(self):
        curses.echo()
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.endwin()

    #Fills in the basic background field
    #TODO: only update affected cells per tick
    def background(self, gen, nodelay):
        for y in xrange(0,self.height):
            for x in range(0,self.width):
                try:
                    #the horizontal sides have pipes
                    if (x == 0) | (x == self.width-1):
                        self.stdscr.addch( y, x, ord('|'))
                    #the vertical sides have hypens
                    elif (y == 0) | (y == self.height-1):
                        self.stdscr.addch( y, x, ord('-'))
                    #and blank space are periods
                    else:
                        self.stdscr.addch( y, x, ord('.') )
                    self.stdscr.addstr(self.height, 1, "gen: "+str(gen))
                    self.stdscr.addstr(self.height, 10, "[r]un [s]tep [n]ew [d]el [q]uit")
                    if self.nodelay:
                        self.stdscr.addstr(self.height, 42, "[running]")
                    else:
                        self.stdscr.addstr(self.height, 42, "[paused] ")
                except curses.error:
                    self.shutdown()
                    raise Exception("Curses broke, probably your width or height is too large for the visible screen")
    
        #after drawing refresh the window
        self.stdscr.refresh()

    #Iterates the collection of active cells and
    #'fills' them into the field
    def fillCells(self, cells):
        for cell in cells:
            cell.fill(self.stdscr)
        self.stdscr.refresh()

    #Adding a cell will ensure the set condition
    #of disallowing duplicates
    def addCell(self, x,y,cells):
        for cell in cells:
            if cell.x == x and cell.y == y:
                return cells
        cells.append(Cell(x,y))
        return cells

    def delCell(self, x,y,cells):
        for cell in cells:
            if cell.x == x and cell.y == y:
                cells.remove(cell)
                return cells
        return cells

    #Finds adjacent alive cells
    def adjacentCells(self, cell, cells):
        adj = []
        for other in cells:
            dx = math.fabs(cell.x-other.x)
            dy = math.fabs(cell.y-other.y)
            if (dx <= 1) & (dy <= 1): adj.append(other)
        for other in adj:
            if other.x == cell.x and other.y == cell.y:
                adj.remove(other)
        return adj

    #Finds adjacent dead points
    #TODO: This could really just be surrounding elements not
    #      in adjacentCells
    def adjacentPoints(self, cell, cells):
        dead = []
        candidates =[(x,y) 
                    for x in [cell.x-1, cell.x, cell.x+1] if (x > 0) & (x < self.width-1)
                    for y in [cell.y-1, cell.y, cell.y+1] if (y > 0) & (y < self.height-1)
                    if (x,y) != (cell.x, cell.y)
                    ]
        cellPos = []
        for other in cells:
             cellPos.append((other.x, other.y))
        dead = self.difference(candidates, cellPos)
        return dead  
  
    #The set difference of two lists a nd b
    #(assuming the lists meet set conditions of
    # uniqueness)
    def difference(self, a,b):
        b = set(b)
        return [aa for aa in a if aa not in b]            
        
    #The main portion of life, a single step through the
    #reproduction routine
    def step(self, cells):
        dead = []
        toRemove = []
        toAdd = []
        for cell in cells:
            dead.extend(self.adjacentPoints(cell, cells))
        for (x,y) in dead:
            candidate = Cell(x,y)
            adjs = self.adjacentCells(candidate, cells)
            bordering = len(adjs)
            if bordering == 3: toAdd.append(candidate)
        for cell in cells:
            adjs = self.adjacentCells(cell, cells)
            bordering = len(adjs)
            if (bordering < 2) or (bordering > 3): toRemove.append(cell)
        for cell in toRemove:
            cells.remove(cell)
        for cell in set(toAdd):
            cells = self.addCell(cell.x, cell.y, cells)
        self.fillCells(cells) 
        return cells 
          
    #Used for manipulating the terminal cursor for cell placement
    def mv_term_cursor(self, ux, uy):
            self.stdscr.move(uy,ux)

    def setupWindowSize(self, w, h):
        width = 50
        height = 30
        try:
            width = int(w)
            height = int(h)
        except:
            raise Exception("Failed to interpret arguments as integers")
        if width < 5 or height < 5:
            raise Exception("The minimum dimensions available are 5, please enter values greater than this")
        return width, height

#A cell is a currently active cell in the game,
#represented by a zero character at some x and
#y position
class Cell:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def fill(self, stdscr):
        try:
            stdscr.addch( self.y, self.x, ord('0') )
        except curses.error:
            pass


if len(argv) > 1 and len(argv) != 3:
    print "Incorrect quantity of arguments provided; please provide only width and height (i.e. both or neither)"
    print "Using defaults: width 50 height 30"
    time.sleep(3)
    w = 50
    h = 30
elif len(argv) == 3:
    this, w, h = argv
else:
    w = 50
    h = 30   

if __name__ == "__main__":
    c = Life(w, h)
    c.run()

     
