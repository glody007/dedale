from utils import inPageBound
from utils import lowerSideOutOfBound
from exception import OutofBoundError

class LayoutStrategy:
    def __init__(self, page_size):
        self.page_size        = page_size
        self.current_position = (0, 0)
        self.max_depth        = 0
        self.max_width        = 0

    def updateCurrentPosition(self, component):
        pass

    def getCurrentPosition(self):
        return self.current_position

    def getMaxDepth(self):
        return self.max_depth

    def getMaxWidth(self):
        return self.max_width

class FlowLayout(LayoutStrategy):
    def __init__(self, page_size):
        LayoutStrategy.__init__(self, page_size)

    def updateCurrentPosition(self, component):
        '''update current position conforming to
           the size of component'''
        component.setRelativeOrigin(self.current_position)
        in_bound  = inPageBound(self.page_size, component)
        comp_size = component.getSize()
        if in_bound:
            '''if there is a space available on the right end
               side and the lower side of the page for the
               component side'''
            comp_depth = self.current_position[1] + comp_size[1]
            comp_ext   = self.current_position[0] + comp_size[0]
            if self.max_depth < comp_depth:
                self.max_depth = comp_depth
            if self.max_width < comp_ext:
                self.max_width = comp_ext
            self.current_position = ((self.current_position[0] +
                                      comp_size[0]),
                                     self.current_position[1])
        else:
            if lowerSideOutOfBound(self.page_size, component):
                '''if there is no space available for Component
                   on lower side of the page'''
                raise OutofBoundError("""component can't
                                      be drawn on page""")
            else:
                self.current_position = (0, self.max_depth)
                self.updateCurrentPosition(component)
