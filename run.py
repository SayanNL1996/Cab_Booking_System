""" Initial file for stating the project."""

from schema import Schema
from admin import Admin
from employee import Employee
import mysql.connector as connector


def sql_connection():
    """
    Setup connection with mysql backend.
    :return: mysql connection object
    """
    # Creating connection with MYSQL
    mydb = connector.connect(
        host='localhost',
        user='root',
        password='Qwerty@123',
        database='cabs'
    )
    print(mydb)

    return mydb


class Run:

    def __init__(self, connection):
        self.conn = connection

    def get_role(self, email, pswd):
        """
        Validate whether the email and password is of a valid user.
        :param email: email given by the user
        :param pswd: password given by the user
        :return: role_id/0
        """
        try:
            c = self.conn.cursor()
            c.execute("SELECT * from users WHERE lower(email)='{}' and password='{}'"
                      .format(email, pswd))
            result = c.fetchone()
            if result is not None:
                return result[2]
            else:
                return 0
        except Exception as e:
            print(type(e), ": ", e)
            return 0

    def login_menu(self):
        """ Display Login options for users to choose.
        :return: True
        """
        print("\n**** LOGIN MENU ****")
        print("Enter '#' for exiting.\n")
        email = input("Email: ").lower()
        if email == '#':
            print("\nExiting...")
            self.conn.close()
        else:
            pswd = input("Password: ")

            role = self.get_role(email, pswd)

            if role == 22:
                Employee(self.conn).employee_menu(email)
            elif role == 11:
                Admin(self.conn).admin_menu(email)
            else:
                print("\nWrong Credentials!  Try again.")

            self.login_menu()

        return True


def main():
    """
    :return: True/False
    """
    try:
        conn = sql_connection()

        if conn is None:
            print("Error while connecting with database")
            print("Retry after sometime!!!")
        else:
            Schema(conn).setup_admin()
            Schema(conn).create_tables()
            Run(conn).login_menu()
            conn.close()
            return True
    except Exception as e:
        print(type(e), ": ", e)

    return False


if __name__ == "__main__":
    main()
