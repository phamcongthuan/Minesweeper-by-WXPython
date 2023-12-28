from imp import init_builtin
from optparse import Option
from random import Random, randint
import time
import wx
import numpy as np

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)

class TabRecord(wx.Panel):
    def __init__(self, parent):
        super(TabRecord, self).__init__(parent)
        self.SetBackgroundColour('White')

class RecordFrame(wx.Frame):
    def __init__(self, parent, title):
        super(RecordFrame, self).__init__(parent, title=title)
        self.SetIcon(wx.Icon('record.png'))
        self.SetBackgroundColour('White')

        self.panelNB = MyPanel(self)
        self.nb = wx.Notebook(self.panelNB)

        self.easyTab = TabRecord(self.nb)
        self.mediumTab = TabRecord(self.nb)
        self.hardTab = TabRecord(self.nb)
        self.nb.AddPage(self.easyTab, 'Easy')
        self.nb.AddPage(self.mediumTab, 'Medium')
        self.nb.AddPage(self.hardTab, 'Hard')

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.nb, 1, wx.ALL | wx.EXPAND)
        self.panelNB.SetSizer(sizer)

        self.Centre()

class MyFrame(wx.Frame):
    def __init__(self, parent, title, style):
        global frameHeight, frameWidth
        super(MyFrame, self).__init__(parent, title=title, style=style)
        self.SetSize(frameWidth, frameHeight)
        self.SetIcon(wx.Icon('mine.png'))
        self.Centre()
        self.panel = MyPanel(self)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimer)

        self.lb = wx.StaticText(self.panel, label="00:00:00")
        font = wx.Font(30, family=wx.FONTFAMILY_MODERN, style=0, weight=90,
                       underline=False, faceName="", encoding=wx.FONTENCODING_DEFAULT)
        self.lb.SetFont(font)
        self.lb.SetSize(300, 70)
        self.lb.SetPosition(wx.Point(frameWidth - 265, frameHeight // 3))

        self.InitMenuBar()
        self.InitButtonMatrix()

    def onTimer(self, event):
        global hour, min, sec
        sec += 1
        if sec == 60:
            sec = 0
            min += 1
        if min == 60:
            min = 0
            hour += 1

        time = ConvertTime(hour, min, sec)
        self.lb.SetLabel(time)

    def InitButtonMatrix(self):
        global mSize, btList, startTime
        btList.clear()

        x = 7
        y = -30
        for i in range(0, mSize * mSize):
            if i % mSize == 0:
                x = 7
                y += 37

            btList.append(wx.Button(self.panel, id=i, pos=(x, y), size=(40, 40)))
            btList[i].SetBackgroundColour('white')

            Img = wx.Image('bg.png', wx.BITMAP_TYPE_ANY)
            Img = Img.Scale(35, 35, quality=wx.IMAGE_QUALITY_HIGH)
            bmp = wx.Bitmap(Img)
            btList[i].SetBitmap(bmp)
            btList[i].Bind(wx.EVT_BUTTON, self.onClick)
            btList[i].Bind(wx.EVT_RIGHT_DOWN, self.onFirstRightClick)
            x += 37

        startTime = time.time()

    def InitMenuBar(self):
        self.menuBar = wx.MenuBar()
        self.gamesMenu = wx.Menu()
        #Menu Items
        self.levelSubMenu = wx.Menu()
        self.recordMenu = wx.MenuItem(self.gamesMenu, wx.NewId(), text = 'Record')
        self.restartMenu = wx.MenuItem(self.gamesMenu, wx.NewId(), text = 'Restart')
        self.exitMenu = wx.MenuItem(self.gamesMenu, wx.ID_EXIT, text = 'Exit')
        #Menu Items of levelMenu
        self.levelSubMenu.Append(0, 'Easy')
        self.levelSubMenu.Append(1, 'Medium')
        self.levelSubMenu.Append(2, 'Hard')
      
        self.gamesMenu.AppendMenu(wx.ID_ANY, 'Level', self.levelSubMenu) #Append subMenu
        self.gamesMenu.AppendItem(self.recordMenu)
        self.gamesMenu.AppendItem(self.restartMenu)
        self.gamesMenu.AppendSeparator()
        self.gamesMenu.AppendItem(self.exitMenu)
        self.menuBar.Append(self.gamesMenu, 'Game')
        self.SetMenuBar(self.menuBar)

        self.Bind(event = wx.EVT_MENU, handler = self.OnExit, source = self.exitMenu)
        self.Bind(event = wx.EVT_MENU, handler = self.showRecord, source = self.recordMenu)
        self.Bind(event = wx.EVT_MENU, handler = self.OnRestart, source = self.restartMenu)
        self.Bind(event = wx.EVT_MENU, handler = self.EasyLevel, source = self.levelSubMenu.FindItemById(0))
        self.Bind(event = wx.EVT_MENU, handler = self.MediumLevel, source = self.levelSubMenu.FindItemById(1))
        self.Bind(event = wx.EVT_MENU, handler = self.HardLevel, source = self.levelSubMenu.FindItemById(2))
          
    def ChangeSize(self):
        global mSize, frameWidth, frameHeight
        if mSize == 9:
            frameWidth = 667
            frameHeight = 407
            self.lb.SetPosition(wx.Point(frameWidth - 265, frameHeight // 3))
        elif mSize == 16:
            frameWidth = 930
            frameHeight = 670
            self.lb.SetPosition(wx.Point(frameWidth - 265, frameHeight // 3 + 50))
        else:
            frameWidth = 1040
            frameHeight = 777
            self.lb.SetPosition(wx.Point(frameWidth - 265, frameHeight // 3 + 100))

        self.SetSize(frameWidth, frameHeight)
        self.Centre()

    def OnExit(self, event):
        self.Close(True)

    def OnRestart(self, event):
        self.timer.Stop()
        global hour, min, sec, firstRow, firstCol, start, mSize, matrix, btList, isFinish
        isFinish = False
        hour = min = sec = 0
        self.lb.SetLabel(ConvertTime(0, 0, 0))
        firstRow = firstCol = -1
        start = False
        for btn in btList:
            btn.Destroy()
        lMatrix = [[0 for i in range(mSize)] for j in range(mSize)]
        matrix = np.array(lMatrix)
        self.InitButtonMatrix()

    def EasyLevel(self, event):
        global mSize 
        mSize = 9
        self.ChangeSize()
        self.OnRestart(wx.EVT_MENU)

    def MediumLevel(self, event):
        global mSize
        mSize = 16
        self.ChangeSize()
        self.OnRestart(wx.EVT_MENU)

    def HardLevel(self, event):
        global mSize
        mSize = 19
        self.ChangeSize()
        self.OnRestart(wx.EVT_MENU)

    def showRecord(self, event):
        self.recordFrame = RecordFrame(parent = self, title = 'Record')
        easyRec = mediumRec = hardRec = ''

        f = open('record.txt', 'r')
        while (True):
            line = f.readline()
            level = line[:1]
            line = line[2:]
            if level == '1':
                easyRec += line.replace('#', '     ')
            elif level == '2':
                mediumRec += line.replace('#', '     ')
            else:
                hardRec += line.replace('#', '     ')

            if line == '':
                break
        f.close()

        lb1 = wx.StaticText(self.recordFrame.easyTab, label = easyRec)
        lb2 = wx.StaticText(self.recordFrame.mediumTab, label = mediumRec)
        lb3 = wx.StaticText(self.recordFrame.hardTab, label = hardRec)
        font = wx.Font(12, family=wx.FONTFAMILY_MODERN, style=0, weight=90,
                       underline=False, faceName="", encoding=wx.FONTENCODING_DEFAULT)
        lb1.SetFont(font)
        lb2.SetFont(font)
        lb3.SetFont(font)

        self.recordFrame.Show()

    def saveRecord(self):
        #Input name
        dlg = wx.TextEntryDialog(self,'Enter your name','','')
        dlg.ShowModal()
        name = dlg.GetValue()
        dlg.Destroy()

        #Output to txt
        if dlg.ShowModal() == wx.ID_OK:
            f = open('record.txt', 'a+')
            if mSize == 9:
                level = 1
            elif mSize == 16:
                level = 2
            else:
                level = 3
            f.write(str(level) + '#' + ConvertTime(hour, min, sec) + '#' + name + "\n")
            f.close()

    def onClick(self, event):
        id = event.GetEventObject().GetId()
        rowIndex = id // mSize
        colIndex = id % mSize

        global start, firstRow, firstCol
        if start == False:
            firstRow = rowIndex
            firstCol = colIndex
            start = True
            GenerateMatrix(mSize)
            self.Widen(firstRow, firstCol)
            self.timer.Start(1000)
        else:
            if matrix[rowIndex][colIndex] == 0:
                self.Widen(rowIndex, colIndex)
            else:
                self.reveal(rowIndex, colIndex)

        matrix[rowIndex][colIndex] = -2

    def onFirstRightClick(self, event):
        id = event.GetEventObject().GetId()
        if matrix[id // mSize][id % mSize] == -2:
            return
        Img = wx.Image('flag.png', wx.BITMAP_TYPE_ANY)
        Img = Img.Scale(35, 35, quality=wx.IMAGE_QUALITY_HIGH)
        bmp = wx.Bitmap(Img)
        btList[id].SetBitmap(bmp)
        btList[id].Bind(wx.EVT_RIGHT_DOWN, self.onSecondRightClick)
        btList[id].Unbind(wx.EVT_BUTTON)

    def onSecondRightClick(self, event):
        id = event.GetEventObject().GetId()
        Img = wx.Image('bg.png', wx.BITMAP_TYPE_ANY)
        Img = Img.Scale(35, 35, quality=wx.IMAGE_QUALITY_HIGH)
        bmp = wx.Bitmap(Img)
        btList[id].SetBitmap(bmp)
        btList[id].Bind(wx.EVT_RIGHT_DOWN, self.onFirstRightClick)
        btList[id].Bind(wx.EVT_BUTTON, self.onClick)

    def reveal(self, r, c):
        global isFinish, countLeftSpace
        id = r * mSize + c

        if matrix[r][c] == -1:
            Img = wx.Image('mine.png', wx.BITMAP_TYPE_ANY)
            isFinish = True
            self.Solved()
            self.timer.Stop()
            wx.MessageBox('Game over\n' + ConvertTime(hour, min, sec))
        else:
            Img = wx.Image(str(matrix[r][c]) + '.png', wx.BITMAP_TYPE_ANY)
        Img = Img.Scale(30, 30, quality=wx.IMAGE_QUALITY_HIGH)
        bmp = wx.Bitmap(Img)
        btList[id].SetBitmap(bmp)

        if isFinish == True:
            return

        matrix[r][c] = -2

        btList[id].Unbind(wx.EVT_BUTTON)

        countLeftSpace -= 1
        if countLeftSpace == 0:
            isFinish = True
            self.Solved()
            self.timer.Stop()
            wx.MessageBox('You won!\n' + ConvertTime(hour, min, sec))
            self.saveRecord()

    def Widen(self, rIndex, cIndex):
        #base
        if matrix[rIndex][cIndex] == -1:
            return

        if matrix[rIndex][cIndex] == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (i != 0 or j != 0):
                        if (rIndex + i >= 0 and rIndex + i < mSize and cIndex + j >= 0 and cIndex + j < mSize):
                            if matrix[rIndex][cIndex] != -2:
                                self.reveal(rIndex, cIndex)
                            self.Widen(rIndex + i, cIndex + j)
        if matrix[rIndex][cIndex] > 0:
            self.reveal(rIndex, cIndex)

    def Solved(self):
        for i in range(0, mSize):
            for j in range(0, mSize):
                if matrix[i][j] != -2:
                    id = i * mSize + j
                    if matrix[i][j] == -1:
                        Img = wx.Image('mine.png', wx.BITMAP_TYPE_ANY)
                    else:
                        Img = wx.Image(str(matrix[i][j]) + '.png', wx.BITMAP_TYPE_ANY)
                    Img = Img.Scale(30, 30, quality=wx.IMAGE_QUALITY_HIGH)
                    bmp = wx.Bitmap(Img)
                    btList[id].SetBitmap(bmp)

                    matrix[i][j] = -2

                    btList[id].Unbind(wx.EVT_BUTTON)

def ConvertTime(hour, min, sec):
    time = ""
    if hour < 10:
        time = time + "0" + str(hour) + ":"
    else:
        time = time + str(hour) + ":"
    if min < 10:
        time = time + "0" + str(min) + ":"
    else:
        time = time + str(min) + ":"
    if sec < 10:
        time = time + "0" + str(sec)
    else:
        time = time + str(sec)
    return time

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(parent=None, title="Minesweeper", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

def GenerateMatrix(mSize):
    if mSize == 9:
        nBomb = 10
    elif mSize == 16:
        nBomb = 40
    elif mSize == 19:
        nBomb = 75

    global firstRow, firstCol, countLeftSpace
    countLeftSpace = mSize * mSize
    matrix[firstRow, firstCol] = 0

    for i in range(0, nBomb):
        randRow = randint(0, mSize - 1)
        randCol = randint(0, mSize - 1)
        while (randRow == firstRow and randCol == firstCol
               or randRow == firstRow - 1 and randCol == firstCol - 1
               or randRow == firstRow - 1 and randCol == firstCol
               or randRow == firstRow - 1 and randCol == firstCol + 1
               or randRow == firstRow and randCol == firstCol - 1
               or randRow == firstRow and randCol == firstCol + 1
               or randRow == firstRow + 1 and randCol == firstCol - 1
               or randRow == firstRow + 1 and randCol == firstCol
               or randRow == firstRow + 1 and randCol == firstCol + 1):
            randRow = randint(0, mSize - 1)
            randCol = randint(0, mSize - 1)
        if matrix[randRow][randCol] == -1:
            i -= 1
        else:
            matrix[randRow, randCol] = -1
            countLeftSpace -= 1

    for i in range(mSize):
        for j in range(mSize):
            if matrix[i, j] != -1:
                count = 0
                for a in range(i - 1, i + 2):
                    if a >= 0 and a < mSize:
                        for b in range(j - 1, j + 2):
                            if b >= 0 and b < mSize:
                                if matrix[a, b] == -1:
                                    count += 1
                matrix[i, j] = count
    return matrix

frameWidth = 667
frameHeight = 407
firstRow = firstCol = -1
start = False
mSize = 9
btList = []
lMatrix = [[0 for i in range(mSize)] for j in range(mSize)]
matrix = np.array(lMatrix)
records = []
countLeftSpace = 0
isFinish = False
hour = min = sec = 0

app = MyApp()
app.MainLoop()