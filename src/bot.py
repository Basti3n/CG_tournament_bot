from dataclasses import dataclass, field

import discord
from discord.ext import commands

from src.tournament import Tournament


@dataclass
class Bot(commands.Bot):
    o_tournament: Tournament = field(init=False, default=Tournament())

    def __post_init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        super(Bot, self).__init__(command_prefix='!', intents=intents)
        self.add_commands()

    @staticmethod
    async def on_ready() -> None:
        print('Bot is ready')

    def add_commands(self):
        @self.command(name='start_tournament', pass_context=True)
        async def start_tournament(ctx: commands.Context) -> None:
            if not self.o_tournament.b_is_running:
                o_embed_message = discord.Embed(title='Tournament', description='The tournament has started',
                                                color=discord.Color.green())
                self._add_header_to_embed(o_embed_message)
                await ctx.channel.send(embed=o_embed_message)
                self.o_tournament.start_tournament()
            else:
                await ctx.channel.send('Tournament already running')

        @self.command(name='end_tournament', pass_context=True)
        async def end_tournament(ctx: commands.Context) -> None:
            if self.o_tournament.b_is_running:
                o_embed_message = discord.Embed(title='Tournament', description='The tournament has finished',
                                                color=discord.Color.green())
                self._add_header_to_embed(o_embed_message)
                await ctx.channel.send(embed=o_embed_message)
                self.o_tournament.end_tournament()
                await ctx.channel.send(embed=self._format_current_result())

            else:
                await ctx.channel.send('No tournament running')

        @self.command(name='add_exercise', pass_context=True)
        async def add_exercise_to_tournament(ctx: commands.Context) -> None:
            if self.o_tournament.b_is_running:
                s_exercise_url = ctx.message.content.split(' ')[1]
                s_exercise_id = self.o_tournament.add_exercise(s_exercise_url)
                o_embed_message = discord.Embed(title='Tournament', description='Added new exercise',
                                                color=discord.Color.green())
                self._add_header_to_embed(o_embed_message)
                self._format_regular_text(o_embed_message, s_exercise_id, s_exercise_url)
                await ctx.channel.send(embed=o_embed_message)
            else:
                await ctx.channel.send('No tournament running')

        @self.command(name='get_exercises', pass_context=True)
        async def get_exercises(ctx: commands.Context) -> None:
            if self.o_tournament.b_is_running:
                o_embed_message = discord.Embed(title='Tournament', description='All current exercise(s)',
                                                color=discord.Color.green())
                self._add_header_to_embed(o_embed_message)
                for dc_exercise in self.o_tournament.get_exercises():
                    self._format_regular_text(o_embed_message, dc_exercise['exercise_id'],
                                              dc_exercise['exercise_url'])
                await ctx.channel.send(embed=o_embed_message)
            else:
                await ctx.channel.send('No tournament running')

        @self.command(name='get_score', pass_context=True)
        async def get_score(ctx: commands.Context) -> None:
            if self.o_tournament.b_is_running:
                await ctx.channel.send(embed=self._format_current_result())
            else:
                await ctx.channel.send('No tournament running')

    def _format_current_result(self) -> discord.Embed:
        l_result = self.o_tournament.get_current_score()
        if l_result:
            o_embed_message = discord.Embed(title='Current score', description='The current game result is',
                                            color=discord.Color.green())
            self._add_header_to_embed(o_embed_message)
            for i_index in range(len(l_result)):
                if i_index == 0:
                    self._format_regular_text(o_embed_message, f'{l_result[i_index].split(":")[0]} :crown:',
                                              f'{l_result[i_index].split(":")[1]} point(s)')
                else:
                    self._format_regular_text(o_embed_message, l_result[i_index].split(':')[0],
                                              f'{l_result[i_index].split(":")[1]} point(s)')
            o_embed_message.set_footer(text='The game is not over !!')
            return o_embed_message
        else:
            o_embed_message = discord.Embed(title='Tournament', description='There is no result yet',
                                            color=discord.Color.green())
            self._add_header_to_embed(o_embed_message)
            return o_embed_message

    def _format_regular_text(self, o_embed_message: discord.Embed, s_name: str, s_value: str) -> None:
        o_embed_message.add_field(name=s_name, value=s_value, inline=False)
        self._add_header_to_embed(o_embed_message)

    @staticmethod
    def _add_header_to_embed(o_embed_message: discord.Embed) -> None:
        o_embed_message.set_thumbnail(url='https://static.codingame.com/assets/favicon_16_16.6776a532.png')
        o_embed_message.set_author(name='CG Tournament Bot', url='https://github.com/Basti3n/CG_tournament_bot',
                                   icon_url='https://cdn-icons-png.flaticon.com/512/4712/4712139.png')
