from fastapi import APIRouter
from crud import stats
router = APIRouter()

@router.get("/stats/posts-count")
def stats_posts():
    return stats.stats_posts()

@router.get("/stats/users")
def stats_users():
    return stats.stats_users()

@router.get("/stats/users/maxid")
def stats_user_id():
    return stats.stats_user_id()

@router.get("/stats/users/posts-count")
def stats_user_posts():
    return stats.stats_user_posts()

@router.get("/stats/users-maxposts")
def stats_user_maxposts():
    return stats.stats_user_maxposts()

@router.get("/stats/posts/comments")
def stats_posts_comments():
    return stats.stats_posts_comments()

@router.get("/stats/posts/likes")
def stats_posts_likes():
    return stats.stats_posts_likes()

@router.get("/stats/users-maxcomments")
def stats_users_maxcomments():
    return stats.stats_users_maxcomments()

@router.get("/stats/tags")
def stats_tags():
    return stats.stats_tags()

@router.get("/stats/posts3/likes")
def stats_posts3_likes():
    return stats.stats_posts3_likes()

@router.get("/stats/users/posts-comments")
def stats_users_posts_comments():
    return stats.stats_users_posts_comments()
