try:
    import unittest2 as unittest
except ImportError:
    import unittest

from ezodf import Cell
from ezodf.xmlns import CN


class TestCurrencyReplacement(unittest.TestCase):
    def test_replacing_currency_with_other_types_clears_currency(self):
        values = [
            (12, 'float'),
            ('text', 'string'),
            (True, 'boolean'),
            (0.25, 'percentage'),
            ('2026-01-01', 'date'),
            ('PT01H00M00S', 'time'),
        ]
        for value, value_type in values:
            cell = Cell(100, currency='EUR')
            cell.set_value(value, value_type)
            self.assertIsNone(cell.currency, value_type)
            self.assertNotIn(CN('office:currency'), cell.xmlnode.attrib)
            self.assertEqual(cell.value_type, value_type)

    def test_currency_without_code_does_not_inherit_previous_code(self):
        cell = Cell(100, currency='EUR')
        cell.set_value(25, value_type='currency')
        self.assertIsNone(cell.currency)
        self.assertEqual(cell.value, 25.0)

    def test_currency_code_does_not_reappear_after_type_changes(self):
        cell = Cell(100, currency='EUR')
        cell.set_value('text')
        cell.set_value(25, value_type='currency')
        self.assertIsNone(cell.currency)

    def test_replacing_currency_with_explicit_code_uses_new_code(self):
        cell = Cell(100, currency='EUR')
        cell.set_value(25, currency='USD')
        self.assertEqual(cell.currency, 'USD')
        self.assertEqual(cell.value, 25.0)

    def test_rejected_value_preserves_currency(self):
        cell = Cell(100, currency='EUR')
        with self.assertRaises(ValueError):
            cell.set_value(None)
        self.assertEqual(cell.currency, 'EUR')
        self.assertEqual(cell.value, 100.0)
