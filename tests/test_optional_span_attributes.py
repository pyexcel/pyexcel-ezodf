try:
    import unittest2 as unittest
except ImportError:
    import unittest

from ezodf import Sheet
from ezodf.xmlns import CN, etree


class TestOptionalSpanAttributes(unittest.TestCase):
    def imported_sheet(self, size, omitted_attribute):
        sheet = Sheet('merged', size=(3, 3))
        sheet['A1'].set_value('keep this value')
        sheet.set_cell_span('A1', size)
        del sheet['A1'].xmlnode.attrib[CN(omitted_attribute)]
        return Sheet(xmlnode=etree.fromstring(etree.tostring(sheet.xmlnode)))

    def assert_removed(self, sheet, formerly_covered):
        sheet.remove_cell_span('A1')
        self.assertEqual(sheet['A1'].span, (1, 1))
        self.assertEqual(sheet['A1'].value, 'keep this value')
        self.assertFalse(sheet[formerly_covered].covered)
        for attribute in ('table:number-rows-spanned',
                          'table:number-columns-spanned'):
            self.assertNotIn(CN(attribute), sheet['A1'].xmlnode.attrib)
        sheet.remove_cell_span('A1')

    def test_remove_column_span_without_unit_row_attribute(self):
        sheet = self.imported_sheet((1, 2), 'table:number-rows-spanned')
        self.assertEqual(sheet['A1'].span, (1, 2))
        self.assert_removed(sheet, 'B1')
        sheet.set_cell_span('A1', (1, 2))
        self.assertTrue(sheet['B1'].covered)

    def test_remove_row_span_without_unit_column_attribute(self):
        sheet = self.imported_sheet((2, 1), 'table:number-columns-spanned')
        self.assertEqual(sheet['A1'].span, (2, 1))
        self.assert_removed(sheet, 'A2')
        sheet.set_cell_span('A1', (2, 1))
        self.assertTrue(sheet['A2'].covered)

    def test_remove_span_with_both_attributes(self):
        sheet = Sheet('merged', size=(3, 3))
        sheet['A1'].set_value('keep this value')
        sheet.set_cell_span('A1', (2, 2))
        self.assert_removed(sheet, 'B2')
