from fastapi import APIRouter
from crud import stats
from app.dependencies import DBSession
router = APIRouter()

@router.get("/stats/posts-count", tags=['Stats'])
async def stats_posts(db: DBSession):
    return await stats.stats_posts(db)

@router.get("/stats/users", tags=['Stats'])
async def stats_users(db: DBSession):
    return await stats.stats_users(db)

@router.get("/stats/users/maxid", tags=['Stats'])
async def stats_user_id(db: DBSession):
    return await stats.stats_user_id(db)

@router.get("/stats/users/posts-count", tags=['Stats'])
async def stats_user_posts(db: DBSession):
    return stats.stats_user_posts(db)

@router.get("/stats/users-maxposts", tags=['Stats'])
async def stats_user_maxposts(db: DBSession):
    return await stats.stats_user_maxposts(db)

@router.get("/stats/posts/comments", tags=['Stats'])
async def stats_posts_comments(db: DBSession):
    return await stats.stats_posts_comments(db)

@router.get("/stats/posts/likes", tags=['Stats'])
async def stats_posts_likes(db: DBSession):
    return await stats.stats_posts_likes(db)

@router.get("/stats/users-maxcomments", tags=['Stats'])
async def stats_users_maxcomments(db: DBSession):
    return await stats.stats_users_maxcomments(db)

@router.get("/stats/tags", tags=['Stats'])
async def stats_tags(db: DBSession):
    return await stats.stats_tags(db)

@router.get("/stats/posts/tags", tags=['Stats'])
async def stats_posts_tags(db: DBSession):
    return await stats.stats_posts_tags(db)

@router.get("/stats/tag/posts-count", tags=['Stats'])
async def stats_tag_posts_count(db: DBSession):
    return await stats.stats_tag_posts_count(db)

@router.get("/stats/popular-tags", tags=['Stats'])
async def stats_popular_tag(db: DBSession):
    return await stats.stats_popular_tag(db)

@router.get("/stats/posts3/likes", tags=['Stats'])
async def stats_posts3_likes(db: DBSession):
    return await stats.stats_posts3_likes(db)

@router.get("/stats/users/posts-comments", tags=['Stats'])
async def stats_users_posts_comments(db: DBSession):
    return await stats.stats_users_posts_comments(db)

@router.get("/stats/users/postmoretwo", tags=['Stats'])
async def stats_users_posts_moretwo(db: DBSession):
    return await stats.stats_users_posts_moretwo(db)

@router.get("/stats/posts/commentsmore3", tags=['Stats'])
async def stats_posts_comments_more3(db: DBSession):
    return await stats.stats_posts_comments_more3(db)

@router.get("/stats/posts/tagsmore2", tags=['Stats'])
async def stats_posts_tags_more2(db: DBSession):
    return await stats.stats_posts_tags_more2(db)

@router.get("/stats/users/commentstop3", tags=['Stats'])
async def stats_users_commentstop3(db: DBSession):
    return await stats.stats_users_commentstop3(db)

@router.get("/stats/users/minlikes", tags=['Stats'])
async def min_posts_user(db: DBSession):
    return await stats.min_posts_user(db)

@router.get("/stats/max/posts/users", tags=['Stats'])
async def stats_max_posts_users(db: DBSession):
    return await stats.stats_max_posts_users(db)

@router.get("/stats/posts/maxlikes", tags=['Stats'])
async def stats_posts_maxlikes(db: DBSession):
    return await stats.stats_posts_maxlikes(db)

@router.get("/stats/users/posts-more-avg", tags=['Stats'])
async def stats_users_posts_more_avg(db: DBSession):
    return await stats.stats_users_posts_more_avg(db)

@router.get("/stats/posts/max-comments", tags=['Stats'])
async def stats_posts_max_comments(db: DBSession):
    return await stats.stats_posts_max_comments(db)

@router.get("/stats/posts/more-avg", tags=['Stats'])
async def stats_posts_moreavg(db: DBSession):
    return await stats.stats_posts_moreavg(db)

@router.get("/stats/comments/more-avg", tags=['Stats'])
async def stats_comments_moreavg(db: DBSession):
    return await stats.stats_comments_moreavg(db)

@router.get("/test", tags=['Stats'])
async def test_joinedload(db: DBSession):
    return await stats.test_joinedload(db)
