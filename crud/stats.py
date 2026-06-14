from app.database import Session
from models import Post, User, Comment, Like, Tag, TagPost
from sqlalchemy import func
def stats_posts():
    with Session() as session:
        post_counter = session.query(func.count(Post.id)).scalar()
        return {'Post_counter': post_counter}

def stats_users():
    with Session() as session:
        users = session.query(func.count(User.id)).scalar()
        print(users)
        return users

def stats_user_id():
    with Session() as session:
        user_max_id = session.query(func.max(Post.user_id)).scalar()
        return {'User': user_max_id}

def stats_user_posts():
    with Session() as session:
        user_posts = session.query(User.id, func.count(Post.id))\
            .join(Post)\
            .group_by(User.id).all()
        print(user_posts)
        return [{'User_id': n[0],
                'Post_counter': n[1]
                } for n in user_posts]

def stats_user_maxposts():
    with Session() as session:
        user_max_posts = session.query(Post.user_id, func.count(Post.id))\
        .group_by(Post.user_id)\
        .order_by(func.count(Post.id).desc()).first()
    print(user_max_posts[0])
    return {'User_id': user_max_posts[0],
            'Max_posts': user_max_posts[1]}

def stats_posts_comments():
    with Session() as session:
        posts_comments = session.query(Comment.post_id, func.count(Comment.id))\
        .group_by(Comment.post_id).all()
        print(posts_comments)
        return [
            {
                'post_id': pc[0],
                'comments': pc[1]
            } for pc in posts_comments
        ]

def stats_posts_likes():
    with Session() as session:
        posts_likes = session.query(Post.id, func.count(Like.id))\
        .join(Like)\
        .group_by(Post.id).all()
        print(posts_likes)
        return [
            {
                'Post': pl[0],
                'Likes': pl[1]
            } for pl in posts_likes
        ]

def stats_users_maxcomments():
    with Session() as session:
        user_max_comments = session.query(User.id, func.count(Comment.id))\
        .join(Comment)\
        .group_by(User.id)\
        .order_by(func.count(Comment.id).desc()).first()
        print(user_max_comments)
        return {
            'User_id': user_max_comments[0],
            'Comments': user_max_comments[1]
        }

def stats_tags():
    with (Session() as session):
        popular_tag = session.query(Tag.name, func.count(TagPost.id))\
        .join(TagPost)\
        .group_by(Tag.id)\
        .order_by(func.count(TagPost.id).desc())\
        .first()
        print(popular_tag)
        return {
            'Tag_name': popular_tag[0],
            'Counter': popular_tag[1]
                }

def stats_posts3_likes():
    with Session() as session:
        posts3_likes = session.query(Post.id, func.count(Like.id))\
        .join(Like)\
        .group_by(Post.id)\
        .order_by(func.count(Like.id).desc()).all()
        print(posts3_likes)
        return [
            {
                'Post_id': pl[0],
                'Likes': pl[1]
            } for pl in posts3_likes
        ]

def stats_users_posts_comments():
    with Session() as session:
        users = session.query(User.username, func.count(Post.id), func.count(Comment.id))\
        .join(Post)\
        .join(Comment)\
        .group_by(User.id).all()
        print(users)
        return [
            {
                'Username': user[0],
                'Posts': user[1],
                'Comments': user[2]
            } for user in users
        ]