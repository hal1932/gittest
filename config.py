# encoding: utf-8
import os

USERNAME = ''
PASSWORD = ''

SSH_PUBLIC_KEY = os.path.join(os.environ['HOME'], '.ssh', 'id_rsa.pub')
SSH_PRIVATE_KEY = os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')
