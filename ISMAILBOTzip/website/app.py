from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import sys
import psycopg2
from psycopg2 import pool
from datetime import datetime
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ISMAIL_BOT'))
from config import FlaskConfig

app = Flask(__name__)
app.secret_key = FlaskConfig.SECRET_KEY

# Validation helpers
def is_valid_player_id(player_id):
    """Validate player ID format - must be numeric"""
    return player_id and len(player_id) >= 5 and player_id.isdigit()

# Database connection pool
db_url = FlaskConfig.DATABASE_URL
try:
    postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 20, db_url)
except Exception as e:
    print(f"Error creating connection pool: {e}")
    postgreSQL_pool = None

def get_db_connection():
    if postgreSQL_pool:
        return postgreSQL_pool.getconn()
    return psycopg2.connect(db_url)

def release_db_connection(conn):
    if postgreSQL_pool:
        postgreSQL_pool.putconn(conn)
    else:
        conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code = request.form.get('code', '').strip()
        if code == FlaskConfig.SECURITY_CODES['main_access_code']:
            session['main_access'] = True
            return redirect(url_for('start'))
        return render_template('login.html', type='main', error=True)
    return render_template('login.html', type='main')

@app.route('/start', methods=['GET', 'POST'])
def start():
    if not session.get('main_access'):
        return redirect(url_for('index'))
    
    status_msg = None
    error_msg = None
    
    if request.method == 'POST':
        player_id = request.form.get('player_id', '').strip()
        
        if not player_id:
            error_msg = "Please enter a valid Player ID"
        elif not is_valid_player_id(player_id):
            error_msg = "Player ID must be at least 5 digits (numbers only)"
        else:
            conn = None
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                
                # Check if already exists
                cur.execute("SELECT status FROM waitlist WHERE player_id = %s", (player_id,))
                row = cur.fetchone()
                
                if row:
                    if row[0] == 'accepted':
                        status_msg = "✅ ACCEPTED! Go to your friend list and accept the bot"
                    elif row[0] == 'pending':
                        status_msg = "⏳ You are in the waitlist. Waiting for approval..."
                    else:
                        status_msg = "❌ Your request was rejected."
                else:
                    cur.execute("INSERT INTO waitlist (player_id) VALUES (%s)", (player_id,))
                    conn.commit()
                    status_msg = "✅ Successfully added to waitlist! Please wait for approval."
                cur.close()
            except Exception as e:
                error_msg = "Database error. Please try again."
                print(f"DB Error: {e}")
            finally:
                if conn:
                    release_db_connection(conn)
            
    return render_template('start.html', status_msg=status_msg, error_msg=error_msg)

@app.route('/dev', methods=['GET', 'POST'])
def dev():
    if request.method == 'POST':
        code = request.form.get('code')
        if code == FlaskConfig.SECURITY_CODES['dev_access_code']:
            session['dev_access'] = True
            return redirect(url_for('dev_area'))
        return "Invalid Dev Code", 403
    return render_template('login.html', type='dev')

@app.route('/dev/area')
def dev_area():
    if not session.get('dev_access'):
        return redirect(url_for('dev'))
    
    filter_status = request.args.get('status', 'pending')
    if filter_status not in ['pending', 'accepted', 'rejected', 'all']:
        filter_status = 'pending'
    
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get stats
        cur.execute("SELECT COUNT(*), status FROM waitlist GROUP BY status")
        stats = {row[1]: row[0] for row in cur.fetchall()}
        cur.execute("SELECT COUNT(*) FROM waitlist")
        stats['total'] = cur.fetchone()[0]
        
        # Get filtered entries
        if filter_status == 'all':
            cur.execute("SELECT id, player_id, status, created_at FROM waitlist ORDER BY created_at DESC")
        else:
            cur.execute("SELECT id, player_id, status, created_at FROM waitlist WHERE status = %s ORDER BY created_at DESC", (filter_status,))
        
        entries = cur.fetchall()
        cur.close()
    except Exception as e:
        print(f"Error: {e}")
        entries = []
        stats = {'total': 0, 'pending': 0, 'accepted': 0, 'rejected': 0}
    finally:
        if conn:
            release_db_connection(conn)
    
    return render_template('dev_area.html', entries=entries, current_filter=filter_status, stats=stats)

@app.route('/dev/action/<int:entry_id>/<action>')
def dev_action(entry_id, action):
    if not session.get('dev_access'):
        return redirect(url_for('dev'))
    
    if action not in ['accepted', 'rejected']:
        return "Invalid Action", 400
        
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE waitlist SET status = %s WHERE id = %s", (action, entry_id))
        conn.commit()
        print(f"[DEV] Entry {entry_id} marked as {action}")
        cur.close()
    except Exception as e:
        print(f"Error updating entry: {e}")
    finally:
        if conn:
            release_db_connection(conn)
    
    return redirect(url_for('dev_area'))

@app.route('/dev/stats')
def dev_stats():
    if not session.get('dev_access'):
        return redirect(url_for('dev'))
    
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get statistics
        cur.execute("SELECT COUNT(*), status FROM waitlist GROUP BY status")
        stats = {row[1]: row[0] for row in cur.fetchall()}
        
        cur.execute("SELECT COUNT(*) FROM waitlist")
        total = cur.fetchone()[0]
        
        cur.close()
    except Exception as e:
        print(f"Stats error: {e}")
        stats = {}
        total = 0
    finally:
        if conn:
            release_db_connection(conn)
    
    return render_template('dev_stats.html', stats=stats, total=total)

@app.route('/logout')
def logout():
    session.pop('main_access', None)
    session.pop('dev_access', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    web_config = FlaskConfig.WEB_CONFIG
    app.run(host=web_config['host'], port=web_config['port'], debug=web_config['debug'])
