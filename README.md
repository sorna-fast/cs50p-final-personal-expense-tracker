# Personal Expense Tracker

#### Video Demo: <URL HERE>(https://youtu.be/h2_84cVJfps?feature=shared)

#### Description:

Personal Expense Tracker is a command-line application written in Python that helps users record, analyze, and visualize their daily spending. It stores expense entries—comprising amount, category, and date—in a SQLite database and provides textual reports based on customizable periods (daily, weekly, monthly, or all time). The tool supports three primary operations: adding a new expense entry, generating a detailed expense report, and plotting a bar chart of expenses by category. Under the hood, it utilizes Python’s standard library for database interactions, `argparse` for parsing command-line arguments, and `matplotlib` for creating charts. This project demonstrates file I/O, database design, argument parsing, data aggregation, chart generation, and test-driven development with pytest.

This README explains how to install and run the application, describes the contents and purpose of each file in the repository, outlines key design decisions, and provides guidance on running automated tests. The application is intended for users who prefer a lightweight, script-based interface instead of a full graphical user interface. It can serve as a foundation for extending into a larger budgeting or financial management system in the future.

## Installation

To install and prepare the project on your local machine, follow these steps:

1. Clone the repository to your computer and navigate into the `project` directory.  
2. Create a virtual environment (optional but recommended):  
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```  
3. Install required Python packages listed in `requirements.txt`:  
   ```bash
   pip install -r requirements.txt
   ```  
4. Ensure that Python 3.8 or later is available on your system.

No additional configuration is required: the SQLite database file `expenses.db` will be created automatically when you first run the application.

## Usage

Once installed, the application can be executed using the `project.py` script. The basic usage pattern is:

```bash
python project.py <command> [options]
```

Available commands:

- `add`  
  Add a new expense entry with the specified amount, category, and optional date.  
  Example:  
  ```bash
  python project.py add --amount 25.50 --category food --date 2025-07-30
  ```  
- `report`  
  Generate a textual report of expenses for a given period (`daily`, `weekly`, `monthly`, or `all`).  
  Example:  
  ```bash
  python project.py report --period weekly
  ```  
- `plot`  
  Produce and save a bar chart (`PNG` image) of expenses by category for a given period. The image file is named `expenses_<period>.png`.  
  Example:  
  ```bash
  python project.py plot --period monthly
  ```

If no command is provided, the script will display help instructions.

## Repository Structure

- `project.py`  
  Contains the `main` function and three core functions—`add_expense`, `get_total_by_category`, and `generate_report`—all defined at the top level. Also includes `plot_expenses` for chart creation and `initialize_db` for setting up the SQLite schema.

- `test_project.py`  
  Defines pytest test cases for verifying the correctness of `add_expense`, `get_total_by_category`, and `generate_report`. Uses temporary database fixtures to isolate tests and ensure repeatability.

- `requirements.txt`  
  Lists all pip-installable dependencies:  
  - `matplotlib` for chart creation  
  - `pytest` for automated testing

- `README.md`  
  Provides project overview, installation instructions, usage examples, and design rationale in a multi-paragraph format of approximately 500 words.

- `video_url.txt`  
  Contains the unlisted YouTube URL for the 3-minute demo video as required by the submission guidelines.

- `expenses.db`  
  SQLite database file created on first run or by `initialize_db`. This file is ignored by version control if `.gitignore` is configured, although it can be committed for convenience.

## Design Decisions

The decision to use SQLite was driven by the need for a durable, file-based storage solution without requiring an external database server. SQLite is included in Python’s standard library, which simplifies deployment. Argument parsing is handled by `argparse` to provide a familiar CLI interface. Data aggregation and filtering logic are implemented using simple Python list comprehensions and dictionary operations to keep dependencies minimal and code readable.

Charts are generated using `matplotlib` because of its flexibility in labeling and saving figures. Tests leverage `pytest` fixtures to create a temporary database for each test, ensuring that test runs do not interfere with one another or with the user’s real data.

## Running Tests

Automated tests validate the core functionality:

```bash
pytest
```

The tests include:

- `test_add_expense_creates_entry`: Verifies that adding an expense stores the correct record in the database.  
- `test_get_total_by_category`: Checks that totals are aggregated correctly by category.  
- `test_generate_report_all`: Confirms that the “all” period report returns accurate totals, category breakdown, and date bounds.

Passing all tests is a requirement for successful project submission.

## Future Enhancements

Potential next steps include:
- Adding an interactive text-based menu instead of direct CLI commands.  
- Supporting CSV export and import for interoperability.  
- Implementing recurring expenses and budget alerts.  
- Enhancing plotting capabilities with additional chart types (pie charts, time series).  
- Building a web front end using Flask or FastAPI on top of the same SQLite schema.

These enhancements would deepen the application’s complexity, broaden its utility, and showcase additional Python skills beyond the core requirements.
---
👋 We hope you find this project useful! 🚀

## Contact Developer  
    Email: masudpythongit@gmail.com 
    Telegram: https://t.me/Masoud_GhasemiI_sorna_fast
🔗 GitHub Profile: [sorna-fast](https://github.com/sorna-fast)
