#!/usr/bin/python
# -*- encoding: utf-8 -*-
from telegram.ext import Updater, CommandHandler
import logging
import requests
import time
### Telegram Token
Token = ''
### Coinhive Private keys
SecretKeys = ['']

class CoinHive:
	def __init__(self):
		self._Token = Token
		self._Secrets = SecretKeys
		self._SiteUrl = 'https://api.coinhive.com/stats/site?secret=%s'
		self._Replys = {}
		self._Replys['help'] = ['Hello darling~','Emmmm, I am a bot for <CoinHive>.','If you want me.\n\r','1. /help : It can reply a helo text to you.','2. /gain : It can reply gains to you.','This is end ,kiss you ~Muaaa~~~']
		self._Replys['notime'] = ['I\'m sorry, Please wait for 10 seconds.']
		self._Replys['onegain'] = ['Hashes/s : %s','Total Hashes : %s','Total XMR : %s']
		self._Replys['aggregate'] = ['This is all : ','HASHES/S : %s','TOTAL HASHES : %s','PENDING PAYMENTS : %s']
		self._Replys['onegainerr'] = ['Emmm I\'m sorry this secret have a error.']
		self._Last = 0
		self._start()

	def _start(self):
		self.Boter = Updater(self._Token)
		self.Boter.dispatcher.add_handler(CommandHandler('help', self._help))
		self.Boter.dispatcher.add_handler(CommandHandler('gain', self._gain))
		self.Boter.start_polling()
		self.Boter.idle()

	def _help(self ,bot ,update):
		update.message.reply_text('\n\r'.join(self._Replys['help']))

	def _gain(self ,bot ,update):
		logging.info('/gain')
		if time.time() - self._Last < 10:
			return update.message.reply_text('\n\r'.join(self._Replys['notime']))
		Hashes = 0
		TotalHash = 0
		PendHash = 0
		for Secret in self._Secrets:
			msg = requests.get(self._SiteUrl % Secret).json()
			if not msg['success'] :
				update.message.reply_text('\n\r'.join(self._Replys['onegainerr']))
				continue
			else:
				reply = self._Replys['onegain'][:]
				reply[0] = reply[0] % int(msg['hashesPerSecond'])
				reply[1] = reply[1] % msg['hashesTotal']
				reply[2] = reply[2] % msg['xmrPending']
				Hashes += msg['hashesPerSecond']
				TotalHash += msg['hashesTotal']
				PendHash += msg['xmrPending']
				update.message.reply_text('\n\r'.join(reply))
		reply = self._Replys['aggregate']
		reply[1] = reply[1] % int(Hashes)
		reply[2] = reply[2] % TotalHash
		reply[3] = reply[3] % PendHash
		self._Last = time.time()
		return update.message.reply_text('\n\r'.join(reply))
coin = CoinHive()
