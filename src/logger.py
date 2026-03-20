import json
import os
from datetime import datetime, timedelta
from typing import Dict


class Logger:
    """
    Handles logging timer entries to daily JSON files.
    """

    def __init__(self, data_dir: str, base_name: str) -> None:
        """
        Initializes the logger with the data directory and base name for files.
        """
        self.data_dir = data_dir
        self.base_name = base_name

    def get_file_path(self, date: datetime | None = None) -> str:
        """
        Returns the file path for the given date or today's date if None.
        """
        if date is None:
            date = datetime.now()
        date_str = date.strftime("%Y-%m-%d")
        return os.path.join(self.data_dir, f"{date_str}.json")

    def create_entry(
        self, start_time: datetime, stop_time: datetime | None, total_time: timedelta
    ) -> Dict:
        """
        Creates a JSON entry dict from the given times.
        """
        entry = {
            "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "stop_time": stop_time.strftime("%Y-%m-%d %H:%M:%S") if stop_time else None,
            "total_time": self._format_timedelta(total_time),
        }
        return entry

    def append_entry(
        self, start_time: datetime, stop_time: datetime | None, total_time: timedelta
    ) -> None:
        """
        Appends a new entry to the appropriate daily log file.
        """
        file_path = self.get_file_path(start_time)
        entry = self.create_entry(start_time, stop_time, total_time)

        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
        else:
            data = []

        # Find the next ID
        next_id = max((item["id"] for item in data), default=0) + 1
        entry["id"] = next_id

        data.append(entry)

        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

    def get_daily_totals(self) -> Dict[str, str]:
        """
        Calculates total time per day from all log files.
        """
        totals = {}
        if not os.path.exists(self.data_dir):
            return totals

        for file in os.listdir(self.data_dir):
            if file.endswith(".json"):
                date_str = file[:-5]  # Remove .json
                file_path = os.path.join(self.data_dir, file)
                with open(file_path, "r") as f:
                    data = json.load(f)

                total_seconds = 0
                for entry in data:
                    if entry["total_time"]:
                        total_seconds += self._parse_timedelta(
                            entry["total_time"]
                        ).total_seconds()

                if total_seconds > 0:
                    totals[date_str] = self._format_timedelta(
                        timedelta(seconds=total_seconds)
                    )

        return totals

    def _format_timedelta(self, td: timedelta) -> str:
        """
        Formats a timedelta to HH:MM:SS.
        """
        hours, remainder = divmod(int(td.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def _parse_timedelta(self, time_str: str) -> timedelta:
        """
        Parses HH:MM:SS string to timedelta.
        """
        hours, minutes, seconds = map(int, time_str.split(":"))
        return timedelta(hours=hours, minutes=minutes, seconds=seconds)
