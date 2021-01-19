class User:
    class Info:
        def __init__(self, id, first, last):
            self.id = id
            if(first):
                self.first = first
            if(last):
                self.last = last

    def __init__(self, id, first=None, last=None, token=None):
        self.info = self.Info(id, first, last)
        if(token):
            self.token = token

    def as_dict(self):
        self.info = vars(self.info)
        return vars(self)


class Creds:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def as_dict(self):
        return vars(self)
