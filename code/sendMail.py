import smtplib

def sendEmailFromAbir(sub, mess,name):
	to = name
	gmail_user = 'alanthehelper@gmail.com'
	gmail_pwd = 'aadi2247'
	smtpserver = smtplib.SMTP("smtp.gmail.com",587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo
	smtpserver.login(gmail_user, gmail_pwd)
	header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:'+sub+' \n'
	print header
	msg = header + '\n'+mess+' \n\n'
	smtpserver.sendmail(gmail_user, to, msg)
	print 'done!'
	smtpserver.close()


