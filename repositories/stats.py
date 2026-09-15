from models import Post, User, Comment, Like, Tag, TagPost
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


class StatRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_posts_count(self):
        result = await self.db.execute(select(func.count(Post.id)))
        return result.scalars().first()

    async def get_all_users(self):
        result = await self.db.execute(select(User.id))
        return result.scalars().all()

    async def get_max_user_id_in_posts(self):
        result = await self.db.execute(select(func.max(Post.user_id)))
        return result.scalars().all()

    async def get_user_post_counts(self):
        result = await self.db.execute(
            select(User.username, func.count(Post.id))
            .outerjoin(Post)
            .group_by(User.id)
        )
        return result.all()

    async def get_user_max_posts(self):
        result = await self.db.execute(
            select(Post.user_id, func.count(Post.id))
            .group_by(Post.user_id)
            .order_by(func.count(Post.id).desc())
        )
        return result.first()

    async def get_posts_comments_counts(self):
        result = await self.db.execute(
            select(Comment.post_id, func.count(Comment.id))
            .group_by(Comment.post_id)
        )
        return result.all()

    async def get_posts_likes_counts(self):
        result = await self.db.execute(
            select(Post.id, func.count(Like.id))
            .outerjoin(Like)
            .group_by(Post.id)
        )
        return result.all()

    async def get_user_max_comments(self):
        result = await self.db.execute(
            select(User.id, func.count(Comment.id))
            .join(Comment)
            .group_by(User.id)
            .order_by(func.count(Comment.id).desc())
        )
        return result.first()

    async def get_tags_stats(self):
        result = await self.db.execute(
            select(Tag.name, func.count(TagPost.id))
            .outerjoin(TagPost)
            .group_by(Tag.id)
            .order_by(func.count(TagPost.id).desc())
        )
        return result.all()

    async def get_posts_tags(self):
        result = await self.db.execute(
            select(User.username, Tag.name)
            .join(Post)
            .join(TagPost)
            .join(Tag)
            .distinct()
        )
        return result.all()

    async def get_tag_posts_count(self):
        result = await self.db.execute(
            select(Tag.name, func.count(TagPost.id))
            .outerjoin(TagPost)
            .group_by(Tag.name)
            .order_by(func.count(TagPost.id))
        )
        return result.all()

    async def get_popular_tag(self):
        result = await self.db.execute(
            select(Tag.name, func.count(TagPost.id))
            .join(TagPost)
            .group_by(Tag.id)
            .order_by(func.count(TagPost.id).desc())
        )
        return result.first()

    async def get_top3_posts_likes(self):
        result = await self.db.execute(
            select(Post.id, func.count(Like.id))
            .join(Like)
            .group_by(Post.id)
            .order_by(func.count(Like.id).desc())
            .limit(3)
        )
        return result.all()

    async def get_users_posts_comments(self):
        result = await self.db.execute(
            select(User.username, func.count(Post.id), func.count(Comment.id))
            .select_from(User)
            .join(Post, Post.user_id==User.id)
            .join(Comment, Comment.user_id==User.id)
            .group_by(User.id)
        )
        return result.all()

    async def get_users_posts_more_than_two(self):
        result = await self.db.execute(
            select(User.username, func.count(Post.id))
            .outerjoin(Post)
            .group_by(User.id)
            .having(func.count(Post.id) > 2)
            .order_by(func.count(Post.id).desc())
        )
        return result.all()

    async def get_posts_comments_more_than3(self):
        result = await self.db.execute(
            select(Post.title, func.count(Comment.id))
            .outerjoin(Comment)
            .group_by(Post.id)
            .having(func.count(Comment.id) > 3)
        )
        return result.all()

    async def get_tags_posts_more_than2(self):
        result = await self.db.execute(
            select(Tag.name, func.count(TagPost.id))
            .outerjoin(TagPost)
            .group_by(Tag.id)
            .having(func.count(TagPost.id) > 2)
        )
        return result.all()

    async def get_top3_users_comments(self):
        result = await self.db.execute(
            select(User.username, func.count(Comment.id))
            .join(Comment)
            .group_by(User.id)
            .order_by(func.count(Comment.id).desc())
            .limit(3)
        )
        return result.all()

    async def get_min_likes_user(self):
        result = await self.db.execute(
            select(User.username, func.count(Like.id))
            .outerjoin(Like)
            .group_by(User.id)
            .order_by(func.count(Like.id))
        )
        return result.first()

    async def get_max_posts_users(self):
        result = await self.db.execute(
            select(User.username, func.count(Post.id))
            .outerjoin(Post)
            .group_by(User.id)
        )
        return result.all()

    async def get_posts_max_likes(self):
        like_stats = (
            select(
                Like.post_id,
                func.count(Like.id).label("likes_counter")
            )
            .group_by(Like.post_id)
            .subquery()
        )

        max_likes_result = await self.db.execute(
            select(func.max(like_stats.c.likes_counter))
        )
        max_likes = max_likes_result.scalars().first()

        posts_result = await self.db.execute(
            select(like_stats.c.post_id, like_stats.c.likes_counter)
            .where(like_stats.c.likes_counter == max_likes)
        )
        return posts_result.all()

    async def get_users_posts_more_avg(self):
        post_stats = (
            select(
                Post.user_id,
                func.count(Post.id).label("post_counter")
            )
            .group_by(Post.user_id)
            .subquery()
        )

        avg_result = await self.db.execute(
            select(func.avg(post_stats.c.post_counter))
        )
        avg_user_posts = avg_result.scalars().first()

        user_posts_result = await self.db.execute(
            select(post_stats.c.user_id, post_stats.c.post_counter)
            .where(post_stats.c.post_counter > avg_user_posts)
        )
        return user_posts_result.all()

    async def get_posts_max_comments(self):
        comments_stats = (
            select(
                Comment.post_id,
                func.count(Comment.id).label("comments_counter")
            )
            .group_by(Comment.post_id)
            .subquery()
        )

        max_comments_result = await self.db.execute(
            select(func.max(comments_stats.c.comments_counter))
        )
        max_comments = max_comments_result.scalars().first()

        post_comments_result = await self.db.execute(
            select(comments_stats.c.post_id, comments_stats.c.comments_counter)
            .where(comments_stats.c.comments_counter == max_comments)
        )
        return post_comments_result.all()

    async def get_posts_more_avg(self):
        posts_stats = (
            select(
                User.id,
                func.count(Post.id).label("post_counter")
            )
            .outerjoin(Post, User.id == Post.user_id)
            .group_by(User.id)
            .subquery()
        )

        avg_result = await self.db.execute(
            select(func.avg(posts_stats.c.post_counter))
        )
        avg_posts = avg_result.scalars().first()

        user_moreavg_result = await self.db.execute(
            select(posts_stats.c.id, posts_stats.c.post_counter)
            .where(posts_stats.c.post_counter > avg_posts)
        )
        return user_moreavg_result.all()

    async def get_comments_more_avg(self):
        comments_stats = (
            select(
                User.id.label("user_id"),
                func.count(Comment.id).label("comments_counter")
            )
            .outerjoin(Comment, User.id == Comment.user_id)
            .group_by(User.id)
            .subquery()
        )

        avg_result = await self.db.execute(
            select(func.avg(comments_stats.c.comments_counter))
        )
        comments_avg = avg_result.scalars().first()

        user_moreavg_result = await self.db.execute(
            select(comments_stats.c.user_id, comments_stats.c.comments_counter)
            .where(comments_stats.c.comments_counter > comments_avg)
        )
        return user_moreavg_result.all()