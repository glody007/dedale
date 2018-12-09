import unittest
from ..utils import isInSideRange, leftSideOutOfBound, rightSideOutOfBound
from stubs import ImageStub

class TestIsInSideRange(unittest.TestCase):

    def setUp(self):
        #'csz': mean container_side_size
        #'esz': mean element_side_size
        self.csz = 100
        self.esz  = 20

    def test_lowerOrigin(self):
        side_origin = -1
        self.assertFalse(isInSideRange(self.csz, self.esz,
                                       side_origin),
                         'lower origin value accepted')

    def test_greaterExtrem(self):
        side_origin = 90
        self.assertFalse(isInSideRange(self.csz, self.esz,
                                       side_origin),
                         'greater extremity value accepted')

    def test_isInContainerSideRange(self):
        side_origin = 50
        self.assertTrue(isInSideRange(self.csz, self.esz,
                                      side_origin),
            """element side in good range refused""")
        self.assertTrue(isInSideRange(self.csz, self.csz, 0),
            """element size and origin the as
               container size and origin refused""")

class test_sideOutOfBound(unittest.TestCase):

    def setUp(self):
        self.page_size = (60, 100)

    def test_rightSideOutOfBound(self):
        comp_in_bound = ImageStub((15, 0), (40, 0))
        self.assertFalse(rightSideOutOfBound(self.page_size,
                                             comp_in_bound),
                         'side in bound refused')
        comp_out_bound = ImageStub((21, 0), (40, 0))
        self.assertTrue(rightSideOutOfBound(self.page_size,
                                             comp_out_bound),
                         'side out of bound accepted')

    def test_leftSideOutOfBound(self):
        comp_in_bound = ImageStub((10, 20), (0, 0))
        self.assertFalse(leftSideOutOfBound(self.page_size,
                                             comp_in_bound),
                         'side in bound refused')
        comp_out_bound = ImageStub((10, 20), (-1, 0))
        self.assertTrue(leftSideOutOfBound(self.page_size,
                                             comp_out_bound),
                         'side out of bound accepted')

if __name__ == '__main__':
    unittest.main()
