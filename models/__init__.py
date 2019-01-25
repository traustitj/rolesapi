class User:
    name = ""
    username = ""
    user_id = ""
    created = ""
    roles = []

class Role:
    role_id = 0
    name = ""
    permanent = False
    users = []

    def to_dict(self):
        nusers = []
        for user in self.users:
            nusers.append(user.__dict__)
        self.users = nusers

        return self.__dict__
