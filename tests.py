import unittest
from Words import chunk_matches_word

class WordTest(unittest.TestCase):

    def test_chunk_matches_word(self):
        self.assertTrue(chunk_matches_word('arterial', ['art', 'e', 'i', 'al']))
        self.assertTrue(chunk_matches_word('hello', ['hello']))
        self.assertTrue(chunk_matches_word('hello', ['h','ello']))
        self.assertTrue(chunk_matches_word('hello', ['hell','o']))
        self.assertTrue(chunk_matches_word('hello', ['hell']))
        self.assertFalse(chunk_matches_word('hello', ['hell','lo']))
        self.assertFalse(chunk_matches_word('hello', ['h','e','a','l','l','o']))

if __name__ == '__main__':
    unittest.main()
