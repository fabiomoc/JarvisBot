# -*- coding: UTF-8 -*-
from datetime import datetime
import ast
import sqlite3
githubs = "https://github.com/JuniorMario/JarvisBot"
bitbucket = "https://bitbucket.org/JuniorMario/jarvisbot/src"
text_messages = {
    
    'comandos':
    	u'/commands\n'
    	u'/dolar\n'
    	u'/info\n'
    	u'/hash\n'
    	u'/google(OFF)\n'
    	u'/youtube\n'
    	u'/code\n'
    	u'/id\n'
    	u'/github\n'
    	u'/scanport\n'
    	u'/pdf\n'
    	u'/user_list\n',
    'jarvoi':
        u'It\'s me.!\n\n'
}
sessao = []
opcoes = []
opc = []

def log_erros(func, erro, mensagem):
    __CREDITOS__ = "Diego Bernades(@EXPL01T3R0) https://github.com/diego-bernardes/"
    arquivo_logs = open('Logs_de_erros.txt', 'a')
    arquivo_logs.write('''
#Erro! Função {fun} {data}
Mensagem de erro:
{log_erro}
Mensagem que originou o erro:
{mensagem}
------------------------------------'''
                  .format(fun = func, data = str(datetime.today()), log_erro = erro,
                          mensagem = str(mensagem).encode('UTF-8', errors='ignore').decode('ASCII', errors='ignore')))
        
    arquivo_logs.close()
    

def log(dados_msg):
    global msg
    msg = dados_msg
    try:
        dados_msg = ast.literal_eval(str(dados_msg).encode('UTF-8', errors='ignore').decode('ASCII', errors='ignore'))
        if dados_msg['chat']['type'] == 'private': origem = 'Mensagem Privada'
        elif dados_msg['chat']['type'] == 'group': origem = 'Grupo'
        elif dados_msg['chat']['type'] == 'supergroup': origem = 'Super Grupo'
        else: origem = dados_msg['chat']['type']
        print('''
LOG: comando recebido
Comando: {comando}
Origem: {origem}
Titulo do chat: {nomechat}
ID do chat: {chat_id}
Nome do remetente: {nome_usuario}
Username: {username}'''
              .format(comando = dados_msg['text'], origem = origem, nomechat = dados_msg['chat']['title'], chat_id = dados_msg['chat']['id'],
                        nome_usuario = dados_msg['from_user']['first_name'] + dados_msg['from_user']['last_name'] if dados_msg['from_user']['last_name'] else dados_msg['from_user']['first_name'],
                          username = dados_msg['from_user']['username']))
        dic = {'first_name':dados_msg['from_user']['first_name'], 'last_name':dados_msg['from_user']['last_name'],  'username':dados_msg['from_user']['username'], 'chat_id':dados_msg['chat']['id']}
        return dic
    except Exception as erro:
        log_erros('LOG', erro, dados_msg)
        print('\n------------------------------------\nErro na função log, consulte o arquivo logs_de_erros,', datetime.today())
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
def is_admin(msg):
    info = log(msg)
    print(info['id'])
    if info['id'] in list_adm:
        return True
    else:
        return False
def default(mensagem, comando, func):
    log_msg(mensagem)
    try:
        bot.reply_to(mensagem, consulta_grupo(comando))
    except Exception as erro:
        log_erros(func, erro, mensagem)