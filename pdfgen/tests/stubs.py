from ..component import Component

''' stub that will stand for image'''
class ImageStub(Component):
    def __init__(self, size, origin = (0, 0), parent = None):
        Component.__init__(self, None, origin, parent)
        self.size = size

    def getSize(self):
        return self.size

class ParentStub:
    def __init__(self, absolute_origin, parent = None):
        self.abs_origin = absolute_origin
        self.parent     = parent

    def getAbsoluteOrigin(self):
        return self.abs_origin

    def getParent(self):
        return self.parent
