from fabric.api import *
from fabric.contrib.console import confirm

#env.password=
#env.user=

def add_user(user=None):
	if user == None:
		abort("No user specified")
	with settings(warn_only=True):
		not_exists = run("id %s" % user).failed
	#User exists and don't continue
	if not not_exists and not confirm("User exists. Continue anyway?"):
		abort("Aborting")
	sudo("adduser --disabled-password --gecos \"\" %s " % user) #No Finger/Password

def set_passwd(user):
	sudo("passwd %s" % user)

def add_pub_key(user, pub_key):
	#ugly hack
	sudo("mkdir /home/%s/.ssh; chmod 700 /home/%s/.ssh; \
		echo \"%s\" >> /home/%s/.ssh/authorized_keys; chmod 600 /home/%s/.ssh/authorized_keys; \
		chown -R %s:%s /home/%s/.ssh" 
		% (user, user, pub_key, user, user, user, user, user));

def add_sudo(user):
	if user == None:
		abort("No user specified");
	with settings(warn_only=True):
		exists = run("id %s" % user)
	#User does not exist and don't continue
	if exists.failed and not confirm("User does not exist. Continue anyway?"):
		abort("Aborting")
	sudo("echo %s ALL=(ALL) ALL >> /etc/sudoers" %user);

def add_new_user(user, pubKey, grantSudo=False):
	add_user(user)
	set_passwd(user)
	add_pub_key(user, pubKey)
	if grantSudo:
		add_sudo(user)
	
