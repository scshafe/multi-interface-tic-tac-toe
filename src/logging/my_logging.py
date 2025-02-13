
import logging

logging.basicConfig(filename="tictactoe.logs", filemode='w', format='%(message)s')

logger = logging.getLogger(__file__)

logger.setLevel(logging.DEBUG)
