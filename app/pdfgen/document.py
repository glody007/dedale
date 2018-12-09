from exception import OutofBoundError
from layout import*
from component import Container, Margin
from utils import autoHorizontalMargin

class DocumentBuilder:
    def __init__(self, page_size, LayoutStrategy, canvas):
        '''LayoutStrategy is class name'''
        self.layout = LayoutStrategy
        self.canvas = canvas
        self.page_size = page_size
        self.pages = []
        self.container = Container(self.canvas,
                                   self.layout(page_size))
        self.pages.append(self.container)

    def addComponent(self, component):
        pass

    def createDocument(self):
        pass

class DefaultDocumentBuilder(DocumentBuilder):
    def __init__(self, page_size, canvas):
        DocumentBuilder.__init__(self, page_size,
                                 FlowLayout, canvas)

    def addComponent(self, component):
        '''can raise OutofBoundError'''
        try:
            self.container.addChild(component)
        except OutofBoundError:
            self.container = Container(self.canvas,
                                       self.layout(self.page_size))
            self.pages.append(self.container)
            self.container.addChild(component)

    def createDocument(self):
        origin = (0, self.page_size[1])
        for page in self.pages:
            self.canvas.translate(origin[0], origin[1])
            margin = autoHorizontalMargin(self.page_size,
                                          page.getSize())
            page_with_margin = Margin(self.canvas, page,
                                      margin)
            page_with_margin.drawToCanvas()
            self.canvas.showPage()
        self.canvas.save()
