import db
import random

from aiogram.types import FSInputFile



def validate_profile_name(name):
    if len(name) < 20:
        return True, name
    else:
        return False, "Имя слишком длинное❌"

def validate_and_serialize_genders(gender):
    gender_data = {"Парень 🧑":"M", "Парни 🧑": "M",
                   "Девушка 👩": "F", "Девушки 👩":"F",
                   "Без разницы 🤷‍♂️":None}
    if gender in gender_data.keys():
        return True, gender_data[gender]
    return False, "Пол неправильный❌"

def transorm_gender_to_emoji(gender):
    gender_data = {"M":"🧑",  "F":"👩"}
    return gender_data[gender]


def validate_institute(institute):
    institutes = ["ИБО", "ИНМиН", "Эко.Тех", "МГИ", "ЭУПП"]
    if institute in institutes:
        return True, institute
    else:
        return False, "Неверный институт ❌"
    
def validate_year(year):
    years = ["I", "II", "III", "IV", "V(Специалитет)", "Магистратура"]
    if year in years:
        return True, year
    else:
        return False, "Неверно введен курс ❌"
    

def validate_age(age):
    if age.isdigit():
        if 15 < int(age) and int(age) < 100:
            return True, age
        else:
            return False, "Введенный возраст не подходит ❌"
    else:
        return False, "Неправильно введен возраст ❌"
    

def validate_description(description):
    correct_words_amount = 350
    max_symbols = 4000
    if len(description.split()) < correct_words_amount and len(description) < max_symbols:
        return True, description
    else:
        return False, f"Описание должно быть меньше❌"


def validate_make_profile_inactive_action(action):  
    if action not in ["Да-✅", "Нет-⛔️"]:
        return False, "Неправильно введен ответ ❌"
    else:
        return True, action
    

def validate_personal_message(personal_message):
    correct_words_amount = 35
    max_symbols = 400
    if len(personal_message.split()) < correct_words_amount and len(personal_message) < max_symbols:
        return True, personal_message
    else:
        return False, f"Сообщение должно быть меньше ❌"


# Search mechanics

def get_random_user_in_search(user_id):
    """  Returns  -> (bool, list)
        the first bool shows if users is empty
        the second list returns the user's list
        if it's not empty  
        ---------------------------------------
        Also it checks if the user which id  
        was given as an argument is not banned  """
    con = db.get_connection("my.db")
    interested_in = db.check_user_existance(con, user_id)[1][7]
    is_banned = db.check_user_existance(con, user_id)[1][13]
    users = db.get_all_users(con, interested_in)
    if users != [] and bool(is_banned) != True:
        random_user = random.choice(users)
        return True, random_user
    else:
        return False, []



# Profile
def display_profile(user_id):
    """ Returns the tuple of:  
        bool: returns if the user is registered  
        str: message text  
        FSInputFile: photo  
    """

    con = db.get_connection("my.db")
    user = db.check_user_existance(con, user_id) # stores the data about the user(bool - existance, tuple - data)
    con.close()
    
    if user[0]:
        
        u_data = user[1]

        # Setting profile description to empty string in case if it's None
        description = u_data[5]
        if description is None:
            description = ""

        m_text = f'Твоя анкета 👤\n\n*{u_data[1]}, {u_data[2]}{transorm_gender_to_emoji(u_data[6])}*\n{u_data[4]}, {u_data[3]} 🏫\n\n_{description}_\n\n'
        photo = FSInputFile(f'media/photo_1_{user_id}.jpg')

        return True, m_text, photo

    else:
        return False, "*Вы не зарегистрированы ❌*\nВы можете зарегистрироваться используя /start", None
    


def check_user_activity_and_set_active(user_id):
    """ This function checks if the user is not
     active and sets it to active """
    con = db.get_connection("my.db")
    user = db.check_user_existance(con, user_id)
    u_data = user[1]

    if not(bool(u_data[12])):
        db.activate_and_inactivate_user(con, user_id=user_id, is_active=True)

    con.close()