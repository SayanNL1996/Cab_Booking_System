""" File for all operations performed under Admin."""

import re


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
        print("\nAdd Employee\n------------")
        fname = input("First Name: ")
        lname = input("Last Name: ")
        email = input("Email: ").lower()
        phone = input("Phone no.: ")

        if re.search(self.regex, email):
            if self.add_employee_action(fname, lname, email, phone):
                return True
        else:
            print("\nInvalid email.")
        return False

    def add_employee_action(self, fname, lname, email, phone):
        """
        Add employee with the given data.
        :param fname: first name of member
        :param lname: last name of member
        :param email: email of member
        :param phone: phone no. of member
        :return: True/False
        """
        try:
            c = self.conn.cursor()
            c.execute("SELECT count(*) from employees WHERE lower(email)='{}'".format(email))
            if c.fetchone()[0] < 1:
                if re.search("^[a-zA-Z]+$", fname):
                    if re.search("^[a-zA-Z]+$", lname):
                        if len(phone) == 10:
                            c.execute("INSERT INTO employees (FNAME,LNAME,EMAIL,PHONE) VALUES('{}','{}','{}','{}')"
                                      .format(fname, lname, email, phone))
                            c.execute("INSERT INTO users VALUES('{}','{}',{})"
                                      .format(email, fname.lower() + '@' + str(123), 22))
                            self.conn.commit()
                            print("\n'{}' added as Employee".format(fname))
                            return True
                        else:
                            print("\nInvalid Phone No.")
                    else:
                        print("\n Only letters are allowed in last name.")
                else:
                    print("\n Only letters are allowed in first name.")
            else:
                print("\n'{}' already exists.\nTry again with new Email".format(email))
        except Exception as e:
            print(type(e).__name__, ": ", e)
        return False

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

                if self.update_member_validation(fname, lname, email, new_email, phone, member[0]):
                    return True

        except Exception as e:
            print(type(e).__name__, ": ", e)

        return False

    def update_member_validation(self, fname, lname, old_email, email, phone, member_id):
        """
        Check whether the email already exists in database or not.
        :param fname: first name of member
        :param lname: last name of member
        :param old_email: previous email stored in database
        :param email: email of member
        :param phone: phone no. of member
        :param member_id: id of member
        :return: True/False
        """
        try:
            c = self.conn.cursor()
            if re.search(self.regex, email):
                c.execute("SELECT count(*) from employees WHERE lower(email)='{}'".format(email))
                if c.fetchone()[0] < 1:
                    return self.update_member_action(fname, lname, old_email, email, phone, member_id)
                else:
                    c.execute("SELECT count(*) from employees WHERE lower(email)='{}' and ID={}"
                              .format(email, member_id))
                    if c.fetchone()[0] > 0:
                        return self.update_member_action(fname, lname, old_email, email, phone, member_id)
                    else:
                        print("\n'{}' already exists.\nTry again with new Email".format(email))
            else:
                print("\nInvalid email.")
        except Exception as e:
            print("\n", type(e), ": ", e)

        return False

    def update_member_action(self, fname, lname, old_email, email, phone, member_id):
        """
        Update the member details w.r.t. member id
        :param fname: first name of member
        :param lname: last name of member
        :param old_email: previous email stored in database
        :param email: email of member
        :param phone: phone no. of member
        :param member_id: id of member
        :return: True/False
        """
        if re.search("^[a-zA-Z]+$", fname):
            if re.search("^[a-zA-Z]+$", lname):
                if len(phone) == 10:
                    try:
                        c = self.conn.cursor()
                        c.execute("DELETE from users WHERE EMAIL='{}'".format(old_email))
                        c.execute("UPDATE employees SET FNAME='{}',LNAME='{}',EMAIL='{}',PHONE='{}' WHERE ID={}"
                                  .format(fname, lname, email, phone, member_id))
                        c.execute("INSERT INTO users VALUES('{}','{}',{})"
                                  .format(email, fname.lower() + '@' + str(123), 22))
                        self.conn.commit()
                        print("\nRecord Updated.")
                        return True
                    except Exception as e:
                        print("\n", type(e), ": ", e)
                else:
                    print("\nInvalid Phone No.")
            else:
                print("\n Only letters are allowed in last name.")
        else:
            print("\n Only letters are allowed in first name.")

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
                if ch == 'y' or ch == 'Y':
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
        cab_no = input("Cab no.: ").upper()
        rider_name = input("Rider Name: ")
        rider_no = input("Rider No.: ")
        capacity = int(input("Capacity: "))

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
                if ch == 'y' or ch == 'Y':
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
