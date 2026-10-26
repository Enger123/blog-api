import time
from fastapi import Request
from typing import Callable

async def my_middleware(request: Request, call_next: Callable):
    request.app.state.stats['requests'] += 1
    path = request.url.path
    response = await call_next(request)
    if path.startswith('/users'):
        request.app.state.stats['users'] += 1
    elif path.startswith('/posts'):
        request.app.state.stats['posts'] += 1
    elif path.startswith('/tags'):
        request.app.state.stats['tags'] += 1
    elif path.startswith('/likes'):
        request.app.state.stats['likes'] += 1
    elif path.startswith('/comments'):
        request.app.state.stats['comments'] += 1
    elif path.startswith('/stats'):
        request.app.state.stats['stats'] += 1
    return response
