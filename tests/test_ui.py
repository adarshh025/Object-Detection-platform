import pytest
import sys

def test_no_sql_dependencies():
    # Ensure mysql-connector is not in modules
    with pytest.raises(ImportError):
        import mysql.connector

def test_ui_import():
    # Should import without errors
    try:
        import ui
        success = True
    except Exception as e:
        success = False
        print(f"Import failed with: {e}")
    assert success
