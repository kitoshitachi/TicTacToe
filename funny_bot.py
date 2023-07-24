from random import shuffle
from typing import Union
import discord
from discord.ext import commands
from discord import User, Member
from TicTacToe import TicTacToe
from settings import LIKE_EMOJI, EMOJI

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="!", intents=intents)
MATCH = {}


@client.event
async def on_ready():
	print("I'm alive now")
	print("-------------")


@client.command(name="clear", help="clear all message\n!clear [amount]")
async def clear_message(ctx: commands.Context,
												amount=commands.parameter(
													converter=int,
													default=100,
													description="limit the number of messages",
													displayed_default="100")):
	await ctx.send(f'clearing ...')
	deleted = await ctx.channel.purge(limit=amount, oldest_first=True)
	await ctx.send(f'deleted {len(deleted)} message(s)', delete_after=5)


@client.command(
	name="vs",
	help=
	"challenge one person to a tic tac toe match\n-show is enable display board\n!vs [user] <-show>"
)
async def battle(ctx: commands.Context,
								 player=commands.parameter(
									 converter=Union[User, Member],
									 description="tag the player you wanna challenge"),
								 show=commands.parameter(converter=str,
																				 displayed_default=False,
																				 description="enable show board")):

	if ctx.guild.id in MATCH:
		await ctx.send(f"The game is running !", delete_after=10)
		return

	msg = await ctx.send(
		f"{ctx.author.mention} challenge you ! {player.mention}, do you agree ?")
	for emoji in LIKE_EMOJI:
		await msg.add_reaction(emoji)

	MATCH[ctx.guild.id] = {
		"game": None,
		"temp_msg": None,
		"show": bool("-show" in show)
	}


@client.command(name="a", help="add marks on the board\n!a [column] [row]")
async def add(ctx: commands.Context,
							x=commands.parameter(
								converter=int, description="column position in range [0,2]"),
							y=commands.parameter(converter=int,
																	 description="row position in range [0,2]")):

	if ctx.guild.id not in MATCH:
		await ctx.send(f"{ctx.author.mention}, There are no matches here!",
									 delete_after=10)
		return

	information = MATCH[ctx.guild.id]
	match: TicTacToe = information['game']

	if ctx.author.id not in match.players.values():
		await ctx.send(f"{ctx.author.mention} is not in match", delete_after=10)
	else:
		if x not in range(3) or y not in range(3):
			await ctx.send(f"column or row is invalid! try again in range [0,2]")
			return

		if match.add(ctx.author.id, x, y):
			result = match.check_winner(x, y)
			if result == 1:
				await ctx.send(f"Winner is {ctx.author.mention}")
				match.is_finished = True
				information['show'] = True
			elif result == -1:
				await ctx.send(f"It's tie")
				match.is_finished = True
				information['show'] = True
			elif result == 2:
				await ctx.send(f"Loser is {ctx.author.mention}")
				match.is_finished = True
				information['show'] = True
			else:
				player_id = match.players[match.turn]
				user = await client.fetch_user(player_id)
				msg = await ctx.send(f"It's {user.mention}'s turn")
				for old_msg in information['temp_msg']:
					await old_msg.delete()
				information['temp_msg'] = [msg, ctx.message]

			if information['show'] == True:
				await ctx.send(f"{match.show_board()}")

			if match.is_finished:
				del MATCH[ctx.guild.id]

		else:
			await ctx.send(f"{ctx.author.mention}, It's not ur turn")


@client.event
async def on_reaction_add(reaction: discord.Reaction, user: Union[User,
																																	Member]):
	if user.bot:
		return

	message = reaction.message
	emoji = reaction.emoji

	if emoji == LIKE_EMOJI[0]:
		await message.delete()

		await message.channel.send("The game has started!")
		players = message.mentions
		if len(players) == 1:
			players = [user, user]
		else:
			shuffle(players)

		await message.channel.send(f"{EMOJI[0]} {players[0].mention}")
		await message.channel.send(f"{EMOJI[2]} {players[1].mention}")
		msg = await message.channel.send(f"It's {players[0].mention}'s turn")
		MATCH[message.guild.id]["game"] = TicTacToe(players[0].id, players[1].id)
		MATCH[message.guild.id]["temp_msg"] = [msg]
		pass
	elif emoji == LIKE_EMOJI[1]:
		await message.delete()
		await message.channel.send(
			f"{message.author.mention}, {user.mention} denied !", delete_after=10)
		del MATCH[message.guild.id]
		pass
	else:
		return


import os
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()
keep_alive()

client.run(os.getenv('discord'))
