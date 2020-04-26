from screen import Screen
from button import OnOffButton,Button

class SettingScene(Screen):
    def __init__(self,game):
        super(SettingScene,self).__init__(game,False)
        ## a list of tuple (x,y,width,height,color)bbh
        x,y = self.game.width, self.game.height
        self.mode = OnOffButton(0,0,x//10,y//8,[(self.game.world.changeMode,("night",))],[(self.game.world.changeMode,("day",))],leftText = "Day",rightText = "Night")
        self.returnBut = Button(0,0,x//8,y//20,"Return",(255,255,255,255),(0,0,0))
        self.returnBut.changeFunc([(self.game.goBack,())])
        self.saveOneBut = Button(0,0,x//3,y//24,"Save on game 1 and Return",(255,255,255,255),(0,0,0))
        self.saveOneBut.changeFunc([
                                (self.game.saveGame,("game1.json",)),
                                (self.game.changeScene,("main",))
                                ])
        self.saveTwoBut = Button(0,0,x//3,y//24,"Save on game 2 and Return",(255,255,255,255),(0,0,0))
        self.saveTwoBut.changeFunc([
                                (self.game.saveGame,("game2.json",)),
                                (self.game.changeScene,("main",))
                                ])

    def screenResize(self,width, height):
        """called when the size of screen changes and change the size of components in setting scene based on that"""
        self.mode.on_resize(width//2,height//2,width//10,height//8)
        self.returnBut.on_resize(20,height - 20 - width//24,width//8,width//20)
        self.saveOneBut.on_resize(5*width//48,height//10,width//3,width//24)
        self.saveTwoBut.on_resize(9*width//16,height//10,width//3,width//24)

    def draw(self):
        """called by game to draw the current setting scene"""
        self._setBGColor(*self.game.world.skyColor())
        self._setup_glbasic()
        self._setup_2d()
        self.mode.draw()
        self.returnBut.draw()
        if self.game.world.world != {}:
            self.saveOneBut.draw()
            self.saveTwoBut.draw()

    def mouseMove(self, x, y, dx, dy):
        """called when player move their mouse"""
        self.returnBut.on_mouse(x,y,(0,255,0,255),(255,255,255))
        if self.game.world.world != {}:
            self.saveOneBut.on_mouse(x,y,(0,255,0,255),(255,255,255))
            self.saveTwoBut.on_mouse(x,y,(0,255,0,255),(255,255,255))

    def mouseClick(self, x, y, button, modifiers):
        """called when player click the mouse"""
        self.mode.on_click(x,y)
        self.returnBut.on_click(x,y)
        if self.game.world.world != {}:
            self.saveOneBut.on_click(x,y)
            self.saveTwoBut.on_click(x,y)
