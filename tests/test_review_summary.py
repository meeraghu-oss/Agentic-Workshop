from expense.review import review_claim_summary


def test_summary_sums_approved_items_only_and_keeps_all_rows():
    summary = review_claim_summary("CL-2001")
    assert len(summary["line_items"]) == 4
    assert summary["reimbursable_total"] == 800.29
