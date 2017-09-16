# encoding: utf-8
import os

USERNAME = ''
PASSWORD = ''

SSH_PUBLIC_KEY = os.path.join(os.environ['HOMEDRIVE'], os.environ['HOMEPATH'], '.ssh', 'id_rsa.pub')
SSH_PRIVATE_KEY = os.path.join(os.environ['HOMEDRIVE'], os.environ['HOMEPATH'], '.ssh', 'id_rsa')

MAIL_ADDRESS = ''
