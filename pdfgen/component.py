from reportlab.pdfgen import canvas
from exception import OutofBoundError
from copy import deepcopy
from utils import *

default_origin = (0, 0)

class Component:
    '''Object that can be drawn on canvas'''

    def __init__(self, canvas,
                 origin = default_origin,
                 parent = None):

        self.canvas = canvas
        self.origin = origin
        self.size   = (0, 0)
        self.parent = parent

    def getSize(self):
        return self.size

    def getPageSize(self):
        return self.canvas.getSize()

    def positionToDraw(self):
        x = 0
        y = - self.size[1]
        return (x, y)

    def getRelativeOrigin(self):
        return self.origin

    def setRelativeOrigin(self, origin):
        self.origin = origin

    def getAbsoluteOrigin(self):
        if self.parent == None:
            return self.getRelativeOrigin()
        parent_origin = self.parent.getAbsoluteOrigin()
        return (self.origin[0] + parent_origin[0],
                self.origin[1] + parent_origin[1])

    def getParent(self):
        return self.parent

    def setParent(self, parent):
        self.parent = parent

    def drawToCanvas(self):
        pass

class Container(Component):
    '''Component that contain other components'''

    def __init__(self, canvas, layout,
                 origin = default_origin,
                 parent = None):

        Component.__init__(self, canvas, origin, parent)
        self.children = []
        self.layout   = layout

    def drawToCanvas(self):
        for child in self.children:
            child.drawToCanvas()

    def getSize(self):
        abs_origin = self.getAbsoluteOrigin()
        x = self.layout.getMaxWidth() - abs_origin[0]
        y = self.layout.getMaxDepth() - abs_origin[1]
        return (x, y)

    def addChild(self, child):
        '''add component to container use layout
           use layout to choose position
           raises OutofBoundError if there is no
           space on page'''
        self.layout.updateCurrentPosition(child)
        child.setParent(self)
        self.children.append(child)

    def getChildren(self):
        return self.children

class Image(Component):

    def __init__(self, canvas, image,
                 origin = default_origin,
                 parent = None):

        Component.__init__(self, canvas, origin, parent)
        self.image = deepcopy(image)
        self.size  = image.getSize()

    def drawToCanvas(self):
        pos_to_draw = self.positionToDraw()
        abs_origin  = self.getAbsoluteOrigin()
        x = pos_to_draw[0] + abs_origin[0]
        y = pos_to_draw[1] - abs_origin[1]
        self.canvas.drawImage(self.image,
                              x, y, mask='auto')

class Margin(Component):
    '''margin is decorator for a component'''
    def __init__(self, canvas, component,
                 margin, origin = default_origin,
                 parent = None):

        Component.__init__(self, canvas, origin, parent)
        comp_size = component.getSize()
        x_pos = x(comp_size) + margin["left"] + margin["right"]
        y_pos = y(comp_size) + margin["top"] + margin["bottom"]
        self.size = (x_pos, y_pos)
        rel_origin = (margin["left"], margin["top"])
        component.setRelativeOrigin(rel_origin)
        component.setParent(self)
        self.component = component

    def drawToCanvas(self):
        self.component.drawToCanvas()
