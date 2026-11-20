import unittest
from scripts.build_advertising_readiness_report import build_report


def base():
    return {
        "inventory": [{
            "id": "slot-a", "name": "Test slot", "status": "disabled",
            "enabled": False, "external_code_present": False,
            "sponsor_id": None, "owner_approved": False
        }],
        "advertisers": [],
        "revenue_events": []
    }


class AdvertisingReadinessTests(unittest.TestCase):
    def test_empty_inventory_is_zero_revenue_and_no_errors(self):
        report, errors = build_report(base())
        self.assertEqual(errors, [])
        self.assertIn("0 Ft", report)

    def test_enabled_without_approval_is_error(self):
        data = base()
        data["inventory"][0].update(enabled=True, status="active")
        _, errors = build_report(data)
        self.assertTrue(any("without owner approval" in item for item in errors))

    def test_enabled_without_registered_advertiser_is_error(self):
        data = base()
        data["inventory"][0].update(enabled=True, status="active", owner_approved=True, sponsor_id="missing")
        _, errors = build_report(data)
        self.assertTrue(any("without a registered advertiser" in item for item in errors))

    def test_contacted_without_outreach_approval_is_error(self):
        data = base()
        data["advertisers"].append({"id":"x", "contacted":True, "outreach_approved":False})
        _, errors = build_report(data)
        self.assertTrue(any("contacted without outreach approval" in item for item in errors))

    def test_only_received_revenue_with_receipt_counts(self):
        data = base()
        data["revenue_events"] = [
            {"id":"a", "amount_huf":12000, "received":True, "receipt_reference":"invoice-1"},
            {"id":"b", "amount_huf":50000, "received":False, "receipt_reference":"invoice-2"},
            {"id":"c", "amount_huf":70000, "received":True, "receipt_reference":None}
        ]
        report, _ = build_report(data)
        self.assertIn("12 000 Ft", report)

    def test_boolean_and_negative_amounts_are_rejected(self):
        data = base()
        data["revenue_events"] = [
            {"id":"bool", "amount_huf":True, "received":True, "receipt_reference":"x"},
            {"id":"negative", "amount_huf":-5, "received":True, "receipt_reference":"y"}
        ]
        _, errors = build_report(data)
        self.assertEqual(len(errors), 2)


if __name__ == "__main__":
    unittest.main()
