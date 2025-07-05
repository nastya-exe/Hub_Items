start_phrases = [
    "Снова ты! Чем займёмся?",
    "Ура! Любимый собеседник на связи!",
    "Как могу тебе помочь?",
    "Я уже успела заскучать, что сейчас будем делать?",
    "Привет-привет, давно не виделись!"]

answer_thanks_phrases = [
    'Рада помочь!',
    'Ты знаешь, где меня найти)',
    'Обращайся',
    'Ой, как мило, пожалуйста!',
    'Заходи ко мне еще)',
]

sticker_1_id = 'CAACAgIAAxkBAAEOrKNoR-RnNgtcd2uS_mFTf7aW-uDzEwAC63IAAn2GQUovOslwdJwkWDYE'
sticker_1_b_id = 'CAACAgIAAxkBAAEOrKVoR-RqBgOOkA8aDtJ2JapWFnWdyAACh34AAsHGQUq8o-X7yDeeTjYE' # стоит полубоком, трогает ухо
sticker_2_id = 'CAACAgIAAxkBAAEOrXRoSFUwtb2jsIRJeCw7nzOdJ-4zSAACxn0AAjRiQEqD23cgOqmTKDYE'
sticker_2_b_id = 'CAACAgIAAxkBAAEOrXZoSFUyHWFKkKfGj6zRrdWP4-halgACjGsAAraQSUo7I-HohdpDzzYE' # Стоит руки скрестила, стесняется
sticker_3_id = 'CAACAgIAAxkBAAEOrKdoR-Ss124jjpIHYO9sHhbFhrh8ZAACImkAAokwQUqSjXxfN4j1EzYE'
sticker_3_b_id = 'CAACAgIAAxkBAAEOrKhoR-Stq0aVKVaI4W6alKhNV6T5DAACxmoAAt28QUq-1JBy0CAfOzYE' # показывает язык
# sticker_4_id = ''
# sticker_4_b_id = ''
# sticker_5_id = ''
# sticker_5_b_id = ''

sticker_7_id = 'CAACAgIAAxkBAAEOrKFoR-Lk7c3J3LpNAtl8j3yKyh07OwACfnMAAj3tQErYsJWS513XXzYE' #1 стикер, тянется обниматься

STICKERS_FIRST = [sticker_1_id, sticker_2_id, sticker_3_id]#, sticker_4_id, sticker_5_id]
STICKER_DEPENDENCIES = {sticker_1_id: sticker_1_b_id, sticker_2_id: sticker_2_b_id,
    sticker_3_id: sticker_3_b_id}#, sticker_4_id: sticker_4_b_id, sticker_5_id: sticker_5_b_id}