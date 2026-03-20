# Time Tracker

A simple Python GUI application for tracking work time with a visual timer and daily logging.

## Features

- Large cyan timer display in the center of the screen
- Start/Stop buttons with complementary colors for dark mode
- Automatic JSON logging of timer sessions with unique IDs
- Daily log files with date-based filenames
- Previous day totals screen with table view
- Timer continues running when viewing totals

## Requirements

- Python 3.8+
- tkinter (usually included with Python)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/cairditas/time-tracker.git
cd time-tracker
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
python src/main.py
```

### Controls

- **Start Button**: Begins the timer
- **Stop Button**: Stops the timer and logs the session
- **Previous Day Totals**: Shows a table of daily work totals
- **Back Button** (in totals view): Returns to timer screen

## Data Storage

Timer sessions are stored as JSON files in the `data/` directory:
- Filename format: `YYYY-MM-DD.json`
- Each entry contains:
  - `id`: Sequential unique ID per file
  - `start_time`: Session start timestamp
  - `stop_time`: Session stop timestamp
  - `total_time`: Session duration in HH:MM:SS format

## Development

### Code Quality

This project uses:
- **Black** for code formatting
- **Type hints** for better code documentation
- **TDD** approach with comprehensive test coverage

### Running Tests

```bash
# Run all tests
python -m unittest discover tests/

# Run specific test file
python -m unittest tests.test_timer

# Run with verbose output
python -m unittest discover tests/ -v
```

### Code Formatting

```bash
# Format all code
black .

# Check formatting without changes
black --check .

# Show diff of changes
black --diff .
```

### Project Structure

```
time_tracker/
├── src/
│   ├── main.py          # Application entry point
│   ├── gui.py           # GUI components and screens
│   ├── timer.py         # Timer logic and state management
│   └── logger.py        # JSON logging functionality
├── tests/
│   ├── test_gui.py      # GUI component tests
│   ├── test_timer.py    # Timer functionality tests
│   └── test_logger.py   # Logger functionality tests
├── data/                # JSON log files (created automatically)
├── prompts/             # Development prompts and documentation
├── .gitignore
├── requirements.txt
└── README.md
```

## Architecture

The application follows OOP best practices:

- **Timer**: Core timer functionality with start/stop capabilities
- **Logger**: Handles JSON file operations and data persistence
- **BaseScreen**: Abstract base class for GUI screens
- **TimerScreen**: Main timer interface with controls
- **TotalsScreen**: Daily totals display with table view

## License

This project is open source and available under the MIT License.
