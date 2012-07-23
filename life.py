import curses
import time

stdscr = curses.initscr()
#pad = curses.newpad(100,100)
cells = []
ux = 0
uy = 0
width = 50
height = 30

def startup():
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)

def shutdown():
    curses.echo()
    curses.nocbreak()
    stdscr.keypad(0)
    curses.endwin()

def background():
    for y in xrange(0,height):
        for x in range(0,width):
            try:
                if (x == 0) | (x == width-1):
                    stdscr.addch( y, x, ord('|'))
                else:
                    stdscr.addch( y, x, ord('.') )
            except curses.error:
                pass
    stdscr.refresh()

def fillCells():
    for cell in cells:
        cell.fill()
    stdscr.refresh()

class Cell:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def fill(self):
        try:
            stdscr.addch( self.y, self.x, ord('0') )
        except curses.error:
            pass

def step():
    fillCells()        
def mv_term_cursor(ux, uy):
        stdscr.addch( uy, ux, ord('.'))

startup()
cells.append(Cell(25,25))
while 1:
    background()
    fillCells()
    mv_term_cursor(ux, uy)
    c = stdscr.getch()
    if c == ord('s'):
        step()
    elif c == curses.KEY_RIGHT: ux = ux + 1 if ux < width-1 else ux
    elif c == curses.KEY_LEFT:  ux = ux - 1 if ux > 0 else ux
    elif c == curses.KEY_UP:    uy = uy - 1 if uy > 0 else uy
    elif c == curses.KEY_DOWN:  uy = uy + 1 if uy < height-1 else uy
    elif c == ord('q'):
        break

shutdown()
