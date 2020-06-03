""" File for all operations performed under Admin."""

import re
from validation import Validation


class Admin:

    def __init__(self, connection):
        self.conn = connection

        # regular expression for validating email
        self.regex = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"

    def admin_menu(self, email):
        """
        Display all features an admin is allowed to perform.
        :param email: email of logged in admin
        :return: True
        """
        print("\nWELCOME -> {}".format(email))
        print("\n### ADMIN MENU ###")
        print("1. Employee\n2. Cabs\n3. Bookings as per employee\n4. Bookings as per dates\n5. Logout")
        choice = input("Choice: ")

        if choice == '1':
            self.admin_employees_menu()
        elif choice == '2':
            self.admin_cabs_menu()
        elif choice == '3':
            self.employee_bookings()
        elif choice == '4':
            self.bookings_for_dates()
        elif choice == '5':
            print()
        else:
            print("\nWrong Input!  Try again.")

        if choice != '5':
            self.admin_menu(email)

        return True

    def admin_employees_menu(self):
        """
        CRUD operations for employee.
        :return: True
        """
        print("\n### EMPLOYEE'S MENU ###")
        print("1. Add Employee\n2. Update Employee\n3. Remove Employee\n4. Show all Employees\n5. GO Back")
        choice = input("Choice: ")

        if choice == '1':
            self.add_employee()
        elif choice == '2':
            self.update_employee()
        elif choice == '3':
            self.delete_employee()
        elif choice == '4':
            self.show_employees()
        elif choice == '5':
            print()
        else:
            print("\nWrong Input!  Try again.")

        if choice != '5':
            self.admin_employees_menu()

        return True

    def add_employee(self):
        """
        Fetch employee details from user.
        :return: True/False
        """
        try:
            print("\nAdd Employee\n------------")
            fname = Validation.input_str_for_create(self, "First name: ")
            lname = Validation.input_str_for_create(self, "Last name: ")
            email = input("Enter Email: ").lower()
            phone = Validation.validate_phn_no("Phone no.: ")

            c = self.conn.cursor()
            c.execute("SELECT count(*) from employees WHERE lower(email)='{}'".format(email))
            c.execute("INSERT INTO employees (FNAME,LNAME,EMAIL,PHONE) VALUES('{}','{}','{}','{}')"
                      .format(fname, lname, email, phone))
            c.execute("INSERT INTO users VALUES('{}','{}',{})"
                      .format(email, fname.lower() + '@' + str(123), 22))
        except Exception as e:
            print("error",e)


    def update_employee(self):
        """
        Fetch record of employee w.r.t. employee email.
        :return: True/False
        """
        print("\nUpdate Employee\n---------------")
        email = input("Enter email: ").lower()

        try:
            c = self.conn.cursor()
            c.execute("SELECT * from employees WHERE lower(email)='{}'".format(email))
            member = c.fetchone()
            if member is None:
                print("\nNo matching record found with '{}'.".format(email))
            else:
                print("\nEnter new details for '{}'\n(Press ENTER to skip the change in value.)".format(email))
                fname = input("First Name: ") or member[1]
                lname = input("Last Name: ") or member[2]
                new_email = input("Email: ").lower() or member[3]
                phone = input("Phone no.: ") or member[4]

                c = self.conn.cursor()
                c.execute("SELECT count(*) from employees WHERE lower(email)='{}'".format(email))

        except Exception as e:
            print(type(e).__name__, ": ", e)

        return False


    def delete_employee(self):
        """
        Delete employee.
        :return: True/False
        """
        print("\nDelete Employee\n---------------")
        email = input("Enter email: ").lower()

        try:
            c = self.conn.cursor()
            c.execute("SELECT * from employees WHERE lower(email)='{}'".format(email))
            if c.fetchone() is not None:
                ch = input("Want to delete '{}' (y/n): ".format(email))
                if ch.lower() == 'y':
                    c.execute("DELETE from users WHERE lower(email)='{}'".format(email))
                    c.execute("DELETE from employees WHERE lower(email)='{}'".format(email))
                    self.conn.commit()
                    print("\nRecord deleted.")
                    return True
                else:
                    print("\nAction aborted!")
            else:
                print("\nNo record found with '{}'".format(email))
        except Exception as e:
            print(type(e).__name__, ": ", e)

        return False

    def show_employees(self):
        """
        Display all employees.
        :return: True/False
        """
        try:
            c = self.conn.cursor()
            c.execute("SELECT * FROM employees;")
            result = c.fetchall()
            if len(result) > 0:
                print("\nEMPLOYEES LIST\n------------")
                print("\nFNAME\tLNAME\tEMAIL\tPHONE NO.")
                print("-----\t-----\t-----\t---------")
                for row in result:
                    print("{}\t\t{}\t\t{}\t\t{}"
                          .format(row[1], row[2], row[3], row[4]))
                return True
            else:
                print("\nNo data found.")
        except Exception as e:
            print(type(e).__name__, ": ", e)

        return False

    def admin_cabs_menu(self):
        """
        CRUD operations for cabs.
        :return: True
        """
        print("\n### CAB'S MENU ###")
        print("1. Add Cab\n2. Update Cab\n3. Remove Cab\n4. Show all Cabs\n5. GO Back")
        choice = input("Choice: ")

        if choice == '1':
            self.add_cab()
        elif choice == '2':
            self.update_cab()
        elif choice == '3':
            self.remove_cab()
        elif choice == '4':
            self.show_cabs()
        elif choice == '5':
            print()
        else:
            print("\nWrong Input!  Try again.")

        if choice != '5':
            self.admin_cabs_menu()

        return True

    def add_cab(self):
        """
        Get input from user for cab details.
        :return: True/False
        """
        print("\nAdd Cab\n-------")
        cab_no = Validation.input_str_for_create(self, "Cab no.: ")
        rider_name = Validation.input_str_for_create(self, "Rider Name: ")
        rider_no = Validation.input_str_for_create(self, "Enter No: ")
        capacity = Validation.input_int_for_create(self, "Capacity: ")

        cab_no = re.sub(' +', ' ', cab_no)

        return self.add_cab_action(cab_no, rider_name, rider_no, capacity)

    def add_cab_action(self, cab_no, rider_name, rider_no, capacity):
        """
        Insert cab details in database.
        :param cab_no: cab registered no.
        :param rider_name: rider name
        :param rider_no: rider phone no.
        :param capacity: max occupancy of the cab
        :return: True/False
        """
        try:
            c = self.conn.cursor()
            c.execute("INSERT INTO cabs(CAB_NO,RIDER_NAME,RIDER_NO,CAPACITY) VALUES('{}','{}','{}',{})"
                      .format(cab_no, rider_name, rider_no, capacity))
            self.conn.commit()
            print("\n'{}' added as Cab".format(cab_no))
            return self.update_cab(cab_no)
        except Exception as e:
            print(type(e).__name__, ": ", e)

        return False

    def update_cab(self, cab_num=None):
        """
        Update routes of the cab for the given cab_no.
        :param cab_num: cab no.
        :return: True/False
        """
        print("\nUpdate Cab\n----------")
        if cab_num is None:
            cab_num = input("\nEnter Cab No.: ").upper()
            cab_num = re.sub(' +', ' ', cab_num)

        try:
            c = self.conn.cursor()
            c.execute("SELECT id,capacity FROM cabs WHERE upper(cab_no)='{}'".format(cab_num))
            cab_data = c.fetchone()

            if cab_data:
                print("Enter routes for cab - {}".format(cab_num))
                print("Enter # to GO Back.")

                while True:
                    print()
                    source = input("Source: ")
                    if source == '#':
                        break
                    destination = input("Destination: ")
                    if destination == '#':
                        break
                    timing = input("Timing (hh:mm): ")
                    if timing == '#':
                        break

                    c.execute("INSERT INTO routes(cab_id,source,destination,timing,seats_available) \
                                VALUES({},'{}','{}','{}',{})"
                              .format(cab_data[0], source, destination, timing, cab_data[1]))
                    self.conn.commit()

                print("\nRoutes Updated.")
                return True
            else:
                print("No data found.")

        except Exception as e:
            print(type(e).__name__, ": ", e)

        return False

    def remove_cab(self):
        """
        Remove cab from the database.
        :return: True/False
        """
        print("\nRemove Cab\n----------")
        cab_num = input("Enter Cab No.: ").upper()

        try:
            c = self.conn.cursor()
            c.execute("SELECT ID from cabs WHERE upper(cab_no)='{}'".format(cab_num))
            cab_id = c.fetchone()

            if cab_id is not None:
                ch = input("Want to delete '{}' (y/n): ".format(cab_num))
                if ch.lower() == 'y':
                    c.execute("DELETE from cabs WHERE cab_no='{}'".format(cab_num))
                    c.execute("DELETE from routes WHERE cab_id='{}'".format(cab_id[0]))
                    self.conn.commit()
                    print("\nCab deleted.")
                    return True
                else:
                    print("\nAction aborted!")
            else:
                print("\nNo record found with '{}'".format(cab_num))
        except Exception as e:
            print(type(e).__name__, ": ", e)

        return False

    def show_cabs(self):
        """
        Display all cabs.
        :return: True/False
        """
        try:
            c = self.conn.cursor()
            c.execute("SELECT * FROM cabs;")
            result = c.fetchall()
            if len(result) > 0:
                print("\nCABS LIST\n------------")
                print("\nCAB NO.\t\t\t\tRIDER NAME\t\tRIDER NO.\tTOTAL CAPACITY")
                print("-------\t\t\t\t----------\t\t---------\t--------------")
                for row in result:
                    print("{}\t\t{}\t{}\t{}"
                          .format(row[1], row[2], row[3], row[4]))
                return True
            else:
                print("\nNo data found.")
        except Exception as e:
            print(type(e).__name__, ": ", e)

        return False

    def employee_bookings(self):
        """
        Show all bookings for a particular employee
        :return: True/False
        """
        emp_email = input("\nEmployee email: ")

        try:
            c = self.conn.cursor()
            c.execute("SELECT id FROM employees WHERE lower(email)='{}'".format(emp_email))
            emp_id = c.fetchone()
            if emp_id:
                c.execute("SELECT bookings.*,cabs.cab_no,routes.* FROM bookings  \
                            JOIN routes ON routes.ID=bookings.ROUTE_ID \
                            JOIN cabs ON cabs.ID=routes.CAB_ID WHERE emp_id={}"
                          .format(emp_id[0]))
                result = c.fetchall()
                if len(result) > 0:
                    print("\nBOOKING DETAILS\n---------------")
                    print("\nCAB NO\tSOURCE\tDESTINATION\tDATE\tTIME\tOCCUPANCY\tSTATUS")
                    print("------\t------\t-----------\t----\t----\t---------\t------")

                    for row in result:
                        status = 'COMPLETED' if row[6] == 1 else 'CANCELED' if row[6] == 0 else 'UPCOMING'
                        print("{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}"
                              .format(row[7], row[10], row[11], row[3], row[4], row[5], status))
                    return True
                else:
                    print("\nNo data found.")
            else:
                print("\nNo record found with '{}'".format(emp_email))
        except Exception as e:
            print(type(e).__name__, ": ", e)

        return False

    def bookings_for_dates(self):
        """
        Show all bookings for a particular period.
        :return: True/False
        """
        from_date = input("From Date (YYYY-MM-DD): ")
        to_date = input("To Date (YYYY-MM-DD): ")

        try:
            c = self.conn.cursor()
            c.execute("SELECT bookings.*,cabs.cab_no,routes.* FROM bookings  \
                       JOIN routes ON routes.ID=bookings.route_ID \
                       JOIN cabs ON cabs.ID=routes.CAB_ID \
                       WHERE DATE>='{}' AND DATE<='{}'"
                      .format(from_date, to_date))
            result = c.fetchall()
            if len(result) > 0:
                print("\nBOOKING DETAILS\n---------------")
                print("\nCAB NO\tSOURCE\tDESTINATION\tDATE\tTIME\tOCCUPANCY\tSTATUS")
                print("------\t------\t-----------\t----\t----\t---------\t------")

                for row in result:
                    status = 'COMPLETED' if row[6] == 1 else 'CANCELED' if row[6] == 0 else 'UPCOMING'
                    print("{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}"
                          .format(row[7], row[10], row[11], row[3], row[4], row[5], status))
                return True
            else:
                print("\nNo data found.")
        except Exception as e:
            print(type(e).__name__, ": ", e)

        return False
