#Author: github.com/kjgorman
#The classic mathematical game of life, written in python for the
#curses augmented terminal. Because it relies on curses it is 
#unavailable for windows at this point.
import curses
import time
import math


#Sets up the curses window
def startup():
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
#Destructs the curses window and reverts key settings
def shutdown():
    curses.echo()
    curses.nocbreak()
    stdscr.keypad(0)
    curses.endwin()

#Fills in the basic background field
#TODO: only update affected cells per tick
def background(gen, nodelay):
    for y in xrange(0,height):
        for x in range(0,width):
            try:
                #the horizontal sides have pipes
                if (x == 0) | (x == width-1):
                    stdscr.addch( y, x, ord('|'))
                #the vertical sides have hypens
                elif (y == 0) | (y == height-1):
                    stdscr.addch( y, x, ord('-'))
                #and blank space are periods
                else:
                    stdscr.addch( y, x, ord('.') )
            except curses.error:
                pass
    stdscr.addstr(height, 1, "gen: "+str(gen))
    stdscr.addstr(height, 20, "[s]tep [n]ew [q]uit")
    if nodelay:
        stdscr.addstr(height, 42, "[running]")
    else:
        stdscr.addstr(height, 42, "[paused] ")
    #after drawing refresh the window
    stdscr.refresh()

#Iterates the collection of active cells and
#'fills' them into the field
def fillCells(cells):
    for cell in cells:
        cell.fill()
    stdscr.refresh()

#A cell is a currently active cell in the game,
#represented by a zero character at some x and
#y position
class Cell:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def fill(self):
        try:
            stdscr.addch( self.y, self.x, ord('0') )
        except curses.error:
            pass

#Adding a cell will ensure the set condition
#of disallowing duplicates
def addCell(x,y,cells):
    for cell in cells:
        if cell.x == x and cell.y == y:
            return cells
    cells.append(Cell(x,y))
    return cells

#Finds adjacent alive cells
def adjacentCells(cell, cells):
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
def adjacentPoints(cell, cells):
    dead = []
    candidates =[(x,y) 
                for x in [cell.x-1, cell.x, cell.x+1] if (x > 0) & (x < width-1)
                for y in [cell.y-1, cell.y, cell.y+1] if (y > 0) & (y < height-1)
                if (x,y) != (cell.x, cell.y)
                ]
    cellPos = []
    for other in cells:
         cellPos.append((other.x, other.y))
    dead = difference(candidates, cellPos)
    return dead  
  
#The set difference of two lists a nd b
#(assuming the lists meet set conditions of
# uniqueness)
def difference(a,b):
    b = set(b)
    return [aa for aa in a if aa not in b]            
    
#The main portion of life, a single step through the
#reproduction routine
def step(cells):
    dead = []
    toRemove = []
    toAdd = []
    for cell in cells:
        dead.extend(adjacentPoints(cell, cells))
    for (x,y) in dead:
        candidate = Cell(x,y)
        adjs = adjacentCells(candidate, cells)
        bordering = len(adjs)
        if bordering == 3: toAdd.append(candidate)
    for cell in cells:
        adjs = adjacentCells(cell, cells)
        bordering = len(adjs)
        if (bordering < 2) or (bordering > 3): toRemove.append(cell)
    for cell in toRemove:
        cells.remove(cell)
    for cell in set(toAdd):
        cells = addCell(cell.x, cell.y, cells)
    fillCells(cells) 
    return cells 
      
#Used for manipulating the terminal cursor for cell placement
def mv_term_cursor(ux, uy):
        #stdscr.addch( uy, ux, ord('.'))
        stdscr.move(uy,ux)

ux = 0
uy = 0
width = 50
height = 30

if __name__ == "__main__":
    stdscr = curses.initscr()
    startup()
    cells = []
    generation = 0
    nodelay = 0
    while 1:
        background(generation, nodelay)
        fillCells(cells)
        mv_term_cursor(ux, uy)
        #by default a blocking function
        #when [r] is pressed we move to
        #a timeout period of a tenth of 
        #a second for animation. 
        c = stdscr.getch()

        if c == ord('s') or nodelay:
            cells = step(cells)
            generation = generation+1
        if c == ord('r'):
            if nodelay: stdscr.timeout(-1) 
            else:       stdscr.timeout(100)
            nodelay = nodelay ^ 1
        elif c == ord('n'):         cells = addCell(ux, uy, cells)
        elif c == curses.KEY_RIGHT: ux = ux + 1 if ux < width-1 else ux
        elif c == curses.KEY_LEFT:  ux = ux - 1 if ux > 0 else ux
        elif c == curses.KEY_UP:    uy = uy - 1 if uy > 0 else uy
        elif c == curses.KEY_DOWN:  uy = uy + 1 if uy < height-1 else uy
        elif c == ord('q'):
            break
    shutdown() 
