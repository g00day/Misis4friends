import sqlite3


# General db functions
def check_db_connection(filename):
    # Returns True in case if successfull connected to db
    # or error message
    try:
        conn = sqlite3.connect(filename)
        return True
    except sqlite3.Error as e:
        return e
    finally:
        if conn:
            conn.close()

def get_connection(filename):
    # Returns Connection instance depended on the db
    # by it's filename
    con = sqlite3.connect(filename)
    return con




# DB operation connected to users
# Создание таблицы пользователей, если она не существует
def create_user_table(con):
    sql_create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        year INTEGER,
        institute TEXT,
        description TEXT,
        gender TEXT CHECK(gender IN ('M', 'F')) NOT NULL,
        interested_in TEXT CHECK(interested_in IN ('M', 'F')),
        pic_1 TEXT NOT NULL,
        pic_2 TEXT,
        pic_3 TEXT,
        pic_4 TEXT,
        is_active INTEGER DEFAULT 1,
        is_banned INTEGER DEFAULT 0
    );
    """
    cursor = con.cursor()
    cursor.execute(sql_create_users_table)

con = get_connection("my.db")
create_user_table(con)
    

# Функция для регистрации нового пользователя
# Или изменения существующего
def register_new_or_edit_user(conn, data, on_change=False, user_id=None):
    sql = None
    cursor = conn.cursor()
    if not on_change:
        sql = """
        INSERT INTO users (user_id, name, age, year, institute, description, gender, interested_in, pic_1, pic_2, pic_3, pic_4)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        cursor.execute(sql, (data["user_id"], data["name"], data["age"], data["year"], data["institute"], data["description"], data["gender"], data["interested_in"], data["pic_1"], data["pic_2"], data["pic_3"], data["pic_4"]))
    else:
        sql = """
        UPDATE  users 
        SET
            name=?, 
            age=?,
            year=?,
            institute=?,
            description=?,
            gender=?,
            interested_in=?,
            pic_1=?,
            pic_2=?,
            pic_3=?,
            pic_4=?
        WHERE user_id = ?;
        """
        cursor.execute(sql, (data["name"], data["age"], data["year"], data["institute"], data["description"], data["gender"], data["interested_in"], data["pic_1"], data["pic_2"], data["pic_3"], data["pic_4"], user_id))

    
    conn.commit()
    return cursor.lastrowid


def check_user_existance(con, user_id):
    cursor = con.cursor()
    
    query = "SELECT * FROM users WHERE user_id = ?"
    
    cursor.execute(query, (user_id,))
    
    user_data = cursor.fetchone()
    
    cursor.close()
    
    if user_data:
        return (True, user_data)
    else:
        return (False, None)



def get_all_users(con, gender=None):
    if gender is None:
        gender = "null"
    
    cursor = con.cursor()
    sql = f"SELECT * FROM users WHERE gender = ? AND is_active = 1 AND is_banned = 0;"
    cursor.execute(sql, (gender,))
    users = cursor.fetchall()
    return users


def activate_and_inactivate_user(con, user_id, is_active):
    is_active = int(is_active)
    cursor = con.cursor()
    sql = f"UPDATE users SET is_active = ? WHERE user_id = ?"
    cursor.execute(sql, (is_active, user_id,))
    con.commit()

def ban_user(con, user_id):
    cursor = con.cursor()
    sql = f"UPDATE users SET is_banned = 1 WHERE user_id = ?"
    cursor.execute(sql, (user_id,))
    con.commit()


def edit_user_text_data(con, user_id, data):
    sql = f"""
        UPDATE users
        SET 
            name = ?,
            age = ?,
            year = ?,
            institute = ?,
            description = ?,
            gender = ?,
            interested_in = ?
        WHERE user_id = ?; 
    """
    cursor = con.cursor()
    cursor.execute(sql, (
        data[0],
        data[1],
        data[2],
        data[3],
        data[4],
        data[5],
        data[6],
        user_id,))
    con.commit()


#ban_user(con, 362877694)




""" Complaint """
def create_compaint_table(con):
    sql_create_complaints_table = """
    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_id INTEGER NOT NULL,
        receiver_id INTEGER NOT NULL,
        reason TEXT
    );
    """
    cursor = con.cursor()
    cursor.execute(sql_create_complaints_table)


def create_complaint_instance(conn, data):
    sql = """
    INSERT INTO complaints (sender_id, receiver_id, reason)
    VALUES (?, ?, ?);
    """
    cursor = conn.cursor()
    cursor.execute(sql, (data["sender_id"],  data["receiver_id"], data["reason"]))
    conn.commit()
    return cursor.lastrowid

def get_all_complaints(con):
    sql = "SELECT * FROM complaints"
    cursor = con.cursor()
    cursor.execute(sql)
    complaints = cursor.fetchall()
    return complaints


data = {
    "sender_id":14566,
    "receiver_id":19008,
    "reason":"gay"
}


# Matches
def create_match_table(con):
    sql_create_matches_table = """
    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_id INTEGER NOT NULL,
        receiver_id INTEGER NOT NULL,
        message TEXT NULL
    );
    """
    cursor = con.cursor()
    cursor.execute(sql_create_matches_table)



def create_match_instance(con, data):
    sql = """
        INSERT INTO matches (sender_id, receiver_id, message)
        VALUES (?, ?, ?);
    """
    cursor = con.cursor()
    cursor.execute(sql, (data["sender_id"], data["receiver_id"], data["message"]))
    con.commit()
    return cursor.lastrowid


def delete_match_instance(con, id):
    sql = "DELETE FROM matches WHERE id = ?;"
    cursor = con.cursor()
    cursor.execute(sql, (id,))
    con.commit()

def delete_all_matches_by_user_id(con, id):
    delete_sent = "DELETE FROM matches WHERE sender_id = ?;"
    delete_received = "DELETE FROM matches WHERE receiver_id = ?;"
    cursor = con.cursor()
    cursor.execute(delete_sent, (id,))
    cursor.execute(delete_received, (id,))
    con.commit()

def get_matches_by_receiver_id(con, receiver_id):
    sql = "SELECT * FROM matches WHERE receiver_id = ?"
    cursor = con.cursor()
    cursor.execute(sql, (receiver_id,))
    return cursor.fetchall()

def get_all_matches(con):
    sql = "SELECT * FROM matches"
    cursor = con.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

def needs_prevent_multiple_matches(con, sender_id, receiver_id):
    matches = get_matches_by_receiver_id(con, receiver_id)
    for match in matches:
        if match[1] == sender_id:
            return True
        
    return False



match_data = {
    "sender_id": 1488,
    "receiver_id": 228,
    "message": "Hey bro nice dick!"
}

complaint_data = {
    "sender_id": 1488,
    "receiver_id": 228,
    "reason":"иди нахуй"
}
print(get_all_users(con, "M"))
create_match_table(con)
#create_match_instance(con, match_data)
#delete_match_instance(con, 3)

"""
data = {
    "user_id":"12345",
    "name":"Arseniy",
    'age':"78",
    'year':"I",
    'institute':"dsgsdgsdgsdg",
    'description':"dsgdsgsdgsdg",
    'gender':"F",
    'interested_in':"M",
    'pic_1':"dsfdsfsd",
    'pic_2':"sdffsdfsd",
    'pic_3':"sdfsdfsdf",
    'pic_4':"dsfsdfsdfsdf",
}

"""

#print(ban_user(con, 362877694))
print(get_all_matches(con))
create_compaint_table(con)
#create_complaint_instance(con, complaint_data)
#print(get_all_matches(con))
#print(get_all_complaints(con))
#print(get_all_users(con))
#register_new_user(con, data)
"""
print(check_user_existance(con, "12345"))"""

