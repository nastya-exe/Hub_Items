from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



def get_articul_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='Еще образ!', callback_data='another'),
        InlineKeyboardButton(text='Спасибо, Унтра!', callback_data='thanks')
    )
    return builder.as_markup()

def get_back_to_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='Да!', callback_data='retry_look'),
        InlineKeyboardButton(text='Нет', callback_data='back_to_menu')
    )
    return builder.as_markup()

def get_hide_photo_keyboard(look_id: int):
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text='Удалить фото из диалога',
            callback_data=f'hide:{look_id}')
    )
    return builder.as_markup()

def find_album_keyboard(message_ids: list[int]) -> InlineKeyboardMarkup:
    ids_str = ','.join(str(mid) for mid in message_ids)
    return InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text='Удалить фото из диалога', callback_data=f"delete_album:{ids_str}")],
        [InlineKeyboardButton(text='Отправить ещё артикулы', callback_data="send_more_articuls")]
        ]
    )

def remove_button_from_keyboard(keyboard: InlineKeyboardMarkup, text_to_remove: str) -> InlineKeyboardMarkup:
    new_keyboard = []
    for row in keyboard.inline_keyboard:
        new_row = [btn for btn in row if btn.text != text_to_remove]
        if new_row:
            new_keyboard.append(new_row)
    return InlineKeyboardMarkup(inline_keyboard=new_keyboard)

def styles_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='Повседневный', callback_data='usual'),
        InlineKeyboardButton(text='Деловой', callback_data='office')
    )
    builder.row(
        InlineKeyboardButton(text='Вечерний', callback_data='evening')#,
        #InlineKeyboardButton(text='Спортивный', callback_data='sport')
    )
    return builder.as_markup()

def category_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Ещё 5 фото", callback_data="more_photos"),
        InlineKeyboardButton(text="Удалить из диалога", callback_data=f"del_album")
    )
    builder.row(
        InlineKeyboardButton(text="Другая категория", callback_data="to_styles")
    )
    return builder.as_markup()

def style_album_keyboard(photo_ids: list[int], category: str) -> InlineKeyboardMarkup:
    ids_str = ",".join(map(str, photo_ids))
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Ещё 5 фото", callback_data=f"send_more_photos:{category}"),
        InlineKeyboardButton(text="Удалить из диалога", callback_data=f"del_album:{ids_str}")
    )
    builder.row(
        InlineKeyboardButton(text="Другая категория", callback_data="to_styles")
    )
    return builder.as_markup()

def admin_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Статистика", callback_data=f"stats"),
        InlineKeyboardButton(text="Рассылка", callback_data=f"admin:broadcast")
    )
    return builder.as_markup()

