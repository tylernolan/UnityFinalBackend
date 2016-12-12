from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
import re
import telnetlib
app = Flask(__name__)

#It's not often for class projects it's encouraged to enumerate all the swear words you can think of!
#On second thought, let's source this from elsewhere...
#Source: http://www.bannedwordlist.com/lists/swearWords.txt
swearlist = open("swears.txt")

def tnSend(command):
	HOST, PORT = "localhost", 9999
	tn = telnetlib.Telnet(HOST, port = PORT)
	tn.write(command+"\r\n")
	tn.close()
	
	
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
		print word
	if len(name) > 12:
		name = name[:12] 
	page = u'<meta name="viewport" content="width=device-width, initial-scale=1.0">'
	page += '<form action="." method="POST">\n'
	page += "Spawn Enemies:<br>"
	page += u'<button name ="action" type="submit" value="{},{}">{}</button>\n'.format(str(name), "0", "Spawn Skele")
	page += u'<button name ="action" type="submit" value="{},{}">{}</button>\n'.format(str(name), "1", "Spawn Mage")
	page += "<br>"
	page += "Help Player:<br>"
	page += u'<button name ="action" type="submit" value="{},{}">{}</button>\n'.format(str(name), "2", "Heal")
	page += u'<button name ="action" type="submit" value="{},{}">{}</button>\n'.format(str(name), "3", "Regen Mana")
	page += u'<button name ="action" type="submit" value="{},{}">{}</button>\n'.format(str(name), "4", "Smite Enemy")
	page += "<br>"
	page += "Other:<br>"
	page += u'<button name ="action" type="submit" value="{},{}">{}</button>\n'.format(str(name), "5", "Say Nice Things")
	page +='</form>'	
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
	app.run(host= '0.0.0.0')