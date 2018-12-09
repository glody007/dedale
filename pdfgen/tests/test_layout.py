import unittest
from stubs import ImageStub
from ..layout import FlowLayout
from ..exception import OutofBoundError

class TestFlowLayoutMetods(unittest.TestCase):

    def setUp(self):
        page_size = (60, 100)
        self.layout = FlowLayout(page_size)

    def test_updateCurrentPosition(self):
        component1 = ImageStub((12,20))
        self.assertEqual(self.layout.getCurrentPosition(),
                         (0, 0), 'bad default position')
        self.layout.updateCurrentPosition(component1)
        self.assertEqual(self.layout.getCurrentPosition(),
                         (12, 0),
                         '''bad position after adding
                            first component''')
        component2 = ImageStub((40, 30))
        self.layout.updateCurrentPosition(component2)
        self.assertEqual(self.layout.getCurrentPosition(),
                         (52, 0),
                         '''bad position after adding
                            second component''')
        component3 = ImageStub((40, 70))
        self.layout.updateCurrentPosition(component3)
        self.assertEqual(self.layout.getCurrentPosition(),
                         (40, 30),
                         '''bad position after adding
                            second component''')
        with self.assertRaises(OutofBoundError):
            component4 = ImageStub((1, 1))
            self.layout.updateCurrentPosition(component3)

if __name__ == '__main__':
    unittest.main()
