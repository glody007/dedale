import unittest
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from ..component import Component

class ComponentTestCase(unittest.TestCase):
    def setUp(self):
        self.c = canvas.Canvas("test.pdf", pagesize=A4)
        self.origin = (0, 0)
        self.component = None

    def tearDown(self):
        self.component = None

class TestComponentMethods(ComponentTestCase):

    def setUp(self):
        ComponentTestCase.setUp(self)
        self.component = Component(self.c, self.origin)

    def test_default_size(self):
        self.assertEqual(self.component.getSize(), (0, 0),
                               'incorrect default size')

    def test_positionToDraw(self):
        self.assertEqual(self.component.positionToDraw(),
                         (0, 0),
                         'incorrect position to draw')

    def test_getAbsoluteOrigin(self):
        from stubs import ParentStub
        #test absoluteOrigin without parent
        self.assertEqual(self.component.getAbsoluteOrigin(),
                        (0, 0),
                        '''incorrect absolute origin
                            without parent''')
        #test absoluteOrigin with parent
        self.parent    = ParentStub((10, 20))
        self.component = Component(self.c, (5, 10),
                                   self.parent)
        self.assertEqual(self.component.getAbsoluteOrigin(),
                         (15, 30),
                         '''incorrect absolute origin
                            with parent''')

class TestImageMethods(ComponentTestCase):

    def setUp(self):
        from ..component import Image
        from stubs import ImageStub

        ComponentTestCase.setUp(self)
        self.component = Image(self.c, ImageStub((72, 72)))

    def test_getSize(self):
        self.assertEqual(self.component.getSize(),
                         (72, 72),
                         'incorrect size of image')

    def test_positionToDraw(self):
        self.assertEqual(self.component.positionToDraw(),
                         (0, -72),
                         'incorrect postion to draw')

if __name__ == '__main__':
    unittest.main()
