class UpdatePasswordRequestDTO:
    def __init__(self, old_password: str, new_password: str):
        self.old_password = old_password
        self.new_password = new_password
