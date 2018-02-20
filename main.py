import telebot, config, time, random, requests
import func as f
from datetime import datetime,date
from somewhere import token
from telebot import types

bot = telebot.TeleBot(token, threaded=False)

def timenow(): return time.strftime("%X", time.localtime())

weekdays=("Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье")


from admins import getadmins
def alert_admins(something):
    for admin in getadmins():
        print(admin)
        bot.send_message(admin, something, parse_mode='MARKDOWN')
alert_admins("`   рил толк`\n` я снова жив`\n  __но это не точно__ ")


def rand_quote(message):
    rand = (random.randint(0,len(config.quote)))
    quote = config.quote[rand]
    user = message.from_user
    k=user
    group = f.id2group(user.id)
    l=group
    print("Вывод")
    if group:
        group = f.str_group(group)
        print("Группа: ", group, " ", timenow(), sep = "")
    print(user.id, ";  Имя: ", user.first_name, ";  Фамилия: ", user.last_name, "; User_name: ", user.username, "\n", "Отправлена цитата:", quote , "\n", sep = "")
    bot.send_message(message.from_user.id, quote , reply_markup = standart_buttons_markup())

def send_message(userid, string, message, reply_markup=None, parse=None):
    k = message.from_user
    l = f.id2group(k.id)
    print("Вывод")
    if(l):
        l = f.str_group(l)
        print("Группа: ", str(l), " ", timenow(), sep = "")
    print(k.id, ";  Имя: ", k.first_name, ";  Фамилия: ", k.last_name, "; User_name: ", k.username, "\n", "Сообщение: ", string, "\n", sep = "")
    return (bot.send_message(userid, string, reply_markup = reply_markup, parse_mode = parse))


def standart_buttons_markup():
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Следующая пара','Номер недели')
    user_markup.row('Расписание на день')
    user_markup.row('Сколько осталось до звонка?')
    user_markup.row('Изменить группу')
    return user_markup

def getinlineOnDay(msgtxt):
    inlineOnDay = types.InlineKeyboardMarkup()
    inlineOnDay.add(types.InlineKeyboardButton(text="⬅", callback_data="⬅"+msgtxt))
    #inlineOnDay.add(types.InlineKeyboardButton(text="⤵", callback_data="⤵"+msgtxt))
    inlineOnDay.add(types.InlineKeyboardButton(text="➡", callback_data="➡"+msgtxt))
    return(inlineOnDay)

def choose_group(message):
    user_group_id = f.id2group(message.from_user.id)
    if user_group_id:
        f.deleteUser(message.from_user.id)
    l = f.listGroup()
    print(l)
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    for i in l:
        user_markup.row(i)
    send_message(message.from_user.id, "Выбери группу", message ,reply_markup = user_markup)

def start(message):
    send_message(message.from_user.id, "Выбери действие", message,  reply_markup = standart_buttons_markup())

def ttOnDay(message,week=(int(datetime.today().strftime("%U")))%2+1):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Понедельник'+'('+'I'*week+')', 'Четверг'+'('+'I'*week+')')
    user_markup.row('Вторник'+'('+'I'*week+')', 'Пятница'+'('+'I'*week+')')
    user_markup.row('Среда'+'('+'I'*week+')', 'Суббота'+'('+'I'*week+')')
    user_markup.row('Сменить неделю'+' ('+'I'*((week)%2+1)+')')
    day = send_message(message.from_user.id, "Выбери день",message , reply_markup = user_markup)
    bot.register_next_step_handler(day, onDay)

# def change_smt(message):
#     user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
#     user_markup.row('Изменить класс')
#     user_markup.row('Изменить школу')
#     my_send_message(message.from_user.id, "Что изменить?", user_markup, message)

def nextLesson(message):
    answer = f.nextLesson(f.id2group(message.from_user.id))

    if answer == "":
        rand_quote(message)
    else:
        send_message(message.from_user.id, answer,message, reply_markup =  standart_buttons_markup())
        if answer in config.not_lesson:
            rand_quote(message)

def untilTheEnd(message):
    answer =  f.untilTheEnd()
    if answer == "":
        rand_quote(message)
    else:
        send_message(message.from_user.id, answer,message ,reply_markup =   standart_buttons_markup())###Передать класс человека
        if answer in config.not_lesson:
            rand_quote(message)
def number_week(message):
    week=(int(datetime.today().strftime("%U")))%2+1
    KRASIVIY_VIVOD_id_Vasya = ('Сейчас идет ' + ['первая','вторая'][week-1] + ' учебная неделя')
    send_message(message.from_user.id,KRASIVIY_VIVOD_id_Vasya,message)
    rand_quote(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        msgtxt=call.data[1:]
        vektor=call.data[0]
        if vektor=='':'⤵'
        else:
            k = call.message.chat
            week=(msgtxt[msgtxt.find('(')+1:-1])
            weekNum=-1
            for I in week:
                if I=='I': weekNum=weekNum+1
                else: weekNum=42
            if weekNum in range(0,2):
                daynum=weekdays.index(msgtxt[:msgtxt.find('(')])
                if vektor=='⬅':
                    daynum=daynum-1
                    if daynum==-1:
                        daynum=5
                        weekNum=1-weekNum
                elif vektor=='➡':
                    daynum=daynum+1
                    if daynum==6:
                        daynum=0
                        weekNum=1-weekNum
                answer = f.onDay(weekdays[daynum], f.id2group(call.message.from_user.id),week=weekNum+1)
                #print((weekdays[daynum], f.id2group(call.message.chat.id),weekNum+1))


                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer,reply_markup=getinlineOnDay(weekdays[daynum]+'('+'I'*(weekNum+1)+')'))

@bot.message_handler(commands=['db'])
def handle_db(message):
    if message.from_user.id in getadmins(): bot.send_document(message.from_user.id,open('tt.db','rb'))

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_group_id = f.id2group(message.from_user.id)
    if user_group_id:
        k = message.from_user
        l = f.str_group(f.id2group(k.id))
        send_message(message.from_user.id, 'я тебя вроде уже знаю, ты из '+str(l),message ,reply_markup =  standart_buttons_markup())
    else:
        choose_group(message)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_group_id = f.id2group(message.from_user.id)
    k = message.from_user
    print("Ввод")
    if(user_group_id):
        l = f.str_group(f.id2group(k.id))
        print("Группа: ",l, " ", timenow(), sep = "")
    print(k.id, ";  Имя: ", k.first_name, ";  Фамилия: ", k.last_name, "; User_name: ", k.username, "\n", "Сообщение от пользователя: ", message.text, "\n", sep = "")

    if user_group_id:
        if message.text == "Следующая пара":
            nextLesson(message)
        elif message.text == "Номер недели":
            number_week(message)
        elif message.text == "Расписание на день":
            ttOnDay(message)
        elif message.text == "Сколько осталось до звонка?":
            untilTheEnd(message)#МЕССЕНДЖ
        elif message.text == "Изменить группу":
            choose_group(message)
        else: start(message)
    elif message.text in f.listGroup():
        k = message.from_user
        f.addUser(k.id, message.text,  k.username, k.first_name,  k.last_name)
        start(message)
    else:
        choose_group(message)

def onDay(message): #рассписание
    print("Ввод")
    k = message.from_user
    user_group_id = f.id2group(k.id)
    if(user_group_id):
        l = f.str_group(user_group_id)
        print("Группа: ",l, " ", timenow(), sep = "")
    print(k.id, ";  Имя: ", k.first_name, ";  Фамилия: ", k.last_name, "; User_name: ", k.username, "\n", "Сообщение от пользователя: ", message.text, "\n", sep = "")
    #конец логов начало логики
    msgtxt=message.text
    if msgtxt[:msgtxt.find('(')] in weekdays or msgtxt.find('(')==-1 and msgtxt in weekdays : # ввели ли день недели с учетом возможного  "(..." на конце(нет проверки того что в скобках)
        week=(msgtxt[msgtxt.find('(')+1:-1])
        weekNum=-1
        for I in week:
            if I=='I': weekNum=weekNum+1
            else: weekNum=42
        if weekNum in range(0,2):
            #print(msgtxt[:msgtxt.find('(')], f.id2group(message.from_user.id),weekNum+1)
            answer = f.onDay(msgtxt[:msgtxt.find('(')], f.id2group(message.from_user.id),week=weekNum+1)
        else: ttOnDay(message)
        if answer == "":
            rand_quote(message)
        else:
            send_message(message.from_user.id, answer, message , reply_markup = getinlineOnDay(msgtxt),parse='MARKDOWN')
            if answer in config.not_lesson:
                rand_quote(message)
    #elif message.text == "Следующий урок": #это тут не нужно
    #     nextLesson(message)
    elif msgtxt[:msgtxt.find('(')] =='Сменить неделю ':
        ttOnDay(message,week=((int(datetime.today().strftime("%U")))%2+1)%2+1)
    else: ttOnDay(message)
while True:
    try:
        bot.polling(none_stop=True)

    except Exception as e:
        print("Ошибка: ",e)
        import traceback; traceback.print_exc()  # или просто print(e) если у вас логгера нет,
        # или import traceback; traceback.print_exc() для печати полной инфы
        time.sleep(15)
