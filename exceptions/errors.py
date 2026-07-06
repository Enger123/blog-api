class PostNotFound(Exception):
    def __init__(self):
        super().__init__('Post not found')