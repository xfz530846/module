from django.test import TestCase

# Create your tests here.
#添加测试数据
from questions.models import Questions

a=Questions.objects.get(id=1)

for i in range(0,100):
    a.id=None
    a.title="你好亮仔，这是第%s条数据"%i
    a.click_count = i
    a.save()



