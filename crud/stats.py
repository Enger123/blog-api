from pydantic import with_config

from app.database import Session
from models import Post, User, Comment, Like, Tag, TagPost
from sqlalchemy import func
from sqlalchemy.orm import joinedload, selectinload
def stats_posts(db):
    post_counter = db.query(func.count(Post.id)).scalar()
    return {'Post_counter': post_counter}

def stats_users(db):
    users = db.query(func.count(User.id)).scalar()
    print(users)
    return users

def stats_user_id(db):
    user_max_id = db.query(func.max(Post.user_id)).scalar()
    return {'User': user_max_id}

def stats_user_posts(db):
    user_posts = db.query(User.username, func.count(Post.id))\
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

def stats_user_maxposts(db):
    user_max_posts = db.query(Post.user_id, func.count(Post.id))\
    .group_by(Post.user_id)\
    .order_by(func.count(Post.id).desc()).first()
    print(user_max_posts[0])
    return {'User_id': user_max_posts[0],
            'Max_posts': user_max_posts[1]}

def stats_posts_comments(db):
    posts_comments = db.query(Comment.post_id, func.count(Comment.id))\
    .group_by(Comment.post_id).all()
    print(posts_comments)
    return [
            {
                'post_id': pc[0],
                'comments': pc[1]
            } for pc in posts_comments
        ]

def stats_posts_likes(db):
    posts_likes = db.query(Post.id, func.count(Like.id))\
    .outerjoin(Like)\
    .group_by(Post.id).all()
    print(posts_likes)
    return [
            {
                'Post': pl[0],
                'Likes': pl[1]
            } for pl in posts_likes
        ]

def stats_users_maxcomments(db):
    user_max_comments = db.query(User.id, func.count(Comment.id))\
    .join(Comment)\
    .group_by(User.id)\
    .order_by(func.count(Comment.id).desc()).first()
    print(user_max_comments)
    return {
            'User_id': user_max_comments[0],
            'Comments': user_max_comments[1]
        }

def stats_tags(db):
    tags = db.query(Tag.name, func.count(TagPost.id))\
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

def stats_posts_tags(db):
    diff_tags_post = db.query(User.username, Tag.name) \
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

def stats_tag_posts_count(db):
    tag_posts = db.query(Tag.name, func.count(TagPost.id))\
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

def stats_popular_tag(db):
    popular_tag = db.query(Tag.name, func.count(TagPost.id))\
        .join(TagPost)\
        .group_by(Tag.id)\
        .order_by(func.count(TagPost.id).desc())\
        .first()
    print(popular_tag)
    return {
            'Tag_name': popular_tag[0],
            'Counter': popular_tag[1]
                }

def stats_posts3_likes(db):
    posts3_likes = db.query(Post.id, func.count(Like.id)) \
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

def stats_users_posts_comments(db):
    user_st = db.query(User.username, func.count(Post.id), func.count(Comment.id))\
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
    users = db.query(User.username, func.count(Post.id))\
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

def stats_posts_comments_more3(db):
    posts = db.query(Post.title, func.count(Comment.id))\
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

def stats_posts_tags_more2(db):
    tags_more2 = db.query(Tag.name, func.count(TagPost.id))\
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

def stats_users_commentstop3(db):
    users = db.query(User.username, func.count(Comment.id))\
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

def min_posts_user(db):
    user = db.query(User.username, func.count(Like.id))\
        .outerjoin(Like)\
        .group_by(User.id)\
        .order_by(func.count(Like.id))\
        .first()
    print(user)
    return {
                'Username': user[0],
                'Likes': user[1]
            }

def stats_max_posts_users(db):
    users = db.query(User.username, func.count(Post.id))\
        .outerjoin(Post)\
        .group_by(User.id)\
        .all()
    print(users)
    return [
            {
                'Username': user[0],
                'Posts': user[1]
            } for user in users
        ]

def stats_posts_maxlikes(db):
    like_stats = (db.query(Like.post_id,
                                   func.count(Like.id)
                                   .label('likes_counter')
                                    )
        .group_by(Like.post_id).subquery()
                      )

    max_likes = session.query(
            func.max(
                like_stats.c.likes_counter)
        ).scalar_subquery()
    print(max_likes)

    posts = db.query(
            like_stats.c.post_id,
            like_stats.c.likes_counter)\
                              .filter(like_stats.c.likes_counter == max_likes)\
                              .all()
    print(posts)
    return [
            {
                'Post_id': p[0],
                'Likes': p[1]
            } for p in posts
        ]

def stats_users_posts_more_avg(db):
    post_stats = (db.query(Post.user_id,
                                   func.count(Post.id)
                                   .label('post_counter')
                                    )
                      .group_by(Post.user_id).subquery()
                      )

    avg_user_posts = db.query(
            func.avg(post_stats.c.post_counter)
        ).scalar_subquery()

    user_posts = db.query(
            post_stats.c.user_id,
            post_stats.c.post_counter
        ).filter(post_stats.c.post_counter > avg_user_posts)\
        .all()
    print(post_stats)
    print(user_posts)
    return [
            {
                'User_id': u[0],
                'Posts_counter': u[1]
            } for u in user_posts
        ]

def stats_posts_max_comments(db):
    comments_stats = (db.query(
            Comment.post_id,
            func.count(Comment.id)
            .label('comments_counter'))
            .group_by(Comment.post_id)
        .subquery()
                          )

    max_comments = db.query(
            func.max(comments_stats.c.comments_counter)
        ).scalar_subquery()

    post_comments = db.query(
            comments_stats.c.post_id,
            comments_stats.c.comments_counter
        ).filter(comments_stats.c.comments_counter == max_comments)\
        .all()

    return [
            {
                'Post_id': p[0],
                'Comments': p[1]
            } for p in post_comments
        ]

def stats_posts_moreavg(db):
    posts_stats = (db.query(
            User.id,
            func.count(Post.id).label('post_counter')
        ).outerjoin(Post, User.id == Post.user_id)
        .group_by(User.id).subquery())

    print(posts_stats)

    avg_posts = db.query(
            func.avg(posts_stats.c.post_counter)
        ).scalar_subquery()

    user_moreavg_posts = db.query(
            posts_stats.c.id,
            posts_stats.c.post_counter
        ).filter(posts_stats.c.post_counter > avg_posts)

    return [
            {
                'User_id': u[0],
                'Posts_more_thanavg': u[1]
            } for u in user_moreavg_posts
        ]

def stats_comments_moreavg(db):
    comments_stats = db.query(
            User.id.label('user_id'),
            func.count(Comment.id).label('comments_counter')
        ).outerjoin(Comment, User.id == Comment.user_id)\
        .group_by(User.id)\
        .subquery()

    comments_avg = db.query(
            func.avg(comments_stats.c.comments_counter)
        ).scalar_subquery()

    user_moreavg_comments = db.query(
            comments_stats.c.user_id,
            comments_stats.c.comments_counter
        ).filter(comments_stats.c.comments_counter > comments_avg)

    return [
            {
                'User_id': u[0],
                'Comments > avg': u[1]
            } for u in user_moreavg_comments
        ]

def test_joinedload(db):
    posts = db.query(Post)\
        .all()
    for post in posts:
        print(post.comments)