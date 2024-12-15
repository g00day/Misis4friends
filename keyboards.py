from aiogram import types


# Inline keyboards
def get_admin_keyboard():
    inline_admin_list = [
        [types.InlineKeyboardButton(text="Админ панель", callback_data='admin')]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=inline_admin_list)



def get_menu_keyboard():
    menu_fields = [
        [
            types.KeyboardButton(text="1🌪️"),
            types.KeyboardButton(text="2"),
            types.KeyboardButton(text="3"),
            types.KeyboardButton(text="4")
        ],
    ]

    menu_keyboard = types.ReplyKeyboardMarkup(
        keyboard=menu_fields,
        resize_keyboard=True,
    )


    return menu_keyboard


def get_likes_mail_keyboard():
    # lm means likes mail
    lm_fields = [
        [
            types.KeyboardButton(text="💙"),
            types.KeyboardButton(text="👎"),
        ]
    ]

    lm_keyboard = types.ReplyKeyboardMarkup(
        keyboard=lm_fields,
        resize_keyboard=True,
    )

    return lm_keyboard


def get_profile_menu_keyboard():
    # 'pm' means profile menu
    pm_fields = [
        [
            types.KeyboardButton(text="1"),
            types.KeyboardButton(text="2"),
            types.KeyboardButton(text="3"),
            types.KeyboardButton(text="4"),
            types.KeyboardButton(text="5"),
        ],
    ]

    pm_keyboard = types.ReplyKeyboardMarkup(
        keyboard=pm_fields,
        resize_keyboard=True,
    )

    return pm_keyboard


def get_edit_description_keyboard():
    # sd means skip description
    sd_fields = [
        [
            types.KeyboardButton(text="Очистить"),
            types.KeyboardButton(text="Оставить текущий"),
        ],
    ]

    sd_keyboard = types.ReplyKeyboardMarkup(
        keyboard=sd_fields,
        resize_keyboard=True,
        input_field_placeholder="Represent yourself"
    )


    return sd_keyboard


def get_make_profile_inactive_keyboard():
    # mpi means 'make_profile_inactive'
    mpi_fields = [
        [
            types.KeyboardButton(text="Да-✅"),
            types.KeyboardButton(text="Нет-⛔️")
        ],
    ]

    mpi_keyboard = types.ReplyKeyboardMarkup(
        keyboard=mpi_fields,
        resize_keyboard=True,
    )


    return mpi_keyboard


def get_leave_name_keyboard(user):
    # ln means 'leave_name'
    ln_fields = [
        [
            types.KeyboardButton(text=user.first_name),
        ],
    ]

    ln_keyboard = types.ReplyKeyboardMarkup(
        keyboard=ln_fields,
        resize_keyboard=True,
        input_field_placeholder="What's your name?"
    )


    return ln_keyboard



def get_choose_year_keyboard():
    # cy means choose year
    cy_fields = [
        [
            types.KeyboardButton(text="I"),
        ],
        [
            types.KeyboardButton(text="II"),
        ],
        [
            types.KeyboardButton(text="III"),
        ],
        [
            types.KeyboardButton(text="IV"),
        ],
        [
            types.KeyboardButton(text="V(Специалитет)"),
        ],
        [
            types.KeyboardButton(text="Магистратура"),
        ]
    ]

    cy_keyboard = types.ReplyKeyboardMarkup(
        keyboard=cy_fields,
        resize_keyboard=True,
        input_field_placeholder="What's your year?"
    )


    return cy_keyboard


def get_choose_institute_keyboard():
    # ci means choose institute
    ci_fields = [
        [
            types.KeyboardButton(text="ИБО"),
        ],
        [
            types.KeyboardButton(text="ИНМиН"),
        ],
        [
            types.KeyboardButton(text="Эко.Тех"),
        ],
        [
            types.KeyboardButton(text="МГИ"),
        ],
        [
            types.KeyboardButton(text="ЭУПП"),
        ],
    ]

    ci_keyboard = types.ReplyKeyboardMarkup(
        keyboard=ci_fields,
        resize_keyboard=True,
        input_field_placeholder="What's your institute?"
    )


    return ci_keyboard


def get_skip_description_keyboard():
    # sd means skip description
    sd_fields = [
        [
            types.KeyboardButton(text="Пропустить"),
        ],
    ]

    sd_keyboard = types.ReplyKeyboardMarkup(
        keyboard=sd_fields,
        resize_keyboard=True,
        input_field_placeholder="Represent yourself"
    )


    return sd_keyboard


def get_gender_keyboard():
    # g means gender
    g_fields = [
        [
            types.KeyboardButton(text="Парень 🧑"),
        ],
        [
            types.KeyboardButton(text="Девушка 👩"),
        ],
    ]

    g_keyboard = types.ReplyKeyboardMarkup(
        keyboard=g_fields,
        resize_keyboard=True,
        input_field_placeholder="What's your gender?"
    )


    return g_keyboard



def get_interested_in_keyboard():
    # ii means 'interested in'
    ii_fields = [
        [
            types.KeyboardButton(text="Парни 🧑"),
        ],
        [
            types.KeyboardButton(text="Девушки 👩"),
        ],
        [
            types.KeyboardButton(text="Без разницы 🤷‍♂️"),
        ],
    ]

    ii_keyboard = types.ReplyKeyboardMarkup(
        keyboard=ii_fields,
        resize_keyboard=True,
        input_field_placeholder="Who are you interested in?"
    )


    return ii_keyboard


def get_search_keyboard():
    search_fields = [
        [
            types.KeyboardButton(text="💙"),
            types.KeyboardButton(text="📩"),
            types.KeyboardButton(text="👎"),
            types.KeyboardButton(text="⚠️"),
            types.KeyboardButton(text="💤"),
        ]
    ]

    search_keyboard = types.ReplyKeyboardMarkup(
        keyboard=search_fields,
        resize_keyboard=True,
    )

    return search_keyboard


def get_update_profile_picture_keyboard():
    # 'uup' means update profile picture
    upp_fields = [
        [types.KeyboardButton(text="Пропустить")]
    ]

    upp_keyboard = types.ReplyKeyboardMarkup(
        keyboard=upp_fields,
        resize_keyboard=True,
    )

    return upp_keyboard


def get_complaint_keyboard():
    complaint_fields = [
        [
            types.KeyboardButton(text="1"),
            types.KeyboardButton(text="2"),
            types.KeyboardButton(text="3"),
        ],
        [
            types.KeyboardButton(text="Отмена ❌"),
        ]
    ]
    
    pm_keyboard = types.ReplyKeyboardMarkup(
        keyboard=complaint_fields,
        resize_keyboard=True,
        input_field_placeholder="Причина жалобы"
    )
    
    return pm_keyboard


def personal_message_keyboard():
    pm_fields = [
        [
            types.KeyboardButton(text="Отмена ❌"),
        ],
    ]

    pm_keyboard = types.ReplyKeyboardMarkup(
        keyboard=pm_fields,
        resize_keyboard=True,
        input_field_placeholder="Напишите сообщения для этого пользователя"
    )

    return pm_keyboard


def get_admin_action_keyboard():
    ac_fields = [
        [
            types.KeyboardButton(text="Смотреть жалобы ⚠"),
            types.KeyboardButton(text="Количество пользователей 👥"),
            types.KeyboardButton(text="Выйти 🚪")
        ],
    ]

    ac_keyboard = types.ReplyKeyboardMarkup(
        keyboard=ac_fields,
        resize_keyboard=True,
        input_field_placeholder="Админ панель"
    )

    return ac_keyboard


def get_complaint_processing_keyboard():
    cp_fields = [
        [
            types.KeyboardButton(text="Бан"),
            types.KeyboardButton(text="Оправдать"),
            types.KeyboardButton(text="💤")
        ],
    ]

    cp_keyboard = types.ReplyKeyboardMarkup(
        keyboard=cp_fields,
        resize_keyboard=True,
        input_field_placeholder="Админ панель"
    )

    return cp_keyboard