import os
import json
import logging
from config import logger, GEMINI_API_KEY

def compile_market_analysis(metrics: dict) -> str:
    """Invokes Google Gemini LLM to write a professional 3-sentence technical market analyst report.
    
    Includes a smart fallback technical copywriter if credentials are not configured.
    """
    ticker = metrics.get("ticker", "Asset")
    price = metrics.get("current_price", 0.0)
    change = metrics.get("pct_change", 0.0)
    sma = metrics.get("sma_20", 0.0)
    rsi = metrics.get("rsi_14", 50.0)
    
    prompt = f"""
    Write a sophisticated, professional, 3-sentence financial technical analysis update for the ticker: {ticker}.
    Use the following quantitative indicators calculated for today:
    - Current Price: ${price}
    - 24h Change: {change}%
    - SMA-20 (Simple Moving Average): ${sma}
    - RSI-14 (Relative Strength Index): {rsi}

    Instructions:
    1. Explain the current trend (bullish/bearish) relative to the SMA-20.
    2. Interpret the RSI signal (overbought if >70, oversold if <30, otherwise neutral consolidation).
    3. Conclude with a clean professional technical recommendation.
    Keep the tone extremely polished and write in Spanish.
    """

    if GEMINI_API_KEY.strip():
        try:
            logger.info(f"Connecting to Gemini API to analyze asset technicals: {ticker}...")
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_API_KEY.strip())
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            response = model.generate_content(prompt)
            summary = response.text.strip()
            logger.info("Successfully fetched technical analysis from Gemini model.")
            return summary
        except Exception as e:
            logger.warning(f"Failed to fetch market analysis from Gemini: {str(e)}. Using fallback...")
    else:
        logger.info(f"No GEMINI_API_KEY configured. Running local quantitative copywriter for: '{ticker}'...")

    # Advanced rule-based financial copywriter simulating actual professional insights
    trend = "alcista" if price >= sma else "bajista"
    sma_relation = "cotiza por encima de" if price >= sma else "se mantiene por debajo de"
    
    # RSI interpretation
    if rsi >= 70:
        rsi_comment = f"El RSI de {rsi} señala una fuerte condición de sobrecompra, lo que advierte sobre posibles tomas de ganancias a corto plazo."
        rec = "Se sugiere cautela y esperar correcciones saludables antes de abrir nuevas posiciones."
    elif rsi <= 30:
        rsi_comment = f"El RSI de {rsi} entra en terreno de sobreventa extrema, indicando agotamiento de la presión bajista y acumulación potencial."
        rec = "Representa un punto de entrada técnicamente atractivo con un ratio riesgo/beneficio favorable."
    else:
        rsi_comment = f"El oscilador RSI en {rsi} refleja una fase neutral de consolidación sin divergencias significativas."
        rec = "Se aconseja vigilar rupturas de niveles de soporte clave en este rango lateral."
        
    summary = (
        f"El activo {ticker} {sma_relation} su media móvil de 20 períodos (${sma}) con un cambio del {change}%, confirmando una tendencia {trend} en el gráfico diario. "
        f"{rsi_comment} "
        f"{rec}"
    )
    return summary
