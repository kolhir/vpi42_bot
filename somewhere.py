# -*- coding: utf-8 -*-
token = 'YOUR TOKEN HERE'
admins=('your admin','another admin')
alive_message="`   рил толк`\n` я снова жив`\n  __но это не точно__ "
def getadmins():
	return(admins)

def i_am_alive(bot):
    for admin in admins: bot.send_message(admin, alive_message, parse_mode='MARKDOWN')
