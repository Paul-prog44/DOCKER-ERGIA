class UpdateUserDTO:
    def __init__(self, firstname=None, lastname=None, email=None, password=None):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
