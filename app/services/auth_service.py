from repository import postgresql_repo

def authenticate(username, password_input):
    user = postgresql_repo.get_user_by_username(username)
    if user:
        # user = (id, username, password)
        db_password = user[2]
        # UNSICHER: Klartext Vergleich wie gewünscht
        if db_password == password_input:
            return user[0] # Gibt ID zurück
    return None