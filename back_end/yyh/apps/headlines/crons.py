import base64
import pickle

from django.utils import timezone
from django_redis import get_redis_connection

from headlines.models import Categories, Headlines
from questions.models import Questions
from talks.models import Talk


def update_hot_headline_to_redis():
    """更新redis中的热门头条"""

    queryset = Categories.objects.all()
    for model in queryset:
        dt = timezone.now() - timezone.timedelta(10)

        data = Headlines.objects.filter(category_id=model.id, is_delete=0, create_time__gt=dt).order_by('-click_counts')

        headline_list = []
        for headline in data[:4]:

            context = {
                "id": headline.id,
                "title": headline.title,
                "category": headline.category_id
            }
            headline_list.append(context)

        data = base64.b64encode(pickle.dumps(headline_list)).decode()

        # 将数据存入redis
        redis_con = get_redis_connection('hot_headlines')
        redis_con.set('headline_{0}'.format(model.id), data)

def update_hot_questions_to_redis():
    """更新redis中的热门问题"""

    dt = timezone.now() - timezone.timedelta(10)
    data = Questions.objects.filter(is_delete=0, create_time__gt=dt).order_by('-click_count')

    question_list = []
    for question in data[:5]:

        context = {
            "id": question.id,
            "title": question.title,
        }
        question_list.append(context)

    data = base64.b64encode(pickle.dumps(question_list)).decode()

    # 将数据存入redis
    redis_con = get_redis_connection('hot_questions')
    redis_con.set('hot_questions', data)


def update_hot_talks_to_redis():
    """更新redis中的热门吐槽"""

    dt = timezone.now() - timezone.timedelta(10)
    data = Talk.objects.filter(is_delete=0, create_time__gt=dt).order_by('-like_count')

    talk_list = []
    for talk in data[:4]:

        context = {
            "id": talk.id,
            "title": talk.title,
        }
        talk_list.append(context)

    data = base64.b64encode(pickle.dumps(talk_list)).decode()

    # 将数据存入redis
    redis_con = get_redis_connection('hot_talks')
    redis_con.set('hot_talks', data)

