from aiogram import Bot, Dispatcher, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode

from database import SessionLocal
from models import Transaction
import asyncio

from pdf_utils import generate_pdf
import os

bot = Bot(token="ТВОЙ_ТОКЕН", parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

class FinanceForm(StatesGroup):
    type = State()
    amount = State()
    category = State()
    description = State()

@dp.message(commands=["start"])
async def cmd_start(message: Message):
    await message.answer("Привет! Я помогу тебе учитывать доходы и расходы.\n\nНапиши /add чтобы внести новую запись.")

@dp.message(commands=["add"])
async def cmd_add(message: Message, state: FSMContext):
    await state.set_state(FinanceForm.type)
    await message.answer("Это доход или расход? Напиши <b>доход</b> или <b>расход</b>.")

@dp.message(FinanceForm.type)
async def process_type(message: Message, state: FSMContext):
    text = message.text.lower()
    if text not in ("доход", "расход"):
        return await message.answer("Пожалуйста, напиши только <b>доход</b> или <b>расход</b>.")
    await state.update_data(type=text)
    await state.set_state(FinanceForm.amount)
    await message.answer("Теперь введи сумму:")

@dp.message(FinanceForm.amount)
async def process_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text.replace(",", "."))
        await state.update_data(amount=amount)
        await state.set_state(FinanceForm.category)
        await message.answer("Укажи категорию (например: аренда, реклама, услуги):")
    except ValueError:
        await message.answer("Сумма должна быть числом. Попробуй ещё раз:")

@dp.message(FinanceForm.category)
async def process_category(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    await state.set_state(FinanceForm.description)
    await message.answer("Добавь описание или напиши - чтобы пропустить:")

@dp.message(FinanceForm.description)
async def process_description(message: Message, state: FSMContext):
    data = await state.get_data()
    description = message.text if message.text != "-" else ""
    data["description"] = description

    # Сохраняем в БД
    async with SessionLocal() as session:
        transaction = Transaction(
            user_id=message.from_user.id,
            type=data["type"],
            amount=data["amount"],
            category=data["category"],
            description=description
        )
        session.add(transaction)
        await session.commit()

    await message.answer(
        f"✅ Запись сохранена:\n"
        f"<b>{data['type'].capitalize()}</b> — {data['amount']}₽\n"
        f"Категория: {data['category']}\n"
        f"Описание: {description or '—'}"
    )
    await state.clear()

@dp.message(commands=["report"])
async def send_report(message: types.Message):
    async with SessionLocal() as session:
        result = await session.execute(
            select(Transaction).where(Transaction.user_id == message.from_user.id).order_by(Transaction.created_at)
        )
        transactions = result.scalars().all()

        if not transactions:
            return await message.answer("У тебя пока нет записей.")

        file_path = f"report_{message.from_user.id}.pdf"
        generate_pdf(transactions, file_path)

        await message.answer_document(types.FSInputFile(file_path), caption="Твой PDF-отчёт 📄")
        os.remove(file_path)