import os
import csv
import logging as log
from kiosk import db
from kiosk.models import Food


def init_food_table():
    # Make sure there is data in the main.foods TABLE
    log.debug(f"Checking Food model table for contents:")
    menu = Food.query.all()
    log.debug(f"Got: {menu}")
    if len(menu) < 2:
        log.info('Reading menu file...')
        filePath = os.path.join('res','menu.csv')
        reader = csv.DictReader(open(filePath))
        log.info('Inserting menu items from menu.csv to Food model table...')
        for row in reader:
            log.debug(f"Menu row: {row}")#['item']}, {row['price']}, {row['description']}")
            food = Food(item=row['item'],
                        price=row['price'],
                        description=row['description'],
                        img=row['img'],
                        options=row['options'])
            db.session.add(food)
            db.session.commit()
    else:
        log.debug(f"Food model table contains: {len(menu)} items.")