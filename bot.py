# -*- coding: UTF-8 -*-
#!/usr/bin/python
import telebot, ast
import os
import crawler
import hashlib
from datetime import datetime
from telebot import types
import sqlite3
import random
from utils import *
bot = telebot.TeleBot('<TOKEN>')
bot.skip_pending = True
@bot.message_handler(commands=['start', 'begin'])
def answer(message):
	result = sql()
	info = log(message)
	conn = sqlite3.connect('user.db')
	curs = conn.cursor()
	chat_id = message.chat.id
	user_id = str(message.from_user.id)
	if user_id not in str(result['lids']):
		if 'None' not in str(info['username']):
			print('Tem um username')
			curs.execute('insert into users values (?, ?, ?, ?)', (info['username'], info['first_name'], info['last_name'], user_id))
			conn.commit()
			conn.close()
			bot.send_message(info['chat_id'], 'Hi, {}!\nVocê acaba de se inscrever no Jarvis Bot Versão Telegram.\nPara saber mais use /info.'.format(info['first_name']))
		else:
			print('nao tem username')
			name = str((info['first_name']) + str(info['last_name']))
			curs.execute('insert into users values (?, ?, ?, ?)', (name, str(info['first_name']), str(info['last_name']), user_id))

		
	else:
		print('ta no mei')
		bot.send_message(chat_id, 'Você ja está inscrito no Jarvis, use /info para mais.')

@bot.message_handler(commands=['admin', '/manager'])
def ad(message):
	if not is_admin(message):
		bot.reply_to(message, 'Você não é admin desse bot.')
	else:
		bot.reply_to(message, 'Hi Junior!')
@bot.message_handler(commands=['me'])
def me(message):
    user = bot.get_me()
    bot.reply_to(message, str(user))
@bot.message_handler(commands=['id', 'my_id'])
def id(message):
	try:
		info = log(message)
		user_id = message.from_user.id
		bot.send_message(info['chat_id'], 'Nome:{} {}.\nID:{}\nUsername:@{}'.format(info['first_name'], info['last_name'], user_id, info['username']))
	except UnicodeError:
		bot.reply_to(message, 'AFF, mas nomes com caracteres especiais povo com espirito de funkeiro...')
@bot.message_handler(func=lambda m: True, content_types=['new_chat_participant'])
def on_user_joins(message):
	try:
	    info = log(message)
	    if hasattr(message.new_chat_participant, info['first_name']) and  info['first_name'] is not None:
			name += u" {}".format(info['last_name'])
			bot.reply_to(message, "Hi, {name}".format(name=name))
	except TypeError:
		pass
@bot.message_handler(func=lambda m: True, content_types=['left_chat_participant'])
def user_left(message):
	name = message.left_chat_participant.first_name
	if hasattr(message.left_chat_participant, 'first_name'):
		try:
			name += " {}".format(message.left_chat_participant.last_name.encode('utf-8'))
			bot.reply_to(message, "Bye, {name}".format(name=name))
		except:
			bot.reply_to(message, 'Tem merda no seu sobrenome e eu não vou quebrar cabeça.')
		if hasattr(message.left_chat_participant, 'username') and message.left_chat_participant.username is not None:
			try:
				bot.reply_to(message, "Bye, {name}".format(name=name))
			except:
				bot.reply_to(message, 'aaaaa')

@bot.message_handler(commands=['cambio', 'dolar'])
def reply_dolar_currency(message):
	dol = crawler.dolar()
	bot.reply_to(message, dol)
@bot.message_handler(commands=['info'])
def hi(message):
	infosql = sql()
	bot.send_message(message.chat.id, 'Hi, {}!\nSou Jarvis bot desenvolvido por @Junior_PyJS.\nQt. de Usuarios: {}.\nPara ver os comandos use /help ou /commands'.format(message.from_user.username, len(infosql['lids'])))

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
@bot.message_handler(commands=['github'])
def github(message):
	arg = str(message.text).strip('/github')
	val = crawler.send_git(arg)
	bot.reply_to(message, val)
#	bot.reply_to(message, 'Sua pesquisa não foi encontrada!')
@bot.message_handler(commands=['help', 'commands'])
def showCommands(message):
	bot.reply_to(message, text_messages['comandos'])

@bot.message_handler(commands=['google', 'search'])
def sear(message):
	try:
		arg = log(message)
		searc = str(message.text)
		searc = searc.strip('/google')
		res = crawler.search(searc)
		print(res)
		bot.reply_to(message, res)
	except:
		bot.reply_to(message, 'Sintaxe invalida!\nUse /google nome da pesquisa')

@bot.message_handler(commands=['hash'])
def md5(message):
	try:
		arg = str(message.text)
		arg = arg.strip('/hash')
		print(arg)
		h = hashlib.md5()
		h.update(arg)
		bot.reply_to(message, 'hash Gerada com sucesso:\n{}'.format(h.hexdigest()))
	except:
		bot.reply_to(message, 'Sintaxe invalida\nUse /hash string a ser transformada.')
@bot.message_handler(commands=['youtube', 'video'])
def youtube(message):
	try:
		arg = str(message.text)
		arg = arg.strip('/youtube')
		result = crawler.pesquisa(arg)
		bot.reply_to(message, result)
	except IndexError:
		bot.reply_to(message, 'Sintaxe invalida!\nUse /youtube string a ser pesquisada.')
@bot.message_handler(commands=['code', 'source'])
def send_code(message):
	global githubs
	global bitbucket
	bot.reply_to(message, "Github: {}\nBitBucket:{}.".format(githubs, bitbucket))
@bot.message_handler(commands=['gay', 'yuri'])
def itsgd(message):
	arrag = ['i\'m sick of it...','Calling Yuri...', 'Ta no desejo dele? ele não te liga?', 'Yuriiiiiiii', 'Só assistindo esse romance...Yuri - Angelo', 'Marcos e seus fetiches com Bots e andorinhas gays']
	bot.reply_to(message, random.choice(arrag))
@bot.message_handler(commands=['pdf','apostila'])
def send_it(message):
	mess = str(message.text).strip('/pdf')
	try:
		bot.reply_to(message, 'Baixando...')
		pdf = crawler.apostilando(mess)
		bot.send_document(message.chat.id, pdf)
	except:
		bot.reply_to(message, 'Sua pesquisa é invalida ou não foi encotrado resultado.')
	'''
@bot.message_handler(commands=['/img','pic'])
def img_send(message):
	'''
@bot.message_handler(commands=['scanport','scaneia'])
def scan(message):
	try:
		arg = str(message.text)
		arg = arg.replace('/scan','')
		arg = arg.split(',')
		result = crawler.scan(arg[0], arg[1])
		bot.reply_to(message, result)
	except:
		bot.reply_to(message, "Sintaxe invalida!\nUse /scanport ip, argumentos")

    	
@bot.message_handler(func=lambda m : True)
def pergunta_parte2(message):
	mes = str(message.text.encode('utf-8'))
	mes = mes.lower()
	arraga = ['My Boss...', 'Calling Junior...', 'It\'s here:\n\t @Junior_PyJS', 'Sdds né?']
	arragdeath = ['My Boss is alive', 'He always back...', 'Ele só ta fazendo algo util demais pra estar aqui...', 'I miss my boss too...',]
	if 'juniu' in mes:
		bot.reply_to(message, random.choice(arraga))
	elif 'junior' in mes and 'morto' in mes:
		bot.reply_to(message, random.choice(arragdeath))
	else:
		pass
		
	
bot.polling()