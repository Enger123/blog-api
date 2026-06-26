from fastapi import APIRouter
from crud import stats
from app.dependencies import DBSession
router = APIRouter()

@router.get("/stats/posts-count")
def stats_posts(db: DBSession):
    return stats.stats_posts(db)

@router.get("/stats/users")
def stats_users(db: DBSession):
    return stats.stats_users(db)

@router.get("/stats/users/maxid")
def stats_user_id(db: DBSession):
    return stats.stats_user_id(db)

@router.get("/stats/users/posts-count")
def stats_user_posts(db: DBSession):
    return stats.stats_user_posts(db)

@router.get("/stats/users-maxposts")
def stats_user_maxposts(db: DBSession):
    return stats.stats_user_maxposts(db)

@router.get("/stats/posts/comments")
def stats_posts_comments(db: DBSession):
    return stats.stats_posts_comments(db)

@router.get("/stats/posts/likes")
def stats_posts_likes(db: DBSession):
    return stats.stats_posts_likes(db)

@router.get("/stats/users-maxcomments")
def stats_users_maxcomments(db: DBSession):
    return stats.stats_users_maxcomments(db)

@router.get("/stats/tags")
def stats_tags(db: DBSession):
    return stats.stats_tags(db)

@router.get("/stats/posts/tags")
def stats_posts_tags(db: DBSession):
    return stats.stats_posts_tags(db)

@router.get("/stats/tag/posts-count")
def stats_tag_posts_count(db: DBSession):
    return stats.stats_tag_posts_count(db)

@router.get("/stats/popular-tags")
def stats_popular_tag(db: DBSession):
    return stats.stats_popular_tag(db)

@router.get("/stats/posts3/likes")
def stats_posts3_likes(db: DBSession):
    return stats.stats_posts3_likes(db)

@router.get("/stats/users/posts-comments")
def stats_users_posts_comments(db: DBSession):
    return stats.stats_users_posts_comments(db)

@router.get("/stats/users/postmoretwo")
def stats_users_posts_moretwo(db: DBSession):
    return stats.stats_users_posts_moretwo(db)

@router.get("/stats/posts/commentsmore3")
def stats_posts_comments_more3(db: DBSession):
    return stats.stats_posts_comments_more3(db)

@router.get("/stats/posts/tagsmore2")
def stats_posts_tags_more2(db: DBSession):
    return stats.stats_posts_tags_more2(db)

@router.get("/stats/users/commentstop3")
def stats_users_commentstop3(db: DBSession):
    return stats.stats_users_commentstop3(db)

@router.get("/stats/users/minlikes")
def min_posts_user(db: DBSession):
    return stats.min_posts_user(db)

@router.get("/stats/max/posts/users")
def stats_max_posts_users(db: DBSession):
    return stats.stats_max_posts_users(db)

@router.get("/stats/posts/maxlikes")
def stats_posts_maxlikes(db: DBSession):
    return stats.stats_posts_maxlikes(db)

@router.get("/stats/users/posts-more-avg")
def stats_users_posts_more_avg(db: DBSession):
    return stats.stats_users_posts_more_avg(db)

@router.get("/stats/posts/max-comments")
def stats_posts_max_comments(db: DBSession):
    return stats.stats_posts_max_comments(db)

@router.get("/stats/posts/more-avg")
def stats_posts_moreavg(db: DBSession):
    return stats.stats_posts_moreavg(db)

@router.get("/stats/comments/more-avg")
def stats_comments_moreavg(db: DBSession):
    return stats.stats_comments_moreavg(db)

@router.get("/test")
def test_joinedload(db: DBSession):
    return stats.test_joinedload(db)
