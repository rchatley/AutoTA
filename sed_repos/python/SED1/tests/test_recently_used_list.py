import unittest
from src.recently_used_list import RecentlyUsedList


class TestRecentlyUsedList(unittest.TestCase):
    def setUp(self):
        self.test_list = RecentlyUsedList()

    def test_list_is_empty_when_initialised(self):
        self.assertEqual(self.test_list.size(), 0)

    def test_able_to_add_things_to_list(self):
        item = "ITEM"
        self.test_list.add(item)
        self.assertTrue(self.test_list.contains(item))

    def test_input_type_is_string(self):
        self.test_list.add("This is a test")
        with self.assertRaises(TypeError):
            self.test_list.add(100)

    def test_able_to_retrieve_from_list(self):
        item = "ITEM"
        self.test_list.add(item)
        self.assertEqual(self.test_list.get_item_at(0), item)

    def test_index_out_of_bounds_exception_thrown(self):
        with self.assertRaises(IndexError):
            self.test_list.get_item_at(1)

    def test_most_recent_item_is_first_in_list(self):
        item1 = "Imperial"
        item2 = "Cambridge"
        self.test_list.add(item1)
        self.test_list.add(item2)
        self.assertEqual(self.test_list.get_most_recent(), item2)

    def test_duplicate_insertions_moved(self):
        item1 = "Imperial"
        item2 = "Cambridge"
        self.test_list.add(item1)
        self.test_list.add(item2)
        self.test_list.add(item1)
        self.assertEqual(self.test_list.size(), 2)
        self.assertEqual(self.test_list.get_most_recent(), item1)


if __name__ == '__main__':
    unittest.main()
