import unittest
from sample_repos.python.SED1.src.main.RecentlyUsedList import RecentlyUsedList
from unittest.mock import patch


class RecentlyUsedListTest(unittest.TestCase):
    def setUp(self):
        self.test_list = RecentlyUsedList()

    # 1. The list should be empty when initialised.
    def test_list_is_empty_when_initialised(self):
        self.assertEqual(self.test_list.size(), 0)

    # 2. We should be able to add things to the list.
    def test_able_to_add_things_to_list(self):
        item = "012345"
        self.test_list.add(item)
        self.assertTrue(self.test_list.contains(item))

    # 3. We should be able to retrieve items from the list.
    def test_able_to_retrieve_from_list(self):
        item = "012345"
        self.test_list.add(item)
        self.assertEqual(self.test_list.get_item_at(0), item)

    # 4. The most recent item should be first in the list.
    def test_most_recent_item_is_first_in_list(self):
        item1 = "Imperial"
        item2 = "Cambridge"
        self.test_list.add(item1)
        self.test_list.add(item2)
        self.assertEqual(self.test_list.get_most_recent(), item2)

    # 5. Items in the list are unique, so duplicate insertions should be moved rather than added
    def test_duplicate_insertions_moved(self):
        item1 = "Imperial"
        item2 = "Cambridge"
        self.test_list.add(item1)
        self.test_list.add(item2)
        self.test_list.add(item1)
        self.assertEqual(self.test_list.size(), 2)
        self.assertEqual(self.test_list.get_most_recent(), item1)

    # Test the input type is strictly string
    def test_input_type_is_string(self):
        with patch('builtins.input', side_effect=["This is a test", 100]):
            self.test_list.add("This is a test")
            with self.assertRaises(ValueError):
                self.test_list.add(100)

    # Test array index out of bounds exception is thrown
    def test_array_index_out_of_bounds_exception_thrown(self):
        with self.assertRaises(IndexError):
            self.test_list.get_item_at(1)


if __name__ == '__main__':
    unittest.main()
