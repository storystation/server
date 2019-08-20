from Model import User


class UserDTO:
    def __init__(self, user: User):
        self.username = user.username
        self.id = str(user.id)
        self.email = user.email
        self.created_at = user.created_at.isoformat()
