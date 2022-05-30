from dataclasses import dataclass
import logging as log
import time

def log_debug():
    log.basicConfig(level=log.DEBUG, format='{%(asctime)s} [%(levelname)s]: %(message)s',
                    filename=f"{time.strftime('%Y-%m-%d %H.%M.%S')}.log", filemode='w')

@dataclass
class Item:
    foodID: str
    name: str
    price: int
    description: str
    image: str
    options: dict