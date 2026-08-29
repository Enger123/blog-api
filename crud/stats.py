from models import Post, User, Comment, Like, Tag, TagPost
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload, selectinload

async def stats_posts(db):
    post_counter_query = await db.execute(select(func.count(Post.id)))
    post_counter = post_counter_query.scalars().first()
    return {'Post_counter': post_counter}

async def stats_users(db):
    users_query = await db.execute(select(User.id))
    users = users_query.all()
    return users

async def stats_user_id(db):
    user_max_id_query = await db.execute(select(func.max(Post.user_id)))
    user_max_id = user_max_id_query.scalars().all()
    return {'User_id max in post': user_max_id}

async def stats_user_posts(db):
    user_posts_query = await db.execute(select(User.username, func.count(Post.id))\
    .outerjoin(Post)\
    .group_by(User.id))
    user_posts = user_posts_query.scalars().all()
    return [
            {
                'Username': u[0],
                'Posts': u[1]
            } for u in user_posts
        ]

async def stats_user_maxposts(db):
    user_max_posts_query = await db.execute(select(Post.user_id, func.count(Post.id))\
    .group_by(Post.user_id)\
    .order_by(func.count(Post.id).desc()))
    user_max_posts = user_max_posts_query.first()
    return {'User_id': user_max_posts[0],
            'Max_posts': user_max_posts[1]}

from sqlalchemy import select, func


async def stats_posts_comments(db):
    posts_comments_query = await db.execute(
        select(
            Comment.post_id,
            func.count(Comment.id)
        )
        .group_by(Comment.post_id)
    )

    posts_comments = posts_comments_query.all()

    print(posts_comments)

    return [
        {
            "post_id": pc[0],
            "comments": pc[1]
        }
        for pc in posts_comments
    ]


async def stats_posts_likes(db):
    posts_likes_query = await db.execute(
        select(
            Post.id,
            func.count(Like.id)
        )
        .outerjoin(Like)
        .group_by(Post.id)
    )

    posts_likes = posts_likes_query.all()

    print(posts_likes)

    return [
        {
            "Post": pl[0],
            "Likes": pl[1]
        }
        for pl in posts_likes
    ]


async def stats_users_maxcomments(db):
    user_max_comments_query = await db.execute(
        select(
            User.id,
            func.count(Comment.id)
        )
        .join(Comment)
        .group_by(User.id)
        .order_by(func.count(Comment.id).desc())
    )

    user_max_comments = user_max_comments_query.first()

    print(user_max_comments)

    return {
        "User_id": user_max_comments[0],
        "Comments": user_max_comments[1]
    }


async def stats_tags(db):
    tags_query = await db.execute(
        select(
            Tag.name,
            func.count(TagPost.id)
        )
        .outerjoin(TagPost)
        .group_by(Tag.id)
        .order_by(func.count(TagPost.id).desc())
    )

    tags = tags_query.all()

    print(tags)

    return [
        {
            "Tag_name": tag[0],
            "Counter": tag[1]
        }
        for tag in tags
    ]


async def stats_posts_tags(db):
    diff_tags_post_query = await db.execute(
        select(
            User.username,
            Tag.name
        )
        .join(Post)
        .join(TagPost)
        .join(Tag)
        .distinct()
    )

    diff_tags_post = diff_tags_post_query.all()

    print(diff_tags_post)

    return [
        {
            "Username": tag[0],
            "Tag_name": tag[1]
        }
        for tag in diff_tags_post
    ]


async def stats_tag_posts_count(db):
    tag_posts_query = await db.execute(
        select(
            Tag.name,
            func.count(TagPost.id)
        )
        .outerjoin(TagPost)
        .group_by(Tag.name)
        .order_by(func.count(TagPost.id))
    )

    tag_posts = tag_posts_query.all()

    print(tag_posts)

    return [
        {
            "Tag_name": tp[0],
            "Post_counter": tp[1]
        }
        for tp in tag_posts
    ]


async def stats_popular_tag(db):
    popular_tag_query = await db.execute(
        select(
            Tag.name,
            func.count(TagPost.id)
        )
        .join(TagPost)
        .group_by(Tag.id)
        .order_by(func.count(TagPost.id).desc())
    )

    popular_tag = popular_tag_query.first()

    print(popular_tag)

    return {
        "Tag_name": popular_tag[0],
        "Counter": popular_tag[1]
    }


async def stats_posts3_likes(db):
    posts3_likes_query = await db.execute(
        select(
            Post.id,
            func.count(Like.id)
        )
        .join(Like)
        .group_by(Post.id)
        .order_by(func.count(Like.id).desc())
        .limit(3)
    )

    posts3_likes = posts3_likes_query.all()

    print(posts3_likes)

    return [
        {
            "Post_id": pl[0],
            "Likes": pl[1]
        }
        for pl in posts3_likes
    ]


async def stats_users_posts_comments(db):
    user_st_query = await db.execute(
        select(
            User.username,
            func.count(Post.id),
            func.count(Comment.id)
        )
        .join(Post)
        .join(Comment)
        .group_by(User.id)
    )

    user_st = user_st_query.all()

    print(user_st)

    return [
        {
            "Username": user[0],
            "Posts": user[1],
            "Comments": user[2]
        }
        for user in user_st
    ]


async def stats_users_posts_moretwo(db):
    users_query = await db.execute(
        select(
            User.username,
            func.count(Post.id)
        )
        .outerjoin(Post)
        .group_by(User.id)
        .having(func.count(Post.id) > 2)
        .order_by(func.count(Post.id).desc())
    )

    users = users_query.all()

    print(users)

    return [
        {
            "Username": u[0],
            "Posts": u[1]
        }
        for u in users
    ]


async def stats_posts_comments_more3(db):
    posts_query = await db.execute(
        select(
            Post.title,
            func.count(Comment.id)
        )
        .outerjoin(Comment)
        .group_by(Post.id)
        .having(func.count(Comment.id) > 3)
    )

    posts = posts_query.all()

    print(posts)

    return [
        {
            "Post_name": p[0],
            "Comments": p[1]
        }
        for p in posts
    ]


async def stats_posts_tags_more2(db):
    tags_more2_query = await db.execute(
        select(
            Tag.name,
            func.count(TagPost.id)
        )
        .outerjoin(TagPost)
        .group_by(Tag.id)
        .having(func.count(TagPost.id) > 2)
    )

    tags_more2 = tags_more2_query.all()

    print(tags_more2)

    return [
        {
            "Post_name": t[0],
            "Comments": t[1]
        }
        for t in tags_more2
    ]


async def stats_users_commentstop3(db):
    users_query = await db.execute(
        select(
            User.username,
            func.count(Comment.id)
        )
        .join(Comment)
        .group_by(User.id)
        .order_by(func.count(Comment.id).desc())
        .limit(3)
    )

    users = users_query.all()

    print(users)

    return [
        {
            "Username": u[0],
            "Comments": u[1]
        }
        for u in users
    ]


async def min_posts_user(db):
    user_query = await db.execute(
        select(
            User.username,
            func.count(Like.id)
        )
        .outerjoin(Like)
        .group_by(User.id)
        .order_by(func.count(Like.id))
    )

    user = user_query.first()

    print(user)

    return {
        "Username": user[0],
        "Likes": user[1]
    }


async def stats_max_posts_users(db):
    users_query = await db.execute(
        select(
            User.username,
            func.count(Post.id)
        )
        .outerjoin(Post)
        .group_by(User.id)
    )

    users = users_query.all()

    print(users)

    return [
        {
            "Username": user[0],
            "Posts": user[1]
        }
        for user in users
    ]


async def stats_posts_maxlikes(db):
    like_stats = (
        select(
            Like.post_id,
            func.count(Like.id).label("likes_counter")
        )
        .group_by(Like.post_id)
        .subquery()
    )

    max_likes_query = await db.execute(
        select(
            func.max(like_stats.c.likes_counter)
        )
    )

    max_likes = max_likes_query.scalars().first()

    print(max_likes)

    posts_query = await db.execute(
        select(
            like_stats.c.post_id,
            like_stats.c.likes_counter
        )
        .where(
            like_stats.c.likes_counter == max_likes
        )
    )

    posts = posts_query.all()

    print(posts)

    return [
        {
            "Post_id": p[0],
            "Likes": p[1]
        }
        for p in posts
    ]


async def stats_users_posts_more_avg(db):
    post_stats = (
        select(
            Post.user_id,
            func.count(Post.id).label("post_counter")
        )
        .group_by(Post.user_id)
        .subquery()
    )

    avg_user_posts_query = await db.execute(
        select(
            func.avg(post_stats.c.post_counter)
        )
    )

    avg_user_posts = avg_user_posts_query.scalars().first()

    user_posts_query = await db.execute(
        select(
            post_stats.c.user_id,
            post_stats.c.post_counter
        )
        .where(
            post_stats.c.post_counter > avg_user_posts
        )
    )

    user_posts = user_posts_query.all()

    print(user_posts)

    return [
        {
            "User_id": u[0],
            "Posts_counter": u[1]
        }
        for u in user_posts
    ]


async def stats_posts_max_comments(db):
    comments_stats = (
        select(
            Comment.post_id,
            func.count(Comment.id).label("comments_counter")
        )
        .group_by(Comment.post_id)
        .subquery()
    )

    max_comments_query = await db.execute(
        select(
            func.max(comments_stats.c.comments_counter)
        )
    )

    max_comments = max_comments_query.scalars().first()

    post_comments_query = await db.execute(
        select(
            comments_stats.c.post_id,
            comments_stats.c.comments_counter
        )
        .where(
            comments_stats.c.comments_counter == max_comments
        )
    )

    post_comments = post_comments_query.all()

    return [
        {
            "Post_id": p[0],
            "Comments": p[1]
        }
        for p in post_comments
    ]


async def stats_posts_moreavg(db):
    posts_stats = (
        select(
            User.id,
            func.count(Post.id).label("post_counter")
        )
        .outerjoin(
            Post,
            User.id == Post.user_id
        )
        .group_by(User.id)
        .subquery()
    )

    avg_posts_query = await db.execute(
        select(
            func.avg(posts_stats.c.post_counter)
        )
    )

    avg_posts = avg_posts_query.scalars().first()

    user_moreavg_posts_query = await db.execute(
        select(
            posts_stats.c.id,
            posts_stats.c.post_counter
        )
        .where(
            posts_stats.c.post_counter > avg_posts
        )
    )

    user_moreavg_posts = user_moreavg_posts_query.all()

    return [
        {
            "User_id": u[0],
            "Posts_more_thanavg": u[1]
        }
        for u in user_moreavg_posts
    ]


async def stats_comments_moreavg(db):
    comments_stats = (
        select(
            User.id.label("user_id"),
            func.count(Comment.id).label("comments_counter")
        )
        .outerjoin(
            Comment,
            User.id == Comment.user_id
        )
        .group_by(User.id)
        .subquery()
    )

    comments_avg_query = await db.execute(
        select(
            func.avg(comments_stats.c.comments_counter)
        )
    )

    comments_avg = comments_avg_query.scalars().first()

    user_moreavg_comments_query = await db.execute(
        select(
            comments_stats.c.user_id,
            comments_stats.c.comments_counter
        )
        .where(
            comments_stats.c.comments_counter > comments_avg
        )
    )

    user_moreavg_comments = user_moreavg_comments_query.all()

    return [
        {
            "User_id": u[0],
            "Comments > avg": u[1]
        }
        for u in user_moreavg_comments
    ]