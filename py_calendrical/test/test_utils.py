import unittest
from py_calendrical.utils import reduce_cond

class Test(unittest.TestCase):

    def test_reduce_cond(self):
        a = [1, 2, 3, 4]
        b = [1, 2, 3, 4]
        c = [2, 2, 3, 4]
        d = [1, 3, 3, 4]
        e = [1, 2, 4, 4]
        f = [1, 2, 3, 5]
        
        self.assertFalse(reduce_cond(lambda _, x: x[0] < x[1], lambda r, x: not r and x[0] == x[1], zip(a, b), False))
        self.assertTrue(reduce_cond(lambda _, x: x[0] < x[1], lambda r, x: not r and x[0] == x[1], zip(a, c), False))
        self.assertTrue(reduce_cond(lambda _, x: x[0] < x[1], lambda r, x: not r and x[0] == x[1], zip(a, d), False))
        self.assertTrue(reduce_cond(lambda _, x: x[0] < x[1], lambda r, x: not r and x[0] == x[1], zip(a, e), False))
        self.assertTrue(reduce_cond(lambda _, x: x[0] < x[1], lambda r, x: not r and x[0] == x[1], zip(a, f), False))

if __name__ == "__main__":
    unittest.main()