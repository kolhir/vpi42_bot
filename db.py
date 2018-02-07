from peewee import *

db = SqliteDatabase('tt.db')

class BaseModel(Model):
    class Meta:
        database = db

class Group(BaseModel):
    name = CharField()

class DaysWeek(BaseModel):
    name = CharField()


class NumberWeek(BaseModel):
    number = IntegerField()


class LessonTime(BaseModel):
    number_lesson = IntegerField()
    start = TimeField()
    end = TimeField()

class Room(BaseModel):
    korpus = CharField()
    number = IntegerField()


class Teacher(BaseModel):
    first_name = CharField(null = True)
    last_name = CharField()
    pobatushke = CharField(null = True)


class TypeLesson(BaseModel):
    type_name = CharField()


class Lessons(BaseModel):
    name = CharField()
    full_name = CharField()

class Users(BaseModel):
    user_id = IntegerField(primary_key=True)
    user_name = CharField(null = True)
    name = CharField(null = True)
    last_name = CharField(null = True)
    group = ForeignKeyField(Group)

class Time_table(BaseModel):
    group = ForeignKeyField(Group)
    day = ForeignKeyField(DaysWeek)
    number_week = ForeignKeyField(NumberWeek)
    lesson_time = ForeignKeyField(LessonTime)
    lesson = ForeignKeyField(Lessons)
    teacher = ForeignKeyField(Teacher)
    room = ForeignKeyField(Room)
    type_lessons = ForeignKeyField(TypeLesson)


# def create_tables():
#     with db:
#         db.create_tables([Users, Group, Time_table, DaysWeek, NumberWeek,
#                             LessonTime, Room, Teacher, TypeLesson, Lessons])
import time
def read_file(s):
    f = open(s, "r")
    for line in f:

        l = list(line.split("|"))
        print(l)
        if len(Group.select().where(Group.name == l[0])) == 0:
            Group.create(name = l[0])
        l0 = Group.select().where(Group.name == l[0]).get()

        l1 = DaysWeek.select().where(DaysWeek.id == int(l[1])).get()

        l2 = NumberWeek.select().where(NumberWeek.number == int(l[2])).get()

        l3 = LessonTime.select().where(LessonTime.number_lesson == int(l[3])).get()

        l4 = Lessons.select().where(Lessons.full_name  == l[4]).get()

        l5 = Teacher.select().where(Teacher.last_name  == l[5]).get()

        l6 = Room.select().where(Room.korpus  == l[6], Room.number == int(l[7])).get()

        l[8] = l[8].replace("\n", "")
        if len(TypeLesson.select().where(TypeLesson.type_name  == l[8])) == 0:
            TypeLesson.create(type_name = l[8])
        l8 = TypeLesson.select().where(TypeLesson.type_name  == l[8]).get()

        print(l)
        print(l8.type_name)

        Time_table.create(group = l0, day = l1, number_week = l2,
            lesson_time = l3, lesson = l4, teacher = l5, room = l6, type_lessons = l8)
        print("done")

#         if  len(Teacher.select().where(Teacher.last_name  == l[5])) == 0:
#             Teacher.create(first_name = "", last_name = l[5], pobatushke = "")

#         Lessons.create(name = l[0], full_name = (' '.join(l[1:])).replace("\n", ""))

#         print(l)
#         try:
#             l[2]
#             print("try1")
#         except IndexError:
#             import traceback
#             traceback.print_exc()
#             l.append("")
#             try:
#                 l[2]
#                 print("try2")
#             except IndexError:
#                 import traceback
#                 traceback.print_exc()
#                 l.append("")
#         Teacher.create(first_name = l[1], last_name = l[0], pobatushke = l[2])

#         Room.create(korpus = l[0], number = int(l[1]))

#         LessonTime.create(number_lesson = int(l[0]), start = l[1], end = l[2])

#         DaysWeek.create(name = line.strip())
