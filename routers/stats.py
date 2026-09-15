from fastapi import APIRouter
from app.dependencies import StatServiceDep

router = APIRouter()

@router.get("/stats/posts-count", tags=['Stats'])
async def stats_posts(stat_service: StatServiceDep):
    return await stat_service.stats_posts()


@router.get("/stats/users", tags=['Stats'])
async def stats_users(stat_service: StatServiceDep):
    return await stat_service.stats_users()


@router.get("/stats/users/maxid", tags=['Stats'])
async def stats_user_id(stat_service: StatServiceDep):
    return await stat_service.stats_user_id()


@router.get("/stats/users/posts-count", tags=['Stats'])
async def stats_user_posts(stat_service: StatServiceDep):
    return await stat_service.stats_user_posts()


@router.get("/stats/users-maxposts", tags=['Stats'])
async def stats_user_maxposts(stat_service: StatServiceDep):
    return await stat_service.stats_user_maxposts()


@router.get("/stats/posts/comments", tags=['Stats'])
async def stats_posts_comments(stat_service: StatServiceDep):
    return await stat_service.stats_posts_comments()


@router.get("/stats/posts/likes", tags=['Stats'])
async def stats_posts_likes(stat_service: StatServiceDep):
    return await stat_service.stats_posts_likes()


@router.get("/stats/users-maxcomments", tags=['Stats'])
async def stats_users_maxcomments(stat_service: StatServiceDep):
    return await stat_service.stats_users_maxcomments()


@router.get("/stats/tags", tags=['Stats'])
async def stats_tags(stat_service: StatServiceDep):
    return await stat_service.stats_tags()


@router.get("/stats/posts/tags", tags=['Stats'])
async def stats_posts_tags(stat_service: StatServiceDep):
    return await stat_service.stats_posts_tags()


@router.get("/stats/tag/posts-count", tags=['Stats'])
async def stats_tag_posts_count(stat_service: StatServiceDep):
    return await stat_service.stats_tag_posts_count()


@router.get("/stats/popular-tags", tags=['Stats'])
async def stats_popular_tag(stat_service: StatServiceDep):
    return await stat_service.stats_popular_tag()


@router.get("/stats/posts3/likes", tags=['Stats'])
async def stats_posts3_likes(stat_service: StatServiceDep):
    return await stat_service.stats_posts3_likes()


@router.get("/stats/users/posts-comments", tags=['Stats'])
async def stats_users_posts_comments(stat_service: StatServiceDep):
    return await stat_service.stats_users_posts_comments()


@router.get("/stats/users/postmoretwo", tags=['Stats'])
async def stats_users_posts_moretwo(stat_service: StatServiceDep):
    return await stat_service.stats_users_posts_moretwo()


@router.get("/stats/posts/commentsmore3", tags=['Stats'])
async def stats_posts_comments_more3(stat_service: StatServiceDep):
    return await stat_service.stats_posts_comments_more3()


@router.get("/stats/posts/tagsmore2", tags=['Stats'])
async def stats_posts_tags_more2(stat_service: StatServiceDep):
    return await stat_service.stats_posts_tags_more2()


@router.get("/stats/users/commentstop3", tags=['Stats'])
async def stats_users_commentstop3(stat_service: StatServiceDep):
    return await stat_service.stats_users_commentstop3()


@router.get("/stats/users/minlikes", tags=['Stats'])
async def min_posts_user(stat_service: StatServiceDep):
    return await stat_service.min_posts_user()


@router.get("/stats/max/posts/users", tags=['Stats'])
async def stats_max_posts_users(stat_service: StatServiceDep):
    return await stat_service.stats_max_posts_users()


@router.get("/stats/posts/maxlikes", tags=['Stats'])
async def stats_posts_maxlikes(stat_service: StatServiceDep):
    return await stat_service.stats_posts_maxlikes()


@router.get("/stats/users/posts-more-avg", tags=['Stats'])
async def stats_users_posts_more_avg(stat_service: StatServiceDep):
    return await stat_service.stats_users_posts_more_avg()


@router.get("/stats/posts/max-comments", tags=['Stats'])
async def stats_posts_max_comments(stat_service: StatServiceDep):
    return await stat_service.stats_posts_max_comments()


@router.get("/stats/posts/more-avg", tags=['Stats'])
async def stats_posts_moreavg(stat_service: StatServiceDep):
    return await stat_service.stats_posts_moreavg()


@router.get("/stats/comments/more-avg", tags=['Stats'])
async def stats_comments_moreavg(stat_service: StatServiceDep):
    return await stat_service.stats_comments_moreavg()