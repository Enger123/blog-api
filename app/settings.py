from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    posts_key: str

def get_settings() -> Settings:
    return Settings(
        posts_key="cache:posts_list"
    )