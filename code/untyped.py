

class Service:
    def save_in_db(self, user):
        print(user)
        return user['id']

    def report(self, id):
        print(id)
    
    def call_external_service(self):
        return { 'id': 12 }

    def get_latest_user_save_to_db(self):
        user = self.call_external_service()
        user_id = self.save_in_db(user)
        self.report(user_id)
        return user_id

Service().get_latest_user_save_to_db()


def function_untyped(argument):
    return argument

a = function_untyped(4)
a.not_existing_method("str") + 1
