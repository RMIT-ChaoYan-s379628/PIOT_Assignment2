import unittest
from unittest_doc.com.Calculator.Calculator import calculator

class simple_test(unittest.TestCase):
   def setUp(self):
       print('--- initialise test_simple ---')
       self.a = calculator(1, 2)

   def test_add(self):
       print('--- sample test_simple add ---')
       self.assertEqual(self.a.minus(), -1, 'equal')
       self.assertEqual(self.a.add(), 3, 'not equal')
       self.assertNotEqual(self.a.divide(), 1, 'not equal')

   def test_divide(self):
       print('--- samle test_simple divide ---')
       self.assertEqual(self.a.divide(), 0.5)

   def tearDown(self):
       print('--- finish test_simple ---')

def suite():  # Create a test add test suite function
   suite = unittest.TestSuite()  # establish test conditions
   suite.addTests([simple_test('test_add'), simple_test('test_divide')])
return suite

if __name__ == '__main__':
   runner = unittest.TextTestRunner(verbosity=2)
   runner.run(suite())
