import unittest
from scripts.discover_france_aides_territoires import eligibility_flags

class FranceEligibilitySafeguardTests(unittest.TestCase):
    def test_eligibility_text_presence_is_not_verification(self):
        row = {"eligibility": "Collectivités territoriales"}
        record = eligibility_flags(row)
        self.assertFalse(record["eligibility_verified"])
        self.assertTrue(record["eligibility_text_available"])

    def test_missing_eligibility_text_is_not_verified(self):
        row = {"eligibility": ""}
        record = eligibility_flags(row)
        self.assertFalse(record["eligibility_verified"])
        self.assertFalse(record["eligibility_text_available"])

if __name__ == "__main__":
    unittest.main()
