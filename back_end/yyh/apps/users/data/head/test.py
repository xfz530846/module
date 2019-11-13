from users import constants
from users.models import User

with open('/home/python/name.txt') as f:
    path = f.read()

with open('/home/python/nickname.txt') as f:
    name = f.read()

name_list = name.split('\n')
path_list = path.split('\n')

import random
user_dict_li = []

for i in range(120):

    a = random.randint(0,len(name_list)-1)
    print(a)
    name = name_list.pop(a)
    path = path_list.pop(a)
    user_dict = {
        "nickname":name,
        "avatar_url": constants.HOST + "default_pic/" + path,
    }
    user_dict_li.append(user_dict)


i = 0

for user_info in user_dict_li:
    i+=1
    n = "user"+ str(i)
    password = "qq123456"
    user = User()
    user.username = n
    user.set_password(password)
    user.nickname = user_info['nickname']
    user.avatar_url = user_info['avatar_url']
    user.save()
