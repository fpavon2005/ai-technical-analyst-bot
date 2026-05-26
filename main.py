import os
from datetime import datetime
from config import logger, DEFAULT_TICKERS
from market_analyzer import fetch_and_analyze_ticker
from ai_agent import compile_market_analysis
from telegram_bot import send_technical_report

def run_portfolio_analysis_pipeline():
    """Loops through target tickers, extracts metrics, generates AI summaries, and reports."""
    logger.info("=========================================")
    logger.info("🚀 STARTING PORTFOLIO AI TECHNICAL ANALYST")
    logger.info("=========================================")
    
    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    markdown_report = f"# 📈 AI Technical Analyst Market Report\n*Compiled on: {timestamp_str}*\n\n"
    
    analyzed_count = 0
    
    for ticker in DEFAULT_TICKERS:
        logger.info(f"\n--- Initiating Technical Pipeline for: '{ticker}' ---")
        
        # 1. Fetch pricing and calculate indicators
        metrics = fetch_and_analyze_ticker(ticker)
        if not metrics:
            logger.warning(f"Skipping pipeline for ticker '{ticker}' due to loading errors.")
            continue
            
        # 2. Compile AI Analytical Report
        ai_analysis = compile_market_analysis(metrics)
        
        # 3. Dispatch to Telegram Channel
        send_technical_report(ticker, metrics, ai_analysis)
        
        # 4. Append to unified offline markdown report
        change_symbol = "📈" if metrics["pct_change"] >= 0 else "📉"
        markdown_report += (
            f"## 📊 {ticker} Technical Overview\n"
            f"- **Current Valuation**: `${metrics['current_price']}` ({change_symbol} `{metrics['pct_change']}%`)\n"
            f"- **24h Range**: High `${metrics['high_24h']}` | Low `${metrics['low_24h']}`\n"
            f"- **Technical Indicator SMA-20**: `${metrics['sma_20']}`\n"
            f"- **Oscillator RSI-14**: `{metrics['rsi_14']}`\n\n"
            f"### 🧠 AI Technical Analyst Insight:\n"
            f"> \"{ai_analysis}\"\n\n"
            f"---\n\n"
        )
        analyzed_count += 1
        
    # Write unified offline report file for recruiters
    output_report_file = "market_report_summary.md"
    try:
        with open(output_report_file, "w", encoding="utf-8") as f:
            f.write(markdown_report)
        logger.info(f"🎉 Successfully wrote offline technical summary markdown at: {os.path.abspath(output_report_file)}")
    except Exception as e:
        logger.error(f"Failed to write offline markdown report: {str(e)}")

    logger.info("\n=========================================")
    logger.info(f"🎉 PIPELINE COMPLETED. {analyzed_count} TICKERS SUCCESSFULLY PROCESS")
    logger.info("=========================================")

if __name__ == "__main__":
    run_portfolio_analysis_pipeline()
