import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from app import app, mail


def save_picture(form_picture):
    
    random_hex = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/post_pics',picture_fn)
    form_picture.save(picture_path)

    return picture_fn
    



def notifiedWhenSomeoneCommented(author, current_user, comment):
    msg = Message('Find Who commented on your Blog',
        sender='noreply@demo.com',
        recipients=[author.email]) 
    msg.body = f'''
Hi { author.username },
Hope you are enjoying with your blogging life with goBLOG and making our nation pride by raising your voice.
Please find the details of your goblog Post:
BLOG POST NAME: { comment.post.title } 
RECEPIENT EMAIL: { author.email }
RECEPIENT Name: { author.username }
SENDER EMAIL : { current_user.email }
COMMENTED MESSAGE: { comment.body }
TIMESTAMP : { comment.date_posted.strftime("%m/%d/%Y, %H:%M:%S") }
Check the link below to get updated:
{url_for('main.home', _external=True)}

Thankyou for being part of goBLog Team, any help or support kindly reach out at support@demo.com
If you did not make this request then simply ignore this email and no change takes place
'''
    print(msg)
    mail.send(msg)