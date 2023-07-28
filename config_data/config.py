from dataclasses import dataclass

from environs import Env


@dataclass
class Authentication:
    email: str
    password: str


@dataclass
class Config:
    auth: Authentication


# Создаем функцию, которая будет читать файл .env и возвращать
# экземпляр класса Config с заполненными полями token и admin_ids
def load_config(path: str | None = None):
    env = Env()
    env.read_env(path)
    return Config(auth=Authentication(
        email=env('email'),
        password=env('password')))


if __name__ == '__main__':
    config = load_config()
    print(config)
