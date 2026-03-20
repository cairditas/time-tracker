import unittest
import tkinter as tk
from datetime import datetime
from unittest.mock import Mock, patch
from src.gui import TimerScreen, TotalsScreen


class TestTimerScreen(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the window
        self.switch_screen = Mock()
        self.timer = Mock()
        self.logger = Mock()
        self.screen = TimerScreen(
            self.root, self.switch_screen, self.timer, self.logger
        )

    def tearDown(self):
        self.root.destroy()

    def test_initial_display(self):
        # The timer label gets updated by update_timer() which calls timer.get_current_time()
        # We need to mock this before the screen is created
        with patch.object(self.timer, "get_current_time", return_value="00:00:00"):
            # Recreate the screen with the mocked timer
            self.screen = TimerScreen(
                self.root, self.switch_screen, self.timer, self.logger
            )
            self.assertEqual(self.screen.timer_label["text"], "00:00:00")
        self.assertEqual(self.screen.start_button["text"], "Start")
        self.assertEqual(self.screen.stop_button["text"], "Stop")

    def test_start_timer(self):
        self.screen.start_timer()
        self.timer.start.assert_called_once()

    def test_stop_timer(self):
        self.timer.is_running = True
        # Mock the timer attributes
        self.timer.start_time = datetime.now()
        self.timer.stop_time = datetime.now()
        # Mock the append_entry call to avoid the subtraction issue
        self.screen.stop_timer()
        self.timer.stop.assert_called_once()
        self.logger.append_entry.assert_called_once()

    def test_show_totals(self):
        self.screen.show_totals()
        self.switch_screen.assert_called_once_with("totals")


class TestTotalsScreen(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the window
        self.switch_screen = Mock()
        self.logger = Mock()
        # Mock the get_daily_totals to return a proper dict
        self.logger.get_daily_totals.return_value = {"2023-01-01": "01:00:00"}
        self.screen = TotalsScreen(self.root, self.switch_screen, self.logger)

    def tearDown(self):
        self.root.destroy()

    def test_go_back(self):
        self.screen.go_back()
        self.switch_screen.assert_called_once_with("timer")

    def test_load_totals(self):
        self.logger.get_daily_totals.return_value = {"2023-01-01": "01:00:00"}
        self.screen.load_totals()
        items = self.screen.tree.get_children()
        self.assertEqual(len(items), 1)
        values = self.screen.tree.item(items[0], "values")
        self.assertEqual(values, ("2023-01-01", "01:00:00"))
