import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from dotenv import find_dotenv, load_dotenv
import os
from aiogram.types import Message, ContentType
from aiogram import types
from PIL import Image, ImageFilter
from io import BytesIO
from pydub import AudioSegment

load_dotenv(find_dotenv())
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привіт! Надішліть мені фотографію або звукове повідомлення для обробки.")

@dp.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Цей бот може обробляти фотографії та звукові повідомлення.')

@dp.message(content_types=ContentType.PHOTO)
async def handle_photo(message: Message):
    photo = await message.photo[-1].download(destination=BytesIO())
    photo.seek(0)
    image = Image.open(photo)
    processed_image = image.filter(ImageFilter.BLUR)
    
    output = BytesIO()
    processed_image.save(output, format="JPEG")
    output.seek(0)

    await message.answer_photo(photo=output, caption="Ось ваша оброблена фотографія!")

@dp.message(content_types=ContentType.VOICE)
async def handle_voice(message: Message):
    voice = await message.voice.download(destination=BytesIO())
    voice.seek(0)
    audio = AudioSegment.from_file(voice)

    processed_audio = audio.speedup(playback_speed=1.5)
    
    output = BytesIO()
    processed_audio.export(output, format="ogg")
    output.seek(0)

    await message.answer_voice(voice=output, caption="Ось ваше оброблене звукове повідомлення!")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
