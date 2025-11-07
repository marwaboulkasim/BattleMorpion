import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BattleMorpion")

def log_move(player, move, model):
    logger.info(f"{player} ({model}) joue en {move}")

