import unittest
from link_checker import check_url

class TestLinkChecker(unittest.TestCase):
    def test_check_url(self):
        # Ensure the function checks URLs correctly
        self.assertTrue(check_url("http://malicious.com"))
        self.assertFalse(check_url("http://safe.com"))

if __name__ == "__main__":
    unittest.main()