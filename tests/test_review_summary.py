from expense.review import review_claim_summary


def test_summary_sums_approved_items_only_and_keeps_all_rows():
    summary = review_claim_summary("CL-2001")
    assert len(summary["line_items"]) == 4
    assert summary["reimbursable_total"] == 800.29
    high_value = next(row for row in summary["line_items"] if row["line_id"] == "L-3001")
    assert high_value["decision"] == "approve"
    assert high_value["requires_human_release"] is True
    assert all(
        not row["requires_human_release"]
        for row in summary["line_items"]
        if row["line_id"] != "L-3001"
    )
