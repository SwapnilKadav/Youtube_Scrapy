# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector

class YoutubeScrapyPipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()
        
    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            passwd = 'admin',
            database = 'scrapy',
        )
        self.curr = self.conn.cursor()
    def create_table(self):
        print("**"*20)
        self.curr.execute("""CREATE TABLE IF NOT EXISTS VideoMetaData(
                        id INT NOT NULL AUTO_INCREMENT,
                        url VARCHAR(255),
                        title VARCHAR(255),
                        description TEXT,
                        PRIMARY KEY (id)
            )""")
        self.curr.execute("""CREATE TABLE IF NOT EXISTS VideoComment(
                        id INT NOT NULL AUTO_INCREMENT,
                        comment LONGTEXT,
                        video_id INT,
                        PRIMARY KEY (id),
                        FOREIGN KEY (video_id)
                        REFERENCES VideoMetaData(id)
            )""")
        self.curr.execute("""CREATE TABLE IF NOT EXISTS VideoCommentReply(
                        id INT NOT NULL AUTO_INCREMENT,
                        reply TEXT,
                        comment_id INT,
                        PRIMARY KEY (id),
                        FOREIGN KEY (comment_id)
                        REFERENCES VideoComment(id)
            )""")
        self.curr.execute("""CREATE TABLE IF NOT EXISTS VideoTranscript(
                        id INT NOT NULL AUTO_INCREMENT,
                        text VARCHAR(255),
                        start FLOAT,
                        duration FLOAT,
                        video_id INT,
                        PRIMARY KEY (id),
                        FOREIGN KEY (video_id)
                        REFERENCES VideoMetaData(id)
            )""")
        print("**"*20)
        
    def process_item(self, item, spider):
        self.store_db(item,spider)
        return item
    def store_db(self, items, spider):
        
        self.curr.execute("SELECT * FROM VideoMetaData WHERE url = '%s'"%(items['URL'][0]))
        result = self.curr.fetchone()
        
        if result:
            spider.logger.warn(f"Item already in database: {items['URL']}")
        else:
            self.curr.execute("INSERT INTO VideoMetaData (url, title, description) VALUES(%s,%s,%s)", (items['URL'][0], items['Title'], items['Description']))
            video_id = self.curr.lastrowid
            for item in list(zip(items['Text'], items['Start'], items['Duration'])):
                self.curr.execute("INSERT INTO VideoTranscript (text, start, duration, video_id) VALUES(%s,%s,%s,%s)", (item[0], item[1], item[2], video_id))
            for item in list(zip(items['Comments'], items['Reply'])):
                self.curr.execute("INSERT INTO VideoComment (comment, video_id) VALUES(%s,%s)", (item[0], video_id))
                comment_id = self.curr.lastrowid
                if item[1] is not None:
                    for reply in item[1]:
                        self.curr.execute("INSERT INTO VideoCommentReply (reply, comment_id) VALUES(%s, %s)", (reply, comment_id))
        self.conn.commit()

    def close_spider(self, spider):
        ## Close cursor & connection to database 
        self.curr.close()
        self.conn.close()