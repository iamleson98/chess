import unittest
import square
import utils

class TestSquareMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.square = square.Square(utils.File_A, utils.Rank_1)

    def test_isWithinBoard(self):
        self.assertEqual(self.square.isWithinBoard(), True)
        self.square = square.Square(self.square.getFile()-1, self.square.getRank()-1)
        self.assertEqual(self.square.isWithinBoard(), False)
        self.assertEqual(str(self.square), "@0")

if __name__ == "__main__":
    unittest.main()
