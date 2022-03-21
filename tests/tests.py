import unittest
import utils
import cat_enum


class MathTransformTestCase(unittest.TestCase):
    def test_math_transform_column(self):
        self.assertAlmostEqual(utils.math_transform_column(2, 0), 9)
        self.assertAlmostEqual(utils.math_transform_column(-1, 0), 0)
        self.assertAlmostEqual(utils.math_transform_column(0, 0), 1)


class CategoricalValueAnomalies(unittest.TestCase):
    def test_categorical_value_anomalies(self):
        self.assertTrue(utils.categorical_value_anomalies('always', cat_enum.ValuesCat7))
        self.assertFalse(utils.categorical_value_anomalies('sometimes', cat_enum.ValuesCat7))
        self.assertTrue(utils.categorical_value_anomalies('happy', cat_enum.ValuesCat8))
        self.assertFalse(utils.categorical_value_anomalies('excited', cat_enum.ValuesCat8))


class RangeAnomalies(unittest.TestCase):
    def test_range_anomalies(self):
        self.assertTrue(utils.range_anomalies(1, -1, 2))
        self.assertTrue(utils.range_anomalies(1, 1, 1))
        self.assertFalse(utils.range_anomalies(-3, -1, 2))
        self.assertFalse(utils.range_anomalies(3, -1, 2))


class ValidateFloat(unittest.TestCase):
    def test_validate_float(self):
        self.assertTrue(utils.validate_float(0))
        self.assertTrue(utils.validate_float(-1))
        self.assertTrue(utils.validate_float(1))
        self.assertTrue(utils.validate_float(1.3))
        self.assertTrue(utils.validate_float(-1.3))
        self.assertTrue(utils.validate_float(1e10))
        self.assertTrue(utils.validate_float(1e-10))
        self.assertTrue(utils.validate_float('NaN'))
        self.assertFalse(utils.validate_float('string'))


class ValidateDiscrete(unittest.TestCase):
    def test_validate_discrete(self):
        self.assertTrue(utils.validate_discrete(0))
        self.assertTrue(utils.validate_discrete(-1))
        self.assertTrue(utils.validate_discrete(1))
        self.assertTrue(utils.validate_discrete('1'))
        self.assertTrue(utils.validate_discrete('-1'))
        self.assertFalse(utils.validate_discrete(1.3))
        self.assertFalse(utils.validate_discrete(-1.3))
        self.assertFalse(utils.validate_discrete(1e10))
        self.assertFalse(utils.validate_discrete(1e-10))
        self.assertFalse(utils.validate_discrete('NaN'))


class ValidateDate(unittest.TestCase):
    def test_validate_discrete(self):
        self.assertFalse(utils.validate_date(0))
        self.assertFalse(utils.validate_date('date'))
        self.assertTrue(utils.validate_date('2020-11-01'))
        self.assertTrue(utils.validate_date('1900-12-13'))
        self.assertFalse(utils.validate_date('2020-13-10'))
        self.assertFalse(utils.validate_date('01-12-2020'))
        self.assertFalse(utils.validate_date('NaN'))


if __name__ == '__main__':
    unittest.main()
