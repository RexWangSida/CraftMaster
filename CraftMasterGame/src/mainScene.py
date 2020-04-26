from screen import Screen
from button import Button

class MainScene(Screen):
    def __init__(self,game):
        super(MainScene,self).__init__(game,False)
        x,y = self.game.width, self.game.height
        self.stage = {
            "stage1":[
                ("start Game",[(self.changeStage,("stage2",))]),
                ("Setting",[(self.game.changeScene,("set",))]),
                ("Quit",[(self.game.close,())]),
            ],
            "stage2":[
                ("Start New Game",[(self.game.StartNewGame,())]),
                ("Load Game",[(self.changeStage,("stage3",))]),
                ("Return",[(self.changeStage,("stage1",))]),
            ],
            "stage3":[
                ("Game one",[(self.game.loadGame,("game1.json",)),(self.game.changeScene,("game",))]),
                ("Game two",[(self.game.loadGame,("game2.json",)),(self.game.changeScene,("game",))]),
                ("Return",[(self.changeStage,("stage2",))]),
            ],
        }
        self.button1 = Button(x//4,y//2,x//2,y//8,"",(255,255,255,255),(0,0,0))
        self.button2 = Button(x//4,(11*y)//32,x//2,y//8,"",(255,255,255,255),(0,0,0))
        self.button3 = Button(x//4,(3*y)//16,x//2,y//8,"",(255,255,255,255),(0,0,0))
        self.buttons = [self.button1,self.button2,self.button3]
        self.changeStage("stage1")

    def mouseClick(self, x, y, button, modifiers):
        """called when player move their mouse"""
        for butt in self.buttons:
            if butt.on_click(x,y):
                return

    def mouseMove(self,x, y, dx, dy):
        """called when player click the mouse"""
        for butt in self.buttons:
            butt.on_mouse(x,y,(0,255,0,255),(255,255,255))

    def screenResize(self,width, height):
        """called when the size of screen changes and change the size of components in setting scene based on that"""
        x,y = width, height
        self.button1.on_resize(x//4,y//2,x//2,y//8)
        self.button2.on_resize(x//4,(11*y)//32,x//2,y//8)
        self.button3.on_resize(x//4,(3*y)//16,x//2,y//8)

    def draw(self):
        """called by game to draw the current main scene"""
        self._setBGColor(*self.game.world.skyColor())
        self._setup_glbasic()
        self._setup_2d()
        self.button1.draw()
        self.button2.draw()
        self.button3.draw()

    def changeStage(self,stage):
        """change function and text of buttons based on the stage setted"""
        if stage in self.stage.keys():
            but = self.stage[stage]
            for i in range(len(self.buttons)):
                self.buttons[i].changeText(but[i][0])
                self.buttons[i].changeFunc(but[i][1])
        self.mouseMove(0,0,0,0)
