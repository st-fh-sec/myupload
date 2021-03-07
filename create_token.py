

import random
import string
import os
import pwd
import random

BASE_DIR = 'uploads'
#USER = 'vagrant'
#USER_ID = pwd.getpwnam(USER).pw_uid


def gen_token(token_len):
     #return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(token_len))
     return str(random.randint(10000,99999))

def create_dir(dir_name):
	target_dir = os.path.join(BASE_DIR, dir_name)
	if not os.path.exists(target_dir):
		os.mkdir(target_dir)
		return target_dir
		#os.chown(target_dir, USER_ID, 0)
	return None

def create_share():
    token = gen_token(6)
    target_dir = create_dir(token)
    if target_dir:
        return token

if __name__ == '__main__':
    create_share()
#    print("{0} created".format(target_dir))
#    prrnt("http://YOURDOMAIN/upload?token={0}".format(token))

