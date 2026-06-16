from pydantic import with_config

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
        user_posts = session.query(User.username, func.count(Post.id))\
        .outerjoin(Post)\
        .group_by(User.id)\
        .all()
        print(user_posts)
        return [
            {
                'Username': u[0],
                'Posts': u[1]
            } for u in user_posts
        ]

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
        .outerjoin(Like)\
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
    with Session() as session:
        tags = session.query(Tag.name, func.count(TagPost.id))\
    .outerjoin(TagPost)\
    .group_by(Tag.id)\
    .order_by(func.count(TagPost.id).desc())\
    .all()
        print(tags)
        return [
            {
                'Tag_name': tag[0],
                'Counter': tag[1]
            } for tag in tags
        ]

def stats_posts_tags():
    with Session() as session:
        diff_tags_post = session.query(User.username, Tag.name) \
            .join(Post)\
            .join(TagPost)\
            .join(Tag)\
        .distinct()\
        .all()
        print(diff_tags_post)
        return [
            {
                'Username': tag[0],
                'Tag_name': tag[1],
            } for tag in diff_tags_post
        ]

def stats_tag_posts_count():
    with (Session() as session):
        tag_posts = session.query(Tag.name, func.count(TagPost.id))\
        .outerjoin(TagPost)\
        .group_by(Tag.name)\
        .order_by(func.count(TagPost.id))\
        .all()
        print(tag_posts)
        return [
            {
                'Tag_name': tp[0],
                'Post_counter': tp[1]
            } for tp in tag_posts
        ]

def stats_popular_tag():
    with Session() as session:
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
        posts3_likes = session.query(Post.id, func.count(Like.id)) \
        .join(Like) \
        .group_by(Post.id) \
        .order_by(func.count(Like.id)\
        .desc()).limit(3).all()
        print(posts3_likes)
        return [
            {
                'Post_id': pl[0],
                'Likes': pl[1]
            } for pl in posts3_likes
        ]

def stats_users_posts_comments():
    with Session() as session:
        user_st = session.query(User.username, func.count(Post.id), func.count(Comment.id))\
        .join(Post)\
        .join(Comment)\
        .group_by(User.id).all()
        print(user_st)
        return [
            {
                'Username': user[0],
                'Posts': user[1],
                'Comments': user[2]
            } for user in user_st
        ]

def stats_users_posts_moretwo():
    with (Session() as session):
        users = session.query(User.username, func.count(Post.id))\
        .outerjoin(Post)\
        .group_by(User.id)\
        .having(func.count(Post.id) > 2)\
        .order_by(func.count(Post.id).desc())\
        .all()
        print(users)
        return [
            {
                'Username': u[0],
                'Posts': u[1]
            } for u in users
        ]

def stats_posts_comments_more3():
    with Session() as session:
        posts = session.query(Post.title, func.count(Comment.id))\
        .outerjoin(Comment)\
        .group_by(Post.id)\
        .having(func.count(Comment.id) > 3)\
            .all()
        print(posts)
        return [
            {
                'Post_name': p[0],
                'Comments': p[1]
            } for p in posts
        ]

def stats_posts_tags_more2():
    with Session() as session:
        tags_more2 = session.query(Tag.name, func.count(TagPost.id))\
        .outerjoin(TagPost)\
        .group_by(Tag.id)\
        .having(func.count(TagPost.id) > 2).all()
        print(tags_more2)
        return [
            {
                'Post_name': t[0],
                'Comments': t[1]
            } for t in tags_more2
        ]

def stats_users_commentstop3():
    with Session() as session:
        users = session.query(User.username, func.count(Comment.id))\
        .join(Comment)\
        .group_by(User.id)\
        .order_by(func.count(Comment.id).desc())\
        .limit(3).all()
        print(users)
        return [
            {
                'Username': u[0],
                'Comments': u[1]
            } for u in users
        ]

def min_posts_user():
    with Session() as session:
        user = session.query(User.username, func.count(Like.id))\
        .outerjoin(Like)\
        .group_by(User.id)\
        .order_by(func.count(Like.id))\
        .first()
        print(user)
        return {
                'Username': user[0],
                'Likes': user[1]
            }

