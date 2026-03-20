import unittest
from datetime import timedelta
from src.timer import Timer


class TestTimer(unittest.TestCase):
    def test_timer_initialization(self):
        timer = Timer()
        self.assertFalse(timer.is_running)
        self.assertIsNone(timer.start_time)
        self.assertIsNone(timer.stop_time)
        self.assertEqual(timer.total_time, timedelta(0))

    def test_start_timer(self):
        timer = Timer()
        timer.start()
        self.assertTrue(timer.is_running)
        self.assertIsNotNone(timer.start_time)
        self.assertIsNone(timer.stop_time)

    def test_stop_timer(self):
        timer = Timer()
        timer.start()
        # Small delay to ensure measurable time
        import time

        time.sleep(0.001)
        timer.stop()
        self.assertFalse(timer.is_running)
        self.assertIsNotNone(timer.stop_time)
        self.assertGreater(timer.total_time, timedelta(0))

    def test_stop_timer_without_start(self):
        timer = Timer()
        timer.stop()
        self.assertFalse(timer.is_running)
        self.assertIsNone(timer.start_time)
        self.assertIsNone(timer.stop_time)
        self.assertEqual(timer.total_time, timedelta(0))

    def test_multiple_start_stop(self):
        timer = Timer()
        timer.start()
        timer.stop()
        first_total = timer.total_time
        # Small delay to ensure different timestamps
        import time

        time.sleep(0.001)
        timer.start()
        timer.stop()
        self.assertGreater(timer.total_time, first_total)

    def test_get_current_time_running(self):
        timer = Timer()
        timer.start()
        current = timer.get_current_time()
        self.assertIsInstance(current, str)
        # Format should be HH:MM:SS
        self.assertRegex(current, r"\d{2}:\d{2}:\d{2}")

    def test_start_timer_when_already_running(self):
        """Test that starting an already running timer doesn't change anything."""
        timer = Timer()
        timer.start()
        original_start_time = timer.start_time
        timer.start()  # Try to start again
        self.assertTrue(timer.is_running)
        self.assertEqual(timer.start_time, original_start_time)

    def test_stop_timer_when_not_running(self):
        """Test that stopping a non-running timer doesn't change anything."""
        timer = Timer()
        original_total = timer.total_time
        timer.stop()  # Try to stop without starting
        self.assertFalse(timer.is_running)
        self.assertIsNone(timer.start_time)
        self.assertIsNone(timer.stop_time)
        self.assertEqual(timer.total_time, original_total)

    def test_get_current_time_format(self):
        """Test that the time format is always HH:MM:SS."""
        timer = Timer()
        # Test when not running
        current = timer.get_current_time()
        self.assertEqual(len(current), 8)  # HH:MM:SS format
        self.assertEqual(current[2], ":")
        self.assertEqual(current[5], ":")

        # Test when running
        timer.start()
        current = timer.get_current_time()
        self.assertEqual(len(current), 8)
        self.assertEqual(current[2], ":")
        self.assertEqual(current[5], ":")

    def test_timer_accumulation(self):
        """Test that timer properly accumulates time across multiple sessions."""
        timer = Timer()
        import time

        # First session
        timer.start()
        time.sleep(0.001)
        timer.stop()
        first_session = timer.total_time

        # Second session
        timer.start()
        time.sleep(0.001)
        timer.stop()
        second_session = timer.total_time - first_session

        # Both sessions should be positive
        self.assertGreater(first_session, timedelta(0))
        self.assertGreater(second_session, timedelta(0))
        # Total should be sum of both sessions
        self.assertGreater(timer.total_time, first_session)
