import unittest
from email_parser import parse_email

class TestEmailParser(unittest.TestCase):
    def test_parse_email(self):
        raw_email = "From: test@example.com\nTo: user@example.com\nSubject: Test Email\n\nThis is a test."
        parsed = parse_email(raw_email)
        self.assertEqual(parsed['from'], "test@example.com")
        self.assertEqual(parsed['subject'], "Test Email")

if __name__ == "__main__":
    unittest.main()