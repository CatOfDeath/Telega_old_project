from flask import Flask, request, send_file
import pandas as pd
import os
import tempfile
from database.dbapi import DatabaseConnector

db_conn = DatabaseConnector("postgresql+psycopg2://postgres:postgres@localhost:5432/bot_base")
app = Flask(__name__)

def get_book_stats(book_id):
    session = db_conn.get_connection()
    query = f"SELECT date_start, date_end FROM borrows WHERE book_id = {book_id}"
    df = pd.read_sql(query, session.bind)
    df.rename(columns={'date_start': 'Дата взятия', 'data_end': 'Дата возврата'}, inplace=True)
    return df

@app.route("/download/<book_id>")
def download_stats(book_id):
    df = get_book_stats(book_id)
    temp_file = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
    temp_file.close()
    df.to_excel(temp_file.name, index=False)
    return send_file(temp_file.name, as_attachment=True, download_name=f"stats_{book_id}.xlsx")
        
if __name__ == '__main__':
    app.run(port=8080)
