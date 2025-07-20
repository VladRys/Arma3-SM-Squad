import logging

def setup_logger():
    logger = logging.getLogger("main_logger")
    logger.setLevel(logging.DEBUG)

    if not logger.hasHandlers():  
        info_handler = logging.FileHandler("logs/info.log", encoding='utf-8')
        info_handler.setLevel(logging.INFO)
        info_handler.addFilter(lambda record: record.levelno < logging.WARNING)
        info_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s"))

        error_handler = logging.FileHandler("logs/error.log", encoding='utf-8')
        error_handler.setLevel(logging.WARNING)
        error_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s"))

        logger.addHandler(info_handler)
        logger.addHandler(error_handler)

    return logger


def unload_logs(bot, msg):
    with open("logs/info.log", "rb") as f:
        lines = f.readlines()
        if lines:
            last_10_lines = lines[-10:]
            decoded_lines = [line.decode('utf-8').strip() for line in last_10_lines]
            
            text = '\n'.join(decoded_lines)
            
            bot.send_message(msg.chat.id,f"🛠️ Последние 10 записей в логах:\n\n{text}",)
            f.seek(0)
            bot.send_document(msg.chat.id, f)


def unload_error_logs(bot, msg):
    with open("logs/error.log", "rb") as f:
        lines = f.readlines()
        if lines:
            bot.send_message(msg.chat.id, f"🛠️ Последняя ошибка из логов:\n\n {lines[-1].decode('utf-8').strip()}")
            f.seek(0)
            bot.send_document(msg.chat.id, f)