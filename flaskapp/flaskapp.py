from flask import Flask
from flask import request
from flask import render_template
from flask import redirect

import telnetlib
app = Flask(__name__)
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
	page = '<form action="." method="POST">\n'
	page += "Spawn Enemies:<br>"
	page += u'<button name ="action" type="submit" value="{},{}">{}</button>\n'.format(str(name), "0", "Spawn Skele")
	page += u'<button name ="action" type="submit" value="{},{}">{}</button>\n'.format(str(name), "1", "Spawn Mage")
	page += "<br>"
	page += "Heal Player:<br>"
	page += u'<button name ="action" type="submit" value="{},{}">{}</button>\n'.format(str(name), "2", "Heal")
	page += u'<button name ="action" type="submit" value="{},{}">{}</button>\n'.format(str(name), "3", "Regen Mana")
	page += "<br>"
	page += "Other:<br>"
	page += u'<button name ="action" type="submit" value="{},{}">{}</button>\n'.format(str(name), "4", "Smite Enemy")
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