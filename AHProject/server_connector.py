import mysql.connector
from user import User

class DatabaseConnector:

    db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="projectUsers"
    )

    cursor = db.cursor()
    table = "user"

    @staticmethod
    def create_user(username, password):
        insert_query = f"INSERT INTO {DatabaseConnector.table} (username, score, password) VALUES (%s, %s, %s)"
        values = (username, 0, password)

        DatabaseConnector.cursor.execute(insert_query, values)
        DatabaseConnector.db.commit()

    @staticmethod
    def update_user(userID, new_username, new_password):
        update_query = f"UPDATE {DatabaseConnector.table} SET username=(%s), password=(%s) WHERE userID = {userID}"
        values = (new_username, new_password)

        DatabaseConnector.cursor.execute(update_query, values)
        DatabaseConnector.db.commit()

    @staticmethod
    def update_password(username, new_password):
        update_query = f"UPDATE {DatabaseConnector.table} SET password=(%s) WHERE username = (%s)"
        values = (new_password, username)

        DatabaseConnector.cursor.execute(update_query, values)
        DatabaseConnector.db.commit()

    @staticmethod
    def get_score(userID):
        select_query = f"SELECT score FROM user WHERE userID = {userID}"

        DatabaseConnector.cursor.execute(select_query)

        score = int(DatabaseConnector.cursor.fetchall()[0][0])
        return score

    @staticmethod
    def update_score(userID, new_score):
        update_query = f"UPDATE {DatabaseConnector.table} SET score={new_score} WHERE userID = {userID}"

        DatabaseConnector.cursor.execute(update_query)
        DatabaseConnector.db.commit()

    @staticmethod
    def select_all():
        select_query = f"SELECT * FROM {DatabaseConnector.table}"

        DatabaseConnector.cursor.execute(select_query)
        return [User(user[0], user[1], user[2], user[3]) for user in DatabaseConnector.cursor.fetchall()]

    @staticmethod
    def get_username(userID):
        select_query = f"SELECT username FROM {DatabaseConnector.table} WHERE userID = (%s)"
        value = [userID]

        DatabaseConnector.cursor.execute(select_query, value)
        return DatabaseConnector.cursor.fetchone()[0]