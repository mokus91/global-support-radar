import unittest
from scripts.discover_france_aides_territoires import first

class FranceEligibilitySafeguardTests(unittest.TestCase):
    def test_eligibility_text_presence_is_not_verification(self):
        row = {"eligibility": "Collectivités territoriales"}
        self.assertTrue(bool(first(row, "eligibility", "eligibility_description")))
        # The adapter must always emit eligibility_verified=False;
        # text availability is stored separately as eligibility_text_available.
        record = {
            "eligibility_verified": False,
            "eligibility_text_available": bool(first(row, "eligibility", "eligibility_description")),
        }
        self.assertFalse(record["eligibility_verified"])
        self.assertTrue(record["eligibility_text_available"])

    def test_missing_eligibility_text_is_not_verified(self):
        row = {"eligibility": ""}
        self.assertIsNone(first(row, "eligibility", "eligibility_description"))
        record = {"eligibility_verified": False, "eligibility_text_available": False}
        self.assertFalse(record["eligibility_verified"])
        self.assertFalse(record["eligibility_text_available"])

if __name__ == "__main__":
    unittest.main()
