# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from sqlalchemy.orm import sessionmaker
from .models import Threads, db_connect, create_threads_table
from sqlalchemy.sql import exists

class CampricePipeline(object):

    def __init__(self):
        engine = db_connect()
        create_threads_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()

        # Pipelines for data
        item['thread_id'] = ''.join(item['thread_id']).replace('t=', ';').replace('&', ';').split(";")[1]
        item['title'] = ''.join(item['thread_id']).replace('t=', ';').replace('&', ';').split(";")[1]

        thread = Threads(**item)

        try:
            exists = session.query(Threads.thread_id).filter_by(thread_id=item['thread_id']).scalar() is not None
            if not exists:
                print("Doesn\'t exist!")
                session.add(thread)
                session.commit()
            else:
                print("Exists! Skipping.")
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
