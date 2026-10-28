"""
Electric Vehicle Market Performance & Insights - Flask Web Application
Optimized for local hosting and Vercel Serverless deployment.
"""

import json
import os
import sqlite3
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'ev_analytics.db')
CSV_PATH = os.path.join(DATA_DIR, 'ev_market_train.csv')
SUMMARY_PATH = os.path.join(BASE_DIR, 'analysis', 'summary_metrics.json')

# Load pre-computed summary metrics
cached_summary = {}
if os.path.exists(SUMMARY_PATH):
    try:
        with open(SUMMARY_PATH, 'r', encoding='utf-8') as f:
            cached_summary = json.load(f)
    except Exception as e:
        print(f"Notice: Failed to load summary cache: {e}")

# Database helper that works seamlessly in Serverless and Local environments
def get_db():
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        return conn
    # Fallback to in-memory if DB file not present
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    return conn

@app.route('/')
def home():
    return render_template('index.html', summary=cached_summary)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', summary=cached_summary)

@app.route('/story')
def story():
    return render_template('story.html', summary=cached_summary)

@app.route('/scenarios')
def scenarios():
    return render_template('scenarios.html', summary=cached_summary)

@app.route('/api/metrics')
def api_metrics():
    return jsonify(cached_summary)

@app.route('/api/filters')
def api_filters():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT manufacturing_country FROM ev_data WHERE manufacturing_country != '' ORDER BY manufacturing_country")
        countries = [r[0] for r in cursor.fetchall()]

        cursor.execute("SELECT DISTINCT category FROM ev_data WHERE category != '' ORDER BY category")
        categories = [r[0] for r in cursor.fetchall()]

        cursor.execute("SELECT DISTINCT manufacturer FROM ev_data WHERE manufacturer != '' ORDER BY manufacturer LIMIT 30")
        manufacturers = [r[0] for r in cursor.fetchall()]
        conn.close()

        return jsonify({
            "countries": countries,
            "categories": categories,
            "manufacturers": manufacturers
        })
    except Exception as e:
        # Fallback from cached summary
        return jsonify({
            "countries": list(cached_summary.get("country_distribution", {}).keys()),
            "categories": list(cached_summary.get("category_distribution", {}).keys()),
            "manufacturers": list(cached_summary.get("manufacturer_market_share", {}).keys())
        })

@app.route('/api/query')
def api_query():
    country = request.args.get('country', '')
    category = request.args.get('category', '')
    manufacturer = request.args.get('manufacturer', '')

    where_clauses = []
    params = []

    if country and country != 'All':
        where_clauses.append("manufacturing_country = ?")
        params.append(country)
    if category and category != 'All':
        where_clauses.append("category = ?")
        params.append(category)
    if manufacturer and manufacturer != 'All':
        where_clauses.append("manufacturer = ?")
        params.append(manufacturer)

    where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

    try:
        conn = get_db()
        cursor = conn.cursor()

        # Dynamic KPIs
        cursor.execute(f"""
            SELECT 
                COUNT(*),
                COUNT(DISTINCT manufacturer),
                COUNT(*),
                COALESCE(SUM(annual_sales_units), 0),
                COALESCE(AVG(customer_rating), 0),
                COALESCE(AVG(range_km), 0),
                COALESCE(AVG(battery_capacity_kwh), 0)
            FROM ev_data
            {where_sql}
        """, params)
        k = cursor.fetchone()
        kpis = {
            "total_records": k[0],
            "total_manufacturers": k[1],
            "total_models": k[2],
            "total_annual_sales": k[3],
            "total_sales_display": f"${k[3]/1e6:,.1f}M",
            "avg_customer_rating": round(k[4], 2),
            "avg_driving_range_km": round(k[5], 2),
            "avg_battery_capacity_kwh": round(k[6], 2)
        }

        # Category breakdown
        cursor.execute(f"""
            SELECT category, COUNT(*) as cnt 
            FROM ev_data 
            {where_sql} 
            GROUP BY category 
            ORDER BY cnt DESC
        """, params)
        cats = {r[0]: r[1] for r in cursor.fetchall()}

        # Top Manufacturers
        cursor.execute(f"""
            SELECT manufacturer, SUM(annual_sales_units) as sales 
            FROM ev_data 
            {where_sql} 
            GROUP BY manufacturer 
            ORDER BY sales DESC 
            LIMIT 10
        """, params)
        mfgs = {r[0]: round(r[1], 2) for r in cursor.fetchall()}

        # Sales trend
        cursor.execute(f"""
            SELECT model_year, SUM(annual_sales_units) as sales 
            FROM ev_data 
            {where_sql} 
            GROUP BY model_year 
            ORDER BY model_year ASC
        """, params)
        trend = {r[0]: round(r[1], 2) for r in cursor.fetchall()}

        # Battery tech
        cursor.execute(f"""
            SELECT battery_type, COUNT(*) as cnt 
            FROM ev_data 
            {where_sql} 
            GROUP BY battery_type 
            ORDER BY cnt DESC
        """, params)
        batt = {r[0]: r[1] for r in cursor.fetchall()}
        conn.close()

        return jsonify({
            "kpis": kpis,
            "categories": cats,
            "manufacturers": mfgs,
            "trend": trend,
            "battery": batt
        })
    except Exception as e:
        return jsonify({"error": str(e), "kpis": cached_summary.get("kpis", {})})

# WSGI application entrypoint for Vercel
app_wsgi = app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting EV Insights Server at http://127.0.0.1:{port}")
    app.run(debug=True, host='127.0.0.1', port=port)
