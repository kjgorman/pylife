import life
import sys

def adjacency():
    print "Testing adjacency"
    cells = []
    sys.stdout.write("Populating...")
    for i in xrange(0,10):
        sys.stdout.write(str(i)+" ")
        cells.append(life.Cell(i,i))
    sys.stdout.write("\n")
    failed = 0 
    for cell in cells:
        adj = life.adjacentCells(cell, cells)
        bordering = len(adj)
        if bordering != 2 and not (cell.x == 0 or cell.x == 9):
            print "Test failed on cell: ", cell.x, cell.y
            failed = failed+1
    print "Test passed with ", str(len(cells)-failed), " of ", str(len(cells)), " successful"
    return 1 if failed == 0 else 0

def adjacentDeadPoints():
    print "Testing for adjacent dead points" 
    cell = life.Cell(10,10)
    cells = [cell]
    points = life.adjacentPoints(cell, cells)
    if len(points) != 8:
        print "Test failed, expected 8 adjacent points but found: ", str(len(points))
        return 0
    else:
        print "Test passed with 8 adjacent points"
    print "Adding cell"
    cells.append(life.Cell(10,11))
    points = life.adjacentPoints(cell, cells)
    if len(points) != 7:
        print "Test failed, expected 7 adjacent points but found: ", str(len(points))        
        return 0
    else:
        print "Test passed with 7 adjacent points"
        return 1

def testDeath():
    print "Test singleton cell death"
    cells = []
    cells.append(life.Cell(10,10))
    try:
        cells = life.step(cells)
    except: #stdscr is not defined
        pass
    if len(cells) != 0:
        print "Test failed, cell alive"
        return 0
    else:
        print "Test passed"
        return 1

def testSpawn():
    print "Testing cell spawning"
    cells = []
    cells.append(life.Cell(10,10))
    cells.append(life.Cell(11,10))
    cells.append(life.Cell(10,11))
    #   00
    #   0  <-- should spawn at 11,11  
    try:
        cells = life.step(cells)
    except: #stdcr is not defined
        pass
    if len(cells) != 4:
        print "Test failed, no new cell, cells length is now: ", str(len(cells))
        return 0
    else:
        sys.stdout.write("Cell spawned")
        correct_pos = False
        for cell in cells:
            if cell.x == 11 and cell.y == 11:
                print " correctly"
                correct_pos = True
                break
        if not correct_pos:
            print " incorrectly"
        print "Test passed" if correct_pos else "Test failed"
    return 1 if correct_pos else 0

def testBlinker():
    print "Testing the 'blinker'"
    cells = []
    cells.append(life.Cell(10,10))
    cells.append(life.Cell(10,11))
    cells.append(life.Cell(10,12))
    print "Cells before step:"
    for cell in cells:
         print "("+str(cell.x)+","+str(cell.y)+")"
    try:
         cells = life.step(cells)
    except:
        pass
    print "Cells after step:"
    for cell in cells:
         print "("+str(cell.x)+","+str(cell.y)+")"
    if not containsCellAt(9,11,cells):
        print "Test failed, did not spawn left hand side"
        return 0
    if not containsCellAt(11,11,cells):
        print "Test failed, did not spawn right hand side"
        return 0
    if not containsCellAt(10,11,cells):
        print "Test failed, did not persist centre"
        return 0
    print "Test passed"
    return 1

def containsCellAt(x,y,cells):
    for cell in cells:
        if cell.x == x and cell.y == y:
            return True
    return False

def runTests():
    tests = [adjacency,adjacentDeadPoints,testDeath,testSpawn,testBlinker]
    passed = 0
    for func in tests:
        passed = passed + func()
        print "================================================"
    print "Tests completed with "+str(passed)+" of "+str(len(tests))+" successful"
runTests()
