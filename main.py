import os

from src.bot import Bot


def check_environmental_variable():
    if 'DISCORD_TOKEN' not in os.environ:
        raise Exception('DISCORD_TOKEN is not set')
    else:
        return os.environ['DISCORD_TOKEN']


def main():
    client = Bot()
    client.run(check_environmental_variable())


if __name__ == '__main__':
    main()
