#------------------------------------------------------
#   File: Step6_solved.py  
#------------------------------------------------------
import toga
from toga.style.pack import (LEFT, RIGHT, COLUMN, ROW, 
                             CENTER, TOP, BOTTOM, NORMAL, 
                             ITALIC, BOLD, MONOSPACE, Pack)

#---------------------------------------------------------
GRAY_0 = '#222222'
GRAY_1 = '#444444'
GRAY_2 = '#666666'
GRAY_3 = '#888888'
GRAY_4 = '#aaaaaa'
GRAY_5 = '#cccccc'
GRAY_6 = '#eeeeee'
pad   = 10 # default padding
padsm = 2 # default padding small 
#--------------------- box styels
mainStyle = Pack( flex=1, padding=pad, direction=COLUMN, alignment=CENTER,
                background_color=GRAY_1, width=368,  height=620,)

canvasStyle = Pack( flex=1, padding=pad, direction=COLUMN, alignment=CENTER,
                background_color=GRAY_2, )

inputStyle = Pack( flex=1, padding=pad, direction=ROW, alignment=CENTER,
                background_color=GRAY_3, )

numStyle = Pack( flex=3, padding=pad, direction=COLUMN, alignment=CENTER,
                background_color=GRAY_3, )

rowStyle = Pack( flex=1, padding=pad, direction=ROW, alignment=CENTER,
                background_color=GRAY_4, )

opStyle = Pack( flex=2, padding=pad, direction=COLUMN, alignment=CENTER,
                background_color=GRAY_3, )

historyStyle = Pack( flex=2, padding=pad, direction=ROW, alignment=CENTER,
                background_color=GRAY_3, )

logStyle = Pack( flex=5, padding=pad, direction=COLUMN, alignment=CENTER,
                background_color=GRAY_4,)

updnStyle = Pack ( flex=1, padding=pad, direction=COLUMN, alignment=CENTER,
                background_color=GRAY_4,)

#--------------------- widget styles 
userStyle = Pack( flex=1, padding=padsm, 
                        font_size = 14,
                        font_family = MONOSPACE, 
                        font_weight = NORMAL, 
                        font_style = ITALIC,
                        color = GRAY_0,
                        background_color = GRAY_4)

btnStyle = Pack( flex=1, padding=padsm, 
                 font_size = 14,
                 font_family  = MONOSPACE, 
                 font_weight = BOLD, 
                 font_style = NORMAL,
                 color = GRAY_0,
                 background_color = GRAY_4)

btnOpStyle = Pack( flex=1, padding=padsm, 
                 font_size = 14,
                 font_family  = MONOSPACE, 
                 font_weight = BOLD, 
                 font_style = NORMAL,
                 color = GRAY_0,
                 background_color = GRAY_5)

#---------------------------------------------------------
class HistoryWidget(toga.Box):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, style=historyStyle, **kwargs)
        self.logDisplayIndex = 0
        self.logText = [] 
        self.label1 = toga.Label('', style=userStyle)
        self.label2 = toga.Label('', style=userStyle)
        self.label3 = toga.Label('', style=userStyle)
        logBox = toga.Box(children=[self.label1, self.label2, self.label3], style=logStyle )
        btnUp   = toga.Button('/\\', style=btnStyle, on_press=self.moveUp)  
        btnDown = toga.Button('\\/', style=btnStyle, on_press=self.moveDown)  
        updnBox = toga.Box(children=[btnUp, btnDown], style=updnStyle)
        self.add(logBox)
        self.add(updnBox)
    def updateLabels(self):
        index = self.logDisplayIndex
        count = len(self.logText)
        if index < count:
            self.label1.text =self.logText[index]
        if (index+1) < count:
            self.label2.text = self.logText[index + 1]
        if (index+2) < count:
            self.label3.text = self.logText[index + 2] 
    def addLog(self, log_text):
        self.logText.append(log_text)
        self.updateLabels()            
    def moveUp(self, btn):
        if self.logDisplayIndex > 0:
            self.logDisplayIndex -= 1
            self.updateLabels()
    def moveDown(self, btn):
        if self.logDisplayIndex < len(self.logText) - 3:
            self.logDisplayIndex += 1
            self.updateLabels()
 
class CalcApp(toga.App):
    def startup(self):
        #----------------------------------button press handlers 
        def submitUserInput(widget):
            userInput.value += widget.text
        def submitEqual(widget):
            historyBox.addLog(userInput.value)
            output = eval(userInput.value)
            userInput.value = output
            historyBox.addLog('='+str(output))
        def submitClear(widget):
            userInput.value = ''
        #----------------------------- user input 
        userInput = toga.TextInput(style=userStyle)            
        inputBox = toga.Box(children=[userInput],style=inputStyle)
        #--------------------------- numeric keypad 0 .. 9
        btnNums = []
        for bn in range(0,10):
            btnNums.append( toga.Button(str(bn), style=btnStyle, on_press=submitUserInput) ) 
        numRow1Box = toga.Box(children=[btnNums[9], btnNums[8], btnNums[7], btnNums[6]],style=rowStyle)
        numRow2Box = toga.Box(children=[btnNums[5], btnNums[4], btnNums[3], btnNums[2]],style=rowStyle)
        numRow3Box = toga.Box(children=[btnNums[1], btnNums[0]], style=rowStyle)
        numBox    = toga.Box(children=[numRow1Box, numRow2Box, numRow3Box], style=numStyle) 
        #------------------------- operator buttons
        btnAdd    = toga.Button( '+', style=btnOpStyle, on_press=submitUserInput )
        btnSub   = toga.Button( '-', style=btnOpStyle, on_press=submitUserInput )
        btnMult  = toga.Button( '*', style=btnOpStyle, on_press=submitUserInput )
        btnDot    = toga.Button( '.', style=btnOpStyle, on_press=submitUserInput )
        btnDiv    = toga.Button( '/', style=btnOpStyle, on_press=submitUserInput )
        btnEqual   = toga.Button( '=', style=btnOpStyle, on_press=submitEqual )
        btnClear  = toga.Button( 'C', style=btnOpStyle, on_press=submitClear )
        #----------------------- operator layout
        opRow1Box = toga.Box(children=[btnAdd, btnSub, btnMult, btnDiv ] ,style=rowStyle)        
        opRow2Box = toga.Box(children=[btnDot, btnClear, btnEqual ] ,style=rowStyle) 
        opBox     = toga.Box(children=[opRow1Box, opRow2Box], style=opStyle) 
        #------------- history widget
        historyBox = HistoryWidget()
        #------------- final package of boxes
        canvasBox  = toga.Box (children=[inputBox, numBox, opBox, historyBox], style=canvasStyle)
        mainBox    = toga.Box( children = [canvasBox] , style=mainStyle) 
        #------------- passing mainBox off to Toga here
        self.main_window = toga.MainWindow(title='Simple Calculator',
           position=(50,50),  #------ locates the phone on a Windows screen 
           size=(370,800),    #------ locks the width and height
           resizable=False,
           minimizable=True)
        self.main_window.content = mainBox
        self.main_window.show()
#----------------------------- start main
def main():
    return CalcApp(formal_name='Simple Calculator',
                   app_id='org.beeware.simplecalc',
                   app_name='simplecalc',
                   icon='icons/brutus',
                   author='bmackay82@gmail.com',
                   version='1.0',
                   description='standalone Toga calculator')
#---------------------------- start main
main().main_loop()
#----------------------------- end main