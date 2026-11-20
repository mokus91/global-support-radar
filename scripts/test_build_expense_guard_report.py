"""Tests for the read-only expense and cash guard."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("build_expense_guard_report.py")
SPEC = importlib.util.spec_from_file_location("expense_guard", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

class ExpenseGuardTests(unittest.TestCase):
    def write_ledger(self, root, data):
        (root / "data").mkdir(exist_ok=True)
        (root / MODULE.LEDGER).write_text(json.dumps(data), encoding="utf-8")

    def base(self):
        return {"opening_balance_huf":0,"owner_approved_spend_limit_huf":0,
                "tax_and_refund_reserve_huf":0,"income":[],"expenses":[],
                "planned_expenses":[{"id":"hosting","category":"Tárhely","amount_huf":0,
                                     "status":"blocked","owner_approved":False}]}

    def test_zero_income_means_zero_spend(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); data=self.base()
            data["planned_expenses"][0]["amount_huf"]=1200
            self.write_ledger(root,data); result=MODULE.audit(root)
        self.assertEqual(result["approved_spend_ceiling_huf"],0)
        self.assertEqual(result["planned_allowed_huf"],0)
        self.assertIn("BLOKKOLVA", result["lines"][0])

    def test_income_does_not_unlock_spend_without_owner_approval(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); data=self.base()
            data["income"]=[{"id":"i1","amount_huf":10000,"received":True,"evidence_ref":"receipt-1"}]
            data["owner_approved_spend_limit_huf"]=10000
            data["planned_expenses"][0].update({"amount_huf":3000})
            self.write_ledger(root,data); result=MODULE.audit(root)
        self.assertEqual(result["planned_allowed_huf"],0)
        self.assertIn("nincs tulajdonosi jóváhagyás",result["lines"][0])

    def test_approved_spend_cannot_exceed_cash_after_reserve(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); data=self.base()
            data["income"]=[{"id":"i1","amount_huf":10000,"received":True,"evidence_ref":"receipt-1"}]
            data["owner_approved_spend_limit_huf"]=9000
            data["tax_and_refund_reserve_huf"]=3000
            data["planned_expenses"][0].update({"amount_huf":8000,"owner_approved":True})
            self.write_ledger(root,data); result=MODULE.audit(root)
        self.assertEqual(result["approved_spend_ceiling_huf"],7000)
        self.assertEqual(result["planned_allowed_huf"],0)

    def test_approved_spend_within_funded_limit_passes_gate_only(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); data=self.base()
            data["income"]=[{"id":"i1","amount_huf":10000,"received":True,"evidence_ref":"receipt-1"}]
            data["owner_approved_spend_limit_huf"]=6000
            data["planned_expenses"][0].update({"amount_huf":5000,"owner_approved":True})
            self.write_ledger(root,data); result=MODULE.audit(root)
        self.assertEqual(result["planned_allowed_huf"],5000)
        self.assertIn("tényleges fizetéshez továbbra is külön jóváhagyás",result["lines"][0])

    def test_unverified_income_is_not_counted(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); data=self.base()
            data["income"]=[{"id":"i1","amount_huf":50000,"received":False}]
            self.write_ledger(root,data); result=MODULE.audit(root)
        self.assertEqual(result["actual_income_huf"],0)
        self.assertEqual(result["state"],"ERROR")

    def test_expense_requires_receipt(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); data=self.base()
            data["expenses"]=[{"id":"e1","amount_huf":500,"paid":True}]
            self.write_ledger(root,data); result=MODULE.audit(root)
        self.assertEqual(result["actual_expenses_huf"],0)
        self.assertEqual(result["state"],"ERROR")

    def test_negative_or_boolean_amount_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); data=self.base()
            data["opening_balance_huf"]=True
            self.write_ledger(root,data); result=MODULE.audit(root)
        self.assertEqual(result["state"],"ERROR")

    def test_report_displays_all_cost_categories(self):
        report=MODULE.build_report()
        for word in ("Tárhely","Domain","API","Könyvelés","Adó","Marketing","Visszatérítések"):
            self.assertIn(word,report)

if __name__ == "__main__":
    unittest.main()
