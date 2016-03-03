# -*- coding: UTF-8 -*-
import lists
tags = []
preTags = []
def findTags(string):
	global tags
	global preTags
	if '<' in string:
		string = string.split('<')
		for stri in string:
			if '>' in stri:
				preTags.append(stri)
			else:
				pass
		for tag in preTags:
			if '>' in tag and tag.endswith('>'):
				tags.append(tag)
			elif '>' in tag and tag.endswith('>') == False:
				tag = tag.split('>')
				tags.append(tag[0])
			else:
				pass
		return tags
	else:
		return False
def filter(filters, arrayTags, typer):
	filtros = []
	if filters in str(arrayTags):
		for it in arrayTags:
			if filters in it:
				it = it.split(filters)
				it = it[1].split('/"')
				it = it[0].strip('=').strip('\'').replace('\"',"").split(' ')
				if typer != None:
					if typer == 'img':
						if '.jpeg' in str(it) or '.jpg' in str(it):
							if 'set=' in str(it):
								it = it[0]
								it = it.split('=')
								filtros.append(it[1])
							else:
								filtros.append(it[0])
						elif '>' in str(it) or 'jquery' in str(it):
							pass
						elif '.png' in str(it):
							if 'set=' in str(it):
								it = it[0]
								it = it.split('=')
								filtros.append(it[1])
							else:
								filtros.append(it[0])
						else:
							pass
					elif typer == 'pdf':
						if '.pdf' in str(it):
							filtros.append(it[0])
						else:
							pass
					elif typer == 'torrent':
						if 'magnet:' in str(it):
							filtros.append(it[0])
						else:
							pass
					elif typer == 'dir':
						dire = str(it[0])
						if dire.startswith('/'):
							filtros.append(it[0])
						else:
							pass
					else:
						pass
				else:
					filtros.append(it[0])
			else:
				pass
		return filtros
	else:
		return False
	

def getIn(param, val, typer):
	if param in lists.list_tags:
		tagsIn = findTags(val)
		tagR = filter(param, tagsIn, typer) 
		return tagR
	else:
		return False
