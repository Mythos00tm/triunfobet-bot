import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN_TELEGRAM = "8959520494:AAEjYsnz81f6KD5HDlII_05PH-I3-CAydQs"

CONFIG_ESTRATEGIA = {
    "monto_apuesta_base": 1000,
    "capital_inicial": 10000,
    "meta_capital_stop": 50000,
    "min_jugadores": 1650,
    "min_multiplicador_1": 2.16,
    "analizar_top_8": True,
    "max_diferencia_escalon": 50000,
    "min_monto_p8": 10000,
    "cashout_estandar": 2.00,
    "cashout_extendido_liquidez": 3.45,
    "activar_sniper_394": True,
    "target_sniper": 3.94,
    "min_jugadores_sniper": 2000,
    "pausa_por_3_rojos": True
}

bot = Bot(token=TOKEN_TELEGRAM)
dp = Dispatcher()

estado_sesion = {
    "capital_actual": 10000,
    "activo": True,
    "intentos_sniper_hoy": 0
}

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🤖 **Bot Triunfobet @xMythos_bot Operativo**\n\n"
        f"• **Capital Actual:** {estado_sesion['capital_actual']} Bs\n"
        f"• **Meta de Sesión:** {CONFIG_ESTRATEGIA['meta_capital_stop']} Bs\n"
        "• **Modo:** Apuestas constantes bajo filtros Top 8.\n\n"
        "Usa `/estado` para ver el balance o `/detener` para pausar."
    )

@dp.message(Command("estado"))
async def cmd_estado(message: types.Message):
    await message.answer(
        f"📊 **Estado del Bot**\n"
        f"• Capital: `{estado_sesion['capital_actual']} Bs`\n"
        f"• Estado del Sistema: `{'ACTIVO 🟢' if estado_sesion['activo'] else 'DETENIDO 🔴'}`"
    )

@dp.message(Command("detener"))
async def cmd_detener(message: types.Message):
    estado_sesion["activo"] = False
    await message.answer("🛑 Bot detenido manualmente por el usuario.")

async def main():
    print("Iniciando motor de @xMythos_bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
  
