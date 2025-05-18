import asyncio
import logging
import sys
import random
from os import getenv
import os
import aiocron
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, time

from aiogram.client import bot

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import hbold

import olymp_parser


data = None
favor_data = {}
# user_id = None

# load_dotenv()
TOKEN = open('config.txt').readline().strip()  # '6521893421:AAFt5ma8WeLdqr_XOwNQ9mIegYaldtMqXZM'
dp = Dispatcher()


HELP_STR = '''Данный бот отображает информацию о начале и завершении школьных олимпиад. Бот предоставляет актуальное расписание провидения олимпиад, и способен напоминать о скором начале олимпиады.
/help-список комманд
/start-начать работу с ботом'''


# диалог удаления олимпиады из избранного
@dp.callback_query(F.data.startswith("7_https://"))
async def olymp_like(callback: types.CallbackQuery):
    global data, favor_data
    user_id = callback.from_user.id
    info = callback.data.split('_')[1]
    for line in data:
        if line['link'] == info:
            break
    for line1 in favor_data[user_id]:
        if line1[0] == info:
            favor_data[user_id].remove(line1)
            break
    rep = ''
    rep += line['title'] + '\n\n'
    rep += 'Олимпиада УДАЛЕНА из Избранного.'
    podr = InlineKeyboardBuilder()
    podr.row(types.InlineKeyboardButton(text='↪ НАЗАД', callback_data='start3'))
    await callback.message.answer(rep, reply_markup=podr.as_markup())


# диалог отключения оповещений об олимпиаде в избранном
@dp.callback_query(F.data.startswith("5_https://"))
async def olymp_like(callback: types.CallbackQuery):
    global data, favor_data
    user_id = callback.from_user.id
    info = callback.data.split('_')[1]
    for line in data:
        if line['link'] == info:
            break
    for line1 in favor_data[user_id]:
        if line1[0] == info:
            line1[1] = 0
            break
    rep = ''
    rep += line['title'] + '\n\n'
    rep += 'Оповещения о событиях данной олимпиады теперь ОТКЛЮЧЕНЫ.'
    podr = InlineKeyboardBuilder()
    podr.row(types.InlineKeyboardButton(text='↪ НАЗАД', callback_data='2_' + info))
    await callback.message.answer(rep, reply_markup=podr.as_markup())
    
    
# диалог включения оповещений об олимпиаде в избранном
@dp.callback_query(F.data.startswith("6_https://"))
async def olymp_like(callback: types.CallbackQuery):
    global data, favor_data
    user_id = callback.from_user.id
    info = callback.data.split('_')[1]
    for line in data:
        if line['link'] == info:
            break
    for line1 in favor_data[user_id]:
        if line1[0] == info:
            line1[1] = 1
            break
    rep = ''
    rep += line['title'] + '\n\n'
    rep += 'Оповещения о событиях данной олимпиады теперь ВКЛЮЧЕНЫ.'
    podr = InlineKeyboardBuilder()
    podr.row(types.InlineKeyboardButton(text='↪ НАЗАД', callback_data='2_' + info))
    await callback.message.answer(rep, reply_markup=podr.as_markup())


# диалог изменения настроек об олимпиаде в избранном
@dp.callback_query(F.data.startswith("4_https://"))
async def olymp_like(callback: types.CallbackQuery):
    global data, favor_data
    user_id = callback.from_user.id
    info = callback.data.split('_')[1]
    for line in data:
        if line['link'] == info:
            break
    for line1 in favor_data[user_id]:
        if line1[0] == info:
            break
    rep = ''
    podr = InlineKeyboardBuilder()
    if line1[1] == 1:
        rep += line['title'] + '\n\n'
        rep += 'Оповещения о событиях олимпиады ВКЛЮЧЕНЫ'
        podr.row(types.InlineKeyboardButton(text='Отключить оповещения', callback_data='5_' + info))
    else:
        rep += line['title'] + '\n\n'
        rep += 'Оповещения о событиях олимпиады ОТКЛЮЧЕНЫ'
        podr.row(types.InlineKeyboardButton(text='Включить оповещения', callback_data='6_' + info))        
    podr.row(types.InlineKeyboardButton(text='↪ НАЗАД', callback_data='2_' + info))
    await callback.message.answer(rep, reply_markup=podr.as_markup())


# диалог подробной информации об олимпиаде в избранном
@dp.callback_query(F.data.startswith("3_https://"))
async def olymp_like(callback: types.CallbackQuery):
    global data, favor_data
    user_id = callback.from_user.id
    info = callback.data.split('_')[1]
    for line in data:
        if line['link'] == info:
            break
    rep = 'Олимпиада уже добавлена в твой календарь.\n\n'
    rep += line['title'] + '\n\n' + 'Предмет: ' + line['subject'] + '\n' + 'Класс: ' + line['form'] + '\n' + 'Рейтинг: ' + line['raiting'] + '\n' + 'Дата: ' + line['time'] + '\n\n' + 'Подробнее: ' + line['link']
    podr = InlineKeyboardBuilder()
    podr.row(types.InlineKeyboardButton(text='↪ НАЗАД', callback_data='2_' + info))
    await callback.message.answer(rep, reply_markup=podr.as_markup())


# диалог изменения настроек для оповещений
@dp.callback_query(F.data.startswith("2_https://"))
async def olymp_like(callback: types.CallbackQuery):
    global data, favor_data
    user_id = callback.from_user.id
    info = callback.data.split('_')[1]
    for line in data:
        if line['link'] == info:
            title = line['title']
            break
    podr = InlineKeyboardBuilder()
    podr.row(types.InlineKeyboardButton(text='📋 Подробности', callback_data='3_' + info))
    podr.row(types.InlineKeyboardButton(text='⏰ Изменить настройки напоминания', callback_data='4_' + info))
    podr.row(types.InlineKeyboardButton(text='❌ Удалить олимпиаду', callback_data='7_' + info))
    podr.row(types.InlineKeyboardButton(text='↪ НАЗАД', callback_data='start3'))

    await callback.message.answer('Настройки:\n\n' + title, reply_markup=podr.as_markup())


# диалог добавления олимпиады в избранное
@dp.callback_query(F.data.startswith("1_https://"))
async def olymp_like(callback: types.CallbackQuery):
    global data, favor_data
    user_id = callback.from_user.id
    info = callback.data.split('_')[1]
    for line in data:
        if line['link'] == info:
            if user_id in favor_data:
                favor_data[user_id].append([info, 1])
            else:
                favor_data[user_id] = [[info, 1]]
            break
    print(favor_data)
    await callback.message.answer('Олимпиада добавлена в твой календарь.\n\nКаждый день в 09.00 тебе будет приходить напоминание о событиях для этой олимпиады\n\nДля изменения настроек оповещения зайди в раздел "Мой календарь" и выбери нужную олимпиаду.', reply_markup=builder1.as_markup())


# диалог подробной информации об олимпиаде
@dp.callback_query(F.data.startswith("https://"))
async def olymp_about(callback: types.CallbackQuery):
    global data
    user_id = callback.from_user.id
    info = callback.data
    for line in data:
        if line['link'] == info:
            break
    rep = line['title'] + '\n\n' + 'Предмет: ' + line['subject'] + '\n' + 'Класс: ' + line['form'] + '\n' + 'Рейтинг: ' + line['raiting'] + '\n' + 'Дата: ' + line['time'] + '\n\n' + 'Подробнее: ' + line['link'] 
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text='✅ Буду участвовать',
        callback_data='1_' + line['link']), types.InlineKeyboardButton(
        text='↪ НАЗАД',
        callback_data='start2')
    )
    await callback.message.answer(rep, reply_markup=builder.as_markup())

num = 0

# диалог после нажатия кнопки "Список олимпиад"
@dp.callback_query(F.data == "start2")
async def filter(callback: types.CallbackQuery):
    '''
    await callback.message.answer(''🔽 Выберите класс'',
                                  reply_markup=kclass.as_markup())
    await callback.message.answer(''🔽 Выберите предмет'',
                                  reply_markup=subject.as_markup())
    '''
    global data, num
    if not data:
        data = olymp_parser.get_data()
    builder = InlineKeyboardBuilder()
    for line in data[num:num + 10]:
        builder.row(types.InlineKeyboardButton(
        text=line['title'],
        callback_data=line['link'])
    )
    builder.row(types.InlineKeyboardButton(text='Главное меню', callback_data='start001'),
                types.InlineKeyboardButton(text='Следующие 10', callback_data='next'))
    await callback.message.answer('Вот список доступных олимпиад:',
                         reply_markup=builder.as_markup())


# диалог после нажатия кнопки "Далее"
@dp.callback_query(F.data == "next")
async def filter(callback: types.CallbackQuery):
    '''
    await callback.message.answer(''🔽 Выберите класс'',
                                  reply_markup=kclass.as_markup())
    await callback.message.answer(''🔽 Выберите предмет'',
                                  reply_markup=subject.as_markup())
    '''
    global data, num
    if num < len(data) - 1:
        num += 10
    builder = InlineKeyboardBuilder()
    for line in data[num:num + 10]:
        builder.row(types.InlineKeyboardButton(
        text=line['title'],
        callback_data=line['link'])
    )
    if num < len(data) - 1:
        builder.row(types.InlineKeyboardButton(text='Предыдущие 10', callback_data='prev'),
                    types.InlineKeyboardButton(text='Главное меню', callback_data='start001'),
                    types.InlineKeyboardButton(text='Следующие 10', callback_data='next'))
    else:
        builder.row(types.InlineKeyboardButton(text='Предыдущие 10', callback_data='prev'),
                    types.InlineKeyboardButton(text='Главное меню', callback_data='start001'))
    await callback.message.answer('Вот список доступных олимпиад:',
                         reply_markup=builder.as_markup())


# диалог после нажатия кнопки "Предыдущие 10"
@dp.callback_query(F.data == "prev")
async def filter(callback: types.CallbackQuery):
    '''
    await callback.message.answer(''🔽 Выберите класс'',
                                  reply_markup=kclass.as_markup())
    await callback.message.answer(''🔽 Выберите предмет'',
                                  reply_markup=subject.as_markup())
    '''
    global data, num
    if num > 0:
        num -= 10
    builder = InlineKeyboardBuilder()
    for line in data[num:num + 10]:
        builder.row(types.InlineKeyboardButton(
        text=line['title'],
        callback_data=line['link'])
    )
    if num > 0:
        builder.row(types.InlineKeyboardButton(text='Предыдущие 10', callback_data='prev'),
                    types.InlineKeyboardButton(text='Главное меню', callback_data='start001'),
                    types.InlineKeyboardButton(text='Следующие 10', callback_data='next'))
    else:
        builder.row(types.InlineKeyboardButton(text='Главное меню', callback_data='start001'),
                    types.InlineKeyboardButton(text='Следующие 10', callback_data='next'))
    await callback.message.answer('Вот список доступных олимпиад:',
                         reply_markup=builder.as_markup())    


# диалог после нажатия кнопки "Поиск олимпиад по предмету"
@dp.callback_query(F.data == "start22")
async def filter(callback: types.CallbackQuery):
    subject = InlineKeyboardBuilder()
    subject.row(types.InlineKeyboardButton(text="Русский язык", callback_data="start221_1"),
                (types.InlineKeyboardButton(text='Математика', callback_data="start221_2")))
    subject.row(types.InlineKeyboardButton(text="Информатика", callback_data="start221_3"),
                (types.InlineKeyboardButton(text='Английский язык', callback_data="start221_4")))
    subject.row(types.InlineKeyboardButton(text="Обществознание", callback_data="start221_5"),
                (types.InlineKeyboardButton(text='История', callback_data="start221_6")))
    subject.row(types.InlineKeyboardButton(text="Биология", callback_data="start221_7"),
                (types.InlineKeyboardButton(text='Химия', callback_data="start221_8")))
    subject.row(types.InlineKeyboardButton(text="Физика", callback_data="start221_9"),
                (types.InlineKeyboardButton(text='Литература', callback_data="start221_10")))
    subject.row(types.InlineKeyboardButton(text='Главное меню', callback_data='start001'))
    await callback.message.answer('''🔽 Выберите предмет''', reply_markup=subject.as_markup())


# диалог после нажатия кнопки "Русский язык и т.п."
@dp.callback_query(F.data.startswith("start221_"))
async def filter(callback: types.CallbackQuery):
    global data
    if not data:
        data = olymp_parser.get_data()
    sub = callback.data.split('_')[1]
    if sub == '1': sub = 'русский язык'
    elif sub == '2': sub = 'математика'
    elif sub == '3': sub = 'информатика'
    elif sub == '4': sub = 'английский язык'
    elif sub == '5': sub = 'обществознание'
    elif sub == '6': sub = 'история'
    elif sub == '7': sub = 'биология'
    elif sub == '8': sub = 'химия'
    elif sub == '9': sub = 'физика'
    elif sub == '10': sub = 'лингвистика'
    filter_data = []
    for line in data:
        if line['subject'].strip().lower() == sub:
            filter_data.append(line)
    builder = InlineKeyboardBuilder()
    for line in filter_data[:10]:
        builder.row(types.InlineKeyboardButton(text=line['title'], callback_data=line['link']))
    builder.row(types.InlineKeyboardButton(text='↪ НАЗАД', callback_data='start22'),
                types.InlineKeyboardButton(text='Главное меню', callback_data='start001'))
    await callback.message.answer('Вот доступные олимпиад по предмету ' + sub + ':',
                         reply_markup=builder.as_markup())


# диалог после нажатия кнопки "Мой календарь"
@dp.callback_query(F.data == "start3")
async def favorite(callback: types.CallbackQuery):
    global favor_data, data
    user_id = callback.from_user.id
    builder = InlineKeyboardBuilder()
    if user_id in favor_data:
        text = 'Вот олимпиады, в которых ты принимаешь участие:'
        for line in favor_data[user_id]:
            for olymp in data:
                if olymp['link'] == line[0]:
                    builder.row(types.InlineKeyboardButton(text=olymp['title'], callback_data='2_' + line[0]))
                    break
    else:
        text = 'Ты не участвуешь ни в одной олимпиаде'
    builder.row(types.InlineKeyboardButton(text='↪ НАЗАД', callback_data='start001'))
    await callback.message.answer(text, reply_markup=builder.as_markup())


# начало диалога с ботом
@dp.callback_query(F.data == "start4")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer(HELP_STR, reply_markup=back1.as_markup())


@dp.callback_query(F.data == "start001")
async def start01(callback: types.CallbackQuery):
    await callback.message.answer("✅ Выберите, что вам нужно:",
                                  reply_markup=builder1.as_markup())


back1 = InlineKeyboardBuilder()
back1.row(types.InlineKeyboardButton(text='↪ НАЗАД', callback_data='start001'))

kclass = InlineKeyboardBuilder()
kclass.row(types.InlineKeyboardButton(text='1️⃣', callback_data='start21'),(types.InlineKeyboardButton(text='2️⃣', callback_data='start21')),(types.InlineKeyboardButton(text='3️⃣', callback_data='start21')))
kclass.row(types.InlineKeyboardButton(text='4️⃣', callback_data='start21'),(types.InlineKeyboardButton(text='5️⃣', callback_data='start21')),(types.InlineKeyboardButton(text='6️⃣', callback_data='start21')))
kclass.row(types.InlineKeyboardButton(text='7️⃣', callback_data='start21'),(types.InlineKeyboardButton(text='8️⃣', callback_data='start21')),(types.InlineKeyboardButton(text='9️⃣', callback_data='start21')))
kclass.row(types.InlineKeyboardButton(text='1️⃣0️⃣', callback_data='start21'),(types.InlineKeyboardButton(text='1️⃣1️⃣', callback_data='start21')))


builder1 = InlineKeyboardBuilder()
builder1.row(types.InlineKeyboardButton(text="🔎 Приступить к выбору олимпиады", callback_data="start2"))
builder1.row(types.InlineKeyboardButton(text="🔎 Поиск олимпиады по предмету", callback_data="start22"))
builder1.row(types.InlineKeyboardButton(text='❤ Мой календарь', callback_data="start3"))
builder1.row(types.InlineKeyboardButton(text='❓ Помощь / Команды', callback_data="start4"))


# диалог справочной информации
@dp.message(Command('help'))
async def command_start(message: Message):
    await message.answer(HELP_STR,
                          reply_markup=back1.as_markup())

# начало диалога с ботом
@dp.message(Command('start'))
async def command_start(message: Message):
    # await message.answer_sticker('CAACAgIAAxkBAAECRVxlbOeBuYcU7hzZnw7VXQAB-Svyx3sAAmcBAAIWQmsKc4m-zqWWaCIzBA')
    user_id = message.from_user.id
    await message.answer(f"🔴 {hbold(message.from_user.first_name)}, добро пожаловать в наш Бот!\n\n" + HELP_STR,
                         reply_markup=builder1.as_markup())


# диалог, если нет подходящего ответа
@dp.message()
async def command_understand(message: Message):
    await message.reply(f'''К сожалению я Вас не понимаю, 
воспользуйтесь командой --> /help''')
    

# рассылка оповещений    
async def send_message_cron(bot: Bot):
    if favor_data:
        for d in favor_data:
            user_id = d
            olymp = favor_data[user_id]
            res = ''
            for line in olymp:
                if line[1] == 1:
                    for line1 in data:
                        if line1['link'] == line[0]:
                            title = line1['title']
                            time = line1['time']
                            break
                res += '🔴 ' + title + '\n' + time + '\n\n'
            # print(data, favor_data[data])
            await bot.send_message(user_id, '''Напоминание!\nВы записаны на следующие олимпиады:\n\n''' + res)


# функция установки времени напоминаний и запуска оповещений
async def main():
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(send_message_cron, trigger='cron', hour=9, minute=0, start_date=datetime.now(), kwargs={'bot': bot})
    scheduler.start()    
    await dp.start_polling(bot)
    

# старт бота    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    aiocron.asyncio.get_event_loop().run_forever()
