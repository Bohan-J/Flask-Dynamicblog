from app import app
from rq import get_current_job
from app import db
from app.models import User, Post, Task
import time
import math
import json
import sys
from app.email import send_email


def _set_task_progress(progress):
    job = get_current_job()
    if job:
        job.meta['progress'] = progress
        job.save_meta()
        task = Task.query.get(job.get_id())
        if progress >= 100:
            task.complete = True
        db.session.commit()

def export_posts(user_id):
    try:
        user = User.query.get(user_id)
        _set_task_progress(0)
        data = []
        i = 0
        total_posts = user.posts.count()
        for post in user.posts.order_by(Post.timestamp.asc()):
            data.append({'body':post.body, 'timestamp':str(post.timestamp) })
            time.sleep(5)
            i += 1
            _set_task_progress(math.ceil(100 * i / total_posts))
            send_email(subject='[Dynamicblog] Your blog posts', sender=app.config['ADMINS'][0],
                       recipients=[user.email], text_body=json.dumps({'posts': data}), html_body='')
    except:
        _set_task_progress(100)
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())














