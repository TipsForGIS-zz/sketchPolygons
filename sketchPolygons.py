from Tkinter import *

class sketchPolygons:

    # The constructor used to setup attributes
    def __init__(self):

        self.firstX = -999999
        self.firstY = -999999
        self.secondToLastX = -999999
        self.secondToLastY = -999999
        self.tempX = -999999
        self.tempY = -999999
        self.tempXs = []
        self.tempYs = []
        self.firstPointByClick = False
        self.widgetStarted = False

        self.drawnCoords = []
        self.drawingLine = 0
        self.drawnLines = []
        self.drawnPolys = []

        self.tempPolys = []
        self.tempCoords = []

        self.curCanWidth = 750
        self.curCanHeight = 550
        self.master = Tk()
        self.createBindMainCanvas()

    # Update the first coordinates of each polygon
    def updateFirsts(self,x,y):
        self.firstX = x
        self.firstY = y

    # Update the second to last coordinates of each polygon
    #  prior to right click to close/complete the polygon
    def updateSecondToLasts(self,x,y):
        self.secondToLastX = x
        self.secondToLastY = y

    # Update the temp coordinates for drawing
    def updateTemps(self,x,y):
        self.tempX = x
        self.tempY = y

    # Reset values after plotting a polygon
    # for plotting another polygon
    def reset(self):
        self.firstX = -999999
        self.firstY = -999999
        self.secondToLastX = -999999
        self.secondToLastY = -999999
        self.tempX = -999999
        self.tempY = -999999
        self.tempXs = []
        self.tempYs = []

        self.drawnCoords = []
        self.drawingLine = 0
        self.drawnLines = []
        self.firstPointByClick = False

    # Draw the points of a polygon, binded to mouse left click
    def drawPoint(self,e):

        # Up
        if self.firstX == -999999:
            self.updateFirsts(e.x,e.y)
            self.drawnCoords.append(e.x)
            self.drawnCoords.append(e.y)
            self.firstPointByClick = True
        if self.tempX == -999999:
            self.updateTemps(e.x,e.y)

    # Sketching the lines of the polygon, binded to mouse motion
    # while holding the left key
    def sketchLine(self,e):

        self.tempXs.append(e.x)
        self.tempYs.append(e.y)
        if len(self.tempXs) == 1:
            self.drawingLine = self.mainCanvas.create_line(self.tempX, self.tempY,
                                             e.x, e.y,fill='red',width=2)

        else:
            self.mainCanvas.delete(self.drawingLine)
            self.drawingLine = self.mainCanvas.create_line(self.tempX, self.tempY,
                                             self.tempXs[len(self.tempXs) - 1],
                                             self.tempYs[len(self.tempYs) - 1],
                                             fill='red',width=2)

    # Plotting a line while sketching, binded to mouse left button release
    def plotLine(self,e):

        self.drawnLines.append(self.mainCanvas.create_line(self.tempX, self.tempY, e.x, e.y,fill='red',width=2))
        if len(self.drawnLines) == 2:
            if self.drawnLines[0] == self.drawnLines[1]:
                self.drawnLines.pop()

        self.drawnCoords.append(e.x)
        self.drawnCoords.append(e.y)
        if len(self.drawnCoords) == 4:
            if self.drawnCoords[0] == self.drawnCoords[2] and self.drawnCoords[1] == self.drawnCoords[3]:
                self.drawnCoords.pop()
                self.drawnCoords.pop()

        self.updateTemps(e.x, e.y)
        self.updateSecondToLasts(e.x, e.y)
        self.tempXs = []
        self.tempYs = []

    # Closing the polygon, binded to mouse right click
    def closePoly(self,e):

        self.drawnLines.append(self.mainCanvas.create_line(self.secondToLastX, self.secondToLastY, self.firstX, self.firstY, fill='red'))
        self.drawnCoords.append(self.firstX)
        self.drawnCoords.append(self.firstY)

        p = self.mainCanvas.create_polygon(self.drawnCoords,fill='pink',width=3,outline='yellow',smooth=0)
        self.drawnPolys.append(p)

        self.reset()

    # Resizing the polygons while resizing the canvas according to the canvas dimensions
    def onCanvasResized(self,e):

        # count is used to distinguish Xs from Ys
        count = 0
        # Do not
        if self.widgetStarted == False:
            self.widgetStarted = True
        else:
            for p in self.drawnPolys:
                for c in self.mainCanvas.coords(p):
                    if count%2 == 0:
                        self.tempCoords.append(c * self.mainCanvas.winfo_width()/self.curCanWidth)
                    else:
                        self.tempCoords.append(c * self.mainCanvas.winfo_height() / self.curCanHeight)

                    count += 1

                self.tempPolys.append(self.tempCoords)
                self.tempCoords = []
                count = 0

            self.curCanWidth = self.mainCanvas.winfo_width()
            self.curCanHeight = self.mainCanvas.winfo_height()

            self.mainCanvas.delete(ALL)
            self.drawnPolys = []

            for newCoords in self.tempPolys:
                newPoly = self.mainCanvas.create_polygon(newCoords, fill='pink', width=3, outline='yellow', smooth=0)
                self.drawnPolys.append(newPoly)

            self.tempPolys = []

    # Create the main canvas and bind the events
    def createBindMainCanvas(self):

        self.mainCanvas = Canvas(master=self.master, width=self.curCanWidth, height=self.curCanHeight, background = 'white')
        self.mainCanvas.pack(fill=BOTH, expand=YES)

        self.mainCanvas.bind("<Configure>", self.onCanvasResized)
        self.mainCanvas.bind("<Button-1>", self.drawPoint)
        self.mainCanvas.bind("<Button-3>", self.closePoly)
        self.mainCanvas.bind("<B1-Motion>", self.sketchLine)
        self.mainCanvas.bind("<ButtonRelease-1>", self.plotLine)

        mainloop()

##########################
#      running main      #
##########################
if __name__ == '__main__':
    dP = sketchPolygons()