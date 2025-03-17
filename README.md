# Secret Santa Assignment System

This application automates the process of assigning Secret Santa pairs for company events, ensuring that employees don't get assigned to the same person as the previous year.

## Overview

The Secret Santa Assignment System is designed to solve the "Acme" company's challenge of automating their annual Secret Santa event. The system takes a list of employees, considers previous year's assignments (if available), and generates new valid pairings following specific rules:

- An employee cannot be their own Secret Santa
- An employee cannot be assigned to the same person as the previous year
- Each employee must be assigned exactly one Secret Santa recipient
- Each employee must be assigned as a recipient exactly once

## Features

- Parses employee data from CSV files
- Handles previous year's assignments to avoid repetition
- Uses backtracking algorithm to find valid assignments
- Implements proper error handling for various scenarios
- Provides clear output in CSV format

## Requirements

- Python 3.6 or higher
- CSV files with required formats (described below)

## Installation

Clone this repository to your local machine:

```bash
git clone <repository-url>
cd secret-santa-assignment
```

No additional dependencies are required beyond the Python standard library.

## Usage

Run the program from the command line with three arguments:

```bash
python secret_santa.py <employee_file> <previous_assignments_file> <output_file>
```

Example:
```bash
python secret_santa.py Employee-List.csv Secret-Santa-Game-Result-2023.csv Secret-Santa-Game-Result-2024.csv
```

Running the unittests 
```bash
python -m unittest tests/test_secret_santa.py
```

### Input Formats

#### Employee List CSV
The employee list CSV must contain the following columns:
- `Employee_Name`: Full name of the employee
- `Employee_EmailID`: Email address of the employee

Example:
```
Employee_Name,Employee_EmailID
John Doe,john.doe@acme.com
Jane Smith,jane.smith@acme.com
```

#### Previous Assignments CSV
The previous assignments CSV should contain:
- `Employee_Name`: Name of the Secret Santa giver
- `Employee_EmailID`: Email of the Secret Santa giver
- `Secret_Child_Name`: Name of the gift recipient
- `Secret_Child_EmailID`: Email of the gift recipient

Example:
```
Employee_Name,Employee_EmailID,Secret_Child_Name,Secret_Child_EmailID
John Doe,john.doe@acme.com,Jane Smith,jane.smith@acme.com
Jane Smith,jane.smith@acme.com,Alice Johnson,alice.johnson@acme.com
```

Note: If no previous assignments exist, the system will still work correctly.

### Output Format

The program generates a CSV file with new Secret Santa assignments in the following format:
```
Employee_Name,Employee_EmailID,Secret_Child_Name,Secret_Child_EmailID
```

## Code Structure

- `Employee`: Class representing an employee with name and email
- `SecretSantaAssigner`: Class handling the assignment logic with backtracking algorithm
- `CSVHandler`: Class for reading employee data and writing assignments
- `main()`: Primary function that orchestrates the entire process

## Error Handling

The system handles various error scenarios:
- Missing employee files
- Incorrectly formatted CSV files
- Employee in previous assignments not found in current list
- No valid assignment possible

## Algorithm

The assignment algorithm uses recursive backtracking to find a valid solution:
1. For each employee (giver), it tries to find a valid recipient
2. If a valid assignment is found, it moves to the next employee
3. If no valid assignment is possible, it backtracks and tries different assignments
4. This continues until all employees are assigned or it's determined no solution exists

## Testing

While tests are not included in this version, the code is designed with clear interfaces that make it highly testable. Key testing scenarios would include:
- Valid assignments with various employee counts
- Edge cases with minimal employees
- Handling of previous year constraints
- Error conditions and recovery
