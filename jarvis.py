# -*- coding: UTF-8 -*-
#!/usr/bin/python
import telebot, ast
import os
import google
import cambio
from datetime import datetime
from telebot import types
from pygoogles import pygoogle
import sqlite3
from consula import ids, usernames, last, first, lids, usert
text_messages = {
    
    'comandos':
    	u'/commands\n'
    	u'/dolar\n'
    	u'/info\n'
    	u'/user_list\n',
    'jarvoi':
        u'It\'s me.!\n\n'
}
def sql():
	conn = sqlite3.connect('user.db')
	curs = conn.cursor()
	curs.execute('select first_name from users')
	first = str(curs.fetchall())
	curs.execute('select last_name from users')
	last = str(curs.fetchall())
	curs.execute('select id from users')
	lids = curs.fetchall()
	ids = str(lids)
	curs.execute('select username from users')
	usert = curs.fetchall()
	usernames = str(usert)
	ids = ids.strip('] [ ').replace('u\'','').strip('(').replace('\"','').strip(',').replace('\'','').strip()
	dic = {'first':first, 'last':last,'lids':lids, 'ids':ids,'usernames':usernames,'userlist':usert}
	return dic
def log_erros(func, erro,mensagem):
    arq = open('Logs_de_erros.txt', 'a')
    data = str()
    arq.write('''
#Erro! Função {fun} {data}
Mensagem de erro:
{log_erro}
Mensagem que originou o erro:
{mensagem}
------------------------------------'''
                  .format(fun = func, data = str(datetime.today()), log_erro = erro, mensagem = str(mensagem).encode('UTF-8', errors='ignore').decode('ASCII', errors='ignore')))
        
    arq.close()

def log(dados_msg):
    try:
        dados_msg = ast.literal_eval(str(dados_msg).encode('UTF-8', errors='ignore').decode('ASCII', errors='ignore'))
        dic = {'first_name':dados_msg['from_user']['first_name'], 'last_name':dados_msg['from_user']['last_name'],  'username':dados_msg['from_user']['username'], 'chat_id':dados_msg['chat']['id']}
        if dados_msg['chat']['type'] == 'private': origem = 'Mensagem Privada'
        elif dados_msg['chat']['type'] == 'group': origem = 'Grupo'
        elif dados_msg['chat']['type'] == 'supergroup': origem = 'Super Grupo'
        else: origem = dados_msg['chat']['type']
        print('''
LOG: comando recebido
Comando: {comando}
Origem: {origem}
Titulo do chat: {nomechat}
ID do chat: {chatid}
Nome do remetente: {first_name}
Username: {username}'''
              .format(comando = dados_msg['text'], origem = origem, nomechat = dados_msg['chat']['title'], chatid = dados_msg['chat']['id'],
                        first_name = dados_msg['from_user']['first_name'], last_name = dados_msg['from_user']['last_name'] if dados_msg['from_user']['last_name'] else dados_msg['from_user']['first_name'],
                        username = dados_msg['from_user']['username']))
        return dic
    except Exception as erro:
        log_erros('LOG', erro, dados_msg)
        print('Erro na função log, consulte o arquivo logs_de_erros,', datetime.today())
bot = telebot.TeleBot('<TOKEN>)
@bot.message_handler(commands=['start', 'begin'])
def answer(message):
	result = sql()
	info = log(message)
	conn = sqlite3.connect('user.db')
	curs = conn.cursor()
	user_id = str(message.from_user.id)
	if user_id not in str(result['lids']):
		if 'None' not in str(info['username']):
			print('Tem um username')
			curs.execute('insert into users values (?, ?, ?, ?)', (str(info['username']), str(info['first_name']), str(info['last_name']), user_id))
			conn.commit()
			conn.close()
			bot.send_message(info['chat_id'], 'Hi, {}!\nVocê acaba de se inscrever no Jarvis Bot Versão Telegram.\nPara saber mais use /info.'.format(first_name))
		else:
			print('nao tem username')
			name = str((info['first_name']) + str(info['last_name']))
			curs.execute('insert into users values (?, ?, ?, ?)', (name, str(info['first_name']), str(info['last_name']), user_id))

		
	else:
		print('ta no mei')
		bot.send_message(info['chat_id'], 'Você ja está inscrito no Jarvis, use /info para mais.')


@bot.message_handler(commands=['id', 'my_id'])
def id(message):
	info = log(message)
	user_id = message.from_user.id
	bot.send_message(info['chat_id'], 'Nome:{} {}.\nID:{}\nUsername:@{}'.format(info['first_name'], info['last_name'], user_id, info['username']))
@bot.message_handler(func=lambda m: True, content_types=['new_chat_participant'])
def on_user_joins(message):
	log(message)
	name = message.new_chat_participant.first_name
	if hasattr(message.new_chat_participant, 'first_name'):
		name += u" {}".format(message.new_chat_participant.last_name)
		bot.reply_to(message, "Hi, {name}".format(name=name))
	if hasattr(message.new_chat_participant, 'username') and message.new_chat_participant.username is not None:
		bot.reply_to(message, "Hi, {name}".format(name=name))
@bot.message_handler(func=lambda m: True, content_types=['left_chat_participant'])
def user_left(message):
	name = message.left_chat_participant.first_name
	if hasattr(message.left_chat_participant, 'first_name'):
		name += " {}".format(message.left_chat_participant.last_name)
		bot.reply_to(message, "Bye, {name}".format(name=name))
	if hasattr(message.left_chat_participant, 'username') and message.left_chat_participant.username is not None:
		bot.reply_to(message, "Bye, {name}".format(name=name))

@bot.message_handler(commands=['cambio', 'dolar'])
def reply_dolar_currency(message):
	dol = cambio.dolar()
	bot.reply_to(message, dol)
@bot.message_handler(commands=['info'])
def hi(message):
	infosql = sql()
	bot.send_message(message.chat.id, 'Hi, {}!\nSou Jarvis bot desenvolvido por @Junior_Mario.\nQt. de Usuarios: {}.\nPara ver os comandos use /help ou /commands'.format(message.from_user.username, len(infosql['lids'])))


@bot.message_handler(commands=['users', 'user_list'])
def listu(message):
	infosql = sql()
	log(message)
	usuarios = []
	print(type(infosql['userlist']))
	for con in infosql['userlist']:
		usuarios.append(con)
	print(usuarios)
	usuarios = str(usuarios)
	usuarios = usuarios.strip('] [ ').replace('u\'','@').strip('(').replace('\"','').strip(',').replace('\'','').replace(',)','\n').replace(', (','')
	
	bot.send_message(message.chat.id, 'Lista de Usuarios:\n{}'.format(usuarios))
@bot.message_handler(commands=['help', 'commands'])
def showCommands(message):
	bot.reply_to(message, text_messages['comandos'])
@bot.message_handler(commands=['newpoll', 'newask'])
def newask(message):
	markup = types.ReplyKeyboardHide(selective=False)
	markup = types.ForceReply(selective=False)
	a =bot.send_message(message.chat.id, "Send me another word:", reply_markup=markup)
	print(a)

bot.polling()