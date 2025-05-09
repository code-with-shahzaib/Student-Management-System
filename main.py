import json
import csv
import os
from typing import List, Dict, Optional
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Constants
DATA_FILE = "students.json"
BACKUP_DIR = "backups"
CSV_EXPORT_FILE = "students_export.csv"

class StudentManagementSystem:
    def __init__(self):
        self.students = self.load_students()
        self.create_backup_dir()
        
    def create_backup_dir(self) -> None:
        """Create backup directory if it doesn't exist"""
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)

    def load_students(self) -> List[Dict]:
        """Load student records from JSON file"""
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r') as file:
                    return json.load(file)
            return []
        except Exception as e:
            print(f"{Fore.RED}❌ Error loading student records: {e}{Style.RESET_ALL}")
            return []

    def save_students(self) -> None:
        """Save students to JSON file and create backup"""
        try:
            with open(DATA_FILE, 'w') as file:
                json.dump(self.students, file, indent=4)
            
            # Create backup
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(BACKUP_DIR, f"students_backup_{timestamp}.json")
            with open(backup_file, 'w') as file:
                json.dump(self.students, file, indent=4)
        except Exception as e:
            print(f"{Fore.RED}❌ Error saving student records: {e}{Style.RESET_ALL}")

    def clear_screen(self) -> None:
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def validate_name(self, name: str) -> bool:
        """Validate student name"""
        return name.strip() != "" and all(c.isalpha() or c.isspace() for c in name)

    def validate_roll_number(self, roll_number: int) -> bool:
        """Validate roll number"""
        return roll_number > 0 and not any(
            student['roll_number'] == roll_number 
            for student in self.students
        )

    def validate_age(self, age: int) -> bool:
        """Validate age"""
        return 5 <= age <= 120

    def validate_cgpa(self, cgpa: float) -> bool:
        """Validate CGPA"""
        return 0.0 <= cgpa <= 4.0

    def add_student(self) -> None:
        """Add a new student to the system"""
        self.clear_screen()
        print(f"{Fore.CYAN}➕ Add New Student{Style.RESET_ALL}\n")

        try:
            # Name input with validation
            while True:
                name = input("Enter Student's Name: ").strip()
                if self.validate_name(name):
                    break
                print(f"{Fore.YELLOW}❌ Invalid name! Only letters and spaces allowed.{Style.RESET_ALL}")

            # Roll number input with validation
            while True:
                try:
                    roll_number = int(input("Enter Student's Roll Number: "))
                    if self.validate_roll_number(roll_number):
                        break
                    print(f"{Fore.YELLOW}❌ Invalid roll number! Must be unique and positive.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.YELLOW}❌ Please enter a valid number.{Style.RESET_ALL}")

            # Age input with validation
            while True:
                try:
                    age = int(input("Enter Student's Age: "))
                    if self.validate_age(age):
                        break
                    print(f"{Fore.YELLOW}❌ Age must be between 5 and 120.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.YELLOW}❌ Please enter a valid number.{Style.RESET_ALL}")

            # CGPA input with validation
            while True:
                try:
                    cgpa = float(input("Enter Student's CGPA (0.0-4.0): "))
                    if self.validate_cgpa(cgpa):
                        break
                    print(f"{Fore.YELLOW}❌ CGPA must be between 0.0 and 4.0.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.YELLOW}❌ Please enter a valid number.{Style.RESET_ALL}")

            # Create and add student
            student = {
                "roll_number": roll_number,
                "name": name,
                "age": age,
                "cgpa": cgpa
            }
            self.students.append(student)
            self.save_students()
            print(f"{Fore.GREEN}✅ Student added successfully!{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}❌ An error occurred: {e}{Style.RESET_ALL}")

    def view_all_students(self, students_list: List[Dict] = None) -> None:
        """Display all students in a formatted table"""
        self.clear_screen()
        students = students_list if students_list else self.students
        print(f"{Fore.CYAN}📋 All Student Records{Style.RESET_ALL}\n")

        if not students:
            print(f"{Fore.YELLOW}No students found.{Style.RESET_ALL}")
            input("\nPress Enter to return to menu...")
            return

        # Table header
        print(f"{Fore.BLUE}{'Roll No':<10}{'Name':<25}{'Age':<10}{'CGPA':<10}{Style.RESET_ALL}")
        print("-" * 55)
        
        # Table rows
        for student in students:
            cgpa_color = Fore.GREEN if student['cgpa'] >= 3.5 else (
                Fore.YELLOW if student['cgpa'] >= 2.5 else Fore.RED
            )
            print(
                f"{student['roll_number']:<10}"
                f"{student['name']:<25}"
                f"{student['age']:<10}"
                f"{cgpa_color}{student['cgpa']:<10}{Style.RESET_ALL}"
            )
        
        # Keep the output visible until user presses Enter
        input("\nPress Enter to return to menu...")

    def search_student(self) -> Optional[Dict]:
        """Search for a student by various criteria"""
        self.clear_screen()
        print(f"{Fore.CYAN}🔍 Search Student{Style.RESET_ALL}\n")
        
        if not self.students:
            print(f"{Fore.YELLOW}No students to search.{Style.RESET_ALL}")
            return None

        print("Search by:")
        print("1. Roll Number")
        print("2. Name")
        print("3. Age Range")
        print("4. CGPA Range")
        print("5. Back to Menu")

        try:
            choice = int(input("Enter your choice [1-5]: "))
            
            if choice == 1:
                roll = int(input("Enter Roll Number: "))
                for student in self.students:
                    if student['roll_number'] == roll:
                        return student
                print(f"{Fore.YELLOW}No student found with this roll number.{Style.RESET_ALL}")
                
            elif choice == 2:
                name = input("Enter Name (partial matches accepted): ").lower()
                matches = [s for s in self.students if name in s['name'].lower()]
                if matches:
                    self.view_all_students(matches)
                    return matches[0] if len(matches) == 1 else None
                print(f"{Fore.YELLOW}No matching students found.{Style.RESET_ALL}")
                
            elif choice == 3:
                min_age = int(input("Minimum Age: "))
                max_age = int(input("Maximum Age: "))
                matches = [s for s in self.students if min_age <= s['age'] <= max_age]
                if matches:
                    self.view_all_students(matches)
                    return matches[0] if len(matches) == 1 else None
                print(f"{Fore.YELLOW}No students in this age range.{Style.RESET_ALL}")
                
            elif choice == 4:
                min_cgpa = float(input("Minimum CGPA: "))
                max_cgpa = float(input("Maximum CGPA: "))
                matches = [s for s in self.students if min_cgpa <= s['cgpa'] <= max_cgpa]
                if matches:
                    self.view_all_students(matches)
                    return matches[0] if len(matches) == 1 else None
                print(f"{Fore.YELLOW}No students in this CGPA range.{Style.RESET_ALL}")
                
            elif choice == 5:
                return None
                
            else:
                print(f"{Fore.YELLOW}Invalid choice.{Style.RESET_ALL}")
                
        except ValueError:
            print(f"{Fore.RED}Please enter valid numbers.{Style.RESET_ALL}")
            
        return None

    def update_student(self) -> None:
        """Update a student's record"""
        self.clear_screen()
        print(f"{Fore.CYAN}✏️ Update Student{Style.RESET_ALL}\n")
        
        student = self.search_student()
        if not student:
            return

        print("\nCurrent Details:")
        print(f"1. Name: {student['name']}")
        print(f"2. Age: {student['age']}")
        print(f"3. CGPA: {student['cgpa']}")
        print("4. Cancel")

        try:
            choice = int(input("Select field to update [1-4]: "))
            
            if choice == 1:
                new_name = input("New Name: ").strip()
                if self.validate_name(new_name):
                    student['name'] = new_name
                    self.save_students()
                    print(f"{Fore.GREEN}✅ Name updated successfully!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}❌ Invalid name!{Style.RESET_ALL}")
                    
            elif choice == 2:
                new_age = int(input("New Age: "))
                if self.validate_age(new_age):
                    student['age'] = new_age
                    self.save_students()
                    print(f"{Fore.GREEN}✅ Age updated successfully!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}❌ Invalid age!{Style.RESET_ALL}")
                    
            elif choice == 3:
                new_cgpa = float(input("New CGPA: "))
                if self.validate_cgpa(new_cgpa):
                    student['cgpa'] = new_cgpa
                    self.save_students()
                    print(f"{Fore.GREEN}✅ CGPA updated successfully!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}❌ Invalid CGPA!{Style.RESET_ALL}")
                    
            elif choice == 4:
                print(f"{Fore.BLUE}Update cancelled.{Style.RESET_ALL}")
                
            else:
                print(f"{Fore.YELLOW}Invalid choice.{Style.RESET_ALL}")
                
        except ValueError:
            print(f"{Fore.RED}Please enter valid input.{Style.RESET_ALL}")

    def delete_student(self) -> None:
        """Delete a student record"""
        self.clear_screen()
        print(f"{Fore.CYAN}❌ Delete Student{Style.RESET_ALL}\n")
        
        student = self.search_student()
        if not student:
            return

        confirm = input(f"Are you sure you want to delete {student['name']}? (y/n): ").lower()
        if confirm == 'y':
            self.students.remove(student)
            self.save_students()
            print(f"{Fore.GREEN}✅ Student deleted successfully!{Style.RESET_ALL}")
        else:
            print(f"{Fore.BLUE}Deletion cancelled.{Style.RESET_ALL}")

    def sort_students(self) -> None:
        """Sort students by different criteria"""
        self.clear_screen()
        print(f"{Fore.CYAN}🔃 Sort Students{Style.RESET_ALL}\n")
        
        if not self.students:
            print(f"{Fore.YELLOW}No students to sort.{Style.RESET_ALL}")
            return

        print("Sort by:")
        print("1. Roll Number (Ascending)")
        print("2. Name (A-Z)")
        print("3. Age (Youngest first)")
        print("4. CGPA (Highest first)")
        print("5. Cancel")

        try:
            choice = int(input("Enter your choice [1-5]: "))
            
            if choice == 1:
                self.students.sort(key=lambda x: x['roll_number'])
                print(f"{Fore.GREEN}✅ Sorted by Roll Number!{Style.RESET_ALL}")
            elif choice == 2:
                self.students.sort(key=lambda x: x['name'].lower())
                print(f"{Fore.GREEN}✅ Sorted by Name!{Style.RESET_ALL}")
            elif choice == 3:
                self.students.sort(key=lambda x: x['age'])
                print(f"{Fore.GREEN}✅ Sorted by Age!{Style.RESET_ALL}")
            elif choice == 4:
                self.students.sort(key=lambda x: x['cgpa'], reverse=True)
                print(f"{Fore.GREEN}✅ Sorted by CGPA!{Style.RESET_ALL}")
            elif choice == 5:
                print(f"{Fore.BLUE}Sorting cancelled.{Style.RESET_ALL}")
                return
            else:
                print(f"{Fore.YELLOW}Invalid choice.{Style.RESET_ALL}")
                return
                
            self.save_students()
            self.view_all_students()
            
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")

    def export_to_csv(self) -> None:
        """Export student records to CSV file"""
        self.clear_screen()
        print(f"{Fore.CYAN}📤 Export to CSV{Style.RESET_ALL}\n")
        
        if not self.students:
            print(f"{Fore.YELLOW}No students to export.{Style.RESET_ALL}")
            return

        try:
            with open(CSV_EXPORT_FILE, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=self.students[0].keys())
                writer.writeheader()
                writer.writerows(self.students)
            print(f"{Fore.GREEN}✅ Students exported to {CSV_EXPORT_FILE}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ Error exporting: {e}{Style.RESET_ALL}")

    def show_statistics(self) -> None:
        """Display statistics about students"""
        self.clear_screen()
        print(f"{Fore.CYAN}📊 Student Statistics{Style.RESET_ALL}\n")
        
        if not self.students:
            print(f"{Fore.YELLOW}No student data available.{Style.RESET_ALL}")
            return

        total = len(self.students)
        ages = [s['age'] for s in self.students]
        cgpas = [s['cgpa'] for s in self.students]
        
        print(f"Total Students: {Fore.BLUE}{total}{Style.RESET_ALL}")
        print(f"Average Age: {Fore.BLUE}{sum(ages)/total:.1f} years{Style.RESET_ALL}")
        print(f"Average CGPA: {Fore.BLUE}{sum(cgpas)/total:.2f}{Style.RESET_ALL}")
        
        # Age distribution
        print("\nAge Distribution:")
        age_groups = {"<18": 0, "18-22": 0, "23-25": 0, ">25": 0}
        for age in ages:
            if age < 18: age_groups["<18"] += 1
            elif 18 <= age <= 22: age_groups["18-22"] += 1
            elif 23 <= age <= 25: age_groups["23-25"] += 1
            else: age_groups[">25"] += 1
        
        for group, count in age_groups.items():
            if count > 0:
                percentage = (count / total) * 100
                print(f"{group}: {Fore.BLUE}{count} ({percentage:.1f}%){Style.RESET_ALL}")
        
        # CGPA distribution
        print("\nCGPA Distribution:")
        cgpa_groups = {"<2.0": 0, "2.0-2.9": 0, "3.0-3.5": 0, ">3.5": 0}
        for cgpa in cgpas:
            if cgpa < 2.0: cgpa_groups["<2.0"] += 1
            elif 2.0 <= cgpa < 3.0: cgpa_groups["2.0-2.9"] += 1
            elif 3.0 <= cgpa < 3.5: cgpa_groups["3.0-3.5"] += 1
            else: cgpa_groups[">3.5"] += 1
        
        for group, count in cgpa_groups.items():
            if count > 0:
                percentage = (count / total) * 100
                print(f"{group}: {Fore.BLUE}{count} ({percentage:.1f}%){Style.RESET_ALL}")

    def show_menu(self) -> None:
        """Display the main menu"""
        self.clear_screen()
        print(f"{Fore.MAGENTA}==============================================")
        print("        🎓 STUDENT MANAGEMENT SYSTEM")
        print("==============================================")
        print(f"{Fore.CYAN}0. Exit")
        print("1. Add New Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Sort Students")
        print("7. Export to CSV")
        print(f"8. Statistics{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}==============================================")

    def run(self) -> None:
        """Run the student management system"""
        while True:
            self.show_menu()
            
            try:
                choice = input(f"{Fore.YELLOW}Enter your choice [0-8]: {Style.RESET_ALL}")
                
                if choice == '0':
                    print(f"{Fore.GREEN}👋 Thank you for using the Student Management System!{Style.RESET_ALL}")
                    break
                    
                elif choice == '1':
                    self.add_student()
                    
                elif choice == '2':
                    self.view_all_students()
                    
                elif choice == '3':
                    result = self.search_student()
                    if result and len(self.students) > 1:
                        input("\nPress Enter to continue...")
                    
                elif choice == '4':
                    self.update_student()
                    
                elif choice == '5':
                    self.delete_student()
                    
                elif choice == '6':
                    self.sort_students()
                    
                elif choice == '7':
                    self.export_to_csv()
                    
                elif choice == '8':
                    self.show_statistics()
                    
                else:
                    print(f"{Fore.RED}⚠️ Invalid choice! Please enter 0-8.{Style.RESET_ALL}")
                    input("\nPress Enter to continue...")
                
                # Removed the general pause since each function handles its own now
                
            except Exception as e:
                print(f"{Fore.RED}❌ An error occurred: {e}{Style.RESET_ALL}")
                input("\nPress Enter to continue...")

if __name__ == "__main__":
    system = StudentManagementSystem()
    system.run()