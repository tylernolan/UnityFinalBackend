from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
import re
import telnetlib
import os 
import random
app = Flask(__name__)
PATH = "C:\\Users\\Tyler\\Dropbox\\Cool Code\\GameDesignPlaysCrypt\\UnityFinalBackend\\flaskapp\\"
#It's not often for class projects it's encouraged to enumerate all the swear words you can think of!
#On second thought, let's source this from elsewhere...
#Source: http://www.bannedwordlist.com/lists/swearWords.txt
swearlist = open("swears.txt")

def tnSend(command):
	HOST, PORT = "localhost", 9999
	tn = telnetlib.Telnet(HOST, port = PORT)
	tn.write(command+"\r\n")
	tn.close()
	
def tnPoll():
	HOST, PORT = "localhost", 9999
	tn = telnetlib.Telnet(HOST, port = PORT)
	tn.write("isboss"+"\r\n")
	received = tn.read_until("\n").strip() == "True"
	tn.close()
	return received

def getImageFromFolder():
	#I tried to get flask workign with local images on my windows box but it wasn't working, this is a really shitty workaround I hope to have fixed before the presentation.
	images = ["http://i.imgur.com/2EBb9wZ.jpg", "http://i.imgur.com/OdR8lyP.png", "http://i.imgur.com/Qb3c5gf.jpg", 
			"http://i.imgur.com/MEWNY5G.jpg", "http://i.imgur.com/Y3jpQHm.jpg"]
	return random.choice(images) 
	
@app.route("/")
def home():
	return open("index.html").read()
	
@app.route('/', methods=['POST'])
def login():
	name = request.form.get('text')
	return redirect("/welcome/{}".format(name))#query(text)#
	
@app.route('/welcome/<name>')
def welcome(name):
	while "," in name:
		name = name.replace(",", "")
	for word in swearlist:
		word = word.strip()
		r = re.compile(word, re.IGNORECASE)
		name = r.sub("*"*len(word), name)
	if len(name) > 12:
		name = name[:12] 
	if not tnPoll():
		page = u'<meta name="viewport" content="width=device-width, initial-scale=1.0">'
		page += '<style type="text/css">button[type=submit] {width:10em; height:10em;}</style>'
		page += '<form action="." method="POST">\n'
		page += "Spawn Enemies:<br>"
		page += u'<button name ="action" type="submit" value="{},{}">{}</button>\n'.format(str(name), "0", "Spawn Skele")
		page += u'<button name ="action" type="submit" value="{},{}">{}</button>\n'.format(str(name), "1", "Spawn Mage")
		page += "<br>"
		page += "Help Player:<br>"
		page += u'<button name ="action" type="submit" value="{},{}">{}</button>\n'.format(str(name), "2", "Heal")
		page += u'<button name ="action" type="submit" value="{},{}">{}</button>\n'.format(str(name), "3", "Regen Mana")
		page += u'<button name ="action" type="submit" value="{},{}">{}</button>\n'.format(str(name), "6", "Empower Weapon")
		page += "<br>"
		page += u'<button name ="action" type="submit" value="{},{}">{}</button>\n'.format(str(name), "7", "Give Barrier")
		page += u'<button name ="action" type="submit" value="{},{}">{}</button>\n'.format(str(name), "4", "Smite Enemy")
		page += "<br>"
		page += "Other:<br>"
		page += u'<button name ="action" type="submit" value="{},{}">{}</button>\n'.format(str(name), "5", "Say Nice Things")
		page +='</form>'	
		return page
	else:
		img = getImageFromFolder()
		page = ""
		page +="<!DOCTYPE html>\n"
		page +="<html>\n"
		page = u'<meta name="viewport" content="width=device-width, initial-scale=1.0">'
		page +="<body>\n"
		page +="<h2>Give Me Your Energy!</h2>\n"
		#page += '<img src = {} style="width:304px;height:228px;">'.format(img)
		page += '<form action="." method="POST"><button type="submit" name="action" value="{}, -1" style="border:0;"> <img src = {} style="width:304px;height:228px;"> </button></form>'.format(name, img)
		page +="</body>\n"
		page +="</html>\n"
		return page
	
@app.route('/welcome/', methods=["POST"])	
def act():
	action = request.form['action']
	try:
		tnSend(str(action))
	except BaseException, e:
		print e
	return redirect('/welcome/{}'.format(action.split(",")[0]))
	
if __name__ == "__main__":
	app.run(host= '0.0.0.0', debug=True)