from datetime import datetime, timedelta


class Timer:
    """
    A simple timer class for tracking elapsed time across multiple start/stop sessions.
    """

    def __init__(self) -> None:
        """
        Initializes the timer with no active session.
        """
        self.is_running: bool = False
        self.start_time: datetime | None = None
        self.stop_time: datetime | None = None
        self.total_time: timedelta = timedelta(0)

    def start(self) -> None:
        """
        Starts the timer if it's not already running.
        """
        if not self.is_running:
            self.is_running = True
            self.start_time = datetime.now()
            self.stop_time = None

    def stop(self) -> None:
        """
        Stops the timer if it's running and accumulates the elapsed time.
        """
        if self.is_running:
            self.stop_time = datetime.now()
            self.total_time += self.stop_time - self.start_time
            self.is_running = False

    def get_current_time(self) -> str:
        """
        Returns the current elapsed time as a formatted string (HH:MM:SS).
        If the timer is running, includes the current session; otherwise, shows total time.
        """
        if self.is_running and self.start_time:
            elapsed = datetime.now() - self.start_time + self.total_time
        else:
            elapsed = self.total_time

        hours, remainder = divmod(int(elapsed.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"
