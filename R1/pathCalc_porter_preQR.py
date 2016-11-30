#Import relevant modules
import numpy as np
import copy
import time
import matplotlib as mpl
from matplotlib import pyplot

recPenalty=0.2
tempX = 0
tempY = 0


class agent:
    locX = 0
    locY = 0
    dist = 0
    startX = 0
    startY = 0
    destX = 0
    destY = 0
    envScore = []
    G_cost = []
    H_cost = []
    F_cost = []
    score = []
    pathmemory = []
    F_cost_list = []
    Motion_list = []
    path_list = []
    F_cost_low = 0
    zero_count = 0
    count = 0

    def __init__(self):
        locX = 0
        locY = 0
        end_dist = 0
        start_dist = 0
        destX = 0
        destY = 0


    def moveFwd(self):
        self.locX -= 1


    def moveBack(self):
        self.locX += 1


    def moveLeft(self):
        self.locY -= 1


    def moveRight(self):
        self.locY += 1


    def setpos(self, x, y):
        self.locY = y
        self.locX = x


    def setdest(self, x, y):
        self.destY = y
        self.destX = x


    def setstart(self, x, y):
        self.startY = y
        self.startX = x


    def move(self, to, rev):
        if to == 0:
            if rev:
                self.moveBack()
            else:
                self.moveFwd()
        elif to == 1:
            if rev:
                self.moveFwd()
            else:
                self.moveBack()
        elif to == 2:
            if rev:
                self.moveLeft()
            else:
                self.moveRight()
        elif to == 3:
            if rev:
                self.moveRight()
            else:
                self.moveLeft()


    def finddist(self):
        self.dist = np.sqrt(np.square(self.locX - self.destX) + np.square(self.locY - self.destY))
        return self.dist


    def envCheck(self, envmap):
        self.envScore = []
        for motion in range(0, 4):
            self.move(motion, 0)
            if envmap[int(self.locX)][int(self.locY)] >= 0:
                self.envScore.append("clear")
            else:
                self.envScore.append("blocked")
            self.move(motion, 1)
        #print("current location is " + str(self.locX) + "," + str(self.locY))
        #print("environment score is " + str(self.envScore))
        return self.envScore


    def calcG_cost(self):
        self.G_cost = []
        for motion in range(0, 4):
            self.move(motion, 0)
            if self.envScore[motion] == "clear":
                self.G_cost.append(int(10 * (len(path) + 1)))
            #else:
            #    self.G_cost.append(np.nan)
            self.move(motion, 1)
        #print("G Cost is " + str(self.G_cost))
        return self.G_cost

    # Calculate distance away from destination (H-Cost) Function

    def calcH_cost(self):
        self.H_cost = []
        for motion in range(0, 4):
            self.move(motion, 0)
            if self.envScore[motion] == "clear":
                self.H_cost.append(int(10 * (np.absolute(self.locX - self.destX) + np.absolute(self.locY - self.destY))))
            #else:
            #    self.H_cost.append(np.nan)
            self.move(motion, 1)
        #print("H Cost is " + str((self.H_cost)))
        return self.H_cost


    def calcF_cost(self):
        for motion in range(0, 4):
            self.move(motion, 0)
            if self.envScore[motion] == "clear":
                self.F_cost_list.append((self.G_cost[self.count] + self.H_cost[self.count]))
                self.count += 1
            #else:
            #    self.F_cost_list.append(np.nan)
            self.move(motion, 1)
        self.F_cost_low = (self.F_cost_list.index(np.nanmin(self.F_cost_list)))
        #print("F_COST LIST IS" + str(self.F_cost_list))
        self.count = 0
        #print(self.count)
        return self.F_cost_list.index, self.F_cost_low


    def path_memory(self):
        if len(self.path_list) <=1:
            for motion in range (0,4):
                self.move(motion,0)
                if self.envScore[motion] == "clear":
                        self.path_list.append([motion])
                #else:
                #    self.path_list.append([np.nan])
                self.move(motion, 1)
        else:
            for motion in range (0,4):
                self.move(motion,0)
                if self.envScore[motion] == "clear":
                    self.pathmemory = []
                    self.pathmemory.extend(self.path_list[self.F_cost_low])
                    self.pathmemory.extend([motion])
                    self.path_list.append(self.pathmemory)
                #else:
                #    self.path_list.append([np.nan])
                self.move(motion, 1)
            del self.path_list[self.F_cost_low]
            #self.path_list[self.F_cost_low] = [np.nan]
        #print("PATH LIST IS" + str(self.path_list))
        return self.path_list.index

    def checkquad(self, envmap):
        self.envCheck(envmap)
        self.calcG_cost()
        self.calcH_cost()
        self.path_memory()
        self.calcF_cost()

def onclick(event):
    global tempX
    global tempY
    #print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          #(event.button, event.x, event.y, event.xdata, event.ydata))
    tempX = event.xdata
    tempY = event.ydata
    pyplot.close()

def putmarker(motion):
    if motion == 0:
        return "^"
    elif motion == 1:
        return "b"
    elif motion == 2:
        return ">"
    elif motion == 3:
        return "<"

A = [[-10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10],
     [-10, -10, -10, 000, 000, 000, 000, -10, 000, 000, -10, 000, 000, 000, -10, -10, -10, 000, 000, -10],
     [-10, 000, 000, -10, 000, 000, 000, -10, 000, 000, -10, 000, 000, 000, -10, 000, -10, 000, 000, -10],
     [-10, 000, 000, -10, 000, -10, -10, -10, 000, -10, -10, -10, -10, 000, -10, 000, -10, 000, 000, -10],
     [-10, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, -10],
     [-10, -10, 000, -10, 000, -10, -10, -10, -10, 000, -10, -10, 000, -10, -10, -10, 000, -10, -10, -10],
     [-10, -10, 000, -10, 000, 000, 000, -10, 000, 000, -10, 000, 000, 000, 000, -10, 000, -10, -10, -10],
     [-10, -10, 000, -10, 000, 000, 000, -10, 000, 000, -10, 000, 000, 000, 000, -10, 000, 000, 000, -10],
     [-10, -10, 000, -10, 000, 000, 000, -10, -10, -10, -10, 000, -10, -10, -10, -10, 000, -10, 000, -10],
     [-10, -10, 000, -10, 000, 000, 000, -10, -10, -10, -10, -10, -10, 000, 000, 000, 000, -10, -10, -10],
     [-10, -10, 000, -10, 000, 000, 000, -10, -10, -10, -10, -10, -10, 000, 000, -10, 000, -10, -10, -10],
     [-10, -10, 000, 000, 000, 000, 000, -10, -10, -10, -10, 000, 000, -10, -10, -10, 000, -10, -10, -10],
     [-10, -10, 000, -10, 000, 000, 000, -10, 000, -10, -10, 000, 000, -10, -10, -10, 000, -10, -10, -10],
     [-10, -10, 000, -10, -10, -10, -10, -10, 000, -10, -10, -10, 000, -10, -10, -10, 000, -10, 000, -10],
     [-10, -10, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, -10],
     [-10, -10, 000, -10, -10, -10, -10, -10, -10, -10, 000, -10, -10, -10, 000, -10, 000, -10, -10, -10],
     [-10, -10, 000, 000, 000, 000, 000, 000, 000, -10, 000, 000, -10, 000, 000, -10, 000, 000, 000, -10],
     [-10, -10, 000, 000, 000, 000, 000, 000, 000, -10, 000, 000, -10, 000, 000, -10, 000, 000, 000, -10],
     [-10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10]]

Abase = copy.deepcopy(A)

cat = agent()

# make a color map of fixed colors

fig = mpl.pyplot.figure()
cmap = mpl.colors.ListedColormap(['gray','magenta','cyan','blue', 'green', 'black', 'red'])
bounds=[-100,-9,-3*float(recPenalty), -2*float(recPenalty), -1*float(recPenalty), 0, 2, 6]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
pyplot.grid(True,color='white', which='both')


img = mpl.pyplot.imshow(A, interpolation='nearest', cmap = cmap,norm=norm)


cid = fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.set_window_title('Select Destination')
mpl.pyplot.show()
####

cat.setdest(int(round(tempY)),int(round(tempX)))
A[cat.destX][cat.destY] = 999

tempX=0
tempY=0

fig = mpl.pyplot.figure()
pyplot.grid(True,color='white', which='both')
img = mpl.pyplot.imshow(A, interpolation='nearest', cmap = cmap,norm=norm)
cid = fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.set_window_title('Select Startpoint')

mpl.pyplot.show()

cat.setpos(int(round(tempY)),int(round(tempX)))
cat.setstart(int(round(tempX)),int(round(tempY)))
startY=round(tempX)
startX=round(tempY)

motionPath = copy.deepcopy(A)
start = time.time()

#print("The current environment...")
i = 0
for row in A:
    #print(A[i])
    i += 1

path = []
nodeList = [[], []]


cat.finddist()


#print("Cat is at " + str(cat.locX) + "," + str(cat.locY) + " at a distance " + "{0:.2f}".format(cat.finddist()) + " to goal")
motionPath[cat.locX][cat.locY] = "X"
nodeList[0].append(cat.locX)
nodeList[1].append(cat.locY)


while True:
    if cat.locX == cat.destX and cat.locY == cat.destY:
        finish = time.time()
        duration = finish - start
        print("it took " + str(duration) + " to finish the navigation")
        #print(startX,startY)
        cat.locX = startX
        cat.locY = startY
        A[int(cat.locX)][int(cat.locY)] -= (2*recPenalty)
        for motion in range(0, len(path)):
            cat.move(path[motion], 0)
            A[int(cat.locX)][int(cat.locY)] -= recPenalty
        break

    cat.checkquad(A)
    if len(cat.path_list[cat.F_cost_low]) > 1:
        cat.zero_count = (cat.path_list[(cat.F_cost_list.index(np.nanmin(cat.F_cost_list)))]).count(0)
        cat.one_count = (cat.path_list[(cat.F_cost_list.index(np.nanmin(cat.F_cost_list)))]).count(1)
        cat.two_count = (cat.path_list[(cat.F_cost_list.index(np.nanmin(cat.F_cost_list)))]).count(2)
        cat.three_count = (cat.path_list[(cat.F_cost_list.index(np.nanmin(cat.F_cost_list)))]).count(3)
    else:
        cat.zero_count = (cat.path_list[(cat.F_cost_list.index(np.nanmin(cat.F_cost_list)))]).count(0)
        cat.one_count = (cat.path_list[(cat.F_cost_list.index(np.nanmin(cat.F_cost_list)))]).count(1)
        cat.two_count = (cat.path_list[(cat.F_cost_list.index(np.nanmin(cat.F_cost_list)))]).count(2)
        cat.three_count = (cat.path_list[(cat.F_cost_list.index(np.nanmin(cat.F_cost_list)))]).count(3)

    cat.locX = cat.one_count - cat.zero_count + startX
    cat.locY = cat.two_count - cat.three_count + startY
    path = (cat.path_list[(cat.F_cost_list.index(np.nanmin(cat.F_cost_list)))])
    del cat.F_cost_list[(cat.F_cost_list.index(np.nanmin(cat.F_cost_list)))]
    motionPath[int(cat.locX)][int(cat.locY)] = "X"
    nodeList[0].append(cat.locX)

    #print("Cat is at " + str(cat.locX) + "," + str(cat.locY) + " at a distance " + "{0:.2f}".format(
        #cat.finddist()) + " to goal")
    #print("path is " + str(len(path)) + " steps long - " + str(path))
    print("__________________________________________")



img2 = mpl.pyplot.imshow(A, interpolation='nearest',cmap=cmap, norm=norm)
mpl.pyplot.colorbar(img2, cmap=cmap, norm=norm, boundaries=bounds, ticks=[-5, 0, 5])
mpl.pyplot.show()
