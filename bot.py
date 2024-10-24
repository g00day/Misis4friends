import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardRemove, FSInputFile
from aiogram.types.update import Update

from aiogram.filters import Command

from aiogram.fsm.context import FSMContext

import asyncio


from aiogram.fsm.storage.memory import MemoryStorage

import keyboards
import utils
from states import *
from db import *

import os
from dotenv import load_dotenv


load_dotenv()



logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(storage=MemoryStorage())




@dp.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await state.clear() # Making every active state clear
    user = message.from_user
    con = get_connection("db/my.db")

    if check_user_existance(con, user.id)[0]:
        utils.check_user_activity_and_set_active(user.id)
        #m_text = check_user_existance(con, user.id)[0]
        await menu(message, state)
    else:
        m_text = f"Привет, {user.first_name} 👋\n\nДобро пожаловать в наше студенческое сообщество! Здесь ты можешь найти единомышленников, завести новые знакомства и поделиться своими увлечениями.🥰\n\nКак тебя зовут?"

        con.close()

        await bot.send_message(message.from_user.id, m_text, reply_markup=keyboards.get_leave_name_keyboard(user=user))
        await state.set_state(RegistrationState.set_name)


@dp.message(Command("stop"))
async def my_profile(message: types.Message, state: FSMContext):
    await state.clear() # Making every active state clear
    await bot.send_message(message.from_user.id, "Так ты не узнаешь, что кому-то интересен…. Точно хочешь отключить свою анкету?\n\nДа, отключить анкету.\nНет, вернуться назад.", reply_markup=keyboards.get_make_profile_inactive_keyboard(), parse_mode="Markdown")
    await state.set_state(MakeProfileInactiveState.set_action)

@dp.message(Command("myprofile"))
async def my_profile(message: types.Message, state: FSMContext):
    await state.clear() # Making every active state clear
    await profile_menu(message, state)


@dp.message(RegistrationState.set_name)
async def set_name(message: types.Message, state: FSMContext):
    name = message.text
    validated_name = utils.validate_profile_name(name)
    if validated_name[0]:
        await state.update_data(is_edit=False, name=name)
        await bot.send_message(message.from_user.id, f"Будем знакомы, *{validated_name[1]}*😊\n\nCколько тебе лет?", reply_markup=ReplyKeyboardRemove(), parse_mode="markdown")
        await state.set_state(RegistrationState.set_age)
    else:
        await bot.send_message(message.from_user.id, f"{validated_name[1]}", reply_markup=keyboards.get_leave_name_keyboard(user=message.from_user), parse_mode="markdown")


@dp.message(RegistrationState.set_age)
async def set_age(message: types.Message, state: FSMContext):
    validated_age = utils.validate_age(age=message.text)
    if validated_age[0]:
        await state.update_data(age=validated_age[1])
        await bot.send_message(message.from_user.id, "На каком курсе ты учишься?", reply_markup=keyboards.get_choose_year_keyboard())
        await state.set_state(RegistrationState.set_year)
    else:
        await bot.send_message(message.from_user.id, f"*{validated_age[1]}*", parse_mode="Markdown")

@dp.message(RegistrationState.set_year)
async def set_year(message: types.Message, state: FSMContext):
    validated_year = utils.validate_year(message.text)
    if validated_year[0]:
        await state.update_data(year=validated_year[1])
        await bot.send_message(message.from_user.id, "В каком институте ты учишься?", reply_markup=keyboards.get_choose_institute_keyboard())
        await state.set_state(RegistrationState.set_institute)
    else:
         await bot.send_message(message.from_user.id, f"{validated_year[1]}", parse_mode="Markdown")
    

@dp.message(RegistrationState.set_institute)
async def set_institute(message: types.Message, state: FSMContext):
    validated_institute = utils.validate_institute(institute=message.text)
    if validated_institute[0]:
        await state.update_data(institute=validated_institute[1])
        data = await state.get_data()
        name = data.get("name")
        await bot.send_message(message.from_user.id, f"*{name}*😊, расскажи что-нибудь интересное о себе", reply_markup=keyboards.get_skip_description_keyboard(), parse_mode="Markdown")
        await state.set_state(RegistrationState.set_description)
    else:
        await bot.send_message(message.from_user.id, f"*{validated_institute[1]}*", parse_mode="Markdown")

@dp.message(RegistrationState.set_description)
async def set_description(message: types.Message, state: FSMContext):
    description = message.text
    validated_description = utils.validate_description(description)
    if validated_description[0]:
        if description == "Пропустить":
            await state.update_data(description=None)
        else:
            await state.update_data(description=description)
        await bot.send_message(message.from_user.id, f"*Интересно*\n\nТы парень или девушка?", reply_markup=keyboards.get_gender_keyboard(), parse_mode="Markdown")
        await state.set_state(RegistrationState.set_gender)
    else:
        await bot.send_message(message.from_user.id, f"{validated_description[1]}", reply_markup=keyboards.get_skip_description_keyboard(), parse_mode="Markdown")

@dp.message(RegistrationState.set_gender)
async def set_gender(message: types.Message, state: FSMContext):
    gender = message.text
    validated_gender = utils.validate_and_serialize_genders(gender)
    if validated_gender[0]:
        await state.update_data(gender=validated_gender[1])
        await bot.send_message(message.from_user.id, f"Кто тебя интересует?", reply_markup=keyboards.get_interested_in_keyboard(), parse_mode="Markdown")
        await state.set_state(RegistrationState.set_interested_in)
    else:
        await bot.send_message(message.from_user.id, f"{validated_gender[1]}", reply_markup=keyboards.get_gender_keyboard(), parse_mode="Markdown")

@dp.message(RegistrationState.set_interested_in)
async def set_interested_in(message: types.Message, state: FSMContext):
    interested_in = message.text
    validated_interested_in = utils.validate_and_serialize_genders(interested_in)
    if validated_interested_in[0]:
        await state.update_data(interested_in=validated_interested_in[1])
        await bot.send_message(message.from_user.id, f"*Последнее*, отправь свои фотографии(до 4, включительно), эти фото будут приложены к твоей анкете", reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown")
        await state.set_state(RegistrationState.set_pics)
    else:
        await bot.send_message(message.from_user.id, validated_interested_in[1], reply_markup=keyboards.get_interested_in_keyboard(), parse_mode="Markdown")


@dp.message(RegistrationState.set_pics)
async def set_pics(message: types.Message, state: FSMContext):
    await state.update_data(pic_1=message.text)

    photo = message.photo[-1]

    file_id = photo.file_id
    
    # Скачиваем фото
    file = await bot.get_file(file_id)
    filename = f"media/photo_1_{message.from_user.id}.jpg"
    await bot.download(file, filename)

    data = await state.get_data()
    data.update({"user_id":message.from_user.id, "pic_1":filename, "pic_2": None, "pic_3":None, "pic_4":None})
    is_edit = data["is_edit"]
    data.pop("is_edit") # Deleting is_edit flag which reports if the profile is gonna be
    #edited or not

    con = get_connection("db/my.db")
    register_new_or_edit_user(con, data, on_change=is_edit, user_id=message.from_user.id)
    

    await menu(message, state)
    #await state.clear()


async def menu(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    profile_data = utils.display_profile(user_id)
    if profile_data[0]:

        con = get_connection("db/my.db")
        matches = get_matches_by_receiver_id(con, receiver_id=user_id)

        m_text = profile_data[1]
        photo = profile_data[2]
        await message.answer_photo(photo=photo, caption=m_text, parse_mode="Markdown", reply_markup=ReplyKeyboardRemove())
        await bot.send_message(message.from_user.id, f"*Подождем пока кто-то увидит твою анкету*\n\n1. Смотреть анкеты\n2. Моя анкета\n3. Посмотреть кто тебя оценил({len(matches)})💙\n4. Больше не хочу никого искать", reply_markup=keyboards.get_menu_keyboard(), parse_mode="Markdown")
        await state.set_state(MenuState.set_action)
    else:
        await bot.send_message(message.from_user.id, profile_data[1], reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown")



async def profile_menu(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    profile_data = utils.display_profile(user_id)
    utils.check_user_activity_and_set_active(user_id)
    if profile_data[0]:
        m_text = profile_data[1]
        photo = profile_data[2]
        await bot.send_message(message.from_user.id, "*Вот так сейчас выглядит твоя анкета:*",  parse_mode="Markdown")
        await message.answer_photo(photo=photo, caption=m_text, parse_mode="Markdown", reply_markup=ReplyKeyboardRemove())
        await bot.send_message(message.from_user.id, '1. Смотреть анкеты.\n2. Заполнить анкету заново.\n3. Изменить фото.\n4. Изменить текст анкеты.\n5. Изменить курс', reply_markup=keyboards.get_profile_menu_keyboard())
        await state.set_state(ProfileMenuState.set_action)
    else:
        await bot.send_message(message.from_user.id, profile_data[1], ReplyKeyboardRemove(), parse_mode="Markdown")




@dp.message(ProfileMenuState.set_action)
async def set_profile_menu_action(message: types.Message, state: FSMContext):
    action = message.text
    if action == "1":
        await search(message, state)
    elif action == "2":
        await bot.send_message(message.from_user.id, "*Отлично*\n\nКак тебя зовут?", reply_markup=keyboards.get_leave_name_keyboard(user=message.from_user), parse_mode="Markdown")
        await state.set_state(ProfileEditState.edit_profile)
    elif action == "3":
        await bot.send_message(message.from_user.id, "Unavailable")
    elif action == "4":
        await bot.send_message(message.from_user.id, "*Отлично*\n\nВведи новый текст для твоей анкеты", reply_markup=keyboards.get_edit_description_keyboard(), parse_mode="Markdown")
        await state.set_state(ProfileEditState.edit_description)
    elif action == "5":
        await bot.send_message(message.from_user.id, "*Отлично*\n\n На каком курсе ты сейчас?", reply_markup=keyboards.get_choose_year_keyboard(), parse_mode="Markdown")
        await state.set_state(ProfileEditState.edit_year)
    else:
        await bot.send_message(message.from_user.id, "Такой опции нет ❌")


@dp.message(ProfileEditState.edit_profile)
async def edit_profile(message: types.Message, state: FSMContext):
    name = message.text
    validated_name = utils.validate_profile_name(name)
    if validated_name[0]:
        await state.update_data(is_edit=True, name=name)
        await bot.send_message(message.from_user.id, f"Будем знакомы, *{validated_name[1]}*😊\n\nCколько тебе лет?", reply_markup=ReplyKeyboardRemove(), parse_mode="markdown")
        await state.set_state(RegistrationState.set_age)
    else:
        await bot.send_message(message.from_user.id, f"{validated_name[1]}", reply_markup=keyboards.get_leave_name_keyboard(user=message.from_user), parse_mode="markdown")



@dp.message(ProfileEditState.edit_description)
async def edit_description(message: types.Message, state: FSMContext):
    description = message.text
    user_id = message.from_user.id
    validated_description = utils.validate_description(description)
    if validated_description[0]:
        
        con = get_connection("db/my.db")
        u_data = list(check_user_existance(con, user_id)[1])[1:8]

        if description == "Очистить":
            description=None
        if description == "Оставить текущий":
            description = u_data[4]

        u_data[4] = description
        edit_user_text_data(con, user_id, u_data)

        con.close()
        
        await profile_menu(message, state)
    else:
        await bot.send_message(message.from_user.id, f"{validated_description[1]}", reply_markup=keyboards.get_edit_description_keyboard(), parse_mode="Markdown")



@dp.message(ProfileEditState.edit_year)
async def edit_year(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    year = message.text
    validated_year = utils.validate_year(year)
    if validated_year[0]:

        con = get_connection("db/my.db")

        u_data = list(check_user_existance(con, user_id)[1])[1:8]
        u_data[2] = validated_year[1]

        edit_user_text_data(con, user_id, u_data)

        con.close()

        await profile_menu(message, state)

    else:
         
        await bot.send_message(message.from_user.id, f"{validated_year[1]}", parse_mode="Markdown")
    



@dp.message(MenuState.set_action)
async def set_menu_action(message: types.Message, state: FSMContext):
    action = message.text
    if action == "1🌪️":
        await search(message, state)
    elif action == "2":
        await profile_menu(message, state)
    elif action == "3":
        await see_likes_mail(message, state)
    elif action == "4":
        await bot.send_message(message.from_user.id, "Так ты не узнаешь, что кому-то интересен…. Точно хочешь отключить свою анкету?\n\nДа, отключить анкету.\nНет, вернуться назад.", reply_markup=keyboards.get_make_profile_inactive_keyboard(), parse_mode="Markdown")
        await state.set_state(MakeProfileInactiveState.set_action)
    else:
        await bot.send_message(message.from_user.id, "Такой опции нет ❌", parse_mode="Markdown")


@dp.message(MakeProfileInactiveState.set_action)
async def set_make_profile_inactive_action(message, state: FSMContext):
    action = message.text
    validated_action = utils.validate_make_profile_inactive_action(action)
    if validated_action[0]:
        action = validated_action[1]
        if action == "Да-✅":
            con = get_connection("db/my.db")
            activate_and_inactivate_user(con, message.from_user.id, is_active=False)
            delete_all_matches_by_user_id(con, message.from_user.id)
            await bot.send_message(message.from_user.id, "Надеюсь ты нашел кого-то благодаря мне! Рад был с тобой пообщаться, будет скучно – пиши, обязательно найдем тебе кого-нибудь\n\nНапиши мне что-нибудь, чтобы смотреть анкеты.")
            con.close()
            await state.set_state(MakeProfileActiveState.make_active)
        elif action == "Нет-⛔️":
            await menu(message, state)
    else:
        await bot.send_message(message.from_user.id, action[1])


@dp.message(MakeProfileActiveState.make_active)
async def set_make_profile_active_action(message, state: FSMContext):
    con = get_connection("db/my.db")
    activate_and_inactivate_user(con, message.from_user.id, is_active=True)
    con.close()
    await menu(message, state)


async def see_likes_mail(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    con = get_connection("db/my.db")

    likes = get_matches_by_receiver_id(con, user_id)
    if likes != []:

        like = likes[0]
        personal_message = like[3]

        sender_id = like[1]
        u_data = check_user_existance(con, sender_id)[1] # In this case u_data is the sender's data
        photo = FSInputFile(f'media/photo_1_{u_data[0]}.jpg')


        description = u_data[5]
        if description is None:
            description = ""

        m_text = f'*{u_data[1]}, {u_data[2]}{utils.transorm_gender_to_emoji(u_data[6])}*\n{u_data[4]}, {u_data[3]} 🏫\n\n_{description}_\n\n'

        
        # Sending sender's data
        await message.answer_photo(photo=photo, caption=m_text, parse_mode="Markdown", reply_markup=keyboards.get_likes_mail_keyboard())

        #Sending personal message if it's provided
        if personal_message is not None:
            await bot.send_message(message.from_user.id, f"*Сообщение от {u_data[1]}📩*\n\n_{personal_message}_", parse_mode="Markdown")

        await state.set_state(LikesMailState.set_reaction)
        await state.update_data(match_id=like[0], sender_id=sender_id)

    else:

        await bot.send_message(message.from_user.id, "*Пока тут ничего нет...*", reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown")

    con.close()

@dp.message(LikesMailState.set_reaction)
async def set_reaction_in_likes_mail(message: types.Message, state: FSMContext):
    rate = message.text
    con = get_connection("db/my.db")
    data = await state.get_data()

    match_id = data["match_id"]
    sender_id = data["sender_id"]
    receiver_id = message.chat.id

    s_data = check_user_existance(con, sender_id)[1] # s_data means the data of sender
    r_data = check_user_existance(con, receiver_id)[1] # r_data means the data of receiver

    if rate == "💙":

        # Here we changing sender's and receiver's descriptions
        # just in case they're None
        s_description = s_data[5]
        if s_description is None:
            s_description = ""

        r_description = r_data[5]
        if r_description is None:
            r_description = ""

        # Firstly send the reaction to sender
        to_sender_photo = FSInputFile(f'media/photo_1_{r_data[0]}.jpg')
        to_sender_text = f'*Есть взаимная оценка💙*\n[{r_data[1]}](tg://user?id={r_data[0]})\n\n*{r_data[1]}, {r_data[2]}{utils.transorm_gender_to_emoji(r_data[6])}*\n{r_data[4]}, {r_data[3]} 🏫\n\n_{r_description}_\n\n'
        await bot.send_photo(sender_id, photo=to_sender_photo)
        await bot.send_message(sender_id, to_sender_text, parse_mode="Markdown")

        # Then we send the reaction to receiver
        to_receiver_photo = FSInputFile(f'media/photo_1_{s_data[0]}.jpg')
        to_receiver_text = f'*Приятно пообщаться!*\n[{s_data[1]}](tg://user?id={s_data[0]})\n\n"*{s_data[1]}, {s_data[2]}{utils.transorm_gender_to_emoji(s_data[6])}*\n{s_data[4]}, {s_data[3]} 🏫\n\n_{s_description}_\n\n'
        await message.answer_photo(photo=to_receiver_photo, caption=to_receiver_text, parse_mode="Markdown")

        delete_match_instance(con, match_id)
        await see_likes_mail(message, state)

    elif rate == "👎":
        delete_match_instance(con, match_id)
        await see_likes_mail(message, state)
    else:
        await bot.send_message(message.from_user.id, "Такой опции нет ❌", parse_mode="Markdown")

    con.close()

async def search(message: types.Message, state: FSMContext):

    user_id = message.from_user.id
    random_user = utils.get_random_user_in_search(user_id)

    if random_user[0]:
        u_data = random_user[1]
        m_text = f'*{u_data[1]}, {u_data[2]}{utils.transorm_gender_to_emoji(u_data[6])}*\n{u_data[4]}, {u_data[3]} 🏫\n\n_{u_data[5]}_\n\n'
        photo = FSInputFile(f'media/photo_1_{u_data[0]}.jpg')

        await message.answer_photo(photo=photo, caption=m_text, parse_mode="Markdown", reply_markup=keyboards.get_search_keyboard())
        await state.set_state(SearchState.set_reaction)
        await state.update_data(user_id=u_data[0])
    else:
        await bot.send_message(message.from_user.id, "Пользовательский список этой категории пуст ❌", parse_mode="Markdown")



@dp.message(SearchState.set_reaction)
async def rate_user(message: types.Message, state: FSMContext):
    rate = message.text
    con = get_connection("db/my.db")
    data = await state.get_data()
    user_id = data["user_id"]
    if rate == "💙":
        data = {
            "sender_id": message.from_user.id,
            "receiver_id": user_id,
            "message": None,
        }
        if not(needs_prevent_multiple_matches(con, sender_id=message.from_user.id, receiver_id=user_id)):
            create_match_instance(con, data)
            # sending message to the receiver
            await bot.send_message(user_id, "*Ты понравился одному человеку💙*", parse_mode="Markdown")
        con.close()
        await bot.send_message(message.from_user.id, "Отправили рекцию.\n*Ждём ответа...*", parse_mode="Markdown")
        await search(message, state)
    elif rate == "👎":
        await search(message, state)
    elif rate == "💤":
        await state.clear()
        await menu(message, state)
    elif rate == "📩":
        await bot.send_message(message.from_user.id, "Напишите сообщение этому человеку📩", parse_mode="Markdown")
        await state.set_state(SearchState.set_personal_message)
    else:
        await bot.send_message(message.from_user.id, "Такой опции нет ❌", parse_mode="Markdown")
        await menu(message, state)



@dp.message(SearchState.set_personal_message)
async def send_personal_message(message: types.Message, state: FSMContext):

    data = await state.get_data()
    user_id = data["user_id"]
    data = {"sender_id": message.from_user.id,
            "receiver_id": user_id}
    
    con = get_connection("db/my.db")

    personal_message = message.text
    personal_message = utils.validate_personal_message(personal_message)

    if personal_message[0]:

        personal_message = personal_message[1]

        # checking if the message is not cancelling
        if personal_message != "Отмена ❌":
            data["message"] = personal_message # appending message in case it's given

        create_match_instance(con, data)

        await bot.send_message(message.from_user.id, "Отправили рекцию.\n*Ждём ответа...*", parse_mode="Markdown")
        # sending message to the receiver
        await bot.send_message(user_id, "*Ты понравился одному человеку💙*", parse_mode="Markdown")
        await search(message, state)

    else:

        await bot.send_message(message.from_user.id, f"*{personal_message[1]}*", parse_mode="Markdown")


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())