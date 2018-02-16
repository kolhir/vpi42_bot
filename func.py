# -*- coding: utf-8 -*-
import time, db
from datetime import datetime,date
start = "начало"
end = "конец"
weekdays=("Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье")
def id2group(user_id):
    group = ""
    if len(db.Users.select().where(db.Users.user_id == user_id)) == 0:
        return 0
    else:
        group = (db.Users.get(db.Users.user_id == user_id).group_id)
        return group

def listGroup():
    l = []
    for i in db.Group.select():
        l.append(i.name)
    return l
def group_name(group):
    h = db.Group.get(db.Group.id == group)
    return(h.name)

def addUser(*args):
    group = db.Group.get(db.Group.name == args[1])
    db.Users.create(user_id = args[0], group_id = group,
        user_name = args[2], name = args[3], last_name = args[4] )

def deleteUser(user_id):
    db.Users.get(db.Users.user_id == user_id).delete_instance()
#Создание словаря времени
def time_dict():
    timeles = [
    {
        "начало": {},
        "конец": {}
    }]

    for i in db.LessonTime.select():
        start_dict = {str(i.number_lesson):str(i.start)}
        end_dict = {str(i.number_lesson):str(i.end)}
        timeles[0][start].update(start_dict)
        timeles[0][end].update(end_dict)
    return timeles
def nextLesson(group):
    timeles = time_dict()

    timenow = time.strptime(time.strftime("%X", time.localtime()), "%X")
    # timenow = time.strptime("13:45:00", "%X")
    weekday_number = date.weekday(datetime.now()) + 1
    weekdays=("Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье")
    day = weekdays[weekday_number]

    week=(int(datetime.today().strftime("%U")))%2+1
    answer=""

    flag = ""
    tt = db.Time_table
    if weekday_number == 7:
        answer = ""
        return answer
    elif weekday_number == 6: #TODO проверить субботу
        answer = ""
        return answer
    else: w = 0
    dayX = weekday_number
    # if not(tt[klass][day]):
    #     answer = "Так хочется учиться сегодня??? Сорри, кажется у тебя сегодня выходной."
    #     return answer

    # while (timeles[w][start][str(n)]):
    #     n = n + 1
    #     if n == 11:
    #         break
    # n = n - 1

    p = tt.select().where(tt.group_id == group , tt.day_id == weekday_number, tt.number_week_id == week)
    n = len(p)

    def answer_next_l(i):
        answer = ""
        lesson = tt.select().where(tt.group_id == group , tt.day_id == weekday_number, tt.number_week_id == week, tt.lesson_time_id == i)
        l =lesson[0]

        lesson_next = db.Lessons.get(id = l.lesson_id)
        teacher_next =  db.Teacher.get(id = l.teacher_id)
        room_next =  db.Room.get(id = l.room_id)
        type_next = db.TypeLesson.get(id = l.type_lessons_id)

        answer = (lesson_next.full_name+"\n"+ type_next.type_name +"\n"\
        +room_next.korpus+" "+str(room_next.number)+"\n"\
        +teacher_next.last_name)

        return answer        #TODO на нах
    for i in range(1,n):
        les1s = time.strptime(timeles[w][start][str(i)], "%X")
        les1e = time.strptime(timeles[w][end][str(i)], "%X")
        les2s = time.strptime(timeles[w][start][str(i + 1)], "%X")
        les2e = time.strptime(timeles[w][end][str(i + 1)], "%X")

        if les1s <= timenow <=  les1e: #TODO timenow неопределенно
            answer = answer_next_l(i+1)
            flag = answer_next_l(i+1)
            break
        elif les1e <= timenow <= les2s:
            answer = answer_next_l(i+1)
            flag = answer_next_l(i+1)
            break
        elif (i == n-1) and (les2s <= timenow <= les2e):
            answer = (str(answer_next_l(i+1)) + str("(последняя пара)"))
            flag  = answer_next_l(i+1)
            break
        elif (i == n-1) and (timenow > les2e):
            answer = ("Все, остановись, сегодня больше нет пар")
            flag = ""
            break
        elif (i==1) and (timenow < les1s):
            lesson = tt.select().where(tt.group_id == group , tt.day_id == dayX, tt.number_week_id == week)
            l = lesson[0]
            lesson_next = db.Lessons.get(id = l.lesson_id)
            teacher_next =  db.Teacher.get(id = l.teacher_id)
            room_next =  db.Room.get(id = l.room_id)
            type_next = db.TypeLesson.get(id = l.type_lessons_id)

            answer = (lesson_next.full_name+"\n"+type_next.type_name+"\n"\
            +room_next.korpus+"-"+str(room_next.number)+"\n"\
            +teacher_next.last_name)

            flag = answer
            # if (tt[klass][day]):
            # for k in range(1,6):
            #     if (tt[klass][day][str(k)]):
            #         answer = ("Следующий урок: "+ str(tt[klass][day][str(k)]))
            #         flag = str(tt[klass][day][str(k)])
            #         break
            # else:
            #     answer = "Сегодня нет уроков"
            #     flag = "1"
            #     break
    if flag:
        return answer
    else:
        answer = "Сегодня больше нет пар"
        return answer

def onDay(day, group):
    answer = ""
    flag = 0
    win = ""
    weekday_number = 42
    for i,k in enumerate(weekdays):
        if day == k:
            weekday_number = i + 1

    if  1 < weekday_number <= 5:
        w = 0
    else: return ""
    timeles = time_dict()
    # if not(tt[klass][day]):
    #     answer = ("Ты разве учишься в этот день?!")
    #     return answer

    tt = db.Time_table
    dayX = weekday_number
    week=(int(datetime.today().strftime("%U")))%2+1

    p = tt.select().where(tt.group_id == group , tt.day_id == dayX, tt.number_week_id == week)
    n = len(p)
    def answer_l(i):
        answer = ""
        lesson = tt.select().where(tt.group_id == group , tt.day_id == dayX, tt.number_week_id == week, tt.lesson_time_id == i)
        for l in lesson:

            lesson_next = db.Lessons.get(id = l.lesson_id)
            teacher_next =  db.Teacher.get(id = l.teacher_id)
            room_next =  db.Room.get(id = l.room_id)
            type_next = db.TypeLesson.get(id = l.type_lessons_id)

            answer = ("\n"+lesson_next.full_name+"\n"+type_next.type_name +"\n"
            +room_next.korpus+"-"+str(room_next.number) + "\n"+ str(teacher_next.last_name))


            return answer
    for i in range(1,7):
        st = str(timeles[w][start][str(i)])
        en = str(timeles[w][end][str(i)])

        l = tt.select().where(tt.group_id == group , tt.day_id == dayX, tt.number_week_id == week,  tt.lesson_time_id == i)
        if (len(l) == 0):
            win = win + ('`'+str(i) + ". " + st[0:5] + " - " +en[0:5]+ "` \n`                 `..." + "" + " \n")
            flag = flag + 1
        else:
           answer = answer + win + ('`'+str(i) + ". " + st[0:5] + " - " +en[0:5]+ "` " + str(answer_l(i)) + " \n")
           win = ""
        if ((i == 6) and (flag == 6)):
            answer = ("Вы не учитесь в этот день")
            break
    return answer

def untilTheEnd():
    def deltaplan(now_time, next_time):
        answer=0
        (now_time,next_time)=(list(now_time),list(next_time))
        if now_time[3]>next_time[3] :next_time[3]=next_time[3]+24
        if now_time[5]>next_time[5] :answer=answer-1
        answer=answer+(next_time[3]-now_time[3])*60+next_time[4]-now_time[4]
        return answer

    def valMinute(delta):
        answer = ("До конца пары осталось: " + str(delta)+ " минут")
        if 11 <= delta <= 19:
            pass
        elif delta % 10 == 1:
            answer += "a"
        elif 2 <= (delta % 10) <= 4:
            answer += "ы"
        else:
            pass
        return answer

    def minute(delta):
        if 11 <= delta <= 19:
            return(" минут" )
        elif delta % 10 == 1:
            return(" минутa" )
        elif 2 <= (delta % 10) <= 4:
            return(" минуты" )
        else:
            return(" минут" )

    timeles = time_dict()
    timenow = time.strptime(time.strftime("%X", time.localtime()), "%X")
    weekday_number = date.weekday(datetime.now())
    weekdays=("Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье")
    day = weekdays[weekday_number]
    answer=""
    flag = ""
    # timenow = time.strptime("12:55:00", "%X")
    if weekday_number == 6:
        answer = ""
        return answer
    elif weekday_number == 5:
        answer = ""
        return answer
    else: w = 0

    # if not(tt[klass][day]):
    #     answer = ("Ты разве учишься сегодня?!")
    #     return answer

    # n = 1
    # while (timeles[w][start][str(n)]):
    #     n = n + 1
    #     if n == 11:
    #         break
    # n = n -1
    n = 6
    for i in range(1, n):
        begin1 = time.strptime(timeles[w][start][str(i)], "%X")
        end1 = time.strptime(timeles[w][end][str(i)], "%X")
        begin2 = time.strptime(timeles[w][start][str(i + 1)], "%X")
        end2 = time.strptime(timeles[w][end][str(i + 1)], "%X")
        if timenow <= begin1:
            delta = deltaplan(timenow, begin1)
            answer = ("Учебный день еще не начался.\nПервая пара начнется через " + str(delta) + minute(delta))
            break
        elif  (begin1 < timenow <= end1):
            delta = deltaplan(timenow, end1)
            answer = valMinute(delta)
            break
        elif (end1 < timenow <= begin2):
            delta = deltaplan(timenow, begin2)
            answer = ("Сейчас перемена!\nДо начала пары: " + str(delta) + minute(delta))
            break
        elif (i == (n - 1)):
            print(1, " ", i)
            if (timenow > end2):
                answer = ("К сожалению учебный день в твоем вузе уже закончился:(")
                break
            elif (end1 < timenow <= begin2):
                delta = deltaplan(timenow, begin2)
                answer = ("Сейчас перерыв!\nДо начала пары : " + str(delta) + minute(delta))
                break
            elif (begin2 < timenow <= end2):
                delta = deltaplan(timenow, end2)
                answer = valMinute(delta)
                break
    if answer == "":
        answer = ("Кажется что-то пошло не так, напиши пожалуйста об этом сюда @nekolhir")
    return answer
