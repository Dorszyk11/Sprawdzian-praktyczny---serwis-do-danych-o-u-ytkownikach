users = {}
current_id = 1

class UserService:
    @staticmethod
    def get_all_users():
        return [user for user in users.values()]

    @staticmethod
    def get_user(user_id):
        return users.get(user_id)

    @staticmethod
    def add_user(user_data):
        global current_id
        users[current_id] = {**user_data, "id": current_id}
        current_id += 1
        return users[current_id - 1]

    @staticmethod
    def update_user(user_id, user_data):
        if user_id in users:
            for key, value in user_data.items():
                if key in users[user_id]:
                    users[user_id][key] = value
            return users[user_id]
        return None

    @staticmethod
    def delete_user(user_id):
        return users.pop(user_id, None)
