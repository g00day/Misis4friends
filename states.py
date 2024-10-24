from aiogram.fsm.state import StatesGroup,State

class RegistrationState(StatesGroup):
    set_name = State()
    set_age = State()
    set_year = State()
    set_institute = State()
    set_description = State()
    set_gender = State()
    set_interested_in = State()
    set_pics = State()



class ProfileMenuState(StatesGroup):
    set_action = State()


class ProfileEditState(StatesGroup):
    edit_profile = State()
    edit_description = State()
    edit_year = State()


class MenuState(StatesGroup):
    set_action = State()

class LikesMailState(StatesGroup):
    set_reaction = State()



class SearchState(StatesGroup):
    set_reaction = State()
    set_personal_message = State()

    
class MakeProfileInactiveState(StatesGroup):
    set_action = State()

class MakeProfileActiveState(StatesGroup):
    make_active = State()