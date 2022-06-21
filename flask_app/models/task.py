from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User


class Task:
    db = "taskmaster"

    def __init__(self, data):
        self.id = data['id']
        self.job = data['job']
        self.description = data['description']
        self.area = data['area']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    # Adding a task
    @classmethod
    def add_task(cls, data):
        query = "INSERT INTO tasks (job, description, area, user_id) VALUES (%(job)s, %(description)s, %(area)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    # Grap all tasks with users
    @classmethod
    def grab_all_tasks_with_users(cls):
        query = "SELECT * FROM tasks JOIN users ON tasks.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        if len(results) == 0:
            return []  # empty list
        else:
            all_task_instances = []  # hold all tasks
            for this_task_dictionary in results:
                # Create a task
                this_task_instance = cls(this_task_dictionary)
                # Create the User
                this_user_dictionary = {
                    "id": this_task_dictionary["users.id"],
                    "first_name": this_task_dictionary["first_name"],
                    "last_name": this_task_dictionary["last_name"],
                    "email": this_task_dictionary["email"],
                    "password": this_task_dictionary["password"],
                    "created_at": this_task_dictionary["users.created_at"],
                    "updated_at": this_task_dictionary["users.updated_at"],
                }
                this_user_instance = User(this_user_dictionary)
                # link the user to task
                this_task_instance.creator = this_user_instance
                # add this task to the list
                all_task_instances.append(this_task_instance)
            return all_task_instances

    # Grap one tasks with user who added it
    @classmethod
    def grab_one_task_with_creator(cls, data):
        query = "SELECT * FROM tasks JOIN users ON tasks.user_id = users.id WHERE tasks.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) == 0:
            return None
        else:
            # Create a task
            this_task_instance = cls(results[0])
            # create a user
            this_user_dictionary = {
                "id": results[0]["users.id"],
                "first_name": results[0]["first_name"],
                "last_name": results[0]["last_name"],
                "email": results[0]["email"],
                "password": results[0]["password"],
                "created_at": results[0]["users.created_at"],
                "updated_at": results[0]["users.updated_at"],
            }
            this_user_instance = User(this_user_dictionary)
            # link the user to task
            this_task_instance.creator = this_user_instance
            return this_task_instance

    @classmethod
    def edit_task(cls, data):
        query = "UPDATE tasks SET job = %(job)s, description = %(description)s, area = %(area)s WHERE id = %(id)s; "
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete_task(cls, data):
        query = "DELETE FROM tasks WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_task(form_data):
        is_valid = True
        print(form_data)
        if len(form_data["job"]) < 4:
            flash("name of job must be 4 or more characters")
            is_valid = False
        if len(form_data["description"]) < 8:
            flash("description of job must be 8 or more characters")
            is_valid = False
        if len(form_data["area"]) < 3:
            flash("description of area must be 3 or more characters")
            is_valid = False
        return is_valid
