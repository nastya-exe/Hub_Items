import asyncio
import random
from datetime import datetime, timedelta
#from itertools import count

# from handlers.router_inline_art import router as inline_art_router

from aiogram.filters import Command, BaseFilter, CommandStart
from aiogram import Dispatcher, types, Bot, F
from aiogram.types import TelegramObject, Message, BotCommand, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import database
import stickers_phrases

from stickers_phrases import STICKERS_FIRST, STICKER_DEPENDENCIES
from keyboards.inline_art import get_articul_keyboard
from keyboards.inline_art import get_hide_photo_keyboard
from keyboards.inline_art import get_back_to_menu_keyboard
from keyboards.inline_art import find_album_keyboard
from keyboards.inline_art import remove_button_from_keyboard
from keyboards.inline_art import styles_keyboard
from keyboards.inline_art import style_album_keyboard
from keyboards.inline_art import admin_keyboard


ADMIN_IDS = [1291634715]

dp = Dispatcher(storage=MemoryStorage())
# dp.include_router(inline_art_router)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="get", description="Получить артикулы"),
        BotCommand(command="find", description="Поиск по артикулу"),
        BotCommand(command="styles", description="Образы по стилю")
    ]
    await bot.set_my_commands(commands)


@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    name = message.from_user.first_name
    now = datetime.now()
    user = await database.get_user(user_id)

    if user is None:
        await database.add_user(user_id, name)
        await message.answer_sticker('CAACAgIAAxkBAAEOoddoPyjiw6kDpyxJic76eKbsx2XvuQAChXQAAljm-ElAqE5fcOsNKjYE')
        await message.answer_sticker('CAACAgIAAxkBAAEOodloPyjmUdRg6EiXAwZ3XYo5xjy-wwAC_m4AAiMB-EmxaHRbXT-u5DYE')
        await message.answer('Привет, я Унтра 💫\n'
                             'Я помогу тебе с поиском артикулов и с подбором образа!\n\n'
                             'Тыкай на кнопку, внутри инструкция)')#, reply_markup=main_menu)
        await database.update_last_sticker_time(user_id) # Обновляем время последнего показа стикеров
    else:
        last_seen = datetime.fromisoformat(user[3]) # Получаем дату последнего визита
        last_sticker_start_raw = user[5] # Получаем время последнего показа стикеров

        show_sticker = True
        if last_sticker_start_raw:
            last_sticker_start_time = datetime.fromisoformat(last_sticker_start_raw)
            if (now - last_sticker_start_time) < timedelta(minutes=5):
                show_sticker = False #Если прошло меньше 5 минут, то не показываем стикеры снова

        if last_seen.date() != now.date(): # Если день изменился и первый заход за день
            if show_sticker:
                sticker = random.choice(STICKERS_FIRST)
                second_sticker = STICKER_DEPENDENCIES[sticker]
                await message.answer_sticker(sticker) #Отправляем стикер + приветствие(в первый раз дня)
                await message.answer_sticker(second_sticker)
                await message.answer('Я Унтра, если ты еще не забыл(а), как меня зовут)')#, reply_markup=main_menu)
                await database.update_last_sticker_time(user_id)
            else: # показывать стикер нельзя(по таймеру)
                await message.answer('Тыкай на кнопку, внутри инструкция)')#, reply_markup=main_menu)
        else: #Уже заходил сегодня
                phrase = random.choice(stickers_phrases.start_phrases)
                if show_sticker: # Проверяем, можно ли сейчас показывать стикер (по 5-минутному таймеру)
                    sticker = random.choice(STICKERS_FIRST)
                    second_sticker = STICKER_DEPENDENCIES[sticker]
                    await message.answer_sticker(sticker)
                    await message.answer_sticker(second_sticker)
                    await database.update_last_sticker_time(user_id)
                await message.answer(phrase)#, reply_markup=main_menu)
        await database.update_last_seen(user_id)

class GetLookState(StatesGroup):
    waiting_for_look_number = State()

@dp.message(Command('get'))
async def get_command(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(GetLookState.waiting_for_look_number)
    await message.answer('Отправляй номер образа, а я тебе скину все артикулы\n\nПример ввода: 5 или 118')

class FindLookState(StatesGroup):
    waiting_for_articul = State()

@dp.message(Command('find'))
async def find_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Скидывай артикулы, найду образы в которые они входят)", )
    await state.set_state(FindLookState.waiting_for_articul)

class Styles(StatesGroup):
    look_by_style = State()

@dp.message(Command('styles'))
async def styles_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Есть 4 стиля. Выбирай, какой тебе по душе', reply_markup=styles_keyboard())
    await state.set_state(Styles.look_by_style)

class IsAdmin(BaseFilter):
    async def __call__(self, obj: TelegramObject) -> bool:
        return obj.from_user.id in ADMIN_IDS


class AddLookState(StatesGroup):
    waiting_for_photo = State()
    waiting_for_look_id = State()
    waiting_for_category = State()

@dp.message(Command('admin'))
async def cmd_admin(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Ты в админ-панеле', reply_markup=admin_keyboard())

class AdminState(StatesGroup):
    waiting_for_broadcast_text = State()
    waiting_for_broadcast_media = State()
    confirming_broadcast = State()

# .............................................../GET..........................................................................................................
@dp.message(GetLookState.waiting_for_look_number)
async def receive_look_number(message: Message, state: FSMContext):
    text = message.text.strip()


    if text.startswith('/'):
        await state.clear()
        return
    data = await state.get_data()
    fails = data.get('fails', 0)

    if not text.isdigit():
        fails += 1
        await state.update_data(fails=fails)
        if fails < 2:
            await message.answer('Что-то не то...')
        else:
            await message.answer(
                'Ты точно хочешь ввести номер образа?)))😅',
                reply_markup=get_back_to_menu_keyboard()
            )
        return

    look_id = int(text)
    items = await database.get_articles_looks(look_id)
    photo = await database.get_look_photo(look_id)

    if not items:
        await message.answer('Я еще не добавила артикулы на этот образ(\nПопробуй через какое-то время прислать его еще раз')
        return

    await message.answer_photo(photo, reply_markup=get_hide_photo_keyboard(look_id))

    text = f"<b>Образ №{look_id}:</b>\n\n"
    for name, article in items:
        text += f"<b>{name}</b>: <code>{article}</code>\n"
    await message.answer(text, parse_mode="HTML", reply_markup=get_articul_keyboard())

@dp.callback_query(F.data.startswith('hide:'))
async def hide_photo(callback: CallbackQuery):
    await callback.message.delete()

@dp.callback_query(F.data=='thanks')
async def thanks(callback: CallbackQuery, state: FSMContext):
    phrases = random.choice(stickers_phrases.answer_thanks_phrases)
    await state.clear()
    await callback.message.answer_sticker(stickers_phrases.sticker_7_id)
    await callback.message.answer(phrases)

@dp.callback_query(F.data=='another')
async def another_looks(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.answer('Конечно, присылай еще номер образа')
    await state.set_state(GetLookState.waiting_for_look_number)
    await callback.answer()

@dp.callback_query(F.data=='retry_look')
async def retry_look(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Ахахахах, ну продолжай-продолжай\n\nНапомню, в номерах образов только цифры)')


@dp.callback_query(F.data=='back_to_menu')
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer('Окей, тогда все обнуляем))')

# .............................................../FIND..........................................................................................................
@dp.message(FindLookState.waiting_for_articul)
async def receive_articuls(message: Message, state: FSMContext):
    text = message.text.strip() #Берет текст сообщения от пользователя и убирает пробелы в начале и в конце

    if text.startswith('/'):
        await state.clear()
        return

    # Разбиваем текст на слова и убираем лишние пробелы, запятые
    raw_parts = text.replace(',', ' ').split()
    articuls = [part.strip() for part in raw_parts if part]

    if not articuls:
        await message.answer('Я ничего не поняла 😕\nНапиши один или несколько артикулов, например: 123456, AB001XZ')
        return

    # Получаем список артикулов, которых нет в базе
    missing = []
    existing = []
    for art in articuls:
        exists = await database.check_articul_exists(art)
        if exists:
            existing.append(art)
        else:
            missing.append(art)

    # Если нет ни одного подходящего артикула — выходим
    if not existing:
        await message.answer('Таких артикулов у меня нет, попробуй ещё раз 🧐')
        return

    # Если есть хотя бы один, но не все — сообщаем
    if missing:
        await message.answer(
            f'Некоторые артикулы не нашлись в базе: {", ".join(missing)}'
        )
        return

    # Ищем образы, в которых есть все оставшиеся артикулы
    look_ids = await database.get_looks_for_articul(existing)

    if not look_ids:
        await message.answer('Образа с такой комбинацией артикулов я пока не собрала 😔')
        return

    media = []
    look_ids_formatted = []

    for idx, look_id in enumerate(look_ids):
        photo = await database.get_look_photo(look_id)
        if not photo:
            continue
        if idx == 0:
            media.append(InputMediaPhoto(media=photo, caption="Образы, которые тебе подойдут:"))
        else:
            media.append(InputMediaPhoto(media=photo))

        look_ids_formatted.append(f"Образ №{str(look_id).zfill(3)}")

    sent_messages = await message.answer_media_group(media)
    photo_message_ids = [msg.message_id for msg in sent_messages]

    caption_text = ', '.join(look_ids_formatted)

    await message.answer(
        text=caption_text,
        reply_markup=find_album_keyboard(photo_message_ids)
    )
    await state.clear()

@dp.callback_query(F.data.startswith('delete_album'))
async def delete_album(callback: CallbackQuery):
    ids_raw = callback.data.split(':')[1]
    ids = [int(mid) for mid in ids_raw.split(',')]

    for mid in ids:
        try:
            await callback.bot.delete_message(callback.message.chat.id, mid)
        except Exception as e:
            print(f"Не смог удалить сообщение {mid}: {e}")
            continue

    markup = callback.message.reply_markup
    updated_markup = remove_button_from_keyboard(markup, 'Удалить фото из диалога')
    await callback.message.edit_reply_markup(reply_markup=updated_markup)

@dp.callback_query(F.data.startswith('send_more_articuls'))
async def send_more_articuls(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.answer('Отправляй - отправляй')
    await state.set_state(FindLookState.waiting_for_articul)
    await callback.answer()

# .............................................../STYLES..........................................................................................................

@dp.callback_query(F.data == 'usual')
async def usual_style(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_reply_markup()
    await callback.message.answer("Хорошо, сейчас тебе пришлю 5 образов")

    photos = await database.get_category_photo('usual')
    media = [InputMediaPhoto(media=photo_url) for photo_url, _ in photos]
    look_ids = [look_id for _, look_id in photos]

    album_messages = await callback.message.answer_media_group(media)
    photo_message_ids = [msg.message_id for msg in album_messages]

    await callback.message.answer(
        "Могу отправить еще 5 фотографий или перейдем в другую категорию",
        reply_markup=style_album_keyboard(photo_message_ids, 'usual')
    )

    await state.update_data(seen_looks=look_ids)

@dp.callback_query(F.data=='office')
async def office_style(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_reply_markup()
    await callback.message.answer('Хорошо, сейчас тебе пришлю 5 образов')

    photos = await database.get_category_photo('office')
    media = [InputMediaPhoto(media=photo_url) for photo_url, _ in photos]
    look_ids = [look_id for _, look_id in photos]

    album_messages = await callback.message.answer_media_group(media)
    photo_message_ids = [msg.message_id for msg in album_messages]
    await callback.message.answer(
        "Могу отправить еще 5 фотографий или перейдем в другую категорию",
        reply_markup=style_album_keyboard(photo_message_ids, 'office')
    )

    await state.update_data(seen_looks=look_ids)

@dp.callback_query(F.data=='evening')
async def evening_style(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_reply_markup()
    await callback.message.answer('Хорошо, сейчас тебе пришлю 5 образов')

    photos = await database.get_category_photo('evening')
    media = [InputMediaPhoto(media=photo_url) for photo_url, _ in photos]
    look_ids = [look_id for _, look_id in photos]

    album_messages = await callback.message.answer_media_group(media)
    photo_message_ids = [msg.message_id for msg in album_messages]
    await callback.message.answer(
        "Могу отправить еще 5 фотографий или перейдем в другую категорию",
        reply_markup=style_album_keyboard(photo_message_ids, 'evening')
    )

    await state.update_data(seen_looks=look_ids)

@dp.callback_query(F.data=='to_styles')
async def new_cat(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer('Есть 4 стиля. Выбирай, какой тебе по душе',
                                  reply_markup=styles_keyboard())
    await state.set_state(Styles.look_by_style)

@dp.callback_query(F.data.startswith("send_more_photos:"))
async def send_more_photos(callback: CallbackQuery, state: FSMContext):
    category = callback.data.split(":")[1]

    data = await state.get_data()
    seen_ids = data.get("seen_looks", [])

    photos_rows = await database.get_category_photo(category, exclude_ids=seen_ids)

    if not photos_rows:
        await callback.message.answer("Все образы этой категории ты уже видел(а)")
        return

    media = []
    new_ids = []

    for photo_url, look_id in photos_rows:
        media.append(InputMediaPhoto(media=photo_url))
        new_ids.append(look_id)

    album_messages = await callback.message.answer_media_group(media)
    photo_message_ids = [msg.message_id for msg in album_messages]

    await callback.message.answer(
        f"Ещё образы категории «{category}»",
        reply_markup=style_album_keyboard(photo_message_ids, category)
    )
    await state.update_data(seen_looks=seen_ids + new_ids)
    await callback.answer()

@dp.callback_query(F.data.startswith('del_album'))
async def delete_album(callback: CallbackQuery):
    ids_raw = callback.data.split(':')[1]
    ids = [int(mid) for mid in ids_raw.split(',')]

    for mid in ids:
        try:
            await callback.bot.delete_message(callback.message.chat.id, mid)
        except Exception as e:
            print(f"Не смог удалить сообщение {mid}: {e}")
            continue

# .............................................../ADMIN..........................................................................................................

#Статистика
@dp.callback_query(F.data =='stats')
async def stats(callback: CallbackQuery):
    count_users = await database.stats_count()
    await callback.message.answer(f'Всего пользователей: {count_users}')

#Рассылка
@dp.callback_query(F.data =='admin:broadcast')
async def broadcast(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer('Текст рассылки:')
    await callback.message.answer('Текст рассылки:')
    await callback.message.answer('Текст рассылки:')
    await state.set_state(AdminState.waiting_for_broadcast_text)
    await callback.answer()

@dp.message(AdminState.waiting_for_broadcast_text)
async def handle_broadcast_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer("Теперь отправь фото для рассылки. /skip, если не нужно)")
    await state.set_state(AdminState.waiting_for_broadcast_media)

@dp.message(AdminState.waiting_for_broadcast_media, F.photo)
async def handle_broadcast_photo(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)
    await message.answer("Готово. Подтвердить рассылку? /send или /cancel")
    await state.set_state(AdminState.confirming_broadcast)

@dp.message(AdminState.waiting_for_broadcast_media, Command("skip"))
async def skip_photo(message: Message, state: FSMContext):
    await message.answer("Ок, только текст. Подтвердить? /send или /cancel")
    await state.set_state(AdminState.confirming_broadcast)

@dp.message(Command("send"))
async def start_broadcast(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    text = data.get("text")
    photo = data.get("photo")

    user_ids = await database.get_all_user_ids()
    sent = 0

    for user_id in user_ids:
        try:
            if photo:
                await bot.send_photo(user_id, photo=photo, caption=text)
            else:
                await bot.send_message(user_id, text)

            await asyncio.sleep(0.2)  # пауза!
            sent += 1
        except Exception as e:
            print(f"Не удалось {user_id}: {e}")
            continue

    await message.answer(f"Рассылка завершена. Отправлено {sent}")
    await state.clear()




async def main():
    bot = Bot(token='7869415583:AAFxgbZ4cg9shyJbZnCKThQUPj7m4IAWC8o')
    await set_commands(bot)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())