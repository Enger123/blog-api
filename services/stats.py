from sqlalchemy.ext.asyncio import AsyncSession

from repositories import StatRepository


class StatService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.stat_repository = StatRepository(db)

    async def stats_posts(self):
        post_counter = await self.stat_repository.get_posts_count()
        return {'Post_counter': post_counter}

    async def stats_users(self):
        return await self.stat_repository.get_all_users()

    async def stats_user_id(self):
        user_max_id = await self.stat_repository.get_max_user_id_in_posts()
        return {'User_id max in post': user_max_id}

    async def stats_user_posts(self):
        user_posts = await self.stat_repository.get_user_post_counts()
        return [
            {'Username': u[0], 'Posts': u[1]}
            for u in user_posts
        ]

    async def stats_user_maxposts(self):
        user_max_posts = await self.stat_repository.get_user_max_posts()
        return {
            'User_id': user_max_posts[0],
            'Max_posts': user_max_posts[1]
        }

    async def stats_posts_comments(self):
        posts_comments = await self.stat_repository.get_posts_comments_counts()
        return [
            {'post_id': pc[0], 'comments': pc[1]}
            for pc in posts_comments
        ]

    async def stats_posts_likes(self):
        posts_likes = await self.stat_repository.get_posts_likes_counts()
        return [
            {'Post': pl[0], 'Likes': pl[1]}
            for pl in posts_likes
        ]

    async def stats_users_maxcomments(self):
        user_max_comments = await self.stat_repository.get_user_max_comments()
        return {
            'User_id': user_max_comments[0],
            'Comments': user_max_comments[1]
        }

    async def stats_tags(self):
        tags = await self.stat_repository.get_tags_stats()
        return [
            {'Tag_name': tag[0], 'Counter': tag[1]}
            for tag in tags
        ]

    async def stats_posts_tags(self):
        diff_tags_post = await self.stat_repository.get_posts_tags()
        return [
            {'Username': tag[0], 'Tag_name': tag[1]}
            for tag in diff_tags_post
        ]

    async def stats_tag_posts_count(self):
        tag_posts = await self.stat_repository.get_tag_posts_count()
        return [
            {'Tag_name': tp[0], 'Post_counter': tp[1]}
            for tp in tag_posts
        ]

    async def stats_popular_tag(self):
        popular_tag = await self.stat_repository.get_popular_tag()
        return {
            'Tag_name': popular_tag[0],
            'Counter': popular_tag[1]
        }

    async def stats_posts3_likes(self):
        posts3_likes = await self.stat_repository.get_top3_posts_likes()
        return [
            {'Post_id': pl[0], 'Likes': pl[1]}
            for pl in posts3_likes
        ]

    async def stats_users_posts_comments(self):
        user_st = await self.stat_repository.get_users_posts_comments()
        return [
            {'Username': user[0], 'Posts': user[1], 'Comments': user[2]}
            for user in user_st
        ]

    async def stats_users_posts_moretwo(self):
        users = await self.stat_repository.get_users_posts_more_than_two()
        return [
            {'Username': u[0], 'Posts': u[1]}
            for u in users
        ]

    async def stats_posts_comments_more3(self):
        posts = await self.stat_repository.get_posts_comments_more_than3()
        return [
            {'Post_name': p[0], 'Comments': p[1]}
            for p in posts
        ]

    async def stats_posts_tags_more2(self):
        tags_more2 = await self.stat_repository.get_tags_posts_more_than2()
        return [
            {'Post_name': t[0], 'Comments': t[1]}
            for t in tags_more2
        ]

    async def stats_users_commentstop3(self):
        users = await self.stat_repository.get_top3_users_comments()
        return [
            {'Username': u[0], 'Comments': u[1]}
            for u in users
        ]

    async def min_posts_user(self):
        user = await self.stat_repository.get_min_likes_user()
        return {
            'Username': user[0],
            'Likes': user[1]
        }

    async def stats_max_posts_users(self):
        users = await self.stat_repository.get_max_posts_users()
        return [
            {'Username': user[0], 'Posts': user[1]}
            for user in users
        ]

    async def stats_posts_maxlikes(self):
        posts = await self.stat_repository.get_posts_max_likes()
        return [
            {'Post_id': p[0], 'Likes': p[1]}
            for p in posts
        ]

    async def stats_users_posts_more_avg(self):
        user_posts = await self.stat_repository.get_users_posts_more_avg()
        return [
            {'User_id': u[0], 'Posts_counter': u[1]}
            for u in user_posts
        ]

    async def stats_posts_max_comments(self):
        post_comments = await self.stat_repository.get_posts_max_comments()
        return [
            {'Post_id': p[0], 'Comments': p[1]}
            for p in post_comments
        ]

    async def stats_posts_moreavg(self):
        user_moreavg_posts = await self.stat_repository.get_posts_more_avg()
        return [
            {'User_id': u[0], 'Posts_more_thanavg': u[1]}
            for u in user_moreavg_posts
        ]

    async def stats_comments_moreavg(self):
        user_moreavg_comments = await self.stat_repository.get_comments_more_avg()
        return [
            {'User_id': u[0], 'Comments > avg': u[1]}
            for u in user_moreavg_comments
        ]