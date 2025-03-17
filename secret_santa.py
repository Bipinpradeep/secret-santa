import csv
import random
import sys
from typing import Dict, List, Optional, Tuple


class Employee:
    """Represents an employee with a name and email ID."""

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def __eq__(self, other):
        return isinstance(other, Employee) and self.email == other.email

    def __hash__(self):
        return hash(self.email)

    def __repr__(self):
        return f"{self.name} ({self.email})"


class SecretSantaAssigner:
    """Handles the logic for assigning Secret Santa pairs."""

    def __init__(self, employees: List[Employee], previous_assignments: Dict[str, str]):
        self.employees = employees
        self.previous_assignments = previous_assignments
        self.assignments: Dict[Employee, Employee] = {}

    def is_valid_assignment(self, giver: Employee, receiver: Employee) -> bool:
        """Checks if assigning receiver to giver violates any rules."""
        if giver == receiver:
            return False
        prev_child_email = self.previous_assignments.get(giver.email)
        if prev_child_email and prev_child_email == receiver.email:
            return False
        return receiver not in self.assignments.values()

    def assign_secret_santas(self) -> Optional[Dict[Employee, Employee]]:
        """Generates a valid Secret Santa assignment for all employees."""
        available = self.employees.copy()
        random.shuffle(available)

        def backtrack(current: int) -> bool:
            if current == len(self.employees):
                return True
            giver = self.employees[current]
            random.shuffle(available)
            for receiver in available:
                if self.is_valid_assignment(giver, receiver):
                    self.assignments[giver] = receiver
                    available.remove(receiver)
                    if backtrack(current + 1):
                        return True
                    del self.assignments[giver]
                    available.append(receiver)
            return False

        if backtrack(0):
            return self.assignments
        return None


class CSVHandler:
    """Handles reading and writing CSV files."""

    @staticmethod
    def read_employees(file_path: str) -> List[Employee]:
        """Reads employee data from a CSV file."""
        employees = []
        try:
            with open(file_path, newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    employees.append(
                        Employee(row["Employee_Name"], row["Employee_EmailID"])
                    )
            return employees
        except FileNotFoundError:
            raise ValueError(f"Employee file {file_path} not found.")
        except KeyError:
            raise ValueError(
                "Employee CSV must contain 'Employee_Name' and 'Employee_EmailID' columns."
            )

    @staticmethod
    def read_previous_assignments(file_path: str) -> Dict[str, str]:
        """Reads previous year's assignments from a CSV file."""
        assignments = {}
        try:
            with open(file_path, newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    assignments[row["Employee_EmailID"]] = row["Secret_Child_EmailID"]
            return assignments
        except FileNotFoundError:
            return {}  # No previous assignments file is okay
        except KeyError:
            raise ValueError(
                "Previous assignments CSV must contain 'Employee_EmailID' and 'Secret_Child_EmailID' columns."
            )

    @staticmethod
    def write_assignments(file_path: str, assignments: Dict[Employee, Employee]):
        """Writes the new assignments to a CSV file."""
        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "Employee_Name",
                    "Employee_EmailID",
                    "Secret_Child_Name",
                    "Secret_Child_EmailID",
                ]
            )
            for giver, receiver in assignments.items():
                writer.writerow(
                    [giver.name, giver.email, receiver.name, receiver.email]
                )


def main():
    """Main function to run the Secret Santa assignment process with command-line arguments."""
    if len(sys.argv) != 4:
        print(
            "Usage: python secret_santa.py <employee_file> <previous_assignments_file> <output_file>"
        )
        print(
            "Example: python secret_santa.py Employee-List.csv Secret-Santa-Game-Result-2023.csv output.csv"
        )
        sys.exit(1)

    employee_file = sys.argv[1]
    prev_file = sys.argv[2]
    output_file = sys.argv[3]

    try:
        employees = CSVHandler.read_employees(employee_file)
        previous_assignments = CSVHandler.read_previous_assignments(prev_file)

        current_emails = {e.email for e in employees}
        for emp_email in previous_assignments.keys():
            if emp_email not in current_emails:
                raise ValueError(
                    f"Employee {emp_email} from previous assignments not found in current list."
                )

        assigner = SecretSantaAssigner(employees, previous_assignments)
        assignments = assigner.assign_secret_santas()

        if assignments is None:
            print("No valid Secret Santa assignment possible.")
            sys.exit(1)

        CSVHandler.write_assignments(output_file, assignments)
        print(f"Assignments written to {output_file}")

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
