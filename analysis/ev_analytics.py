"""
Electric Vehicle Market Performance & Insights - Exploratory Data Analysis & Metric Extraction
Uses Python standard library (csv, sqlite3, json) for high-performance, policy-safe execution.
Processes 200,000 rows across 39 columns and generates comprehensive analytical metrics for:
- Executive Dashboard (Emily Johnson)
- Automotive Business Intelligence (David Chen)
- Sustainable Mobility Research (Dr. Sarah Williams)
"""

import csv
import json
import os
import sqlite3
import time

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'ev_market_train.csv')
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), 'summary_metrics.json')

def run_analysis():
    start_time = time.time()
    print(f"Loading and analyzing dataset from: {DATA_PATH}...")

    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    with open(DATA_PATH, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        headers = [h.strip().lower() for h in next(reader)]
        
        # Build SQL table schema dynamically
        col_defs = [f'"{h}" TEXT' for h in headers]
        cursor.execute(f"CREATE TABLE ev_data ({', '.join(col_defs)})")
        
        placeholders = ', '.join(['?'] * len(headers))
        insert_sql = f"INSERT INTO ev_data VALUES ({placeholders})"
        
        batch = []
        count = 0
        for row in reader:
            if row:
                batch.append(row)
                count += 1
                if len(batch) >= 10000:
                    cursor.executemany(insert_sql, batch)
                    batch = []
        if batch:
            cursor.executemany(insert_sql, batch)
        conn.commit()

    print(f"Loaded {count:,} rows into in-memory SQLite engine in {time.time() - start_time:.2f}s.")

    # 1. Overall KPIs
    cursor.execute("""
        SELECT 
            COUNT(*),
            COUNT(DISTINCT manufacturer),
            COUNT(DISTINCT vehicle_id),
            SUM(CAST(annual_sales_units AS REAL)),
            AVG(CAST(customer_rating AS REAL)),
            AVG(CAST(range_km AS REAL)),
            AVG(CAST(battery_capacity_kwh AS REAL))
        FROM ev_data
    """)
    kpi_row = cursor.fetchone()
    total_records = kpi_row[0]
    total_manufacturers = kpi_row[1]
    total_models = kpi_row[2]
    total_sales = kpi_row[3]
    avg_rating = round(kpi_row[4], 2)
    avg_range = round(kpi_row[5], 2)
    avg_capacity = round(kpi_row[6], 2)

    print("\n--- KPI SCORECARD ---")
    print(f"Total Records: {total_records:,}")
    print(f"Total Manufacturers: {total_manufacturers}")
    print(f"Total Unique Models: {total_models:,}")
    print(f"Total Annual Sales Units: {total_sales:,.0f} (${total_sales/1e6:,.1f}M)")
    print(f"Avg Customer Rating: {avg_rating} / 5.0")
    print(f"Avg Driving Range: {avg_range} km")
    print(f"Avg Battery Capacity: {avg_capacity} kWh")

    # 2. EV Category Distribution
    cursor.execute("""
        SELECT category, COUNT(*) as cnt, SUM(CAST(annual_sales_units AS REAL)) as sales
        FROM ev_data
        GROUP BY category
        ORDER BY cnt DESC
    """)
    category_rows = cursor.fetchall()
    category_distribution = {row[0]: row[1] for row in category_rows}

    # 3. Market Share by Manufacturer (Top 10)
    cursor.execute("""
        SELECT manufacturer, SUM(CAST(annual_sales_units AS REAL)) as total_sales, COUNT(*) as model_cnt
        FROM ev_data
        GROUP BY manufacturer
        ORDER BY total_sales DESC
        LIMIT 10
    """)
    top_mfg_rows = cursor.fetchall()
    top_manufacturers = {row[0]: round(row[1], 2) for row in top_mfg_rows}

    # 4. Annual Sales Trend by Model Year (2018-2026)
    cursor.execute("""
        SELECT model_year, SUM(CAST(annual_sales_units AS REAL)) as sales
        FROM ev_data
        WHERE model_year IS NOT NULL AND model_year != ''
        GROUP BY model_year
        ORDER BY CAST(model_year AS INTEGER) ASC
    """)
    trend_rows = cursor.fetchall()
    sales_trend = {row[0]: round(row[1], 2) for row in trend_rows}

    # 5. Battery Technology Distribution & Market Share %
    cursor.execute("""
        SELECT battery_type, COUNT(*) as cnt, AVG(CAST(range_km AS REAL)) as avg_range, AVG(CAST(co2_saved_tons_per_year AS REAL)) as avg_co2
        FROM ev_data
        WHERE battery_type IS NOT NULL AND battery_type != ''
        GROUP BY battery_type
        ORDER BY cnt DESC
    """)
    battery_rows = cursor.fetchall()
    battery_share = {row[0]: row[1] for row in battery_rows}
    battery_pct = {row[0]: round((row[1] / total_records) * 100, 2) for row in battery_rows}

    # 6. Global Manufacturing Footprint by Country
    cursor.execute("""
        SELECT manufacturing_country, COUNT(*) as cnt, SUM(CAST(annual_sales_units AS REAL)) as sales
        FROM ev_data
        WHERE manufacturing_country IS NOT NULL AND manufacturing_country != ''
        GROUP BY manufacturing_country
        ORDER BY cnt DESC
    """)
    country_rows = cursor.fetchall()
    country_distribution = {row[0]: row[1] for row in country_rows}

    # 7. Customer Rating & Record Count by Category
    cursor.execute("""
        SELECT category, COUNT(*) as cnt, AVG(CAST(customer_rating AS REAL)) as avg_rating
        FROM ev_data
        GROUP BY category
        ORDER BY cnt DESC
    """)
    rating_rows = cursor.fetchall()
    customer_ratings_by_cat = [
        {"category": r[0], "count": r[1], "avg_rating": round(r[2], 2)}
        for r in rating_rows
    ]

    # 8. Scenario Analysis Specifics
    # Emily Johnson (Market Strategy Director): Category profitability, avg range & models
    cursor.execute("""
        SELECT category, SUM(CAST(annual_sales_units AS REAL)) as sales, AVG(CAST(range_km AS REAL)) as avg_range, COUNT(*) as models
        FROM ev_data
        GROUP BY category
        ORDER BY sales DESC
    """)
    emily_insights = [
        {"category": r[0], "total_sales": round(r[1], 2), "avg_range_km": round(r[2], 2), "models": r[3]}
        for r in cursor.fetchall()
    ]

    # David Chen (BI Manager): Top OEMs in key countries
    cursor.execute("""
        SELECT manufacturing_country, manufacturer, SUM(CAST(annual_sales_units AS REAL)) as sales
        FROM ev_data
        GROUP BY manufacturing_country, manufacturer
        ORDER BY manufacturing_country, sales DESC
    """)
    david_raw = cursor.fetchall()
    david_dict = {}
    for country, mfg, sales in david_raw:
        if country not in david_dict:
            david_dict[country] = []
        if len(david_dict[country]) < 3:
            david_dict[country].append({"manufacturer": mfg, "sales": round(sales, 2)})

    # Dr. Sarah Williams (Sustainable Mobility Researcher): Battery Chemistry Comparison
    cursor.execute("""
        SELECT 
            battery_type,
            COUNT(*) as total_vehicles,
            AVG(CAST(range_km AS REAL)) as avg_range,
            AVG(CAST(battery_capacity_kwh AS REAL)) as avg_capacity,
            AVG(CAST(co2_saved_tons_per_year AS REAL)) as avg_co2_saved,
            AVG(CAST(battery_degradation_pct_5yr AS REAL)) as avg_degradation
        FROM ev_data
        WHERE battery_type IS NOT NULL AND battery_type != ''
        GROUP BY battery_type
        ORDER BY total_vehicles DESC
    """)
    sarah_insights = [
        {
            "battery_type": r[0],
            "total_vehicles": r[1],
            "avg_range_km": round(r[2], 2),
            "avg_capacity_kwh": round(r[3], 2),
            "avg_co2_saved_tons": round(r[4], 2),
            "avg_degradation_5yr_pct": round(r[5], 2)
        }
        for r in cursor.fetchall()
    ]

    summary_data = {
        "kpis": {
            "total_records": total_records,
            "total_manufacturers": total_manufacturers,
            "total_models": total_models,
            "total_annual_sales": total_sales,
            "total_sales_display": f"${total_sales/1e6:,.1f}M",
            "avg_customer_rating": avg_rating,
            "avg_driving_range_km": avg_range,
            "avg_battery_capacity_kwh": avg_capacity
        },
        "category_distribution": category_distribution,
        "manufacturer_market_share": top_manufacturers,
        "annual_sales_trend": sales_trend,
        "battery_technology_share": battery_share,
        "battery_technology_percentage": battery_pct,
        "country_distribution": country_distribution,
        "customer_rating_by_category": customer_ratings_by_cat,
        "scenarios": {
            "emily_strategy": emily_insights,
            "david_bi": david_dict,
            "sarah_sustainability": sarah_insights
        }
    }

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as out_f:
        json.dump(summary_data, out_f, indent=4)

    print(f"\nAll metrics successfully calculated and saved to: {OUTPUT_PATH}")
    print(f"Total processing time: {time.time() - start_time:.2f}s")

if __name__ == '__main__':
    run_analysis()
