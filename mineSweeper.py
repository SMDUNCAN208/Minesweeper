#Minesweeper
#Sophia Duncan
#class mineSweeperModule(object) :

import random, pygame, sys
from pygame.locals import *

pygame.init()

class ABox (object) :
    global clicked, mine, posX, posY, width, height, flag

    #The positions are to create a box layout. (left x, top x, box width, box height)
    def __init__(self, _posX, _posY, _width, _height) :
        self.clicked = False
        self.mine = False
        self.posX = _posX
        self.posY = _posY
        self.width = _width
        self.height = _height
        self.flag = False

    def isClicked(self):
        return self.clicked

    def hasMine(self):
        return self.mine

    def changeMine(self) :
        self.mine = True

    def changeClicked(self):
        self.clicked = True

    def getXPosOne (self):
        return self.posX

    def getYPosOne(self):
        return self.posY

    def getXPosTwo (self):
        return self.width

    def getYPosTwo(self):
        return self.height

    def flagged(self):
        return self.flag

    def changeFlagged(self):
        if self.flag == False :
            self.flag = True
        elif self.flag == True :
            self.flag = False

boxes = []

fps = 30
windowWidth = 960 #The window is 1000 x 800
windowHeight = 760 #There needs to be 950 x 950 for the boxes
boxHeight = 45 #The boxes are 50 x 50
gapSize = 3 #There is a 10 pixel gap inbetween boxes
boxRows = 16 #There are 16 boxes across
boxColumns = 16 #There are 16 boxes down

#Determining the empty space
xMargin = 200
yMargin = 1050

boxNum = 16

mines = 15


#Colours (  r,   g,   b)
grey    = (200, 200, 200)
greyTwo = (140, 140, 140)
black   = (0  ,   0,   0)
white   = (255, 255, 255)
blue    = (102, 102, 255)
blueTwo = (102, 150, 255)
flagged = (175, 144, 205)
yellow  = (255, 255, 103)
tan     = (253, 240, 228)

MINEHIT = False

#Fonts
fontObj = pygame.font.Font('freesansbold.ttf', 28)
fontObjTwo = pygame.font.Font('freesansbold.ttf', 16)
fontObjThree = pygame.font.Font('freesansbold.ttf', 20)

SCREEN = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Minesweeper')

audioMain = pygame.mixer_music.load('home.mp3')

def main () :
    draw(windowWidth, windowHeight)
    timesClicked = 0

    global points
    points = 0

    mouseX = 0 #Stores the mouse's x position
    mouseY = 0 #Stores the mouse's y position

    global ended
    ended = False #Shows whether the game is still is in play


    #Sets the board up
    setBoard()
    undoX = 200
    undoY = 0

    # pygame.mixer_music.load('SkillsAudio.wav')
    pygame.mixer_music.play(-1, 0.0)
    while True : #Event loop
        for event in pygame.event.get():
            if ended == False and points != (boxNum * boxNum) - mines :
                if event.type == MOUSEMOTION :
                    undoHighlight(undoX, undoY)
                    mouseX, mouseY = event.pos
                    highlight(mouseX, mouseY)
                    undoX = mouseX
                    undoY = mouseY
                    #print(str(mouseX) + ' and ' + str(mouseY))
                elif event.type == MOUSEBUTTONUP and event.button == BUTTON_LEFT:
                    mouseX, mouseY = event.pos
                    indexX = (mouseX - 200) // 48  #Used to get the x box position. (mouse position - margin // box + line size)
                    indexY = mouseY // 48 #Used to get the y box position (mouse position // box + line size)
                    if timesClicked == 0 :
                        addMines(mines, indexX, indexY)
                        timesClicked += 1
                    openBox(indexX, indexY)
                    #The following code will show mouse position
                    #print('mouseclicked')
                    #print(str(mouseX) + ' and ' + str(mouseY))
                elif event.type == MOUSEBUTTONUP and event.button == BUTTON_RIGHT:
                    indexX = (mouseX - 200) // 48  # Used to get the x box position. (mouse position - margin // box + line size)
                    indexY = mouseY // 48  # Used to get the y box position (mouse position // box + line size)
                    flagBox(indexX, indexY, mouseX, mouseY)
                elif event.type == KEYUP and event.key == pygame.K_SPACE :
                    indexX = (mouseX - 200) // 48  # Used to get the x box position. (mouse position - margin // box + line size)
                    indexY = mouseY // 48  # Used to get the y box position (mouse position // box + line size)
                    flagReveal(indexX, indexY)
                elif event.type == QUIT or (event.type == KEYUP and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
            elif ended == True and event.type == MOUSEMOTION :
                xCentre = (windowWidth + 200) / 2
                mouseX, mouseY = event.pos
                if mouseX >= xCentre - 90 and mouseX <= xCentre - 10 and mouseY >= 375 and mouseY <= 415:
                    yesDrawing(grey)
                elif mouseX >= xCentre + 14 and mouseX <= xCentre + 94 and mouseY >= 375 and mouseY <= 415:
                    noDrawing(grey)
                else :
                    yesDrawing(white)
                    noDrawing((white))
            elif ended == True and event.type == MOUSEBUTTONUP:
                if event.type == MOUSEBUTTONUP :
                    mouseX, mouseY = event.pos
                    xCentre = (windowWidth + 200) / 2
                    #Checks if the user clicks to play again and then restarts the game
                    if mouseX >= xCentre - 90 and mouseX <= xCentre - 10 and mouseY >= 375 and mouseY <= 415 :
                        ended = False
                        boxes.clear()
                        setBoard()
                        draw(windowWidth, windowHeight)
                        undoX = 200
                        undoY = 0
                        points = 0
                        timesClicked = 0
                    #Quits the game if the user decides not to play again
                    elif mouseX >= xCentre + 14 and mouseX <= xCentre + 94 and mouseY >= 375 and mouseY <= 415 :
                        pygame.quit()
                        sys.exit()
            elif points == (boxNum * boxNum) - mines :
                endGame(False, white)
            elif event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            pygame.display.update()


def flagReveal(clickedX, clickedY) :
    if (boxes[clickedX][clickedY].isClicked() == True) :
        minesFlagged = True
        xValues = []
        yValues = []
        if clickedX != 0 and clickedY != 0 and clickedX != boxNum - 1 and clickedY != boxNum - 1:
            # Loops through inside boxes. NOT those on the edges
            for i in range(clickedX - 1, clickedX + 2, 1):
                for j in range(clickedY - 1, clickedY + 2, 1):
                    # if i != clickedX and j != clickedY : #Checks the program isn't checking the clicked tile
                    if boxes[i][j].flagged() == False and boxes[i][j].isClicked() != True and boxes[i][j].hasMine() != True:
                        openBox(i,j)
                    elif boxes[i][j].flagged() == False and boxes[i][j].isClicked() != True and boxes[i][j].hasMine() == True:
                        xValues.append(i)
                        yValues.append(j)
        # Left edge, not corner
        elif clickedX == 0 and clickedY != 0 and clickedY != boxNum - 1:
            for i in range(clickedX, clickedX + 2, 1):
                for j in range(clickedY - 1, clickedY + 2, 1):
                    # if i != clickedX and j != clickedY : #Checks the program isn't checking the clicked tile
                    if boxes[i][j].flagged() == False and boxes[i][j].isClicked() != True:
                        openBox(i, j)
                    elif boxes[i][j].flagged() == False and boxes[i][j].isClicked() != True and boxes[i][j].hasMine() == True:
                        xValues.append(i)
                        yValues.append(j)
        # Right edge, not corner
        elif clickedX == boxNum - 1 and clickedY != 0 and clickedY != boxNum - 1:
            for i in range(clickedX - 1, clickedX + 1, 1):
                for j in range(clickedY - 1, clickedY + 2, 1):
                    # if i != clickedX and j != clickedY : #Checks the program isn't checking the clicked tile
                    if boxes[i][j].flagged() == False and boxes[i][j].isClicked() != True:
                        openBox(i, j)
                    elif boxes[i][j].flagged() == False and boxes[i][j].isClicked() != True and boxes[i][j].hasMine() == True:
                        xValues.append(i)
                        yValues.append(j)
        # Top edge, not corner
        elif (clickedX != 0 and clickedX != boxNum - 1 and clickedY == 0):
            for i in range(clickedX - 1, clickedX + 2, 1):
                for j in range(clickedY, clickedY + 2, 1):
                    # if i != clickedX and j != clickedY : #Checks the program isn't checking the clicked tile
                    if boxes[i][j].flagged() == False and boxes[i][j].isClicked() != True:
                        openBox(i, j)
                    elif boxes[i][j].flagged() == False and boxes[i][j].isClicked() != True and boxes[i][j].hasMine() == True:
                        xValues.append(i)
                        yValues.append(j)
        # Bottom edge, not corner
        elif clickedX != 0 and clickedX != boxNum - 1 and clickedY == boxNum - 1:
            for i in range(clickedX - 1, clickedX + 2, 1):
                for j in range(clickedY - 1, clickedY + 1, 1):
                    # if i != clickedX and j != clickedY : #Checks the program isn't checking the clicked tile
                    if boxes[i][j].flagged() == False and boxes[i][j].isClicked() != True:
                        openBox(i, j)
                    elif boxes[i][j].flagged() == False and boxes[i][j].isClicked() != True and boxes[i][j].hasMine() == True:
                        xValues.append(i)
                        yValues.append(j)
        # Top left corner
        elif clickedX == 0 and clickedY == 0:
            for i in range(clickedX, clickedX + 2, 1):
                for j in range(clickedY, clickedY + 2, 1):
                    # if i != clickedX and j != clickedY : #Checks the program isn't checking the clicked tile
                    if boxes[i][j].flagged() == False and boxes[i][j].isClicked() != True:
                        openBox(i, j)
                    elif boxes[i][j].flagged() == False and boxes[i][j].isClicked() != True and boxes[i][j].hasMine() == True:
                        xValues.append(i)
                        yValues.append(j)
        # Bottom left corner
        elif clickedX == 0 and clickedY == boxNum - 1:
            for i in range(clickedX, clickedX + 2, 1):
                for j in range(clickedY - 1, clickedY + 1, 1):
                    # if i != clickedX and j != clickedY : #Checks the program isn't checking the clicked tile
                    if boxes[i][j].flagged() == False and boxes[i][j].isClicked() != True:
                        openBox(i, j)
                    elif boxes[i][j].flagged() == False and boxes[i][j].isClicked() != True and boxes[i][j].hasMine() == True:
                        xValues.append(i)
                        yValues.append(j)
        # Top right corner
        elif clickedX == boxNum - 1 and clickedY == 0:
            for i in range(clickedX - 1, clickedX + 1, 1):
                for j in range(clickedY, clickedY + 2, 1):
                    # if i != clickedX and j != clickedY : #Checks the program isn't checking the clicked tile
                    if boxes[i][j].flagged() == False and boxes[i][j].isClicked() != True:
                        openBox(i, j)
                    elif boxes[i][j].flagged() == False and boxes[i][j].isClicked() != True and boxes[i][j].hasMine() == True:
                        xValues.append(i)
                        yValues.append(j)
        # Bottom right corner
        elif clickedX == boxNum - 1 and clickedY == boxNum - 1:
            for i in range(clickedX - 1, clickedX + 1, 1):
                for j in range(clickedY - 1, clickedY + 1, 1):
                    # if i != clickedX and j != clickedY : #Checks the program isn't checking the clicked tile
                    if boxes[i][j].flagged() == False and boxes[i][j].isClicked() != True:
                        openBox(i, j)
                    elif boxes[i][j].flagged() == False and boxes[i][j].isClicked() != True and boxes[i][j].hasMine() == True:
                        xValues.append(i)
                        yValues.append(j)

        if len(xValues) != 0 :
            openBox(xValues[0], yValues[0])



#Sets the board up [add difficulties? Add in a number input for the method or update mines]
def setBoard() :
    global boxes
    # Makes a list filled with lists
    for i in range(0, boxNum, 1):
        boxes.append([])

    x = 200
    y = 0
    for i in range(0, boxNum, 1):
        xTemp = x
        x += boxHeight + gapSize
        y = 0
        for j in range(0, boxNum, 1):
            boxes[i].append(ABox(xTemp, y, boxHeight, boxHeight))  # Putting the box positions in
            y += boxHeight + gapSize

def undoHighlight(x,y) :
    newX = (((x - 200) // 48) * 48 + 200)
    newY = (y // 48) * 48
    boxX = (x - 200) // 48
    boxY = y // 48
    if boxes[boxX][boxY].flagged() == False:
        if (x >= 200):
            if boxes[boxX][boxY].isClicked() == False:
                pygame.draw.rect(SCREEN, blue, (newX, newY, boxHeight - 1, boxHeight - 1))
                pygame.display.update()

#Input x and y mouse position
def highlight(x, y) :
    newX = (((x - 200)//48) * 48 + 200)
    newY = (y // 48) * 48
    boxX = (x - 200) // 48
    boxY = y // 48
    if boxes[boxX][boxY].flagged() == False :
        if (x >=200) :
            if boxes[boxX][boxY].isClicked() == False :
                pygame.draw.rect(SCREEN,blueTwo, (newX, newY, boxHeight - 1, boxHeight - 1))
                pygame.display.update()



#Adds mines into the board
def addMines (mineNum, x, y) :
    addedMines = 0 #Counts how many mines have been added
    original = [x, y]
    #Loops through until the number of mines are added
    for i in range(0, mineNum, 1) :
        mineAdded = False #To make sure a mine is added
        while mineAdded == False :
            randX = random.randrange(0, boxNum)
            randY = random.randrange(0, boxNum)
            temp = [randX, randY]
            #Only runs if there hasn't been a mine added to the box
            if boxes[randX][randY].hasMine() == False and original != temp:
                mineAdded = True
                boxes[randX][randY].changeMine()
                addedMines += 1
                pygame.display.update()


def openBox(boxX, boxY) :
    if boxes[boxX][boxY].flagged() == False :
        if boxes[boxX][boxY].isClicked() == False and boxes[boxX][boxY].hasMine() == False:
            boxes[boxX][boxY].changeClicked()
            pygame.draw.rect(SCREEN, blueTwo, ((boxX * 48) + 200, boxY * 48, boxHeight - 1, boxHeight - 1))
            touchingMines = surroundingMines(boxX, boxY) #Is the number of mines the box is touching
            global points
            points += 1

            pygame.draw.rect(SCREEN, tan, (0, 50, 200, 300)) #Clears the previous point count

            pointsText = fontObjTwo.render(str(points), True, black)  # The Minesweeper text
            pointsWidth = pointsText.get_width()
            SCREEN.blit(pointsText, ((200 - pointsWidth)/2, 100))

            #Keeps instructions on the board
            flagText = fontObjTwo.render('Right clicked : flag box', True, black)
            clickText = fontObjTwo.render('Left click : open box', True, black)
            openText = fontObjTwo.render('Space bar : open ', True, black)
            openTextTwo = fontObjTwo.render('surrounding boxes', True, black)

            SCREEN.blit(clickText, (5, 200))
            SCREEN.blit(flagText, (5, 250))
            SCREEN.blit(openText, (5, 300))
            SCREEN.blit(openTextTwo, (5, 325))
            pygame.display.update()
        elif boxes[boxX][boxY].hasMine() == True :
            MINEHIT = True
            endGame(MINEHIT, white)

#Marks a box as flagged
def flagBox(boxX, boxY, x, y) :
    temp = boxes[boxX][boxY].flagged()
    boxes[boxX][boxY].changeFlagged()
    if temp == False :
        changeColour(flagged, x, y)
    elif temp == True :
        undoHighlight(x,y)

def changeColour(colour, x, y) :
    newX = (((x - 200) // 48) * 48 + 200)
    newY = (y // 48) * 48
    boxX = (x - 200) // 48
    boxY = y // 48
    if (x >= 200):
        if boxes[boxX][boxY].isClicked() == False:
            pygame.draw.rect(SCREEN, flagged, (newX, newY, boxHeight - 1, boxHeight - 1))
            pygame.display.update()

#Gets any mines surrounding the box and prints them
def surroundingMines(clickedX, clickedY) :
    counter = 0
    minesFlagged = True
    if clickedX != 0 and clickedY != 0 and clickedX != boxNum - 1 and clickedY != boxNum - 1:
        #Loops through inside boxes. NOT those on the edges
        for i in range(clickedX - 1, clickedX + 2, 1) :
            for j in range(clickedY - 1, clickedY + 2, 1) :
                #if i != clickedX and j != clickedY : #Checks the program isn't checking the clicked tile
                if boxes[i][j].hasMine() == True :
                    counter = counter + 1
                    if boxes[i][j].flagged() != True :
                        minesFlagged = False
    #Left edge, not corner
    elif clickedX == 0 and clickedY != 0  and clickedY != boxNum - 1:
        for i in range(clickedX,  clickedX + 2, 1) :
            for j in range(clickedY - 1, clickedY + 2, 1):
                #if i != clickedX and j != clickedY : #Checks the program isn't checking the clicked tile
                if boxes[i][j].hasMine() == True :
                    counter = counter + 1
    #Right edge, not corner
    elif clickedX == boxNum - 1and clickedY != 0 and clickedY != boxNum - 1 :
        for i in range(clickedX - 1, clickedX +  1, 1):
            for j in range(clickedY - 1, clickedY + 2, 1) :
                #if i != clickedX and j != clickedY : #Checks the program isn't checking the clicked tile
                if boxes[i][j].hasMine() == True :
                    counter = counter + 1
    #Top edge, not corner
    elif (clickedX != 0 and clickedX != boxNum - 1 and clickedY == 0 ):
        for i in range(clickedX - 1, clickedX + 2, 1):
            for j in range(clickedY, clickedY + 2, 1) :
                #if i != clickedX and j != clickedY : #Checks the program isn't checking the clicked tile
                if boxes[i][j].hasMine() == True :
                    counter = counter + 1
    #Bottom edge, not corner
    elif clickedX != 0 and clickedX != boxNum - 1 and clickedY == boxNum - 1:
        for i in range(clickedX - 1, clickedX + 2, 1):
            for j in range(clickedY - 1, clickedY + 1, 1):
                #if i != clickedX and j != clickedY : #Checks the program isn't checking the clicked tile
                if boxes[i][j].hasMine() == True :
                    counter = counter + 1
    #Top left corner
    elif clickedX == 0 and clickedY == 0:
        for i in range(clickedX, clickedX + 2, 1) :
            for j in range(clickedY, clickedY + 2, 1) :
                #if i != clickedX and j != clickedY : #Checks the program isn't checking the clicked tile
                if boxes[i][j].hasMine() == True :
                    counter = counter + 1
    #Bottom left corner
    elif clickedX == 0 and clickedY == boxNum - 1:
        for i in range(clickedX, clickedX + 2, 1):
            for j in range(clickedY - 1, clickedY + 1, 1):
                #if i != clickedX and j != clickedY : #Checks the program isn't checking the clicked tile
                if boxes[i][j].hasMine() == True :
                    counter = counter + 1
    #Top right corner
    elif clickedX == boxNum - 1 and clickedY == 0 :
        for i in range(clickedX - 1, clickedX + 1, 1) :
            for j in range(clickedY, clickedY + 2, 1):
                #if i != clickedX and j != clickedY : #Checks the program isn't checking the clicked tile
                if boxes[i][j].hasMine() == True :
                    counter = counter + 1
    #Bottom right corner
    elif clickedX == boxNum - 1 and clickedY == boxNum - 1 :
        for i in range(clickedX - 1, clickedX + 1, 1):
            for j in range(clickedY - 1, clickedY + 1, 1) :
                #if i != clickedX and j != clickedY : #Checks the program isn't checking the clicked tile
                if boxes[i][j].hasMine() == True :
                    counter = counter + 1

    xCentre = (clickedX * 48) + 200 + 24
    yCentre = (clickedY * 48) + 24

    mineText = fontObj.render(str(counter), True, yellow)  # The Minesweeper text
    mineTextSurface = mineText.get_rect()
    mineTextSurface.center = (xCentre, yCentre)
    SCREEN.blit(mineText, mineTextSurface)
    pygame.display.update()

    if counter == 0 :
        expansion(clickedX, clickedY)
    return counter

#Occurs when the user hits a mine
def endGame(hit, buttonColour) :
    global ended
    ended = True

    randCounter = 0
    for i in range(0, boxNum, 1) :
        for j in range(0, boxNum, 1) :
            if (boxes[i][j].hasMine() == True) :
                randCounter += 1
                image = pygame.image.load("mine.png").convert_alpha()
                image = pygame.transform.scale(image, (boxHeight,boxHeight))
                SCREEN.blit(image, (boxes[i][j].getXPosOne(), boxes[i][j].getYPosOne()))

    #Makes the screen darker
    opaque = (0, 0, 0, 25)  # Black

    screenTwo = pygame.Surface((windowHeight, windowHeight))
    screenTwo.set_alpha(150)
    screenTwo.fill((0, 0, 0))

    SCREEN.blit(screenTwo, (200, 0))

    if hit == False :
        win()
    elif hit == True :
        lose()
    repeatText = fontObj.render('Would you like to play again?', True, black, white)
    repeatTextSurface = repeatText.get_rect()
    repeatTextSurface.center = ((windowWidth + 200) / 2, 325)
    SCREEN.blit(repeatText, repeatTextSurface)

    yesDrawing((buttonColour))
    noDrawing((buttonColour))

def yesDrawing(buttonColour) :
    xCentre = (windowWidth + 200) / 2
    # Create a bordered yes and no box
    pygame.draw.rect(SCREEN, yellow, (xCentre - 92, 373, 84, 44))
    pygame.draw.rect(SCREEN, buttonColour, (xCentre - 90, 375, 80, 40))

    # Prints out the yes and no
    yesText = fontObjThree.render('Yes', True, black)
    yesTextSurface = yesText.get_rect()
    yesTextSurface.center = (xCentre - 50, 395)
    SCREEN.blit(yesText, yesTextSurface)

def noDrawing(buttonColour) :
    xCentre = (windowWidth + 200) / 2
    # Create a bordered yes and no box
    pygame.draw.rect(SCREEN, yellow, (xCentre + 12, 373, 84, 44))
    pygame.draw.rect(SCREEN, buttonColour, (xCentre + 14, 375, 80, 40))

    noText = fontObjThree.render('No', True, black)
    noTextSurface = noText.get_rect()
    noTextSurface.center = (xCentre + 55, 395)
    SCREEN.blit(noText, noTextSurface)

#Used when the user completes the game
def win() :
    winText = fontObj.render('You have won!', True, black, white)
    winTextSurface = winText.get_rect()
    winTextSurface.center = ((windowWidth + 200) / 2, (windowHeight / 2) - 200)
    SCREEN.blit(winText, winTextSurface)

def lose() :
    loseText = fontObj.render('You have lost', True, black, white)
    loseTextSurface = loseText.get_rect()
    loseTextSurface.center = ((windowWidth + 200) / 2, (windowHeight / 2) - 200)
    SCREEN.blit(loseText, loseTextSurface)

#Expands when there are no mines surrounding the box clicked
def expansion(clickedX, clickedY) :
    if clickedX != 0 and clickedY != 0 and clickedX != boxNum - 1 and clickedY != boxNum - 1:
        #Loops through inside boxes. NOT those on the edges
        for i in range(clickedX - 1, clickedX + 2, 1) :
            for j in range(clickedY - 1, clickedY + 2, 1) :
                if boxes[i][j].isClicked() == False:
                    openBox(i, j)
    #Left edge, not corner
    elif clickedX == 0 and clickedY != 0  and clickedY != boxNum - 1:
        for i in range(clickedX,  clickedX + 2, 1) :
            for j in range(clickedY - 1, clickedY + 2, 1):
                if boxes[i][j].isClicked() == False:
                    openBox(i, j)
    #Right edge, not corner
    elif clickedX == boxNum - 1and clickedY != 0 and clickedY != boxNum - 1 :
        for i in range(clickedX - 1, clickedX +  1, 1):
            for j in range(clickedY - 1, clickedY + 2, 1) :
                if boxes[i][j].isClicked() == False:
                    openBox(i, j)
    #Top edge, not corner
    elif (clickedX != 0 and clickedX != boxNum - 1 and clickedY == 0 ):
        for i in range(clickedX - 1, clickedX + 2, 1):
            for j in range(clickedY, clickedY + 2, 1) :
                if boxes[i][j].isClicked() == False:
                    openBox(i, j)
    #Bottom edge, not corner
    elif clickedX != 0 and clickedX != boxNum - 1 and clickedY == boxNum - 1:
        for i in range(clickedX - 1, clickedX + 2, 1):
            for j in range(clickedY - 1, clickedY + 1, 1):
                if boxes[i][j].isClicked() == False:
                    openBox(i, j)
    #Top left corner
    elif clickedX == 0 and clickedY == 0:
        for i in range(clickedX, clickedX + 2, 1) :
            for j in range(clickedY, clickedY + 2, 1) :
                if boxes[i][j].isClicked() == False:
                    openBox(i, j)
    #Bottom left corner
    elif clickedX == 0 and clickedY == boxNum - 1:
        for i in range(clickedX, clickedX + 2, 1):
            for j in range(clickedY - 1, clickedY + 1, 1):
                if boxes[i][j].isClicked() == False:
                    openBox(i, j)
    #Top right corner
    elif clickedX == boxNum - 1 and clickedY == 0 :
        for i in range(clickedX - 1, clickedX + 1, 1) :
            for j in range(clickedY, clickedY + 2, 1):
                if boxes[i][j].isClicked() == False:
                    openBox(i, j)
    #Bottom right corner
    elif clickedX == boxNum - 1 and clickedY == boxNum - 1 :
        for i in range(clickedX - 1, clickedX + 1, 1):
            for j in range(clickedY - 1, clickedY + 1, 1) :
                if boxes[i][j].isClicked() == False:
                    openBox(i, j)

def draw(xSize, ySize) :
    SCREEN.fill(tan)
    x = xMargin + boxHeight
    y = boxHeight
    pygame.draw.rect(SCREEN, blue, (200, 0, 1000, 1050))
    for i in range(0, boxNum, 1) :
        pygame.draw.line(SCREEN, black, (x, 0), (x, windowHeight), gapSize)
        x += boxHeight + gapSize
    for i in range(0, boxNum, 1) :
        pygame.draw.line(SCREEN, black, (xMargin, y), (windowWidth, y), gapSize)
        y += boxHeight + gapSize

    boardText = fontObj.render('Minesweeper', True, black) #The Minesweeper text
    boardTextSurface = boardText.get_rect()
    boardTextSurface.center = (xMargin - 100, 20)

    flagText = fontObjTwo.render('Right clicked : flag box', True, black)
    clickText = fontObjTwo.render('Left click : open box', True, black)
    openText = fontObjTwo.render('Space bar : open ', True, black)
    openTextTwo = fontObjTwo.render('surrounding boxes', True, black)

    SCREEN.blit(boardText, boardTextSurface)
    SCREEN.blit(clickText, (5, 200))
    SCREEN.blit(flagText, (5, 250))
    SCREEN.blit(openText, (5, 300))
    SCREEN.blit(openTextTwo, (5, 325))
    pygame.display.update()

if __name__ == '__main__':
    main()

