# Electric Vehicle Market Performance & Insights

> **An End-to-End Business Intelligence, Visual Analytics, and Web-Integrated Platform**  
> Developed for the SmartBridge & SkillWallet Minor Project Capstone.

---

## ⚡ Executive Summary
The Electric Vehicle (EV) market is expanding rapidly worldwide. This project delivers an executive intelligence platform built upon **200,000 real-world records across 39 features**. It addresses the decision-making needs of three primary industry stakeholders:
* **Emily Johnson (EV Market Strategy Director):** Category sales dynamics, price/range optimization, and consumer satisfaction.
* **David Chen (Automotive BI Manager):** Competitive OEM benchmarking (AmpereWorks, CircuitWorks, etc.) and global manufacturing footprints.
* **Dr. Sarah Williams (Sustainable Mobility Researcher):** Battery chemistry market penetration (NMC, LFP, Sodium-Ion), degradation, and decarbonization impact.

---

## 📁 Project Directory Structure
```text
D:\Minor Project\
├── data/
│   ├── ev_market_train.csv             # Primary dataset (200,000 rows x 39 columns)
│   └── ev_market_test.csv              # Test dataset
├── analysis/
│   ├── ev_analytics.py                 # SQLite & Python exploratory analysis engine
│   └── summary_metrics.json            # High-speed pre-calculated metrics cache
├── tableau/
│   ├── Tableau_Design_Guide.md         # Step-by-step workbook creation instructions
│   └── Tableau_Public_Embed_Snippet.html
├── documentation/
│   ├── Electric_Vehicle_Market_Performance_Report.md  # Comprehensive academic project report
│   └── Presentation_and_Viva_Defense_Guide.md         # 5-7 min video script & Viva Q&A
├── templates/
│   ├── index.html                      # Executive landing page & hero section
│   ├── dashboard.html                  # Interactive dashboard with filters & charts
│   ├── story.html                      # 8-scene analytical narrative data story
│   └── scenarios.html                  # Dedicated Emily, David, and Sarah analysis
├── static/
│   ├── css/style.css                   # Modern dark executive theme
│   └── js/dashboard.js                 # Chart.js interactive filtering engine
├── app.py                              # Flask full-stack controller with in-memory SQLite
├── requirements.txt                    # Project dependencies
├── run.bat                             # One-click Windows launch script
└── README.md                           # Documentation overview
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
Ensure you have Python 3.8+ installed on your Windows machine.

### 2. Install Dependencies
Open PowerShell or Command Prompt in `D:\Minor Project`:
```powershell
pip install -r requirements.txt
```

### 3. Run the Web Application
Double-click `run.bat` or execute:
```powershell
python app.py
```
Open your browser and navigate to:
```text
http://127.0.0.1:5000
```

---

## 📊 Core Analytical Metrics (From 200,000 Records)
* **Total Manufacturers:** 200 Distinct OEMs
* **Total Models:** 17,980 Unique Models
* **Total Annual Sales:** $1,550.7 Million Units
* **Average Customer Rating:** 4.01 / 5.0
* **Average Driving Range:** 324.54 km
* **Average Battery Capacity:** 78.24 kWh
* **Top 3 Vehicle Categories:** Two-Wheeler Scooters (19.2K), Hatchbacks (17K), Compact SUVs (16.8K)
* **Top 3 Battery Chemistries:** NMC (33.8%), LFP (32.0%), NCA (17.1%)
* **Top 3 OEMs by Revenue:** AmpereWorks ($9.45M), CircuitWorks ($8.92M), MomentumMobility ($8.78M)

---

## 🎓 SkillWallet Submission Checklist
- [x] **Data Collection & Extraction:** 200,000 rows loaded in `data/ev_market_train.csv`.
- [x] **Data Preparation:** Data types, measures, and geographic roles assigned.
- [x] **Data Visualizations:** 7 distinct visual sheets + 6 KPI cards created.
- [x] **Dashboard:** Responsive layout with global interactive filters.
- [x] **Story:** 8-scene narrative covering all 3 stakeholder scenarios.
- [x] **Performance Testing:** Verified 200K row rendering speed and zero calculated field bottlenecks.
- [x] **Web Integration:** Full-stack Python Flask web application deployed with dual native & Tableau embeds.
- [x] **Project Documentation:** Complete academic report in `documentation/`.
- [x] **Demonstration Video:** 5–7 minute script ready in `documentation/Presentation_and_Viva_Defense_Guide.md`.
