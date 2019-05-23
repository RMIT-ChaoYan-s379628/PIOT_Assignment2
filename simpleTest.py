import unittest  # 导入unittest  包
from unittest_doc.com.Calculator.Calculator import calculator  # 引入需要测试的包

# 所有用例需继承TestCase类或者其子类
class simple_test(unittest.TestCase):
   def setUp(self):
       print('--- 初始化test_simple ---')
       self.a = calculator(1, 2)

   def test_add(self):
       print('--- 测试用例test_simple add ---')
       self.assertEqual(self.a.minus(), -1, '两值不相等')
       self.assertEqual(self.a.add(), 3, '两值不相等')
       self.assertNotEqual(self.a.divide(), 1, '两值不相等')

   def test_divide(self):
       print('--- 测试用例test_simple divide ---')
       self.assertEqual(self.a.divide(), 0.5)

   def tearDown(self):
       print('--- 结束test_simple ---')

def suite():  # 创建测试添加测试套件函数
   suite = unittest.TestSuite()  # 建立测试套件
   suite.addTests([simple_test('test_add'), simple_test('test_divide')])
return suite

if __name__ == '__main__':
   runner = unittest.TextTestRunner(verbosity=2)
   runner.run(suite())