from shape import Shape2D
from pyglet.gl import *
##  Documentation for Button and OnOffButton
#   @brief Module for creating Button and OnOffButton
class Button(object):
##  @brief Button module
#   @details Create a button with specified position, sizes, text, color, and functions
    def __init__(self,x,y,width,height,text,textColor,quadColor):
    ##  @brief Initializer
    #   @param x,y position of button
    #   @param width, height size of button
    #   @param text text in button to be displayed
    #   @param textColor, quadColor color of text and Button
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.textColor = textColor
        self.quadColor = quadColor
        #list of functions that will be executed when the button is clicked
        self.funcList = []
        self.text = text
        self.label = pyglet.text.Label(text = text, font_name='Arial', font_size = 3 * height / 8,
            x= x + width//2, y=y + height//2, anchor_x='center', anchor_y='center',
            color=textColor)
        self.quad = pyglet.graphics.vertex_list(4,
                ('v2i', Shape2D.quad_vertices(x,y,width,height)),
                ('c3B',quadColor*4))

    def draw(self):
    ##  @brief display button on screen
    #   @details display shape then text
        self.quad.draw(pyglet.gl.GL_QUADS)
        self.label.draw()

    def on_click(self,x,y):
    ##  @brief detect whether button is clicked
    #   @return True if clicked, False if not
        if self._checkMouse(x,y):
            for function in self.funcList:
                func,args = function
                func(*args)
            return True
        return False

    def on_mouse(self,x,y,textColor,quadColor):
    ##  @brief detect whether mouse is on button
    #   @details set dark color to show it's selected
        if len(textColor) != 4 or [i for i in textColor if i < 0 or i > 255]:
            raise ValueError("The color should be rgba in which each number is between 0 and 255")
        if len(quadColor) != 3 or [i for i in quadColor if i < 0 or i > 255]:
            raise ValueError("The color should be rgb in which each number is between 0 and 255")
        if self._checkMouse(x,y):
            self.label.color = textColor
            self.quad.colors = quadColor*4
        else:
            self.label.color = self.textColor
            self.quad.colors = self.quadColor*4

    def on_resize(self,x,y,width,height):
    ##  @brief resize button with screen resized
    #   @details
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label.x = x + width//2
        self.label.y = y + height//2
        self.label.font_size = 3 * height / 8
        self.quad.vertices = Shape2D.quad_vertices(x,y,width,height)

    def changeFunc(self,funcList):
    ##  @brief change the function of this button
        self.funcList = funcList

    def _checkMouse(self,x,y):
    ##  @brief check whether mouse is on buttton
        return x > self.x and x < self.x+self.width and y > self.y and y < self.y+self.height

    def changeText(self,text):
    ##  @brief change text on button
        self.text = text
        self.label.text = text

class OnOffButton():
##  @brief OnOffButton module
#   @details Create an on-off button with specified position, sizes, text, color, and functions
    def __init__(self, x, y, width, height, LeftToRightFunc, RightToLeftFunc,  textColor = (255,0,0,255),
                    quadColor = (0,0,0), slideQuadColor = (64,64,64),state = False, leftText = "OFF", rightText = "ON"):
    ##  @brief Initializer
    #   @param x,y position of button
    #   @param width, height size of button
    #   @param LeftToRightFunc, RightToLeftFunc functions at each side of button
    #   @param leftText, rightText text in button to be displayed
    #   @param textColor, quadColor, slideQuadColor color of text and Button
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.state = state
        self.LeftToRightFunc = LeftToRightFunc
        self.RightToLeftFunc = RightToLeftFunc
        self.leftText = pyglet.text.Label(text = leftText, font_name='Arial', font_size = 3 * height // 7,
            x = x - width//2 -10, y=y, anchor_x='right', anchor_y='center',
            color = textColor)
        self.rightText = pyglet.text.Label(text = rightText, font_name='Arial', font_size = 3 * height // 7,
            x= x + 10 + width//2, y = y, anchor_x='left', anchor_y='center',
            color = textColor)
        self.quad = pyglet.graphics.vertex_list(4,
                ('v2i', Shape2D.quad_vertices(x - width //2 ,y - height //2,width,height)),
                ('c3B',quadColor*4))
        self.slideQuad = pyglet.graphics.vertex_list(4,
                ('v2i', Shape2D.quad_vertices(x - 3 * width//8,y - 5 * height //8,width//4, 5 * height// 4)),
                ('c3B',slideQuadColor*4))

    def draw(self):
    ##  @brief display on-off button on screen
    #   @details display shape then text
        self.leftText.draw()
        self.rightText.draw()
        self.quad.draw(pyglet.gl.GL_QUADS)
        self.slideQuad.draw(pyglet.gl.GL_QUADS)

    def on_resize(self,x,y,width,height):
    ##  @brief resize on-off button with screen resized
    #   @details
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        #leftText
        self.leftText.x = x - width//2 -10
        self.leftText.y = y
        self.leftText.font_size = 3 * height // 7
        #rightText
        self.rightText.x = x + width//2 +10
        self.rightText.y = y
        self.rightText.font_size = 3 * height // 7
        #quads
        self.quad.vertices = Shape2D.quad_vertices(x - width //2 ,y - height //2,width,height)
        #slideQuad
        self._changeState(self.state)

    def on_click(self,x,y):
    ##  @brief detect whether on-off button is clicked
    #   @return True if clicked, False if not
        if self._checkMouseOn(x,y):
            funcList = self.RightToLeftFunc if self.state else self.LeftToRightFunc
            for function in funcList:
                func,args = function
                func(*args)
            self._changeState(not self.state)
            return True
        return False

    def _changeState(self, state):
    #@param state bool
        if state:
            #change to True(Right)
            self.slideQuad.vertices = Shape2D.quad_vertices(self.x + self.width//8, self.y - 5 * self.height //8, self.width//4, 5 * self.height// 4)
        else:
            #change to Left(True)
            self.slideQuad.vertices = Shape2D.quad_vertices(self.x - 3 * self.width//8, self.y - 5 * self.height //8, self.width//4, 5 * self.height// 4)
        self.state = state

    def _checkMouseOn(self,x,y):
    ##  @brief check whether mouse is on buttton
        return self.x - self.width // 2  < x and x < self.x + self.width // 2 and self.y - self.height //2 < y  and self.y < self.y + self.height //2
