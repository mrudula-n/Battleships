"""
Battleship Project
Name:
Roll No:
"""

import battleship_tests as test

project = "Battleship" # don't edit this

### SIMULATION FUNCTIONS ###

from tkinter import *
import random

EMPTY_UNCLICKED = 1
SHIP_UNCLICKED = 2
EMPTY_CLICKED = 3
SHIP_CLICKED = 4


'''
makeModel(data)
Parameters: dict mapping strs to values
Returns: None
'''
def makeModel(data):
    data["rows"] = 10
    data["cols"] = 10
    data["boardSize"] = 500
    data["cellSize"] = data["boardSize"]/data["rows"]
    data["numBoards"] = 2
    data["numShips"] = 5
    data["computerBoard"] = emptyGrid(data["rows"],data["cols"]) 
    data["userBoard"] = emptyGrid(data["rows"],data["cols"]) 
    #data["userBoard"] = test.testGrid()
    data["computerBoard"] = addShips(data["computerBoard"],data["numShips"]) 
    data["temporary_ship"]=[]
    data["num_User_Ship"]=0
    data["winner"]=None
    return



'''
makeView(data, userCanvas, compCanvas)
Parameters: dict mapping strs to values ; Tkinter canvas ; Tkinter canvas
Returns: None
'''
def makeView(data, userCanvas, compCanvas):
    canvas= drawGrid(data,userCanvas,data["userBoard"],True)
    userCanvas=drawShip(data,userCanvas,data["temporary_ship"])
    compCanvas= drawGrid(data,compCanvas,data["computerBoard"],True)
    if data["winner"]=="user":
        drawGameOver(data,userCanvas)
    elif data["winner"]=="comp":
        drawGameOver(data,compCanvas)
    return


'''
keyPressed(data, events)
Parameters: dict mapping strs to values ; key event object
Returns: None
'''
def keyPressed(data, event):
    pass


'''
mousePressed(data, event, board)
Parameters: dict mapping strs to values ; mouse event object ; 2D list of ints
Returns: None
'''
def mousePressed(data, event, board):
    cell=getClickedCell(data, event)
    if board=="user":
        clickUserBoard(data,cell[0],cell[1])
    elif board=="comp":
        runGameTurn(data,cell[0],cell[1])
    return

#### WEEK 1 ####

'''
emptyGrid(rows, cols)
Parameters: int ; int
Returns: 2D list of ints
'''
def emptyGrid(rows, cols):
    grid=[]
    for i in range(rows):
        col = []
        for j in range(cols):
            col.append(EMPTY_UNCLICKED)
        grid.append(col)
    return grid


'''
createShip()
Parameters: no parameters
Returns: 2D list of ints
'''
def createShip():
    row=random.randint(1,8)
    col=random.randint(1,8)
    ship=random.randint(0,1)
    emptyShip=[[]]
    if ship == 0:
        emptyShip=[[row,col-1],[row,col],[row,col+1]]
    else:
        emptyShip=[[row-1,col],[row,col],[row+1,col]]
    return emptyShip
    


'''
checkShip(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def checkShip(grid, ship):
    count=0
    for each in ship:
        column=each[0]
        row=each[1]
        if grid[column][row]==EMPTY_UNCLICKED:
            count+=1
    return count==len(ship)


'''
addShips(grid, numShips)
Parameters: 2D list of ints ; int
Returns: 2D list of ints
'''
def addShips(grid, numShips):
    count=0
    while count<numShips:
        ship=createShip()
        if checkShip(grid,ship)==True:
            for each in ship:
                column=each[0]
                row=each[1]
                grid[column][row]=SHIP_UNCLICKED
        count=count+1
    return grid



'''
drawGrid(data, canvas, grid, showShips)
Parameters: dict mapping strs to values ; Tkinter canvas ; 2D list of ints ; bool
Returns: None
'''
def drawGrid(data, canvas, grid, showShips):
    for i in range(data["rows"]):
        for j in range(data["cols"]):
            if grid[i][j]==SHIP_UNCLICKED:
                canvas.create_rectangle(data["cellSize"]*j, data["cellSize"]*i, data["cellSize"]*(j+1), data["cellSize"]*(i+1), fill="yellow")
            elif grid[i][j]==EMPTY_UNCLICKED:
                canvas.create_rectangle(data["cellSize"]*j, data["cellSize"]*i, data["cellSize"]*(j+1), data["cellSize"]*(i+1), fill="blue")
            elif grid[i][j]==SHIP_CLICKED:
                canvas.create_rectangle(data["cellSize"]*j, data["cellSize"]*i, data["cellSize"]*(j+1), data["cellSize"]*(i+1), fill="red")
            elif grid[i][j]==EMPTY_CLICKED:
                canvas.create_rectangle(data["cellSize"]*j, data["cellSize"]*i, data["cellSize"]*(j+1), data["cellSize"]*(i+1), fill="white")
            if grid[i][j]==SHIP_UNCLICKED and (showShips==False): 
                canvas.create_rectangle(data["cellSize"]*j, data["cellSize"]*i, data["cellSize"]*(j+1), data["cellSize"]*(i+1), fill="blue")
    return data


### WEEK 2 ###

'''
isVertical(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isVertical(ship):
    ship.sort()
    if ship[0][1]==ship[1][1]==ship[2][1]==ship[0][0]+1==ship[1][0]==ship[2][0]-1:
        return True
    return False



'''
isHorizontal(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isHorizontal(ship):
    ship.sort()
    if ship[0][0]==ship[1][0]==ship[2][0]==ship[0][1]+1==ship[1][1]==ship[2][1]-1:
        return True
    return False


'''
getClickedCell(data, event)
Parameters: dict mapping strs to values ; mouse event object
Returns: list of ints
'''
def getClickedCell(data, event):
    coordinate_of_x=int(event.x/data["cellSize"])
    coordinate_of_y=int(event.y/data["cellSize"])
    return[coordinate_of_y,coordinate_of_x]

'''
drawShip(data, canvas, ship)
Parameters: dict mapping strs to values ; Tkinter canvas; 2D list of ints
Returns: None
'''
def drawShip(data, canvas, ship):
    for row in range(len(ship)):
        canvas.create_rectangle(data["cellSize"]*ship[row][1],data["cellSize"]*ship[row][0],data["cellSize"]*(ship[row][1]+1),data["cellSize"]*(ship[row][0]+1),fill="white")
    return

'''
shipIsValid(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def shipIsValid(grid, ship):
    if checkShip(grid, ship):
        if isVertical(ship) or isHorizontal(ship):
            return True
    return False

'''
placeShip(data)
Parameters: dict mapping strs to values
Returns: None
'''
def placeShip(data):
    if shipIsValid(data["userBoard"],data["temporary_ship"]):
        for ship in data["temporary_ship"]:
            data["userBoard"][ship[0]][ship[1]]=SHIP_UNCLICKED
        data["num_User_Ship"]+=1
    else:
        print("ship is not valid")
    data["temporary_ship"]=[]
    return


'''
clickUserBoard(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def clickUserBoard(data, row, col):
    if data["num_User_Ship"]==5:
        print("you can start the game")
        return
    if [row, col] not in data["temporary_ship"]:
        data["temporary_ship"].append([row, col])
        if len(data["temporary_ship"])==3:
            placeShip(data)
    return


### WEEK 3 ###

'''
updateBoard(data, board, row, col, player)
Parameters: dict mapping strs to values ; 2D list of ints ; int ; int ; str
Returns: None
'''
def updateBoard(data, board, row, col, player):
    if board==data["computerBoard"] or data["userBoard"]:
        if board[row][col]==SHIP_UNCLICKED:
            board[row][col]=SHIP_CLICKED
        elif board[row][col]==EMPTY_UNCLICKED:
            board[row][col]=EMPTY_CLICKED
    if isGameOver(board):
        data["winner"]=player
    return


'''
runGameTurn(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def runGameTurn(data, row, col):
    if (data["computerBoard"][row][col]==SHIP_CLICKED) or (data["computerBoard"][row][col]==EMPTY_CLICKED):
        return
    else:
        updateBoard(data,data["computerBoard"],row,col,"user")
    compGuess=getComputerGuess(data["userBoard"])
    updateBoard(data,data["userBoard"],compGuess[0],compGuess[1],"comp")
    

'''
getComputerGuess(board)
Parameters: 2D list of ints
Returns: list of ints
'''
def getComputerGuess(board):
    clickCell=0
    while(clickCell<1):
        i=random.randint(0,9)
        j=random.randint(0,9)
        if(board[i][j]==SHIP_UNCLICKED) or (board[i][j]==EMPTY_UNCLICKED):
                clickCell=clickCell+1
                return[i,j]


'''
isGameOver(board)
Parameters: 2D list of ints
Returns: bool
'''
def isGameOver(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j]==SHIP_UNCLICKED:
                return False
    return True


'''
drawGameOver(data, canvas)
Parameters: dict mapping strs to values ; Tkinter canvas
Returns: None
'''
def drawGameOver(data, canvas):
    if (data["winner"]=="user"):
        canvas.create_text(100, 50, text="congratulations... you won the game!", fill="black", font=("Times New Roman 15 bold"))
    if (data["winner"]=="comp"):
        canvas.create_text(100, 50, text="You lost the game...Try again!", fill="black", font=("Times New Roman 15 bold"))
    return


### SIMULATION FRAMEWORK ###

from tkinter import *

def updateView(data, userCanvas, compCanvas):
    userCanvas.delete(ALL)
    compCanvas.delete(ALL)
    makeView(data, userCanvas, compCanvas)
    userCanvas.update()
    compCanvas.update()

def keyEventHandler(data, userCanvas, compCanvas, event):
    keyPressed(data, event)
    updateView(data, userCanvas, compCanvas)

def mouseEventHandler(data, userCanvas, compCanvas, event, board):
    mousePressed(data, event, board)
    updateView(data, userCanvas, compCanvas)

def runSimulation(w, h):
    data = { }
    makeModel(data)

    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window

    # We need two canvases - one for the user, one for the computer
    Label(root, text = "USER BOARD - click cells to place ships on your board.").pack()
    userCanvas = Canvas(root, width=w, height=h)
    userCanvas.configure(bd=0, highlightthickness=0)
    userCanvas.pack()

    compWindow = Toplevel(root)
    compWindow.resizable(width=False, height=False) # prevents resizing window
    Label(compWindow, text = "COMPUTER BOARD - click to make guesses. The computer will guess on your board.").pack()
    compCanvas = Canvas(compWindow, width=w, height=h)
    compCanvas.configure(bd=0, highlightthickness=0)
    compCanvas.pack()

    makeView(data, userCanvas, compCanvas)

    root.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    compWindow.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    userCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "user"))
    compCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "comp"))

    updateView(data, userCanvas, compCanvas)

    root.mainloop()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    # test.testIsGameOver()
    ## Finally, run the simulation to test it manually ##
    runSimulation(500, 500)
