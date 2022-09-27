# CG_tournament_bot

## Description

The goal of this script is to handle a tournament in coding_game.
__

## Needed

- Python version: `3.10`
- Conda

_

## Installation

- `conda create -y --name CG_tournament_bot_3_10 python=3.10`
- `conda activate CG_tournament_bot_3_10`
- `pip install -r requirements.txt`*
- Add the environment variable `DISCORD_TOKEN` with the value of the token of the bot.

_

## Running

- Run `python -m main`.
- The script should run normally.

## Command

| Command | Arguments | Description|
|--|--|--|
| `!start_tournament` | `None` | Start a tournament |
| `!add_exercise` | `URL` | Add an exercise to the current tournament. Just pass the full `URL` to the command |
| `!get_exercises` | `None` | Get all exercise from the current tournament|
| `!end_tournament` | `None` | End the current tournament|
| `!get_score` | `None` | Get the score of the current tournament|

