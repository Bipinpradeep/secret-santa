import csv
import os
import unittest

from secret_santa import CSVHandler, Employee, SecretSantaAssigner


class TestSecretSanta(unittest.TestCase):
    def setUp(self):
        self.employees = [
            Employee("Alice", "alice@acme.com"),
            Employee("Bob", "bob@acme.com"),
            Employee("Charlie", "charlie@acme.com"),
        ]
        self.previous_assignments = {
            "alice@acme.com": "bob@acme.com",
            "bob@acme.com": "charlie@acme.com",
            "charlie@acme.com": "alice@acme.com",
        }
        self.assigner = SecretSantaAssigner(self.employees, self.previous_assignments)

    def test_employee_equality(self):
        emp1 = Employee("Alice", "alice@acme.com")
        emp2 = Employee("Alice", "alice@acme.com")
        emp3 = Employee("Bob", "bob@acme.com")
        self.assertEqual(emp1, emp2)
        self.assertNotEqual(emp1, emp3)

    def test_valid_assignment(self):
        alice = self.employees[0]
        bob = self.employees[1]
        charlie = self.employees[2]
        self.assertFalse(self.assigner.is_valid_assignment(alice, alice))
        self.assertFalse(self.assigner.is_valid_assignment(alice, bob))
        self.assertTrue(self.assigner.is_valid_assignment(alice, charlie))

    def test_assign_secret_santas(self):
        assignments = self.assigner.assign_secret_santas()
        self.assertIsNotNone(assignments)
        self.assertEqual(len(assignments), len(self.employees))
        for giver, receiver in assignments.items():
            self.assertNotEqual(giver, receiver)
            prev_child_email = self.previous_assignments.get(giver.email)
            if prev_child_email:
                self.assertNotEqual(receiver.email, prev_child_email)
        receivers = set(assignments.values())
        self.assertEqual(len(receivers), len(self.employees))

    def test_csv_read_employees(self):
        test_file = "test_employees.csv"
        with open(test_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Employee_Name", "Employee_EmailID"])
            for emp in self.employees:
                writer.writerow([emp.name, emp.email])
        read_employees = CSVHandler.read_employees(test_file)
        self.assertEqual(len(read_employees), len(self.employees))
        self.assertEqual(read_employees[0].email, "alice@acme.com")
        os.remove(test_file)

    def test_csv_read_previous_assignments(self):
        test_file = "test_previous.csv"
        with open(test_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "Employee_Name",
                    "Employee_EmailID",
                    "Secret_Child_Name",
                    "Secret_Child_EmailID",
                ]
            )
            writer.writerow(["Alice", "alice@acme.com", "Bob", "bob@acme.com"])
            writer.writerow(["Bob", "bob@acme.com", "Charlie", "charlie@acme.com"])
            writer.writerow(["Charlie", "charlie@acme.com", "Alice", "alice@acme.com"])
        prev_assignments = CSVHandler.read_previous_assignments(test_file)
        self.assertEqual(prev_assignments, self.previous_assignments)
        os.remove(test_file)

    def test_csv_write_assignments(self):
        test_file = "test_output.csv"
        assignments = {
            self.employees[0]: self.employees[1],
            self.employees[1]: self.employees[2],
        }
        CSVHandler.write_assignments(test_file, assignments)
        with open(test_file, newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["Employee_EmailID"], "alice@acme.com")
            self.assertEqual(rows[0]["Secret_Child_EmailID"], "bob@acme.com")
        os.remove(test_file)

    def test_error_handling(self):
        try:
            CSVHandler.read_employees("nonexistent.csv")
        except Exception as e:
            print(f"Caught: {type(e).__name__}: {e}")
        with self.assertRaises(ValueError):
            CSVHandler.read_employees("nonexistent.csv")


if __name__ == "__main__":
    unittest.main()
