import re
import datetime


class Validation:

    def __init__(self):
        pass

    def input_str_for_create(self, data):
        result = False
        a = ''
        while result is not True:
            a = input(data)
            result = Validation.validate_str(self, a) and Validation.validate_empty_string(self, a)
        return a

    def validate_time(self, data):
        result = False
        a = ''
        while result is not True:
            a = input(data)
            result = Validation.validate_iput_time(self, a)
        return a

    def validate_iput_time(self, input_time):

        timeformat = "%H:%M"
        # caminput1 = input("Enter time: ")
        try:
            validtime = datetime.datetime.strptime(input_time, timeformat)
            if validtime:
                return True

        except ValueError:
            return False

    def validate_emp_str(self, data):
        result = False
        a = ''
        while result is not True:
            a = input(data)
            result = Validation.validate_empty_string(self, a)
        return a

    def validate_empty_string(self, input_str):
        res = bool(re.match('^$', input_str))
        if res:
            return True
        return False

    def validate_str(self, input_str):
        for i in input_str:
            if i.isalpha() is False:
                if i is ' ':
                    continue
                return False
        return True

    def input_int_for_create(self, data):
        result = False
        a = ''
        while result is not True:
            a = input(data)
            result = Validation.validate_int(self, a) and Validation.validate_empty_string(self, a)
        return a

    def validate_int(self, input_str):
        try:
            for i in input_str:
                x = int(i)
                if x in range(10):
                    pass
            return True
        except:
            return False

    def validate_email(self, input_str):

        result = False
        a = ''
        while result is not True:
            a = input(input_str)
            result = Validation.validate_empty_string(self, a) and Validation.validate_email_req(self, a)
        return a

    def validate_email_req(self, input_str):
        try:
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            if re.search(regex, input_str):
                return True
            else:
                return False
        except:
            return False

    def input_not_null_pass(self, data):
        result = False
        a = ''
        while result is not True:
            a = input(data)
            result = Validation.validate_empty_string(self, a) and Validation.validate_pass(self, a)
        return a

    def validate_pass(self, data):

        try:
            reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
            pat = re.compile(reg)
            mat = re.search(pat, data)
            if mat:
                return True
            else:
                return False
        except:
            return False
