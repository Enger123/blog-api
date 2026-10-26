from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    posts_key: str
    cache_ttl_seconds: int

def get_settings() -> Settings:
    return Settings(
        posts_key="cache:posts_list",
        cache_ttl_seconds=3600
    )