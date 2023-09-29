# 공부 디스코드 서버 유지 및 보수를 위한 디스코드 봇 '0Bu'
# 개발 │ 석지우
# All rights reserved. © 2023. 석지우
# 개발자의 허락 없이 무단 배포 및 무단 수정을 허용합니다 ^^ 

import os
import discord
import datetime
import pytz
import random
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True
bot = commands.Bot(command_prefix = "공부야 ", intents=discord.Intents.all()) 

bot.remove_command('help') # 쓸모없는 기본 탑재 명령어 삭제

@bot.event 
async def on_message(message):
    if message.author.bot:
        return None
    if message.content == '공부야':
        replies = ['네?', '반갑습니다!', '저 살아있어요!', '열공']
        reply = random.choice(replies)
        await message.channel.send(reply)
    elif message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)



@bot.event # 'on_ready' - 봇을 켜는 이벤트
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="공부야"))
    os.system('cls')
    print('-------------------------')
    print(f'Network Status : {round(round(bot.latency, 4)*1000)}ms')
    print(f'Bot ID : {bot.user.id}')
    print('-------------------------')
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} commands have been available.")
    except Exception as e:
        print(f"Error: {e}")
    print("　")
    print("　")
    print(" ----- Logs -----")




@bot.tree.command(name="상태", description="네트워크 상태를 확인합니다.") # '상태' - 봇의 네트워크 상태를 embed로 대답하는 명령어입니다.
async def network_status(interaction: discord.Interaction):
    if bot.latency * 1000 >= 100:
        not_good = discord.Embed(title= "**🔴 이상 🔴**", description= f"현재 네트워크 지연시간은 **{round(round(bot.latency, 4)*1000)}ms** 이므로, 석지우에게 관리를 요청하세요.", timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0xff0000)
        await interaction.response.send_message(embed=not_good)
    else:
        good = discord.Embed(title= "**🟢 정상 🟢**", description= f"현재 네트워크 지연시간은 **{round(round(bot.latency, 4)*1000)}ms** 으로, 정상입니다.", timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0x00ff00)
        await interaction.response.send_message(embed=good)

    log_channel = bot.get_channel(1157241419518459974)
    await log_channel.send(f"{interaction.user.mention} 이(가)   */상태*   명령어를 사용함.")



@bot.tree.command(name="공지", description="/공지 [내용] | ⚙️") # '공지' - 공지 채널에 내용을 공지합니다.
@app_commands.describe(내용="공지 내용")
@commands.has_permissions(administrator=True)
async def notice(interaction: discord.Interaction, 내용: str, 멘션: bool = False):
    log_channel = bot.get_channel(1157241419518459974)
    await log_channel.send(f"{interaction.user.mention} 이(가)   */공지*   명령어를 사용함.")
    channel = bot.get_channel(1157244212740370522)

    if channel is None:
        await interaction.response.send_message('공지 채널을 찾을 수 없습니다.')
        return
    
    if 멘션 == True:
        embed=discord.Embed(title="🔔 **공지** 🔔", description=f"\n\n {내용} \n\n||@everyone||", timestamp= datetime.datetime.now(pytz.timezone('UTC')), color= 0xFF6633)
        await channel.send(embed=embed)
        await interaction.response.send_message('공지를 전송했습니다.', ephemeral=True)
    else:
        embed=discord.Embed(title="🔔 **공지** 🔔", description=f"\n\n {내용} \n\n", timestamp= datetime.datetime.now(pytz.timezone('UTC')), color= 0xFF6633)
        await channel.send(embed=embed)
        await interaction.response.send_message('공지를 전송했습니다.', ephemeral=True)

@notice.error
async def notice_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingPermissions):
        log_channel = bot.get_channel(1157241419518459974)
        await log_channel.send(f"{interaction.user.mention} 이(가)   */공지*   명령어를 사용하였으나, 관리자 권한이 없으므로 거부당했습니다.")

        embed = discord.Embed(title='❌거부❌', description='당신은 관리자 권한이 없습니다.', color=0xff0000)
        await interaction.response.send_message(embed=embed)



@bot.tree.command(name="청소", description="/청소 [1 이상의 자연수] | ⚙️") # '청소' - 채널의 메시지를 삭제합니다.
@commands.has_permissions(administrator=True)
@app_commands.describe(amount="청소할 메시지의 개수")
async def clear_chat(interaction: discord.Interaction, amount: int):
    log_channel = bot.get_channel(1157241419518459974)
    await log_channel.send(f"{interaction.user.mention} 이(가)   */청소*   명령어를 사용함.")
    
    if amount < 1 :
        embed = discord.Embed(title='*오류!*', description='1 이상의 자연수를 입력해주세요.', color=0xff0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message("청소를 시작합니다...")
        await interaction.channel.purge(limit=amount + 1)
        embed = discord.Embed(title= "🧹 **채팅 청소** 🧹", description= f"__{amount}__ 개의 메시지를 청소했습니다. \n 　", timestamp= datetime.datetime.now(pytz.timezone('UTC')), color= 0x99ffff)
        embed.add_field(name= "*처리자*", value= f"<@{interaction.user.id}>", inline= False)
        await interaction.channel.send(embed=embed)

@clear_chat.error
async def clear_chat_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingPermissions):
        log_channel = bot.get_channel(1157241419518459974)
        await log_channel.send(f"{interaction.user.mention} 이(가)   */청소*   명령어를 사용하였으나, 관리자 권한이 없으므로 거부당했습니다.")

        embed = discord.Embed(title='❌거부❌', description='당신은 관리자 권한이 없습니다.', color=0xff0000)
        await interaction.response.send_message(embed=embed)



@bot.tree.command(name="credit", description="크레딧")
async def credit(interaction: discord.Interaction):
    embed = discord.Embed(title='🎖️ **크레딧** 🎖️', description='서버 관리봇, "0Bu"입니다. \n 편하게 공부라고 불러주세요!', color=0xffffff)
    embed.add_field(name='개발자', value='`dev_maco`', inline=False)
    embed.add_field(name='개발 언어', value='`Python`', inline=False)
    embed.add_field(name='개발 라이브러리', value='`discord.py`', inline=False)
    embed.add_field(name='소스 코드', value='https://github.com/seokjw0727/0Bu'  )
    embed.set_footer(text='*All rights reserved. © 2023. 석지우*')
    await interaction.response.send_message(embed=embed, ephemeral=True)



@bot.event # 'on_voice_state_update' 이벤트, 유저가 채널에 접속하면 알림.
async def on_voice_state_update(member, before, after):
    # 채널
    chat_channel = bot.get_channel(1157241419518459974) # 0Bu_log 채널
    voice_plaza = bot.get_channel(1157309186548432917) # 광장 채널
    voice_study = bot.get_channel(1157309089622282260) # 공부 채널

    if before.channel is None and after.channel is not None:
        if after.channel is voice_plaza: 
            await chat_channel.send(f"{member.mention} 이(가) __⛲광장__ 채널에 접속했습니다.")
        elif after.channel is voice_study:
            await chat_channel.send(f"{member.mention} 이(가) __📚공부__ 채널에 접속했습니다.")



load_dotenv()
load_dotenv('.env')
bot.run(os.getenv('TOKEN'))
