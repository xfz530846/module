

from django.test import TestCase

# Create your tests here.
from headlines.models import Comments,Headlines
import random

# h = Headlines.objects.get(id=1)
# for i in range(100):
#     h.id = None
#     h.author_id = 1
#     h.category_id = random.randint(1, 7)
#     h.title = "哈哈哈哈哈哈哈"
#     h.content = "<p>啊几点了看见嘎啦看见滤镜all决定来分开就</p>"
#     h.status = 1
#     h.save()


h = Comments.objects.get(id=1)
for i in range(20):
    h.id = None
    h.headlines_id = 1
    h.user_id = 1
    h.headlines_id = random.randint(1, 7)
    h.create_time = '2019-08-25 15:10:33'
    h.parent_id = None
    h.content = "<p>啊几点了看见嘎啦看见滤镜all决定来分开就</p>%s" %i
    h.save()
