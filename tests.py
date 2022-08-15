import unittest
from Words import chunk_matches_word
from Shape import Shape

class WordTest(unittest.TestCase):

    def test_chunk_matches_word(self):
        self.assertTrue(chunk_matches_word('arterial', ['art', 'e', 'i', 'al']))
        self.assertTrue(chunk_matches_word('hello', ['hello']))
        self.assertTrue(chunk_matches_word('hello', ['h','ello']))
        self.assertTrue(chunk_matches_word('hello', ['hell','o']))
        self.assertTrue(chunk_matches_word('hello', ['hell']))
        self.assertFalse(chunk_matches_word('hello', ['hell','lo']))
        self.assertFalse(chunk_matches_word('hello', ['h','e','a','l','l','o']))

class ShapeTest(unittest.TestCase):

    def test_shape_size(self):
        shape = Shape([], [(0, 0), (0, 1), (1, 0), (1, 1), (1, 2)])
        self.assertEqual(shape.size(), 5)
        self.assertEqual(shape.numSides(), 6)

        shape2 = Shape([], [(0, 3), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 2), (2, 3)])
        self.assertEqual(shape2.size(), 9)
        self.assertEqual(shape2.numSides(), 12)

if __name__ == '__main__':
    unittest.main()
