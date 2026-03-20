import tkinter as tk
from tkinter import ttk
from typing import Callable
from src.timer import Timer
from src.logger import Logger

GREY = "grey"
BLACK = "black"
CYAN = "cyan"
WHITE = "white"


class BaseScreen(tk.Frame):
    """
    Base class for all screens in the application.
    """

    def __init__(self, master: tk.Tk, switch_screen: Callable[[str], None]) -> None:
        """
        Initializes the base screen with master and screen switching callback.
        """
        super().__init__(master)
        self.master = master
        self.switch_screen = switch_screen

    def show(self) -> None:
        """
        Shows this screen by packing it.
        """
        self.pack(fill=tk.BOTH, expand=True)

    def hide(self) -> None:
        """
        Hides this screen by forgetting it.
        """
        self.pack_forget()


class TimerScreen(BaseScreen):
    """
    Main timer screen with large cyan timer and start/stop buttons.
    """

    def __init__(
        self,
        master: tk.Tk,
        switch_screen: Callable[[str], None],
        timer: Timer,
        logger: Logger,
    ) -> None:
        """
        Initializes the timer screen with timer and logger.
        """
        super().__init__(master, switch_screen)
        self.timer = timer
        self.logger = logger
        self.running = False

        # Configure the frame
        self.configure(bg=BLACK)  # Dark mode background

        # Start and stop buttons frame
        top_button_frame = tk.Frame(self, bg=BLACK)
        top_button_frame.grid(row=0, column=0, sticky="nsew")
        top_button_frame.grid_columnconfigure(0, weight=1)

        # Start and stop buttons frame
        bottom_button_frame = tk.Frame(self, bg=BLACK)
        bottom_button_frame.grid(row=2, column=0, sticky="nsew")
        bottom_button_frame.grid_columnconfigure(0, weight=1)

        # Create a centering container for the top buttons
        top_center_frame = tk.Frame(top_button_frame, bg=BLACK)
        top_center_frame.pack(expand=True)

        # Create a centering container for the bottom buttons
        bottom_center_frame = tk.Frame(bottom_button_frame, bg=BLACK)
        bottom_center_frame.pack(expand=True)

        # Previous day totals button
        self.totals_button = tk.Button(
            top_center_frame,
            text="Previous Day Totals",
            command=self.show_totals,
            bg=GREY,
            fg=BLACK,
            font=("Arial", 12),
        )
        self.totals_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Exit button
        self.exit_button = tk.Button(
            top_center_frame,
            text="Exit",
            command=self.exit_app,
            bg=GREY,
            fg=BLACK,
            font=("Arial", 12),
        )
        self.exit_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Large cyan timer display
        self.timer_label = tk.Label(
            self, text="00:00:00", font=("Arial", 48), fg=CYAN, bg=BLACK
        )
        self.timer_label.grid(row=1, column=0, sticky="nsew")

        self.start_button = tk.Button(
            bottom_center_frame,
            text="Start",
            command=self.start_timer,
            fg=BLACK,
            font=("Arial", 16),
            width=10,
        )
        self.start_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.stop_button = tk.Button(
            bottom_center_frame,
            text="Stop",
            command=self.stop_timer,
            fg=BLACK,
            font=("Arial", 16),
            width=10,
        )
        self.stop_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Configure grid weights for dynamic resizing
        self.grid_rowconfigure(0, weight=0)  # Top button row
        self.grid_rowconfigure(1, weight=1)  # Timer row (expands)
        self.grid_rowconfigure(2, weight=0)  # Button row
        self.grid_columnconfigure(0, weight=1)  # Main column expands

        # Update timer every second
        self.update_timer()

    def update_timer(self) -> None:
        """
        Updates the timer display every second.
        """
        self.timer_label.config(text=self.timer.get_current_time())
        self.after(10, self.update_timer)

    def start_timer(self) -> None:
        """
        Starts the timer.
        """
        self.timer.start()

    def stop_timer(self) -> None:
        """
        Stops the timer and logs the entry.
        """
        if self.timer.is_running:
            self.timer.stop()
            # Log the entry
            self.logger.append_entry(
                self.timer.start_time,
                self.timer.stop_time,
                self.timer.stop_time - self.timer.start_time,
            )

    def exit_app(self) -> None:
        """
        Stops the timer and closes the application.
        """
        if self.timer.is_running:
            self.timer.stop()
            # Log the entry if timer was running
            self.logger.append_entry(
                self.timer.start_time,
                self.timer.stop_time,
                self.timer.stop_time - self.timer.start_time,
            )
        self.master.quit()

    def show_totals(self) -> None:
        """
        Switches to the totals screen.
        """
        self.switch_screen("totals")


class TotalsScreen(BaseScreen):
    """
    Screen displaying daily totals in a table format.
    """

    def __init__(
        self, master: tk.Tk, switch_screen: Callable[[str], None], logger: Logger
    ) -> None:
        """
        Initializes the totals screen with logger.
        """
        super().__init__(master, switch_screen)
        self.logger = logger

        self.configure(bg=BLACK)

        # Back button
        self.back_button = tk.Button(
            self,
            text="Back",
            command=self.go_back,
            bg=GREY,
            fg=WHITE,
            font=("Arial", 12),
        )
        self.back_button.pack(anchor=tk.NW, padx=10, pady=10)

        # Table for totals
        self.tree = ttk.Treeview(self, columns=("Date", "Total Time"), show="headings")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Total Time", text="Total Time (HH:MM:SS)")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Style for dark mode
        style = ttk.Style()
        style.configure(
            "Treeview", background=BLACK, foreground="white", fieldbackground=BLACK
        )
        style.configure("Treeview.Heading", background="gray", foreground="white")

        self.load_totals()

    def load_totals(self) -> None:
        """
        Loads and displays daily totals in the table, sorted by date (most recent first).
        """
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        totals = self.logger.get_daily_totals()
        # Sort by date descending (most recent first)
        sorted_totals = sorted(totals.items(), key=lambda x: x[0], reverse=True)
        for date, total in sorted_totals:
            self.tree.insert("", tk.END, values=(date, total))

    def go_back(self) -> None:
        """
        Switches back to the timer screen.
        """
        self.switch_screen("timer")
