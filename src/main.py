import tkinter as tk
from typing import Dict
from src.timer import Timer
from src.logger import Logger
from src.gui import TimerScreen, TotalsScreen


class TimeTrackerApp:
    """
    Main application class managing screens and overall flow.
    """

    def __init__(self) -> None:
        """
        Initializes the application with timer, logger, and screens.
        """
        self.timer = Timer()
        self.logger = Logger("data", "time_log")

        self.root = tk.Tk()
        self.root.title("Time Tracker")
        self.root.geometry("350x200")
        self.root.configure(bg="black")  # Dark mode

        self.screens: Dict[str, tk.Frame] = {
            "timer": TimerScreen(
                self.root, self.switch_screen, self.timer, self.logger
            ),
            "totals": TotalsScreen(self.root, self.switch_screen, self.logger),
        }

        self.current_screen: str | None = None
        self.switch_screen("timer")

    def switch_screen(self, screen_name: str) -> None:
        """
        Switches to the specified screen.
        """
        if self.current_screen:
            self.screens[self.current_screen].hide()
        self.current_screen = screen_name
        self.screens[screen_name].show()

    def run(self) -> None:
        """
        Starts the application main loop.
        """
        self.root.mainloop()


if __name__ == "__main__":
    app = TimeTrackerApp()
    app.run()
