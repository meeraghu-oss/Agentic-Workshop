import sqlite3

from expense.review import review_claim
from expense.tools import DECISIONS_DB_PATH


def test_review_claim_records_every_line_with_explanations():
    rows = review_claim("CL-2001")
    assert len(rows) == 4
    assert {row["line_id"] for row in rows} == {"L-3001", "L-3002", "L-3003", "L-3004"}
    assert all(row["explanation"] for row in rows)
    with sqlite3.connect(DECISIONS_DB_PATH) as conn:
        count = conn.execute("SELECT COUNT(*) FROM decisions WHERE line_id LIKE 'L-300%'").fetchone()[0]
    assert count == 4
