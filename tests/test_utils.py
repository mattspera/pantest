import unittest

from pantest.utils import *

class TestUtils(unittest.TestCase):

    def setUp(self):
        self.sample_dict_1 = {
            'key1' : 'val1',
            'key2' : 'val2'
        }

        self.sample_dict_2 = {
            'key1' : 'val1',
            'key2' : 'val4',
            'key3' : 'val3'
        }

        self.sample_dict_3 = {
            'key1' : 'val1',
            'key2' : 'val2',
            'key3' : 'val3'            
        }

        self.sample_list_1 = [
            'item1',
            'item2'
        ]

        self.sample_list_2 = [
            'item1',
            'item5',
            'item2'
        ]

        self.sample_list_dicts_1 = [
            self.sample_dict_1,
            self.sample_dict_2
        ]

        self.sample_list_dicts_2 = [
            self.sample_dict_1,
            self.sample_dict_2,
            self.sample_dict_3
        ]

    def test_compare_dict_added(self):
        output = compare_dict(self.sample_dict_1, self.sample_dict_3)
        self.assertTrue(output['added'])
        self.assertFalse(output['removed'])
        self.assertFalse(output['changed'])

    def test_compare_dict_removed(self):
        output = compare_dict(self.sample_dict_3, self.sample_dict_1)
        self.assertTrue(output['removed'])
        self.assertFalse(output['added'])
        self.assertFalse(output['changed'])

    def test_compare_dict_changed(self):
        output = compare_dict(self.sample_dict_2, self.sample_dict_3)
        self.assertTrue(output['changed'])
        self.assertFalse(output['added'])
        self.assertFalse(output['removed'])

    def test_compare_list_added(self):
        output = compare_list(self.sample_list_1, self.sample_list_2)
        self.assertTrue(output['added'])
        self.assertFalse(output['removed'])

    def test_compare_list_removed(self):
        output = compare_list(self.sample_list_2, self.sample_list_1)
        self.assertTrue(output['removed'])
        self.assertFalse(output['added'])

    def test_compare_list_dicts_added(self):
        output = compare_list_of_dicts(self.sample_list_dicts_1, self.sample_list_dicts_2)
        self.assertTrue(output['added'])
        self.assertFalse(output['removed'])

    def test_compare_list_dicts_removed(self):
        output = compare_list_of_dicts(self.sample_list_dicts_2, self.sample_list_dicts_1)
        self.assertTrue(output['removed'])
        self.assertFalse(output['added'])

    def test_find_seq_number(self):
        pass

if __name__ == "__main__":
    unittest.main()