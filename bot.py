import logging

from dataclasses import dataclass
import json
from aiogram import Bot, Dispatcher, executor, types


import inline_keyboard
import messages
import config
import re
import pickle

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_API_TOKEN)
dp = Dispatcher(bot)
flag = False
flag2 = False









try:
    with open('data.pickle', 'rb') as f:
        dict_of_clothes = pickle.load(f)
except:
    dict_of_clothes = {}

try:
    with open('data1.pickle', 'rb') as g:
        dict_of_coordinates = pickle.load(g)
except:
    dict_of_coordinates = {}





@dp.message_handler(commands=['start', 'weather'])
async def show_weather(message: types.Message):
    await message.answer(text=messages.weather(message.chat.username),
                         reply_markup=inline_keyboard.WEATHER)

@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    #global dict_of_coordinates
    lat = message.location.latitude
    lon = message.location.longitude
    dict_of_coordinates[message.chat.username] = [lat, lon]
    with open('data1.pickle', 'wb') as g:
        pickle.dump(dict_of_coordinates, g)



@dp.message_handler(commands='help')
async def show_help_message(message: types.Message):
    await message.answer(text=f'This bot can get the current weather from your IP address.',
                         reply_markup=inline_keyboard.HELP)


@dp.message_handler(commands='wind')
async def show_wind(message: types.Message):
    await message.answer(text=messages.wind(message.chat.username), reply_markup=inline_keyboard.WIND)


@dp.message_handler(commands='sun_time')
async def show_sun_time(message: types.Message):
    await message.answer(text=messages.sun_time(message.chat.username), reply_markup=inline_keyboard.SUN_TIME)





@dp.callback_query_handler(text='weather')
async def process_callback_weather(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        text=messages.weather(callback_query.from_user.username),
        reply_markup=inline_keyboard.WEATHER
    )


@dp.callback_query_handler(text='wind')
async def process_callback_wind(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        text=messages.wind(callback_query.from_user.username),
        reply_markup=inline_keyboard.WIND
    )


@dp.callback_query_handler(text='sun_time')
async def process_callback_sun_time(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        text=messages.sun_time(callback_query.from_user.username),
        reply_markup=inline_keyboard.SUN_TIME
    )


@dp.callback_query_handler(text='add_thing')
async def sent(callback_query: types.CallbackQuery):
    global flag
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        text="отправьте в сообщении построчно:\nназвание одежды\nтемпературный режим (диапазон через пробел)\nветряной режим (диапазон через пробел)\nфотографию\nесли вешь добавлена в ваш гардероб, вам придет сообщение"
    )
    flag = True



@dp.message_handler(content_types=['photo'])
async def processing(message: types.Message):
    global dict_of_clothes
    global flag
    if flag:
        answer = message.caption
        user = message.chat.username
        ph = message.photo
        if (answer.count("\n")==2):
            thing = re.split("\n| ", answer)
            #print(thing)
            try:
                thing[1] = int(thing[1])
                thing[2] = int(thing[2])
                thing[3] = int(thing[3])
                thing[4] = int(thing[4])
                thing.append(ph[-1]["file_id"])
                if (user in dict_of_clothes.keys()):
                    dict_of_clothes[user].append(thing)
                else:
                    dict_of_clothes[user] = [thing]
                with open('data.pickle', 'wb') as f:
                    pickle.dump(dict_of_clothes, f)

                await message.answer(text=f"{thing[0]} added in your clothes", reply_markup=inline_keyboard.THINGS)
            except ValueError:
                await message.answer(text="wind or temperature parametrs arent numbers", reply_markup=inline_keyboard.THINGS)
        else:
            await message.answer(text="uncorrect input",
                                 reply_markup=inline_keyboard.THINGS)
        flag = False


#запрос одежды через команду и кнопку


@dp.callback_query_handler(text='delete_thing')
async def numb(callback_query: types.CallbackQuery):
    global flag2
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        text="введите номер удаляемой вещи в вашем гардеробе"
    )
    flag2 = True




@dp.message_handler()
async def processing(message: types.Message):
    global dict_of_clothes
    global flag2
    if flag2:
        user = message.chat.username
        number = message.text
        if (str(int(number))==number):
            number = int(number)
            if(len(dict_of_clothes[user])>=number):
                await message.answer(text=f"теперь в вашем гардеробе нет {dict_of_clothes[user][number-1][0]}")
                dict_of_clothes[user].pop(number-1)
                with open('data.pickle', 'wb') as f:
                    pickle.dump(dict_of_clothes, f)

    flag2 = False



@dp.callback_query_handler(text='clothes')
async def process_callback_w(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    try:
        await bot.send_message(
            callback_query.from_user.id,
            text=messages.clothe(dict_of_clothes[callback_query.from_user.username], callback_query.from_user.username),
            reply_markup=inline_keyboard.THINGS
        )
        for i in range(len(messages.photoes)):
            await bot.send_photo(callback_query.from_user.id, photo=messages.photoes[i])
        messages.photoes.clear()
    except KeyError:
        await bot.send_message(
            callback_query.from_user.id,
            text="вы еще не добавили вещи в свой гардероб, но вы можете это сделать с помощью кнопки add thing",
            reply_markup=inline_keyboard.THINGS
        )

@dp.callback_query_handler(text='list')
async def process_callback_wardrobe(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        text="ваш гардероб:" ,
        reply_markup=inline_keyboard.WARDOBE
    )
    try:
        y = messages.st(dict_of_clothes[callback_query.from_user.username])
        if(len(y)>0):
            for i in y:
                await bot.send_message(
                    callback_query.from_user.id,
                    text=i
                )
        else:
            await bot.send_message(
                callback_query.from_user.id,
                text="у вас пока что пустой гардероб"
            )
    except KeyError:
        await bot.send_message(
            callback_query.from_user.id,
            text="у вас пока что пустой гардероб")





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
