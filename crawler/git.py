# -*- coding: utf-8 -*-
import urllib2
import reg
import requests
import urllib
import random
def send_git(param):
	link = 'https://github.com/search?utf8=✓&q={}'.format(param)
	header = {
	    'User-Agent': 'Mozilla/5.0',
	    
	}
	html = requests.get(link, headers = header)
	html = html.content
	tags = reg.findTags(html)
	filtrando = reg.filter('href', tags, 'dir')
	res = []
	for i in filtrando:
		if '&' in i or '.xml' in i:
			pass 
		elif '.png' in i or '?' in i:
			pass
		elif '/pricing' in i or 'features' in i:
			pass
		elif '/explore' in i:
			pass 
		else:
			compiled =  'https://github.com{}\n\n'.format(i)
			res.append(compiled)
			
	try:	
		strires = "{}\n {}\n {}\n".format(res[0], res[1], res[2])
	except IndexError:
		strires = "Argumento vazio ou invalido."
	return strires
			