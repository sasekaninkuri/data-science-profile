import unittest
from attachment_analyzer import analyze_attachment

class TestAttachmentAnalyzer(unittest.TestCase):
    def test_analyze_attachment(self):
        self.assertEqual(analyze_attachment("malicious.exe"), "Suspicious file type")
        self.assertEqual(analyze_attachment("document.pdf"), "Safe")

if __name__ == "__main__":
    unittest.main()