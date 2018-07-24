# -*- coding: utf-8 -*-

from LineAPI.linepy import *
from gtts import gTTS
from bs4 import BeautifulSoup
from datetime import datetime
from googletrans import Translator
import ast, codecs, json, os, pytz, re, random, requests, sys, time, urllib.parse

listApp = ["CHROMEOS", "DESKTOPWIN", "DESKTOPMAC", "IOSIPAD", "WIN10"]
try:
	for app in listApp:
		try:
			try:
				with open("authToken.txt", "r") as token:
					authToken = token.read()
					if not authToken:
						client = LINE()
						with open("authToken.txt","w") as token:
							token.write(client.authToken)
						continue
					client = LINE(authToken, speedThrift=False, appName="{}\t2.1.5\tUnknownCode!\t2.1.5".format(app))
				break
			except Exception as error:
				print(error)
				if error == "REVOKE":
					exit()
				elif "auth" in error:
					continue
				else:
					exit()
		except Exception as error:
			print(error)
except Exception as error:
	print(error)
with open("authToken.txt", "w") as token:
    token.write(str(client.authToken))
clientMid = client.profile.mid
clientStart = time.time()
clientPoll = OEPoll(client)

languageOpen = codecs.open("language.json","r","utf-8")
readOpen = codecs.open("read.json","r","utf-8")
settingsOpen = codecs.open("setting.json","r","utf-8")
unsendOpen = codecs.open("unsend.json","r","utf-8")

language = json.load(languageOpen)
read = json.load(readOpen)
settings = json.load(settingsOpen)
unsend = json.load(unsendOpen)

def restartBot():
	print ("[ INFO ] BOT RESETTED")
	python = sys.executable
	os.execl(python, python, *sys.argv)

def logError(text):
    client.log("[ ERROR ] {}".format(str(text)))
    tz = pytz.timezone("Asia/Makassar")
    timeNow = datetime.now(tz=tz)
    timeHours = datetime.strftime(timeNow,"(%H:%M)")
    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    inihari = datetime.now(tz=tz)
    hr = inihari.strftime('%A')
    bln = inihari.strftime('%m')
    for i in range(len(day)):
        if hr == day[i]: hasil = hari[i]
    for k in range(0, len(bulan)):
        if bln == str(k): bln = bulan[k-1]
    time = "{}, {} - {} - {} | {}".format(str(hasil), str(inihari.strftime('%d')), str(bln), str(inihari.strftime('%Y')), str(inihari.strftime('%H:%M:%S')))
    with open("errorLog.txt","a") as error:
        error.write("\n[{}] {}".format(str(time), text))

def timeChange(secs):
	mins, secs = divmod(secs,60)
	hours, mins = divmod(mins,60)
	days, hours = divmod(hours,24)
	weeks, days = divmod(days,7)
	months, weeks = divmod(weeks,4)
	text = ""
	if months != 0: text += "%02d Bulan" % (months)
	if weeks != 0: text += " %02d Minggu" % (weeks)
	if days != 0: text += " %02d Hari" % (days)
	if hours !=  0: text +=  " %02d Jam" % (hours)
	if mins != 0: text += " %02d Menit" % (mins)
	if secs != 0: text += " %02d Detik" % (secs)
	if text[0] == " ":
		text = text[1:]
	return text

def command(text):
	pesan = text.lower()
	if settings["setKey"] == True:
		if pesan.startswith(settings["keyCommand"]):
			cmd = pesan.replace(settings["keyCommand"],"")
		else:
			cmd = "Undefined command"
	else:
		cmd = text.lower()
	return cmd

def backupData():
	try:
		backup = read
		f = codecs.open('read.json','w','utf-8')
		json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
		backup = settings
		f = codecs.open('setting.json','w','utf-8')
		json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
		backup = unsend
		f = codecs.open('unsend.json','w','utf-8')
		json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
		return True
	except Exception as error:
		logError(error)
		return False

def menuHelp():
	if settings['setKey'] == True:
		key = settings['keyCommand']
	else:
		key = ''
	menuHelp =	"| • | < ʜᴇʟᴘ ᴍᴇssᴀɢᴇ >" + "\n" + \
				"| • | " + key + "ʜᴇʟᴘ" + "\n" + \
				"| • | " + key + "sᴀʏʜᴇʟᴘ" + "\n" + \
				"| • | " + key + "ᴄʀᴇᴀᴛᴏʀ" + "\n" + \
				"| • | " + key + "ʟᴏɢᴏᴜᴛ" + "\n" + \
				"| • | " + key + "ʀᴇsᴛᴀʀᴛʙᴏᴛ" + "\n" + \
				"| • | " + key + "sᴘᴇᴇᴅʙᴏᴛ" + "\n" + \
				"| • | " + key + "sᴛᴀᴛᴜsʙᴏᴛ" + "\n" + \
				"| • | " + key + "ᴜɴsᴇɴᴅᴄʜᴀᴛ [ ᴏɴ/ᴏғғ ]" + "\n" + \
				"| • | " + key + "ᴍᴇ" + "\n" + \
				"| • | " + key + "ᴍʏᴍɪᴅ" + "\n" + \
				"| • | " + key + "ᴍʏɴᴀᴍᴇ" + "\n" + \
				"| • | " + key + "ᴍʏʙɪᴏ" + "\n" + \
				"| • | " + key + "ᴍʏᴘɪᴄᴛᴜʀᴇ" + "\n" + \
				"| • | " + key + "ᴍʏᴠɪᴅᴇᴏᴘʀᴏғɪʟᴇ" + "\n" + \
				"| • | " + key + "ᴍʏᴄᴏᴠᴇʀ" + "\n" + \
				"| • | " + key + "sᴛᴀʟᴋʙɪᴏ [ ᴍᴇɴᴛɪᴏɴ ]" + "\n" + \
				"| • | " + key + "sᴛᴀʟᴋᴘɪᴄᴛᴜʀᴇ [ ᴍᴇɴᴛɪᴏɴ ]" + "\n" + \
				"| • | " + key + "sᴛᴀʟᴋᴠɪᴅᴇᴏᴘʀᴏғɪʟᴇ [ ᴍᴇɴᴛɪᴏɴ ]" + "\n" + \
				"| • | " + key + "sᴛᴀʟᴋᴄᴏᴠᴇʀ [ ᴍᴇɴᴛɪᴏɴ ]" + "\n" + \
				"| • | " + key + "ғʀɪᴇɴᴅʟɪsᴛ" + "\n" + \
				"| • | " + key + "ʙʟᴏᴄᴋʟɪsᴛ" + "\n" + \
				"| • | " + key + "ᴍᴇᴍʙᴇʀʟɪsᴛ" + "\n" + \
				"| • | " + key + "ɢʀᴏᴜᴘɪɴғᴏ" + "\n" + \
				"| • | " + key + "ᴍᴀᴄʀᴏ [ ᴏɴ/ᴏғғ ]" + "\n" + \
				"| • | " + key + "ᴍᴀᴄʀᴏʟɪsᴛ" + "\n" + \
				"| • | " + key + "ᴍᴀᴄʀᴏᴀᴅᴅ [ ᴍᴇɴᴛɪᴏɴ ]" + "\n" + \
				"| • | " + key + "ᴍᴀᴄʀᴏᴅᴇʟ[ ᴍᴇɴᴛɪᴏɴ ]" + "\n" + \
				"| • | " + key + "ᴍᴇɴᴛɪᴏɴ" + "\n" + \
				"| • | " + key + "sᴘʏʙᴏᴛ [ ᴏɴ/ᴏғғ/ʀᴇsᴇᴛ ]" + "\n" + \
				"| • | " + key + "sᴄᴀɴ" + "\n" + \
				"| • | < ᴜɴᴋɴᴏᴡɴ ᴄᴏᴅᴇ >"
	return menuHelp

def displayCreator():
	if settings['setKey'] == True:
		key = settings['keyCommand']
	else:
		key = ''
	displayCreator =	"| • | < ᴀʙᴏᴜᴛ ʙᴏᴛ >" + "\n" + \
				"| • | " + key + "ᴀᴜᴛʜᴏʀ : ᴅᴡɪᴡɪʀᴀɴᴀᴛʜᴀ" + "\n" + \
				"| • | " + key + "ᴇᴍᴀɪʟ : dwiwiranatha@gmail.com" + "\n" + \
				"| • | " + key + "ʏᴛ ᴄʜᴀɴɴᴇʟ : bit.ly/2uzmcGy" + "\n" + \
				"| • | " + key + "ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ : line.me/ti/p/CmNvfCneIG" + "\n" + \
				"| • | < ᴜɴᴋɴᴏᴡɴ ᴄᴏᴅᴇ >"
	return displayCreator

def menuTextToSpeech():
	if settings['setKey'] == True:
		key = settings['keyCommand']
	else:
		key = ''
	menuTextToSpeech = "| • | < ᴛᴇxᴛ ᴛᴏ sᴘᴇᴇᴄʜ >" + "\n" + \
                        		"| • | " + key + "ɪᴅ : ɪɴᴅᴏɴᴇsɪᴀ" + "\n" + \
                       	 		"| • | " + key + "ᴇɴ : ᴇɴɢʟɪsʜ" + "\n" + \
                       			"| • | " + key + "ᴊᴀ : ᴊᴀᴘᴀɴᴇsᴇ" + "\n" + \
                        		"| • | " + key + "ᴋᴏ : ᴋᴏʀᴇᴀɴ" + "\n" + \
                        		"| • | " + key + "ᴛʜ : ᴛʜᴀɪʟᴀɴᴅ" + "\n" + \
                        		"| • | " + key + "ᴢʜ : ᴄʜɪɴᴀ" + "\n" + \
                        		"ᴇxᴀᴍᴘʟᴇ : " + key + "/sᴀʏ-ɪᴅ ᴅᴡɪᴡɪʀᴀɴᴀᴛʜᴀ"
	return menuTextToSpeech

def clientBot(op):
	try:
		if op.type == 0:
			print ("[ 0 ] END OF OPERATION")
			return

		if op.type == 5:
			print ("[ 5 ] NOTIFIED ADD CONTACT")
			if settings["autoAdd"] == True:
				client.findAndAddContactsByMid(op.param1)
			client.sendMention(op.param1, settings["autoAddMessage"], [op.param1])

		if op.type == 13:
			print ("[ 13 ] NOTIFIED INVITE INTO GROUP")
			if settings["autoJoin"] and clientMid in op.param3:
				client.acceptGroupInvitation(op.param1)
				client.sendMention(op.param1, settings["autoJoinMessage"], [op.param2])

		if op.type == 25:
			try:
				print("[ 25 ] SEND MESSAGE")
				msg = op.message
				text = str(msg.text)
				msg_id = msg.id
				receiver = msg.to
				sender = msg._from
				cmd = command(text)
				setKey = settings["keyCommand"].title()
				if settings["setKey"] == False:
					setKey = ''
				if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
					if msg.toType == 0:
						if sender != client.profile.mid:
							to = sender
						else:
							to = receiver
					elif msg.toType == 1:
						to = receiver
					elif msg.toType == 2:
						to = receiver
					if msg.contentType == 0:
						if cmd == "logout":
							client.sendMessage(to, "sʜᴜᴛᴛɪɴɢ ᴅᴏᴡɴ . . .")
							client.sendMessage(to, "ᴜsᴇʀ ʟᴏɢᴏғғ")
							sys.exit("[ INFO ] BOT SHUTDOWN")
							return
						elif cmd == "restartbot":
							client.sendMessage(to, "ʀᴇsᴛᴀʀᴛɪɴɢ . . .")
							client.sendMessage(to, "ʀᴇsᴛᴀʀᴛ sᴜᴄᴄᴇssғᴜʟ (ᴛʏᴘᴇ=ᴀ)")
							restartBot()
						elif cmd == "speedbot":
							start = time.time()
							client.sendMessage(to, "ᴄᴏɴɴᴇᴄᴛɪɴɢ . . .")
							elapsed_time = time.time() - start
							client.sendMessage(to, "sᴇɴᴅɪɴɢ ᴍᴇssᴀɢᴇs {}/s".format(str(elapsed_time)))
						elif cmd == "creator":
							aboutCreator = displayCreator()
							contact = client.getContact(sender)
							icon = "https://cdn.icon-icons.com/icons2/909/PNG/512/code_icon-icons.com_70999.png"
							name = "dwiwiranatha ηF"
							link = "https://line.me/ti/p/CmNvfCneIG"
							client.sendFooter(to, aboutCreator, icon, name, link)
						elif cmd == "help":
							helpMessage = menuHelp()
							contact = client.getContact(sender)
							icon = "https://cdn.icon-icons.com/icons2/909/PNG/512/code_icon-icons.com_70999.png"
							name = "dwiwiranatha ηF"
							link = "https://line.me/ti/p/CmNvfCneIG"
							client.sendFooter(to, helpMessage, icon, name, link)
						elif cmd == "sayhelp":
							helpTextToSpeech = menuTextToSpeech()
							contact = client.getContact(sender)
							icon = "https://cdn.icon-icons.com/icons2/909/PNG/512/code_icon-icons.com_70999.png"
							name = "dwiwiranatha ηF"
							link = "https://line.me/ti/p/CmNvfCneIG"
							client.sendFooter(to, helpTextToSpeech, icon, name, link)

						elif cmd == "statusbot":
							try:
								icon = "https://cdn.icon-icons.com/icons2/909/PNG/512/code_icon-icons.com_70999.png"
								name = "dwiwiranatha ηF"
								link = "https://line.me/ti/p/CmNvfCneIG"
								ret_ = "| • | < sᴛᴀᴛᴜs ʙᴏᴛ >"
								if settings["detectUnsend"] == True: ret_ += "\n| • | ᴜɴsᴇɴᴅᴄʜᴀᴛ : ᴏɴ"
								else: ret_ += "\n| • | ᴜɴsᴇɴᴅᴄʜᴀᴛ : ᴏғғ"
								if settings["mimic"]["status"] == True: ret_ += "\n| • | ᴍᴀᴄʀᴏ : ᴏɴ"
								else: ret_ += "\n| • | ᴍᴀᴄʀᴏ : ᴏғғ"
								if settings["mimic"]["target"] == {}: ret_ += "\n| • | ᴍᴀᴄʀᴏʟɪsᴛ : ᴛᴀʀɢᴇᴛ ɴᴏᴛ ғᴏᴜɴᴅ"
								else: 
									no = 0
									ret_ = "| • | < ᴍᴀᴄʀᴏ ʟɪsᴛ >"
									target = []
									for mid in settings["mimic"]["target"]:
										target.append(mid)
										no += 1
										ret_ += "\n| • | {}. @!".format(no)
									ret_ += "\n| • | ᴛᴏᴛᴀʟ {} ᴍᴀᴄʀᴏ".format(str(len(target)))
								client.sendFooter(to, ret_, icon, name, link)
							except Exception as error:
								logError(error)
						elif cmd == "unsendchat on":
							if settings["detectUnsend"] == True:
								client.sendMessage(to, "ᴅᴇᴛᴇᴄᴛ ᴜɴsᴇɴᴅ ɪs ᴇɴᴀʙʟᴇ")
							else:
								settings["detectUnsend"] = True
								client.sendMessage(to, "sᴜᴄᴄᴇssғᴜʟʟʏ ᴇɴᴀʙʟᴇ ᴅᴇᴛᴇᴄᴛ ᴜɴsᴇɴᴅ")
						elif cmd == "unsendchat off":
							if settings["detectUnsend"] == False:
								client.sendMessage(to, "ᴅᴇᴛᴇᴄᴛ ᴜɴsᴇɴᴅ ɪs ᴅɪsᴀʙʟᴇ")
							else:
								settings["detectUnsend"] = False
								client.sendMessage(to, "sᴜᴄᴄᴇssғᴜʟʟʏ ᴅɪsᴀʙʟᴇ ᴅᴇᴛᴇᴄᴛ ᴜɴsᴇɴᴅ")
						elif cmd == "me":
							client.sendMention(to, "@!", [sender])
							client.sendContact(to, sender)
						elif cmd == "mymid":
							contact = client.getContact(sender)
							client.sendMention(to, "@!: {}".format(contact.mid), [sender])
						elif cmd == "myname":
							contact = client.getContact(sender)
							client.sendMention(to, "@!: {}".format(contact.displayName), [sender])
						elif cmd == "mybio":
							contact = client.getContact(sender)
							client.sendMention(to, "@!: {}".format(contact.statusMessage), [sender])
						elif cmd == "mypicture":
							contact = client.getContact(sender)
							client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus))
						elif cmd == "myvideoprofile":
							contact = client.getContact(sender)
							if contact.videoProfile == None:
								return client.sendMessage(to, "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀ ᴠɪᴅᴇᴏ ᴘʀᴏғɪʟᴇ")
							client.sendVideoWithURL(to, "http://dl.profile.line-cdn.net/{}/vp".format(contact.pictureStatus))
						elif cmd == "mycover":
							cover = client.getProfileCoverURL(sender)
							client.sendImageWithURL(to, str(cover))
						elif cmd.startswith("mid "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									client.sendMention(to, "@!: {}".format(ls), [ls])
						elif cmd.startswith("stalkbio "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									contact = client.getContact(ls)
									client.sendMention(to, "@!: {}".format(contact.statusMessage), [ls])
						elif cmd.startswith("stalkpicture "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									contact = client.getContact(ls)
									client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus))
						elif cmd.startswith("stalkvideoprofile "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									contact = client.getContact(ls)
									if contact.videoProfile == None:
										return client.sendMention(to, "@!ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀ ᴠɪᴅᴇᴏ ᴘʀᴏғɪʟᴇ", [ls])
									client.sendVideoWithURL(to, "http://dl.profile.line-cdn.net/{}/vp".format(contact.pictureStatus))
						elif cmd.startswith("stalkcover "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									cover = client.getProfileCoverURL(ls)
									client.sendImageWithURL(to, str(cover))
						elif cmd == "friendlist":
							contacts = client.getAllContactIds()
							num = 0
							result = "| • | < ғʀɪᴇɴᴅ ʟɪsᴛ >"
							for listContact in contacts:
								contact = client.getContact(listContact)
								num += 1
								result += "\n| • | {}. {}".format(num, contact.displayName)
							result += "\n| • | ᴛᴏᴛᴀʟ {} ғʀɪᴇɴᴅ".format(len(contacts))
							client.sendMessage(to, result)
						elif cmd == "blocklist":
							blockeds = client.getBlockedContactIds()
							num = 0
							result = "| • | < ʙʟᴏᴄᴋᴇᴅ ʟɪsᴛ >"
							for listBlocked in blockeds:
								contact = client.getContact(listBlocked)
								num += 1
								result += "\n| • | {}. {}".format(num, contact.displayName)
							result += "\n| • | ᴛᴏᴛᴀʟ {} ʙʟᴏᴄᴋᴇᴅ ]".format(len(blockeds))
							client.sendMessage(to, result)

						elif cmd == "openqr":
							if msg.toType == 2:
								group = client.getGroup(to)
								group.preventedJoinByTicket = False
								client.updateGroup(group)
								groupUrl = client.reissueGroupTicket(to)
								client.sendMessage(to, "ǫʀ ɢʀᴏᴜᴘ\n\nᴜʀʟ : line://ti/g/{}".format(groupUrl))
						elif cmd == "closeqr":
							if msg.toType == 2:
								group = client.getGroup(to)
								group.preventedJoinByTicket = True
								client.updateGroup(group)
								client.sendMessage(to, "ǫʀ ɢʀᴏᴜᴘ ᴄʟᴏsᴇᴅ")
						elif cmd == "memberlist":
							if msg.toType == 2:
								group = client.getGroup(to)
								num = 0
								ret_ = "| • | < ᴍᴇᴍʙᴇʀ ʟɪsᴛ >"
								for contact in group.members:
									num += 1
									ret_ += "\n| • | {}. {}".format(num, contact.displayName)
								ret_ += "\n| • | ᴛᴏᴛᴀʟ {} ᴍᴇᴍʙᴇʀ".format(len(group.members))
								client.sendMessage(to, ret_)
						elif cmd == "groupinfo":
							group = client.getGroup(to)
							try:
								try:
									groupCreator = group.creator.mid
								except:
									groupCreator = "ɴᴏᴛ ғᴏᴜɴᴅ"
								if group.invitee is None:
									groupPending = "0"
								else:
									groupPending = str(len(group.invitee))
								if group.preventedJoinByTicket == True:
									groupQr = "ᴄʟᴏsᴇᴅ"
								else:
									groupQr = "ᴏᴘᴇɴ"
								ret_ = "| • | < ɢʀᴏᴜᴘ ɪɴғᴏʀᴍᴀᴛɪᴏɴ >"
								ret_ += "\n| • | ɢʀᴏᴜᴘ ɴᴀᴍᴇ : {}".format(group.name)
								ret_ += "\n| • | ɢʀᴏᴜᴘ ᴄʀᴇᴀᴛᴏʀ : @!"
								ret_ += "\n| • | ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀ : {}".format(str(len(group.members)))
								ret_ += "\n| • | ᴛᴏᴛᴀʟ ᴘᴇɴᴅɪɴɢ : {}".format(groupPending)
								ret_ += "\n| • | ǫʀ ɢʀᴏᴜᴘ : {}".format(groupQr)
								client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(group.pictureStatus))
								client.sendMention(to, str(ret_), [groupCreator])
							except:
								ret_ = "| • | < ɢʀᴏᴜᴘ ɪɴғᴏʀᴍᴀᴛɪᴏɴ >"
								ret_ += "\n| • | ɢʀᴏᴜᴘ ɴᴀᴍᴇ : {}".format(group.name)
								ret_ += "\n| • | ɢʀᴏᴜᴘ ᴄʀᴇᴀᴛᴏʀ : {}".format(groupCreator)
								ret_ += "\n| • | ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀ : {}".format(str(len(group.members)))
								ret_ += "\n| • | ᴛᴏᴛᴀʟ ᴘᴇɴᴅɪɴɢ : {}".format(groupPending)
								ret_ += "\n| • | ǫʀ ɢʀᴏᴜᴘ : {}".format(groupQr)
								client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(group.pictureStatus))
								client.sendMessage(to, str(ret_))

						elif cmd == 'mention':
							group = client.getGroup(to)
							midMembers = [contact.mid for contact in group.members]
							midSelect = len(midMembers)//100
							for mentionMembers in range(midSelect+1):
								no = 0
								ret_ = "| • | < ᴍᴇɴᴛɪᴏɴ ᴍᴇᴍʙᴇʀs >"
								dataMid = []
								for dataMention in group.members[mentionMembers*100 : (mentionMembers+1)*100]:
									dataMid.append(dataMention.mid)
									no += 1
									ret_ += "\n| • | {}. @!".format(str(no))
								ret_ += "\n| • | ᴛᴏᴛᴀʟ {} ᴍᴇɴᴛɪᴏɴ".format(str(len(dataMid)))
								client.sendMention(to, ret_, dataMid)
						elif cmd == "spybot on":
							tz = pytz.timezone("Asia/Makassar")
							timeNow = datetime.now(tz=tz)
							day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
							hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
							bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
							hr = timeNow.strftime("%A")
							bln = timeNow.strftime("%m")
							for i in range(len(day)):
								if hr == day[i]: hasil = hari[i]
							for k in range(0, len(bulan)):
								if bln == str(k): bln = bulan[k-1]
							readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nᴛɪᴍᴇ : [ " + timeNow.strftime('%H:%M:%S') + " ]"
							if to in read['readPoint']:
								try:
									del read['readPoint'][to]
									del read['readMember'][to]
								except:
									pass
								read['readPoint'][to] = msg_id
								read['readMember'][to] = []
								client.sendMessage(to, "sᴜᴄᴄᴇssғᴜʟʟʏ ᴇɴᴀʙʟᴇ sᴘʏʙᴏᴛ")
							else:
								try:
									del read['readPoint'][to]
									del read['readMember'][to]
								except:
									pass
								read['readPoint'][to] = msg_id
								read['readMember'][to] = []
								client.sendMessage(to, "sᴇᴛ ʀᴇᴀᴅɪɴɢ ᴘᴏɪɴᴛ : \n{}".format(readTime))
						elif cmd == "spybot off":
							tz = pytz.timezone("Asia/Makassar")
							timeNow = datetime.now(tz=tz)
							day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
							hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
							bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
							hr = timeNow.strftime("%A")
							bln = timeNow.strftime("%m")
							for i in range(len(day)):
								if hr == day[i]: hasil = hari[i]
							for k in range(0, len(bulan)):
								if bln == str(k): bln = bulan[k-1]
							readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nᴛɪᴍᴇ : [ " + timeNow.strftime('%H:%M:%S') + " ]"
							if to not in read['readPoint']:
								client.sendMessage(to,"sᴜᴄᴄᴇssғᴜʟʟʏ ᴅɪsᴀʙʟᴇ sᴘʏʙᴏᴛ")
							else:
								try:
									del read['readPoint'][to]
									del read['readMember'][to]
								except:
									pass
								client.sendMessage(to, "ᴅᴇʟᴇᴛᴇ ʀᴇᴀᴅɪɴɢ ᴘᴏɪɴᴛ : \n{}".format(readTime))
						elif cmd == "scan":
							if to in read['readPoint']:
								if read["readMember"][to] == []:
									return client.sendMessage(to, "sɪʟᴇɴᴛ ʀᴇᴀᴅᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ")
								else:
									no = 0
									result = "| • | < ʀᴇᴀᴅᴇʀ >"
									for dataRead in read["readMember"][to]:
										no += 1
										result += "\n| • | {}. @!".format(str(no))
									result += "\n| • | ᴛᴏᴛᴀʟ {} ʀᴇᴀᴅᴇʀ".format(str(len(read["readMember"][to])))
									client.sendMention(to, result, read["readMember"][to])
									read['readMember'][to] = []
						elif cmd == "changepictureprofile":
							settings["changePictureProfile"] = True
							client.sendMessage(to, "ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴛʜᴇ ᴘɪᴄᴛᴜʀᴇ")
						elif cmd == "changegrouppicture":
							if msg.toType == 2:
								if to not in settings["changeGroupPicture"]:
									settings["changeGroupPicture"].append(to)
								client.sendMessage(to, "ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴛʜᴇ ᴘɪᴄᴛᴜʀᴇ")
						elif cmd == "macro on":
							if settings["mimic"]["status"] == True:
								client.sendMessage(to, "ʀᴇᴘʟʏ ᴍᴇssᴀɢᴇ ɪs ᴇɴᴀʙʟᴇ")
							else:
								settings["mimic"]["status"] = True
								client.sendMessage(to, "sᴜᴄᴄᴇssғᴜʟʟʏ ᴇɴᴀʙʟᴇ ʀᴇᴘʟʏ ᴍᴇssᴀɢᴇ")
						elif cmd == "macro off":
							if settings["mimic"]["status"] == False:
								client.sendMessage(to, "ʀᴇᴘʟʏ ᴍᴇssᴀɢᴇ ɪs ᴅɪsᴀʙʟᴇ")
							else:
								settings["mimic"]["status"] = False
								client.sendMessage(to, "sᴜᴄᴄᴇssғᴜʟʟʏ ᴅɪsᴀʙʟᴇ ʀᴇᴘʟʏ ᴍᴇssᴀɢᴇ")
						elif cmd == "macrolist":
							if settings["mimic"]["target"] == {}:
								client.sendMessage(to, "ᴛᴀʀɢᴇᴛ ɴᴏᴛ ғᴏᴜɴᴅ")
							else:
								no = 0
								ret_ = "| • | < ᴍᴀᴄʀᴏ ʟɪsᴛ >"
								target = []
								for mid in settings["mimic"]["target"]:
									target.append(mid)
									no += 1
									result += "\n| • | {}. @!".format(no)
								result += "\n| • | ᴛᴏᴛᴀʟ {} ᴍᴀᴄʀᴏ".format(str(len(target)))
								client.sendMention(to, result, target)
						elif cmd.startswith("macroadd "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									try:
										if ls in settings["mimic"]["target"]:
											client.sendMessage(to, "ᴛʜᴇ ᴛᴀʀɢᴇᴛ ɪs ᴀʟʀᴇᴀᴅʏ ɪɴ ᴛʜᴇ ʟɪsᴛ")
										else:
											settings["mimic"]["target"][ls] = True
											client.sendMessage(to, "ᴀᴅᴅᴇᴅ ᴛᴀʀɢᴇᴛ sᴜᴄᴄᴇssғᴜʟ")
									except:
										client.sendMessage(to, "ᴀᴅᴅᴇᴅ ᴛᴀʀɢᴇᴛ ғᴀɪʟᴇᴅ")
						elif cmd.startswith("macrodel "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									try:
										if ls not in settings["mimic"]["target"]:
											client.sendMessage(to, "ᴛᴀʀɢᴇᴛ ɪs ᴏᴜᴛ ᴏғ ᴛʜᴇ ʟɪsᴛ")
										else:
											del settings["mimic"]["target"][ls]
											client.sendMessage(to, "ᴅᴇʟᴇᴛᴇ ᴛᴀʀɢᴇᴛ sᴜᴄᴄᴇssғᴜʟ")
									except:
										client.sendMessage(to, "ғᴀɪʟᴇᴅ ᴀᴅᴅᴇᴅ ᴛᴀʀɢᴇᴛ")


						elif cmd.startswith("/instainfo"):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							url = requests.get("http://rahandiapi.herokuapp.com/instainfo/{}?key=betakey".format(txt))
							data = url.json()
							icon = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/599px-Instagram_icon.png"
							name = "Instagram"
							link = "https://www.instagram.com/{}".format(data["result"]["username"])
							result = "╔══[ Instagram Info ]"
							result += "\n╠ Name : {}".format(data["result"]["name"])
							result += "\n╠ Username: {}".format(data["result"]["username"])
							result += "\n╠ Bio : {}".format(data["result"]["bio"])
							result += "\n╠ Follower : {}".format(data["result"]["follower"])
							result += "\n╠ Following : {}".format(data["result"]["following"])
							result += "\n╠ Private : {}".format(data["result"]["private"])
							result += "\n╠ Post : {}".format(data["result"]["mediacount"])
							result += "\n╚══[ Finish ]"
							client.sendImageWithURL(to, data["result"]["url"])
							client.sendFooter(to, result, icon, name, link)
						elif cmd.startswith("/instastory "):
							sep = text.split(" ")
							query = text.replace(sep[0] + " ","")
							cond = query.split("|")
							search = str(cond[0])
							if len(cond) == 2:
								url = requests.get("http://rahandiapi.herokuapp.com/instastory/{}?key=betakey".format(search))
								data = url.json()
								num = int(cond[1])
								if num <= len(data["url"]):
									search = data["url"][num - 1]
									if search["tipe"] == 1:
										client.sendImageWithURL(to, str(search["link"]))
									elif search["tipe"] == 2:
										client.sendVideoWithURL(to, str(search["link"]))
						elif cmd == "/quotes":
							url = requests.get("https://botfamily.faith/api/quotes/?apikey=beta")
							data = url.json()
							result = "╔══[ Quotes ]"
							result += "\n╠ Author : {}".format(data["result"]["author"])
							result += "\n╠ Category : {}".format(data["result"]["category"])
							result += "\n╠ Quote : {}".format(data["result"]["quote"])
							result += "\n╚══[ Finish ]"
							client.sendMessage(to, result)
						elif cmd.startswith("/say-"):
							sep = text.split("-")
							sep = sep[1].split(" ")
							lang = sep[0]
							if settings["setKey"] == False:
								txt = text.lower().replace("say-" + lang + " ","")
							else:
								txt = text.lower().replace(settings["keyCommand"] + "say-" + lang + " ","")
							if lang not in language["gtts"]:
								return client.sendMessage(to, "ʟᴀɴɢᴜᴀɢᴇ {} ɴᴏᴛ ғᴏᴜɴᴅ".format(lang))
							tts = gTTS(text=txt, lang=lang)
							tts.save("line/tmp/tts-{}.mp3".format(lang))
							client.sendAudio(to, "line/tmp/tts-{}.mp3".format(lang))
							client.deleteFile("line/tmp/tts-{}.mp3".format(lang))
						elif cmd.startswith("/searchyoutube "):
							sep = text.split(" ")
							txt = msg.text.replace(sep[0] + " ","")
							cond = txt.split("|")
							search = cond[0]
							url = requests.get("http://api.w3hills.com/youtube/search?keyword={}&api_key=86A7FCF3-6CAF-DEB9-E214-B74BDB835B5B".format(search))
							data = url.json()
							if len(cond) == 1:
								no = 0
								result = "╔══[ Youtube Search ]"
								for anu in data["videos"]:
									no += 1
									result += "\n╠ {}. {}".format(str(no),str(anu["title"]))
								result += "\n╚══[ Total {} Result ]".format(str(len(data["videos"])))
								client.sendMessage(to, result)
							elif len(cond) == 2:
								num = int(str(cond[1]))
								if num <= len(data):
									search = data["videos"][num - 1]
									ret_ = "╔══[ Youtube Info ]"
									ret_ += "\n╠ Channel : {}".format(str(search["publish"]["owner"]))
									ret_ += "\n╠ Title : {}".format(str(search["title"]))
									ret_ += "\n╠ Release : {}".format(str(search["publish"]["date"]))
									ret_ += "\n╠ Viewers : {}".format(str(search["stats"]["views"]))
									ret_ += "\n╠ Likes : {}".format(str(search["stats"]["likes"]))
									ret_ += "\n╠ Dislikes : {}".format(str(search["stats"]["dislikes"]))
									ret_ += "\n╠ Rating : {}".format(str(search["stats"]["rating"]))
									ret_ += "\n╠ Description : {}".format(str(search["description"]))
									ret_ += "\n╚══[ {} ]".format(str(search["webpage"]))
									client.sendImageWithURL(to, str(search["thumbnail"]))
									client.sendMessage(to, str(ret_))
						elif cmd.startswith("/searchimage "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							url = requests.get("http://rahandiapi.herokuapp.com/imageapi?key=betakey&q={}".format(txt))
							data = url.json()
							client.sendImageWithURL(to, random.choice(data["result"]))
						elif cmd.startswith("/searchmusic "):
							sep = text.split(" ")
							query = text.replace(sep[0] + " ","")
							cond = query.split("|")
							search = str(cond[0])
							url = requests.get("http://api.ntcorp.us/joox/search?q={}".format(str(search)))
							data = url.json()
							if len(cond) == 1:
								num = 0
								ret_ = "╔══[ Result Music ]"
								for music in data["result"]:
									num += 1
									ret_ += "\n╠ {}. {}".format(str(num), str(music["single"]))
								ret_ += "\n╚══[ Total {} Music ]".format(str(len(data["result"])))
								ret_ += "\n\nUntuk mengirim music, silahkan gunakan command {}SearchMusic {}|「number」".format(str(setKey), str(search))
								client.sendMessage(to, str(ret_))
							elif len(cond) == 2:
								num = int(cond[1])
								if num <= len(data["result"]):
									music = data["result"][num - 1]
									url = requests.get("http://api.ntcorp.us/joox/song_info?sid={}".format(str(music["sid"])))
									data = url.json()
									ret_ = "╔══[ Music ]"
									ret_ += "\n╠ Title : {}".format(str(data["result"]["song"]))
									ret_ += "\n╠ Album : {}".format(str(data["result"]["album"]))
									ret_ += "\n╠ Size : {}".format(str(data["result"]["size"]))
									ret_ += "\n╠ Link : {}".format(str(data["result"]["mp3"][0]))
									ret_ += "\n╚══[ Finish ]"
									client.sendImageWithURL(to, str(data["result"]["img"]))
									client.sendMessage(to, str(ret_))
									client.sendAudioWithURL(to, str(data["result"]["mp3"][0]))
						elif cmd.startswith("/searchlyric "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							cond = txt.split("|")
							query = cond[0]
							with requests.session() as web:
								web.headers["user-agent"] = "Mozilla/5.0"
								url = web.get("https://www.musixmatch.com/search/{}".format(urllib.parse.quote(query)))
								data = BeautifulSoup(url.content, "html.parser")
								result = []
								for trackList in data.findAll("ul", {"class":"tracks list"}):
									for urlList in trackList.findAll("a"):
										title = urlList.text
										url = urlList["href"]
										result.append({"title": title, "url": url})
								if len(cond) == 1:
									ret_ = "╔══[ Musixmatch Result ]"
									num = 0
									for title in result:
										num += 1
										ret_ += "\n╠ {}. {}".format(str(num), str(title["title"]))
									ret_ += "\n╚══[ Total {} Lyric ]".format(str(len(result)))
									ret_ += "\n\nUntuk melihat lyric, silahkan gunakan command {}SearchLyric {}|「number」".format(str(setKey), str(query))
									client.sendMessage(to, ret_)
								elif len(cond) == 2:
									num = int(cond[1])
									if num <= len(result):
										data = result[num - 1]
										with requests.session() as web:
											web.headers["user-agent"] = "Mozilla/5.0"
											url = web.get("https://www.musixmatch.com{}".format(urllib.parse.quote(data["url"])))
											data = BeautifulSoup(url.content, "html5lib")
											for lyricContent in data.findAll("p", {"class":"mxm-lyrics__content "}):
												lyric = lyricContent.text
												client.sendMessage(to, lyric)
						elif cmd.startswith("/tr-"):
							sep = text.split("-")
							sep = sep[1].split(" ")
							lang = sep[0]
							if settings["setKey"] == False:
								txt = text.lower().replace("tr-" + lang + " ","")
							else:
								txt = text.lower().replace(settings["keyCommand"] + "tr-" + lang + " ","")
							if lang not in language["googletrans"]:
								return client.sendMessage(to, "Bahasa {} tidak ditemukan".format(lang))
							translator = Translator()
							result = translator.translate(txt, dest=lang)
							client.sendMessage(to, result.text)
						if text.lower() == "mykey":
							client.sendMessage(to, "Keycommand yang diset saat ini : 「{}」".format(str(settings["keyCommand"])))
						elif text.lower() == "setkey on":
							if settings["setKey"] == True:
								client.sendMessage(to, "Setkey telah aktif")
							else:
								settings["setKey"] = True
								client.sendMessage(to, "Berhasil mengaktifkan setkey")
						elif text.lower() == "setkey off":
							if settings["setKey"] == False:
								client.sendMessage(to, "Setkey telah nonaktif")
							else:
								settings["setKey"] = False
								client.sendMessage(to, "Berhasil menonaktifkan setkey")
						if text is None: return
						if "/ti/g/" in msg.text.lower():
							if settings["autoJoinTicket"] == True:
								link_re = re.compile('(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?')
								links = link_re.findall(text)
								n_links = []
								for l in links:
									if l not in n_links:
										n_links.append(l)
								for ticket_id in n_links:
									group = client.findGroupByTicket(ticket_id)
									client.acceptGroupInvitationByTicket(group.id,ticket_id)
									client.sendMessage(to, "Berhasil masuk ke group %s" % str(group.name))
					elif msg.contentType == 1:
						if settings["changePictureProfile"] == True:
							path = client.downloadObjectMsg(msg_id, saveAs="LineAPI/tmp/{}-cpp.bin".format(time.time()))
							settings["changePictureProfile"] = False
							client.updateProfilePicture(path)
							client.sendMessage(to, "Berhasil mengubah foto profile")
							client.deleteFile(path)
						if msg.toType == 2:
							if to in settings["changeGroupPicture"]:
								path = client.downloadObjectMsg(msg_id, saveAs="LineAPI/tmp/{}-cgp.bin".format(time.time()))
								settings["changeGroupPicture"].remove(to)
								client.updateGroupPicture(to, path)
								client.sendMessage(to, "Berhasil mengubah foto group")
								client.deleteFile(path)
					elif msg.contentType == 7:
						if settings["checkSticker"] == True:
							stk_id = msg.contentMetadata['STKID']
							stk_ver = msg.contentMetadata['STKVER']
							pkg_id = msg.contentMetadata['STKPKGID']
							ret_ = "╔══[ Sticker Info ]"
							ret_ += "\n╠ STICKER ID : {}".format(stk_id)
							ret_ += "\n╠ STICKER PACKAGES ID : {}".format(pkg_id)
							ret_ += "\n╠ STICKER VERSION : {}".format(stk_ver)
							ret_ += "\n╠ STICKER URL : line://shop/detail/{}".format(pkg_id)
							ret_ += "\n╚══[ Finish ]"
							client.sendMessage(to, str(ret_))
					elif msg.contentType == 13:
						if settings["checkContact"] == True:
							try:
								contact = client.getContact(msg.contentMetadata["mid"])
								cover = client.getProfileCoverURL(msg.contentMetadata["mid"])
								ret_ = "╔══[ Details Contact ]"
								ret_ += "\n╠ Nama : {}".format(str(contact.displayName))
								ret_ += "\n╠ MID : {}".format(str(msg.contentMetadata["mid"]))
								ret_ += "\n╠ Bio : {}".format(str(contact.statusMessage))
								ret_ += "\n╠ Gambar Profile : http://dl.profile.line-cdn.net/{}".format(str(contact.pictureStatus))
								ret_ += "\n╠ Gambar Cover : {}".format(str(cover))
								ret_ += "\n╚══[ Finish ]"
								client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(str(contact.pictureStatus)))
								client.sendMessage(to, str(ret_))
							except:
								client.sendMessage(to, "Kontak tidak valid")
					elif msg.contentType == 16:
						if settings["checkPost"] == True:
							try:
								ret_ = "╔══[ Details Post ]"
								if msg.contentMetadata["serviceType"] == "GB":
									contact = client.getContact(sender)
									auth = "\n╠ Penulis : {}".format(str(contact.displayName))
								else:
									auth = "\n╠ Penulis : {}".format(str(msg.contentMetadata["serviceName"]))
								purl = "\n╠ URL : {}".format(str(msg.contentMetadata["postEndUrl"]).replace("line://","https://line.me/R/"))
								ret_ += auth
								ret_ += purl
								if "mediaOid" in msg.contentMetadata:
									object_ = msg.contentMetadata["mediaOid"].replace("svc=myhome|sid=h|","")
									if msg.contentMetadata["mediaType"] == "V":
										if msg.contentMetadata["serviceType"] == "GB":
											ourl = "\n╠ Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(msg.contentMetadata["mediaOid"]))
											murl = "\n╠ Media URL : https://obs-us.line-apps.com/myhome/h/download.nhn?{}".format(str(msg.contentMetadata["mediaOid"]))
										else:
											ourl = "\n╠ Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(object_))
											murl = "\n╠ Media URL : https://obs-us.line-apps.com/myhome/h/download.nhn?{}".format(str(object_))
										ret_ += murl
									else:
										if msg.contentMetadata["serviceType"] == "GB":
											ourl = "\n╠ Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(msg.contentMetadata["mediaOid"]))
										else:
											ourl = "\n╠ Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(object_))
									ret_ += ourl
								if "stickerId" in msg.contentMetadata:
									stck = "\n╠ Stiker : https://line.me/R/shop/detail/{}".format(str(msg.contentMetadata["packageId"]))
									ret_ += stck
								if "text" in msg.contentMetadata:
									text = "\n╠ Tulisan : {}".format(str(msg.contentMetadata["text"]))
									ret_ += text
								ret_ += "\n╚══[ Finish ]"
								client.sendMessage(to, str(ret_))
							except:
								client.sendMessage(to, "Post tidak valid")
			except Exception as error:
				logError(error)


		if op.type == 26:
			try:
				print("[ 26 ] RECEIVE MESSAGE")
				msg = op.message
				text = str(msg.text)
				msg_id = msg.id
				receiver = msg.to
				sender = msg._from
				if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
					if msg.toType == 0:
						if sender != client.profile.mid:
							to = sender
						else:
							to = receiver
					elif msg.toType == 1:
						to = receiver
					elif msg.toType == 2:
						to = receiver
					if sender in settings["mimic"]["target"] and settings["mimic"]["status"] == True and settings["mimic"]["target"][sender] == True:
						if msg.contentType == 0:
							client.sendMessage(to, text)
						elif msg.contentType == 1:
							path = client.downloadObjectMsg(msg_id, saveAs="LineAPI/tmp/{}-mimic.bin".format(time.time()))
							client.sendImage(to, path)
							client.deleteFile(path)
					if msg.contentType == 0:
						if settings["autoRead"] == True:
							client.sendChatChecked(to, msg_id)
						if sender not in clientMid:
							if msg.toType != 0 and msg.toType == 2:
								if 'MENTION' in msg.contentMetadata.keys()!= None:
									names = re.findall(r'@(\w+)', text)
									mention = ast.literal_eval(msg.contentMetadata['MENTION'])
									mentionees = mention['MENTIONEES']
									for mention in mentionees:
										if clientMid in mention["M"]:
											if settings["autoRespon"] == True:
												client.sendMention(sender, settings["autoResponMessage"], [sender])
											break
						if text is None: return
						if "/ti/g/" in msg.text.lower():
							if settings["autoJoinTicket"] == True:
								link_re = re.compile('(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?')
								links = link_re.findall(text)
								n_links = []
								for l in links:
									if l not in n_links:
										n_links.append(l)
								for ticket_id in n_links:
									group = client.findGroupByTicket(ticket_id)
									client.acceptGroupInvitationByTicket(group.id,ticket_id)
									client.sendMessage(to, "Berhasil masuk ke group %s" % str(group.name))
						if settings["detectUnsend"] == True:
							try:
								unsendTime = time.time()
								unsend[msg_id] = {"text": text, "from": sender, "time": unsendTime}
							except Exception as error:
								logError(error)
					if msg.contentType == 1:
						if settings["detectUnsend"] == True:
							try:
								unsendTime = time.time()
								image = client.downloadObjectMsg(msg_id, saveAs="LineAPI/tmp/{}-image.bin".format(time.time()))
								unsend[msg_id] = {"from": sender, "image": image, "time": unsendTime}
							except Exception as error:
								logError(error)
			except Exception as error:
				logError(error)


		if op.type == 55:
			print ("[ 55 ] NOTIFIED READ MESSAGE")
			if op.param1 in read["readPoint"]:
				if op.param2 not in read["readMember"][op.param1]:
					read["readMember"][op.param1].append(op.param2)


		if op.type == 65:
			try:
				if settings["detectUnsend"] == True:
					to = op.param1
					sender = op.param2
					if sender in unsend:
						unsendTime = time.time()
						contact = client.getContact(unsend[sender]["from"])
						if "text" in unsend[sender]:
							try:
								sendTime = unsendTime - unsend[sender]["time"]
								sendTime = timeChange(sendTime)
								ret_ = "╔══[ Unsend Message ]"
								ret_ += "\n╠ Sender : @!"
								ret_ += "\n╠ Time : {} yang lalu".format(sendTime)
								ret_ += "\n╠ Type : Text"
								ret_ += "\n╠ Text : {}".format(unsend[sender]["text"])
								ret_ += "\n╚══[ Finish ]"
								client.sendMention(to, ret_, [contact.mid])
								del unsend[sender]
							except:
								del unsend[sender]
						elif "image" in unsend[sender]:
							try:
								sendTime = unsendTime - unsend[sender]["time"]
								sendTime = timeChange(sendTime)
								ret_ = "╔══[ Unsend Message ]"
								ret_ += "\n╠ Sender : @!"
								ret_ += "\n╠ Time : {} yang lalu".format(sendTime)
								ret_ += "\n╠ Type : Image"
								ret_ += "\n╠ Text : None"
								ret_ += "\n╚══[ Finish ]"
								client.sendMention(to, ret_, [contact.mid])
								client.sendImage(to, unsend[sender]["image"])
								client.deleteFile(unsend[sender]["image"])
								del unsend[sender]
							except:
								client.deleteFile(unsend[sender]["image"])
								del unsend[sender]
					else:
						client.sendMessage(to, "Data unsend tidak ditemukan")
			except Exception as error:
				logError(error)
		backupData()
	except Exception as error:
		logError(error)

def run():
	while True:
		ops = clientPoll.singleTrace(count=50)
		if ops != None:
			for op in ops:
				try:
					clientBot(op)
				except Exception as error:
					logError(error)
				clientPoll.setRevision(op.revision)

if __name__ == "__main__":
	run()
