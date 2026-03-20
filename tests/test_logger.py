import unittest
from datetime import datetime, timedelta
import json
import os
import tempfile
import shutil
from src.logger import Logger


class TestLogger(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test data
        self.test_dir = tempfile.mkdtemp()
        self.addCleanup(lambda: shutil.rmtree(self.test_dir))

    def test_log_entry_creation(self):
        logger = Logger(self.test_dir, "test_log")
        start_time = datetime(2023, 1, 1, 9, 0, 0)
        stop_time = datetime(2023, 1, 1, 10, 30, 0)
        total_time = timedelta(hours=1, minutes=30)

        entry = logger.create_entry(start_time, stop_time, total_time)
        self.assertIn("start_time", entry)
        self.assertIn("stop_time", entry)
        self.assertIn("total_time", entry)
        self.assertEqual(entry["start_time"], "2023-01-01 09:00:00")
        self.assertEqual(entry["stop_time"], "2023-01-01 10:30:00")
        self.assertEqual(entry["total_time"], "01:30:00")

    def test_append_entry_to_file(self):
        logger = Logger(self.test_dir, "test_log")
        start_time = datetime(2023, 1, 1, 9, 0, 0)
        stop_time = datetime(2023, 1, 1, 10, 0, 0)
        total_time = timedelta(hours=1)

        logger.append_entry(start_time, stop_time, total_time)
        file_path = logger.get_file_path(start_time)
        self.assertTrue(os.path.exists(file_path))

        with open(file_path, "r") as f:
            data = json.load(f)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["id"], 1)
            self.assertEqual(data[0]["start_time"], "2023-01-01 09:00:00")
            self.assertEqual(data[0]["stop_time"], "2023-01-01 10:00:00")
            self.assertEqual(data[0]["total_time"], "01:00:00")

    def test_multiple_entries_sequential_ids(self):
        logger = Logger(self.test_dir, "test_log")
        # Use a specific date to avoid file path issues
        test_date = datetime(2023, 1, 1)
        start_time1 = datetime(2023, 1, 1, 9, 0, 0)
        stop_time1 = datetime(2023, 1, 1, 10, 0, 0)
        total_time1 = timedelta(hours=1)

        start_time2 = datetime(2023, 1, 1, 10, 30, 0)
        stop_time2 = datetime(2023, 1, 1, 11, 30, 0)
        total_time2 = timedelta(hours=1)

        logger.append_entry(start_time1, stop_time1, total_time1)
        logger.append_entry(start_time2, stop_time2, total_time2)

        file_path = logger.get_file_path(test_date)
        with open(file_path, "r") as f:
            data = json.load(f)
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]["id"], 1)
            self.assertEqual(data[1]["id"], 2)
            # Verify the entries contain the correct data
            self.assertEqual(data[0]["start_time"], "2023-01-01 09:00:00")
            self.assertEqual(data[1]["start_time"], "2023-01-01 10:30:00")

    def test_get_daily_totals(self):
        logger = Logger(self.test_dir, "test_log")
        start_time1 = datetime(2023, 1, 1, 9, 0, 0)
        stop_time1 = datetime(2023, 1, 1, 10, 0, 0)
        total_time1 = timedelta(hours=1)

        start_time2 = datetime(2023, 1, 1, 10, 30, 0)
        stop_time2 = datetime(2023, 1, 1, 11, 30, 0)
        total_time2 = timedelta(hours=1)

        logger.append_entry(start_time1, stop_time1, total_time1)
        logger.append_entry(start_time2, stop_time2, total_time2)

        totals = logger.get_daily_totals()
        self.assertEqual(totals, {"2023-01-01": "02:00:00"})

    def test_get_daily_totals_multiple_days(self):
        logger1 = Logger(self.test_dir, "test_log_2023-01-01")
        start_time1 = datetime(2023, 1, 1, 9, 0, 0)
        stop_time1 = datetime(2023, 1, 1, 10, 0, 0)
        total_time1 = timedelta(hours=1)
        logger1.append_entry(start_time1, stop_time1, total_time1)

        logger2 = Logger(self.test_dir, "test_log_2023-01-02")
        start_time2 = datetime(2023, 1, 2, 9, 0, 0)
        stop_time2 = datetime(2023, 1, 2, 10, 30, 0)
        total_time2 = timedelta(hours=1, minutes=30)
        logger2.append_entry(start_time2, stop_time2, total_time2)

        totals = logger1.get_daily_totals()
        self.assertIn("2023-01-01", totals)
        self.assertIn("2023-01-02", totals)
        self.assertEqual(totals["2023-01-01"], "01:00:00")
        self.assertEqual(totals["2023-01-02"], "01:30:00")
