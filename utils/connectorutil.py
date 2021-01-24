import psycopg2
import psycopg2.extras
from typing import Dict, Any, NoReturn
import pandas as pd
class Connector():
    def __init__(self, db_name: str, user: str):
        self.db_name=db_name
        self.user=user
        
    def queryTransaction(self, query: str)-> NoReturn:
        if not query:
            return
        connection = psycopg2.connect(f"dbname={self.db_name} user={self.user}")
        with connection.cursor() as cursor:
            cursor.execute(query)
            cursor.closer()
        connection.commit()
        connection.close()
        
    def saveTextBatch(self, articles: Dict[str, Any])-> NoReturn:
        if not articles:
            return
        connection = psycopg2.connect(f"dbname={self.db_name} user={self.user}")
        with connection.cursor() as cursor:
            iter_articles = ({'text': article['title']} for article in articles)
            psycopg2.extras.execute_batch(cursor, """
            INSERT INTO documents_raw(text) VALUES (%(text)s);
            """, iter_articles)
            cursor.close()
        connection.commit()

    def getTextDF(self) -> pd.DataFrame:
        connection = psycopg2.connect(f"dbname={self.db_name} user={self.user}")
        cur = connection.cursor()
        cur.execute("SELECT * FROM documents_raw;")
        df = pd.DataFrame(cur.fetchall(), columns=['id','text'])
        df.set_index(['id'], inplace=True)
        cur.close()
        connection.close()
        return df
    
    def saveText(self, text: str)-> NoReturn:
        connection = psycopg2.connect(f"dbname={self.db_name} user={self.user}")
        if not text:
            return
        with connection.cursor() as cursor:
            cursor.execute("""
            INSERT INTO documents_raw(text) VALUES (%s);
            """, (text,))
            connection.commit()
            cursor.close()
        connection.close()