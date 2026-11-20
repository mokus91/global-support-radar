#!/usr/bin/env python3
"""Read-only cash and expense gate. It never initiates payments or changes budgets."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = "data/financial-ledger.json"

def load_ledger(root=ROOT):
    path = root / LEDGER
    if not path.is_file():
        return None, ["A pénzügyi főkönyv hiányzik."]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, [f"A pénzügyi főkönyv nem olvasható: {exc}"]
    errors = []
    for key in ("income", "expenses", "planned_expenses"):
        if not isinstance(data.get(key), list):
            errors.append(f"A(z) {key} mezőnek listának kell lennie.")
    for key in ("opening_balance_huf", "owner_approved_spend_limit_huf", "tax_and_refund_reserve_huf"):
        value = data.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            errors.append(f"Hibás vagy hiányzó összeg: {key}.")
    if errors:
        return None, errors
    return data, []

def _valid_amount(item, label, errors):
    amount = item.get("amount_huf")
    if not isinstance(amount, int) or isinstance(amount, bool) or amount < 0:
        errors.append(f"{label}: hibás összeg.")
        return 0
    return amount

def audit(root=ROOT):
    data, errors = load_ledger(root)
    if data is None:
        return {"state":"ERROR", "available_cash_huf":0, "actual_income_huf":0,
                "actual_expenses_huf":0, "planned_allowed_huf":0, "errors":errors, "lines":[]}
    income = expenses = 0
    ids = set()
    for row in data["income"]:
        if not isinstance(row, dict):
            errors.append("Hibás bevételi rekord.")
            continue
        rid = row.get("id")
        if not rid or rid in ids:
            errors.append("Hiányzó vagy duplikált pénzügyi rekordazonosító.")
        ids.add(rid)
        amount = _valid_amount(row, f"Bevétel {rid}", errors)
        if row.get("received") is not True or row.get("evidence_ref") in (None, ""):
            errors.append(f"A bevétel nem tekinthető igazoltnak: {rid}.")
        else:
            income += amount
    for row in data["expenses"]:
        if not isinstance(row, dict):
            errors.append("Hibás kiadási rekord.")
            continue
        rid = row.get("id")
        if not rid or rid in ids:
            errors.append("Hiányzó vagy duplikált pénzügyi rekordazonosító.")
        ids.add(rid)
        amount = _valid_amount(row, f"Kiadás {rid}", errors)
        if row.get("paid") is not True or row.get("evidence_ref") in (None, ""):
            errors.append(f"A kiadás nem rendelkezik fizetési bizonylattal: {rid}.")
        else:
            expenses += amount
    opening = data["opening_balance_huf"]
    reserve = data["tax_and_refund_reserve_huf"]
    approved_limit = data["owner_approved_spend_limit_huf"]
    cash_before_reserve = opening + income - expenses
    if cash_before_reserve < 0:
        errors.append("A nyilvántartott tényleges kiadások meghaladják a rendelkezésre álló pénzt.")
    available = max(0, cash_before_reserve - reserve)
    spend_ceiling = min(available, approved_limit)
    lines = []
    planned_ids = set()
    planned_total = 0
    allowed_total = 0
    for item in data["planned_expenses"]:
        if not isinstance(item, dict):
            errors.append("Hibás tervezett kiadási rekord.")
            continue
        pid = item.get("id")
        if not pid or pid in planned_ids:
            errors.append("Hiányzó vagy duplikált tervezett kiadásazonosító.")
        planned_ids.add(pid)
        amount = _valid_amount(item, f"Tervezett kiadás {pid}", errors)
        planned_total += amount
        approved = item.get("owner_approved") is True
        status = item.get("status")
        if status == "paid":
            errors.append(f"A tervezett kiadás fizetettként szerepel, de nincs a kiadási főkönyvben: {pid}.")
        elif amount == 0:
            lines.append(f"- {item.get('category', pid)}: 0 Ft tervezett összeg; nincs költési engedély.")
        elif not approved:
            lines.append(f"- {item.get('category', pid)}: BLOKKOLVA – nincs tulajdonosi jóváhagyás.")
        elif amount > spend_ceiling - allowed_total:
            lines.append(f"- {item.get('category', pid)}: BLOKKOLVA – nincs elegendő szabad, jóváhagyott keret.")
        else:
            allowed_total += amount
            lines.append(f"- {item.get('category', pid)}: keretellenőrzés teljesült; tényleges fizetéshez továbbra is külön jóváhagyás kell.")
    return {
        "state":"ERROR" if errors else "OK",
        "actual_income_huf":income,
        "actual_expenses_huf":expenses,
        "cash_before_reserve_huf":cash_before_reserve,
        "reserved_huf":reserve,
        "available_cash_huf":available,
        "owner_approved_spend_limit_huf":approved_limit,
        "approved_spend_ceiling_huf":spend_ceiling,
        "planned_total_huf":planned_total,
        "planned_allowed_huf":allowed_total,
        "errors":errors,
        "lines":lines
    }

def build_report(root=ROOT):
    result = audit(root)
    lines = [
        "# Kiadási és önfinanszírozási kapu", "",
        "Ez automatikus, csak olvasási ellenőrzés. Nem könyvel, nem fizet, nem módosít keretet és nem indít előfizetést.", "",
        f"- Ellenőrzés: **{result['state']}**",
        f"- Igazolt beérkezett bevétel: {result.get('actual_income_huf', 0):,} Ft",
        f"- Bizonylattal rögzített kiadás: {result.get('actual_expenses_huf', 0):,} Ft",
        f"- Elkülönített tartalék: {result.get('reserved_huf', 0):,} Ft",
        f"- Szabad pénz a tartalék után: {result.get('available_cash_huf', 0):,} Ft",
        f"- Tulajdonos által jóváhagyott költési plafon: {result.get('owner_approved_spend_limit_huf', 0):,} Ft",
        f"- Maximális jóváhagyható keret: {result.get('approved_spend_ceiling_huf', 0):,} Ft",
        f"- Tervezett kiadások összesen: {result.get('planned_total_huf', 0):,} Ft",
        f"- Keretellenőrzésen átment tervezett összeg: {result.get('planned_allowed_huf', 0):,} Ft", "",
        "## Kiadási kategóriák"
    ]
    lines.extend(result.get("lines", []))
    lines += ["", "## Ellenőrzési hibák"] + ([f"- {e}" for e in result.get("errors", [])] or ["- Nincs."])
    lines += ["", "## Kötelező szabály", "Ha nincs ténylegesen beérkezett pénz, vagy nincs külön tulajdonosi jóváhagyás, a költési keret 0 Ft. A rendszer semmilyen körülmények között nem fizet automatikusan.", ""]
    return "\n".join(lines)

if __name__ == "__main__":
    print(build_report())
