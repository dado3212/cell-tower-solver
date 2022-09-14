import unittest
from Words import chunk_matches_word, is_word_composable
from Shape import Shape
from Utils import is_number_composable
from Grid import Grid, easyGrid
from typing import List, Dict, Optional
from Types import Square

class WordTest(unittest.TestCase):

    def test_chunk_matches_word(self):
        self.assertTrue(chunk_matches_word('arterial', ['art', 'e', 'i', 'al']))
        self.assertTrue(chunk_matches_word('hello', ['hello']))
        self.assertTrue(chunk_matches_word('hello', ['h','ello']))
        self.assertTrue(chunk_matches_word('hello', ['hell','o']))
        self.assertTrue(chunk_matches_word('hello', ['hell']))
        self.assertFalse(chunk_matches_word('hello', ['hell','lo']))
        self.assertFalse(chunk_matches_word('hello', ['h','e','a','l','l','o']))

    def test_is_composable(self):
        self.assertTrue(is_word_composable('override', 4, 8))
        self.assertFalse(is_word_composable('underdog', 4, 8))
        self.assertFalse(is_word_composable('overzzbg', 4, 8))
        # self.assertTrue(is_word_composable('underdog', 4, 8))

class ShapeTest(unittest.TestCase):

    def test_shape_size(self):
        shape = Shape([(0, 0), (0, 1), (1, 0), (1, 1), (1, 2)])
        self.assertEqual(shape.size(), 5)
        self.assertEqual(shape.numSides(), 6)

        shape2 = Shape([(0, 3), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 2), (2, 3)])
        self.assertEqual(shape2.size(), 9)
        self.assertEqual(shape2.numSides(), 12)

class BuilderTest(unittest.TestCase):

    # def build_mapping_from_grid_shape(this, grid: Grid, shapes: List[Shape]) -> Dict[Square, Optional[Shape]]:
    #     shape_mapping: Dict[Square, Optional[Shape]] = dict()
    #     for square in grid.squares():
    #         found_shape = False
    #         for shape in shapes:
    #             if square in shape.squares:
    #                 found_shape = True
    #                 shape_mapping[square] = shape
    #         if not found_shape:
    #             shape_mapping[square] = None
    #     return shape_mapping

    # def test_is_valid(self):
    #     grid = Grid(8, 1, 4, 4)

    #     shape = Shape([], [(0, 1), (0, 2), (0, 3), (0, 4)])
    #     shape_mapping = self.build_mapping_from_grid_shape(grid, [shape])
    #     self.assertEqual(is_valid(grid, shape_mapping), False)

    #     shape = Shape([], [(0, 2), (0, 3), (0, 4), (0, 5)])
    #     shape_mapping = self.build_mapping_from_grid_shape(grid, [shape])
    #     self.assertEqual(is_valid(grid, shape_mapping), False)

    #     shape = Shape([], [(0, 0), (0, 1), (0, 2), (0, 3)])
    #     shape_mapping = self.build_mapping_from_grid_shape(grid, [shape])
    #     self.assertEqual(is_valid(grid, shape_mapping), True)

    def test_is_number_composable(self):
        self.assertEqual(is_number_composable(4, 4, 5), True)
        self.assertEqual(is_number_composable(7, 4, 5), False)
        self.assertEqual(is_number_composable(9, 4, 5), True)
        self.assertEqual(is_number_composable(8, 4, 5), True)
        self.assertEqual(is_number_composable(40001, 4, 12), True)

if __name__ == '__main__':
    unittest.main()
