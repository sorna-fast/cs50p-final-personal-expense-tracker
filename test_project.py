import os
import tempfile
import sqlite3
import pytest

from project import (
    initialize_db,
    add_expense,
    get_all_expenses,
    get_total_by_category,
    generate_report,
)

@pytest.fixture
def temp_db():
    # create and initialize a temporary SQLite file
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    initialize_db(path)
    yield path
    os.remove(path)

def test_add_expense_creates_entry(temp_db):
    entry = add_expense(12.5, "food", "2025-07-30", temp_db)
    assert entry == {"amount": 12.5, "category": "food", "date": "2025-07-30"}
    conn = sqlite3.connect(temp_db)
    cur = conn.cursor()
    cur.execute("SELECT amount,category,date FROM expenses")
    rows = cur.fetchall()
    conn.close()
    assert rows == [(12.5, "food", "2025-07-30")]

def test_get_total_by_category(temp_db):
    add_expense(5, "a", "2025-07-01", temp_db)
    add_expense(7, "a", "2025-07-02", temp_db)
    add_expense(3, "b", "2025-07-02", temp_db)
    totals = get_total_by_category(temp_db)
    assert totals["a"] == 12
    assert totals["b"] == 3

def test_generate_report_all(temp_db):
    add_expense(1, "x", "2025-07-01", temp_db)
    add_expense(2, "y", "2025-07-02", temp_db)
    rpt = generate_report("all", temp_db)
    assert rpt["period"] == "all"
    assert rpt["total"] == 3
    assert rpt["by_category"] == {"x": 1, "y": 2}
    assert rpt["first_date"] == "2025-07-01"
    assert rpt["last_date"] == "2025-07-02"
