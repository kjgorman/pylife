import life
import sys

#utility
def containsCellAt(x,y,cells):
    for cell in cells:
        if cell.x == x and cell.y == y:
            return True
    return False


def adjacency():
    print "Testing adjacency"
    model = life.Life(50,50)
    cells = []
    sys.stdout.write("Populating...")
    for i in xrange(0,10):
        sys.stdout.write(str(i)+" ")
        cells.append(life.Cell(i,i))
    sys.stdout.write("\n")
    failed = 0 
    for cell in cells:
        adj = model.adjacentCells(cell, cells)
        bordering = len(adj)
        if bordering != 2 and not (cell.x == 0 or cell.x == 9):
            print "Test failed on cell: ", cell.x, cell.y
            failed = failed+1
    print "Test passed with ", str(len(cells)-failed), " of ", str(len(cells)), " successful"
    return 1 if failed == 0 else 0

def adjacentDeadPoints():
    print "Testing for adjacent dead points" 
    model = life.Life(50,50)
    cell = life.Cell(10,10)
    cells = [cell]
    points = model.adjacentPoints(cell, cells)
    if len(points) != 8:
        print "Test failed, expected 8 adjacent points but found: ", str(len(points))
        return 0
    else:
        print "Test passed with 8 adjacent points"
    print "Adding cell"
    cells.append(life.Cell(10,11))
    points = model.adjacentPoints(cell, cells)
    if len(points) != 7:
        print "Test failed, expected 7 adjacent points but found: ", str(len(points))        
        return 0
    else:
        print "Test passed with 7 adjacent points"
        return 1

def testDeath():
    print "Test singleton cell death"
    model = life.Life(50,50)
    cells = []
    cells.append(life.Cell(10,10))
    try:
        cells = model.step(cells)
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
    model = life.Life(50,50)
    cells = []
    cells.append(life.Cell(10,10))
    cells.append(life.Cell(11,10))
    cells.append(life.Cell(10,11))
    #   00
    #   0  <-- should spawn at 11,11  
    try:
        cells = model.step(cells)
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
    model = life.Life(50,50)
    cells = []
    cells.append(life.Cell(10,10))
    cells.append(life.Cell(10,11))
    cells.append(life.Cell(10,12))
    print "Cells before step:"
    for cell in cells:
         print "("+str(cell.x)+","+str(cell.y)+")"
    try:
         cells = model.step(cells)
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

def testWindowDimensions():
    print "Test negative dimensions"
    passed = 0
    try:
        model = life.Life(-1,10)
        model.run()
        
    except:
        print "Test passed"
        passed = passed + 1
    
    try:
        print "Test dimensions less than limit (5,5)"
        model = life.Life(4, 3)
        
    except:
        print "Test passed"
        passed = passed + 1

    try:
        print "Test dimensions that are valid"
        model = life.Life(20,20)
        passed = passed + 1
    except:
        print "Test failed"
        
    print "Dimension tests completed with " + str(passed) + " of 3 successful"
    return 1 if passed == 3 else 0

def runTests():
    tests = [adjacency,adjacentDeadPoints,testDeath,testSpawn,testBlinker, testWindowDimensions]
    passed = 0
    for func in tests:
        passed = passed + func()
        print "================================================"
    print "Tests completed with "+str(passed)+" of "+str(len(tests))+" successful"

if __name__ == "__main__":
    runTests()
 
