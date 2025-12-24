import pymysql
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

print('=== FEEDBACK ANALYZER DATABASE DATA ===')
print(f'Timestamp: {datetime.now()}')
print()

connection = pymysql.connect(
    host='localhost',
    user='root', 
    password='',
    database='feedback_analyser',
    cursorclass=pymysql.cursors.DictCursor
)

with connection.cursor() as cursor:
    print('👥 USERS TABLE:')
    cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
    users = cursor.fetchall()
    if users:
        for user in users:
            print(f'  ID: {user["id"]} | Email: {user["email"]} | Name: {user.get("name", "N/A")} | Created: {user["created_at"]}')
    else:
        print('  No users found')
    
    print()
    print('📊 ANALYSIS DATA:')
    cursor.execute('SELECT * FROM user_analyses ORDER BY created_at DESC LIMIT 10')
    analyses = cursor.fetchall()
    if analyses:
        for analysis in analyses:
            print(f'  ID: {analysis["id"]} | User: {analysis["user_id"]} | Sentiment: {analysis.get("sentiment", "N/A")}')
            feedback_text = analysis.get("feedback_text", "N/A") or "N/A"
            print(f'    Text: {feedback_text[:60]}...')
            print(f'    Created: {analysis["created_at"]}')
            print()
    else:
        print('  No analyses found')
    
    print('🔑 SESSION DATA:')
    cursor.execute('SELECT * FROM user_sessions ORDER BY created_at DESC LIMIT 5')
    sessions = cursor.fetchall()
    if sessions:
        for session in sessions:
            print(f'  ID: {session["id"]} | User: {session["user_id"]} | Created: {session["created_at"]}')
    else:
        print('  No sessions found')

connection.close()
print()
print('✅ Database query completed!')