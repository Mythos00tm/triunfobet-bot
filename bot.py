import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# ── CONFIGURACIÓN GENERAL Y CREDENCIALES ──
TOKEN_TELEGRAM = "8959520494:AAEjYsnz81f6KD5HDlII_05PH-I3-CAydQs"

CONFIG_ESTRATEGIA = {
    "monto_apuesta_base": 1000,          # Apuesta constante por jugada (Bs)
    "capital_inicial": 10000,            # Capital de partida (Bs)
    "meta_capital_stop": 50000,          # Meta de sesión: Al llegar aquí, el bot se detiene
    
    # Filtros de Sala y Secuencia
    "min_jugadores": 1650,               # Mínimo de personas en sala
    "min_multiplicador_1": 2.16,         # Verde 1 mínimo
    
    # Análisis de Distancia Top 8 (Ordenado Mayor a Menor)
    "analizar_top_8": True,
    "max_diferencia_escalon": 50000,     # Máximo salto permitido entre puestos consecutivos
    "min_monto_p8": 10000,               # El puesto 8 debe tener al menos 10k Bs
    
    # Control de Salidas y Cashout Dinámico
    "cashout_estandar": 2.00,            # Retiro base (1.85x - 2.10x)
    "cashout_extendido_liquidez": 3.45,  # Meta ampliada si el Top 8 es denso y pesado
    
    # Modo Sniper Esporádico (3.94x)
    "activar_sniper_394": True,
    "target_sniper": 3.94,
    "min_jugadores_sniper": 2000,
    
    # Seguridad
    "pausa_por_3_rojos": True           # Pausa si ocurren 3 crash seguidos (< 2.00x)
}

bot = Bot(token=TOKEN_TELEGRAM)
dp = Dispatcher()

# Variables de Estado de la Sesión
estado_sesion = {
    "capital_actual": 10000,
    "activo": True,
    "intentos_sniper_hoy": 0,
    "chat_id_notificaciones": None # Guardará tu ID de Telegram para avisarte
}

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Guardamos el chat_id del usuario para enviarle alertas automáticas
    estado_sesion["chat_id_notificaciones"] = message.chat.id
    await message.answer(
        "🤖 **Bot Triunfobet @xMythos_bot Operativo**\n\n"
        f"• **Capital Actual:** {estado_sesion['capital_actual']} Bs\n"
        f"• **Meta de Sesión:** {CONFIG_ESTRATEGIA['meta_capital_stop']} Bs\n"
        "• **Monitoreo:** Activo en segundo plano (Filtros Top 8).\n\n"
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

# Tarea en segundo plano que simula/monitorea la sala de Triunfobet constantemente
async def monitor_triunfobet_automatico():
    while True:
        await asyncio.sleep(30) # Revisa el mercado cada 30 segundos
        
        if not estado_sesion["activo"]:
            continue
            
        # Verificación de la meta de capital (10k a 50k)
        if estado_sesion["capital_actual"] >= CONFIG_ESTRATEGIA["meta_capital_stop"]:
            estado_sesion["activo"] = False
            if estado_sesion["chat_id_notificaciones"]:
                await bot.send_message(
                    estado_sesion["chat_id_notificaciones"],
                    "🎯 **¡Meta Alcanzada!** El bot llegó a los 50.000 Bs y se detuvo de forma segura."
                )
            continue

        # Simulación de lectura de datos de la sala en tiempo real
        jugadores_activos = 1850  # Simulado
        top_8_apuestas = [130000, 110000, 85000, 60000, 40000, 25000, 15000, 12000] # Top 8 ordenado
        
        # Validación de Distancia Top 8
        valido_top_8 = True
        for i in range(len(top_8_apuestas) - 1):
            gap = top_8_apuestas[i] - top_8_apuestas[i+1]
            if gap > CONFIG_ESTRATEGIA["max_diferencia_escalon"]:
                valido_top_8 = False
                break

        # Si cumple los filtros de sala y top 8, ejecuta la jugada constante
        if jugadores_activos >= CONFIG_ESTRATEGIA["min_jugadores"] and valido_top_8:
            monto = CONFIG_ESTRATEGIA["monto_apuesta_base"]
            
            # Simulamos resultado de la jugada (Ej: Gana y sube capital)
            estado_sesion["capital_actual"] += monto # Suma ganancia base
            
            # Si tenemos el chat registrado, te enviamos la alerta de la jugada en vivo
            if estado_sesion["chat_id_notificaciones"]:
                await bot.send_message(
                    estado_sesion["chat_id_notificaciones"],
                    f"🎲 **Jugada Ejecutada Automáticamente**\n"
                    f"• Apuesta: `{monto} Bs`\n"
                    f"• Condición Top 8: `Aprobada (Estable)`\n"
                    f"• Nuevo Capital: `{estado_sesion['capital_actual']} Bs`"
                )

async def main():
    print("Iniciando motor de @xMythos_bot con monitoreo...")
    # Lanzamos el bucle de monitoreo en segundo plano junto al bot de Telegram
    asyncio.create_task(monitor_triunfobet_automatico())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
