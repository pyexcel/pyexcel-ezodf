try:
    import unittest2 as unittest
except ImportError:
    import unittest

from lxml import etree

from ezodf import Sheet


class TestOverlappingSpans(unittest.TestCase):
    def setUp(self):
        self.sheet = Sheet('merged cells', size=(6, 6))
        self.sheet['B2'].set_value('original merge')
        self.sheet.set_cell_span('B2', (3, 3))

    def assert_overlap_rejected(self, position, size):
        original = etree.tostring(self.sheet.xmlnode)
        with self.assertRaises(ValueError):
            self.sheet.set_cell_span(position, size)
        self.assertEqual(etree.tostring(self.sheet.xmlnode), original)

    def test_merge_starting_inside_covered_area_is_rejected(self):
        self.assert_overlap_rejected('C3', (2, 2))

    def test_merge_crossing_covered_area_is_rejected(self):
        self.assert_overlap_rejected('A3', (1, 2))

    def test_adjacent_merge_is_allowed(self):
        self.sheet.set_cell_span('E2', (3, 2))
        self.assertEqual(self.sheet['B2'].span, (3, 3))
        self.assertEqual(self.sheet['E2'].span, (3, 2))
        self.assertTrue(self.sheet['D4'].covered)
        self.assertTrue(self.sheet['F4'].covered)

    def test_previously_covered_area_can_be_merged_after_removal(self):
        self.sheet.remove_cell_span('B2')
        self.sheet.set_cell_span('C3', (2, 2))
        self.assertEqual(self.sheet['C3'].span, (2, 2))
