import unittest
from unittest.mock import patch

from logics import *


@patch('logics.SIZE', 4)
class Test_2048(unittest.TestCase):

    def test_get_number_from_index_1(self):
        self.assertEqual(get_number_from_index(1, 2), 7)

    def test_get_number_from_index_2(self):
        self.assertEqual(get_number_from_index(3, 3), 16)

    def test_get_empty_list_with_all_empty(self):
        a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        mas = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        self.assertEqual(get_empty_list(mas), a)

    def test_get_empty_list_with_partial_empty(self):
        a = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        mas = [
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        self.assertEqual(get_empty_list(mas), a)

    def test_get_empty_list_with_no_empty(self):
        a = []
        mas = [
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
        ]
        self.assertEqual(get_empty_list(mas), a)

    def test_get_index_from_number_1(self):
        self.assertEqual(get_index_from_number(7), (1, 2))

    def test_get_index_from_number_2(self):
        self.assertEqual(get_index_from_number(16), (3, 3))

    def test_get_index_from_number_3(self):
        self.assertEqual(get_index_from_number(1), (0, 0))

    def test_is_zero_in_mas_with_no_zero(self):
        mas = [
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
        ]
        self.assertEqual(is_zero_in_mas(mas), False)

    def test_is_zero_in_mas_with_one_zero(self):
        mas = [
            [1, 1, 1, 1],
            [1, 0, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
        ]
        self.assertEqual(is_zero_in_mas(mas), True)

    def test_is_zero_in_mas_multi_zero(self):
        mas = [
            [0, 1, 0, 1],
            [1, 1, 1, 1],
            [1, 1, 0, 1],
            [1, 0, 1, 1],
        ]
        self.assertEqual(is_zero_in_mas(mas), True)

    def test_move_left_1(self):
        mas = [
            [2, 2, 0, 0],
            [0, 4, 4, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        rez = [
            [4, 0, 0, 0],
            [8, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        self.assertEqual(move_left(mas), (rez, 12))

    def test_move_left_2(self):
        mas = [
            [2, 4, 4, 2],
            [4, 0, 0, 2],
            [0, 0, 0, 0],
            [8, 8, 4, 4],
        ]
        rez = [
            [2, 8, 2, 0],
            [4, 2, 0, 0],
            [0, 0, 0, 0],
            [16, 8, 0, 0],
        ]
        self.assertEqual(move_left(mas), (rez, 32))

    def test_move_up(self):
        mas = [
            [2, 4, 0, 2],
            [2, 0, 2, 0],
            [4, 0, 2, 4],
            [4, 4, 0, 0],
        ]
        rez = [
            [4, 8, 4, 2],
            [8, 0, 0, 4],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        self.assertEqual(move_up(mas), (rez, 24))

    def test_move_down(self):
        mas = [
            [2, 4, 0, 2],
            [2, 0, 2, 0],
            [4, 0, 2, 4],
            [4, 4, 0, 0],
        ]
        rez = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [4, 0, 0, 2],
            [8, 8, 4, 4],
        ]
        self.assertEqual(move_down(mas), (rez, 24))

    def test_can_move_YES(self):
        mas = [
            [2, 4, 0, 2],
            [2, 0, 2, 0],
            [4, 0, 2, 4],
            [4, 4, 0, 0],
        ]
        self.assertEqual(can_move(mas), True)

    def test_can_move_NO(self):
        mas = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16],
        ]
        self.assertEqual(can_move(mas), False)


if __name__ == 'main':
    unittest.main()
