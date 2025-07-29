import discord
from discord.ext import commands
import subprocess
import threading

# 디스코드 봇 토큰 설정
TOKEN = ''
CHANNEL_ID = 
# 클라이언트 인스턴스 생성
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


def run_external_program1():
    subprocess.run(['C:/Users/rlaej/OneDrive/바탕 화면/Auto_Stock/stock_program.bat'], check=True)

def run_external_program2():
    subprocess.run(['C:/Users/rlaej/OneDrive/바탕 화면/Auto_Stock/'], check=True)


# 봇 준비 완료 이벤트
@bot.event
async def on_ready():
    print(f'투자 봇 준비 완료.')
    channel = bot.get_channel(CHANNEL_ID)
    if channel is not None:
        await channel.send("투자 봇 준비 완료.")
    else:
        print(f'채널 ID {CHANNEL_ID}를 찾을 수 없습니다.')

# 메시지 수신 이벤트
@bot.event
async def on_message(message):
    # 봇 자신이 보낸 메시지는 무시

    if message.author == bot.user:
        return

    # 메시지 내용이 "투자 시작"을 포함하면 배치 파일 실행
    if "모의투자" in message.content:
        try:
            # 배치 파일 실행
            await message.channel.send("프로그램이 성공적으로 실행되었습니다.")
            thread = threading.Thread(target=run_external_program1)
            thread.start()
            thread.join()
            await message.channel.send("프로그램을 종료합니다.")
            
        except subprocess.CalledProcessError as e:
            await message.channel.send(f"프로그램 실행 중 오류가 발생했습니다: {e}")

    if "실전투자" in message.content:
        try:
            # 배치 파일 실행
            await message.channel.send("프로그램이 성공적으로 실행되었습니다.")
            thread = threading.Thread(target=run_external_program2)
            thread.start()
            thread.join()
            await message.channel.send("프로그램을 종료합니다.")
            
        except subprocess.CalledProcessError as e:
            await message.channel.send(f"프로그램 실행 중 오류가 발생했습니다: {e}")
    
# 봇 시작
bot.run(TOKEN)