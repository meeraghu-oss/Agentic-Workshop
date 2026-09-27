import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def read_rows(path):
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def test_case_a_seed_and_labelled_examples_are_loadable():
    expected_counts = {
        "cases/expense/seed/claims.csv": 40,
        "cases/expense/seed/line_items.csv": 159,
        "cases/expense/seed/employees.csv": 12,
        "cases/expense/seed/limits.csv": 80,
        "cases/expense/eval/labelled.csv": 119,
    }

    for relative_path, expected_count in expected_counts.items():
        rows = read_rows(ROOT / relative_path)
        assert len(rows) == expected_count
