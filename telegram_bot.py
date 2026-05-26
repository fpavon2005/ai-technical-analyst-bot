import requests
from config import logger, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_technical_report(ticker: str, metrics: dict, ai_analysis: str) -> bool:
    """Dispatches a highly-stylized HTML market report via the Telegram Bot API.
    
    Logs to stdout if credentials are not configured.
    """
    price = metrics.get("current_price", 0.0)
    change = metrics.get("pct_change", 0.0)
    sma = metrics.get("sma_20", 0.0)
    rsi = metrics.get("rsi_14", 50.0)
    high = metrics.get("high_24h", 0.0)
    low = metrics.get("low_24h", 0.0)
    
    # Emojis for changes
    change_emoji = "🟢" if change >= 0 else "🔴"
    trend_emoji = "🚀" if price >= sma else "⚠️"
    
    # Styled HTML Telegram Message Body
    html_message = (
        f"📊 <b><u>REPORTE TÉCNICO DIARIO: {ticker}</u></b>\n\n"
        f"💰 <b>Precio Actual</b>: ${price} ({change_emoji} {change}%)\n"
        f"📈 <b>Máx 24h</b>: ${high} | 📉 <b>Mín 24h</b>: ${low}\n\n"
        f"📐 <b>MÉTRICAS CLAVE:</b>\n"
        f"• <b>Medio Móvil SMA-20</b>: ${sma} {trend_emoji}\n"
        f"• <b>Fuerza Relativa RSI-14</b>: {rsi}\n\n"
        f"🧠 <b>ANÁLISIS COGNITIVO IA:</b>\n"
        f"<i>\"{ai_analysis}\"</i>\n\n"
        f"🌐 <i>Enviado por AI Analyst Bot Portfolio</i>"
    )

    credentials_exist = TELEGRAM_BOT_TOKEN.strip() and TELEGRAM_CHAT_ID.strip()
    
    if not credentials_exist:
        logger.warning("No active Telegram Bot Token/ChatID set in variables. Logging simulated message...")
        print(f"\n=================== SIMULATED TELEGRAM REPORT ===================\n{html_message}\n=================================================================\n")
        return True
        
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN.strip()}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID.strip(),
        "text": html_message,
        "parse_mode": "HTML"
    }
    
    try:
        logger.info(f"Dispatching live Telegram message to Chat ID: {TELEGRAM_CHAT_ID}...")
        response = requests.post(url, json=payload, timeout=8.0)
        
        if response.status_code == 200:
            logger.info("Successfully dispatched Telegram technical report.")
            return True
        else:
            logger.error(f"Telegram API responded with error code {response.status_code}: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Critical error communicating with Telegram Bot API: {str(e)}")
        return False
