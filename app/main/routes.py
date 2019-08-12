from flask import render_template, request, Blueprint
from app.models import Post
import sys
from jinja2 import Template
main = Blueprint("main",__name__) 


@main.route('/')
@main.route('/home')
def home():
    print('This is standard output', file=sys.stdout)
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=6)
    return render_template("home.html",posts=posts, len=len(posts.items))
 
@main.route('/about')
def about():
    return render_template("about.html",title="About")


# <article class="media content-section">
#     <img class="rounded-circle article-img" src="{{ url_for('static', filename='profile_pics/'+post.author.image_file)}}">
#     <div class="media-body">
#         <div class="article-metadata">
#             <a class="mr-2" href="{{ url_for('users.user_posts', username=post.author.username) }}">{{ post.author.username }}</a>
#             <small class="text-muted">{{ post.date_posted.strftime('%Y-%m-%d') }}</small>
#         </div>
#         <h2><a class="article-title" href="{{ url_for('posts.post',post_id=post.id) }}">{{ post.title }}</a></h2>
#         <p class="article-content">{{ post.content }}</p>
#     </div>
# </article>