import discord
import os
import asyncio
from keep_alive import keep_alive

intents = discord.Intents.all()
client = discord.Client(intents=intents)

n = 10


@client.event
async def on_ready():
  print("on_ready")
  print(discord.__version__)


# @client.event
# async def on_reaction_add(reaction, user):
#   # やらかしリアクションが10個溜まった場合の処理(旧)
#   if isinstance(
#       reaction.emoji, discord.Emoji
#   ) and reaction.emoji.name == "emoji_40" and reaction.count == n:
#     message = reaction.message
#     channel = message.channel
#     member = message.guild.get_member(message.author.id)
#     new_nickname = "私はやらかしました"
#     await member.edit(nick=new_nickname)
#     await message.reply("やらかしましたねぇ…")


@client.event
async def on_message(message):
  # ニックネームを元に戻すコマンドが入力された際の処理
  if message.content == "?restoreNickname":
    member = message.guild.get_member(message.author.id)
    await member.edit(nick=None)
    sent_message = await message.channel.send(
        f"<:info:1166560475752964107>{member.mention} さんのニックネームを元に戻しました！")
    await asyncio.sleep(3)
    await sent_message.delete()
    await message.delete()
  # 反応するリアクション数を変更するコマンドが入力された際の処理
  elif message.content.startswith("?setReactionCount"):
    global n
    n = int(message.content.split()[1])
    sent_message = await message.channel.send(f"<:info:1166560475752964107>{n}個の<:emoji_40:1166242190029226034>で反応するように設定しました。")
    await asyncio.sleep(3)
    await sent_message.delete()
    await message.delete()

# やらかしリアクションが10個溜まった場合の処理
@client.event
async def on_raw_reaction_add(payload):
  if payload.emoji.name == "emoji_40":
    print("emoji_40が押されました")
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    reaction = discord.utils.get(message.reactions, emoji=payload.emoji)
    if reaction and reaction.count == n:
      member = message.guild.get_member(message.author.id)
      new_nickname = "私はやらかしました"
      await member.edit(nick=new_nickname)
      await message.reply("やらかしましたねぇ...")


keep_alive()
TOKEN = os.getenv("ACCESS_TOKEN")
try:
  client.run(TOKEN)
except:
  os.system("kill 1")
