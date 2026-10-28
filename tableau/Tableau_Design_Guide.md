# Tableau Workbook Design & Publishing Guide
## Electric Vehicle Market Performance & Insights

This guide provides step-by-step instructions for replicating the exact Tableau visualizations, interactive dashboard, and 8-scene data story seen in the SkillWallet portal.

---

## 1. Data Connection & Preparation
1. Open **Tableau Desktop** or **Tableau Public**.
2. Under **Connect $\rightarrow$ To a File**, select **Text file** and choose `D:\Minor Project\data\ev_market_train.csv`.
3. Verify that all 200,000 rows and 39 columns are loaded.
4. Set Field Data Types:
   - `manufacturing_country` $\rightarrow$ Right-click $\rightarrow$ **Geographic Role $\rightarrow$ Country/Region**.
   - `annual_sales_units` $\rightarrow$ Number (Whole) $\rightarrow$ Continuous Measure.
   - `range_km`, `battery_capacity_kwh`, `customer_rating` $\rightarrow$ Number (Decimal) $\rightarrow$ Continuous Measure.
   - `model_year` $\rightarrow$ Date or Whole Number.
5. In the top-right corner of the Data Source tab, choose **Extract** (required for saving to Tableau Public).

---

## 2. Worksheet Configurations (The 7 Visualizations)

### Sheet 1: EV Market Performance at a Glance (KPI Cards)
* **Goal:** Displays the 6 core executive figures.
* **Fields:**
  - `COUNTD([Manufacturer])` = **200**
  - `COUNT([Vehicle Id])` = **17,980**
  - `SUM([Annual Sales Units])` = **$1,550.7M Units**
  - `AVG([Customer Rating])` = **4.01 / 5**
  - `AVG([Range Km])` = **324.54 km**
  - `AVG([Battery Capacity Kwh])` = **78.24 kWh**
* **Formatting:** Large bold numbers, centered, with clean subtitle labels.

### Sheet 2: EV Category Performance & Distribution
* **Type:** Vertical Bar Chart.
* **Columns:** `Category`
* **Rows:** `CNT(ev_market_train)`
* **Color:** `Category`
* **Label:** `CNT(ev_market_train)`
* **Sort:** Descending (Two-Wheeler Scooter, Hatchback, Compact SUV, Sedan, etc.).

### Sheet 3: Market Share by Manufacturer
* **Type:** Horizontal Bar Chart.
* **Columns:** `SUM(Annual Sales Units)`
* **Rows:** `Manufacturer` (Filter: Top 10 by Annual Sales Units Sum).
* **Color:** Fixed accent color or sales gradient.
* **Label:** `SUM(Annual Sales Units)` formatted as Currency ($M).
* **Top OEMs:** AmpereWorks ($9.45M), CircuitWorks ($8.92M), MomentumMobility ($8.78M), SurgeDynamics ($8.76M), TerraMotors ($8.75M).

### Sheet 4: Customer Rating Records by EV Category
* **Type:** Tree Map / Heatmap Blocks.
* **Marks:** Square / Treemap.
* **Size:** `CNT(ev_market_train)`
* **Color:** `AVG(Customer Rating)` (Sequential Green/Teal palette).
* **Label:** `Category` + `CNT(ev_market_train)` + `AVG(Customer Rating)`.

### Sheet 5: Annual EV Sales Trend by Model Year
* **Type:** Line Chart.
* **Columns:** `Model Year` (2018–2026).
* **Rows:** `SUM(Annual Sales Units)`.
* **Marks:** Line (Size: Medium, Color: Royal Blue).
* **Label:** Show mark labels for each year.

### Sheet 6: Battery Technology Market Share
* **Type:** Donut Chart or Pie Chart.
* **Marks:** Pie.
* **Color:** `Battery Type`.
* **Angle:** `CNT(ev_market_train)`.
* **Label:** `Battery Type` + `Percent of Total` (NMC 34%, LFP 32%, NCA 17%, Sodium-ion 10%, Solid-State 7%).

### Sheet 7: Electric Vehicle Distribution by Manufacturing Country
* **Type:** Filled World Map (Choropleth).
* **Detail:** `Manufacturing Country`.
* **Color:** `CNT(ev_market_train)` (Sequential Green).
* **Map Layers:** Clean Light or Outdoor layer.

---

## 3. Dashboard Assembly & Interactivity
1. Create a **New Dashboard** (`EV Market Performance & Insights`).
2. Set Size to **Fixed Size (1400 $\times$ 950 px)**.
3. Top Header: Add title and KPI horizontal container.
4. Middle Section:
   - Left: Category Distribution
   - Center: Market Share by Manufacturer
   - Right: Customer Rating Treemap
5. Bottom Section:
   - Left: Annual Sales Trend
   - Center: Battery Technology Share
   - Right: Global Manufacturing Footprint Map
6. Add Global Filters:
   - Right-click map sheet $\rightarrow$ **Filters $\rightarrow$ Manufacturing Country**.
   - Repeat for `Category` and `Manufacturer`.
   - On each filter, select: **Apply to Worksheets $\rightarrow$ All Using This Data Source**.

---

## 4. Multi-Scene Tableau Story
1. Click **New Story**.
2. Add 8 Story Points (scenes):
   - Scene 1: *EV Market Performance at a Glance*
   - Scene 2: *Understanding EV Category Distribution*
   - Scene 3: *Leading Manufacturers Driving the EV Market*
   - Scene 4: *Customer Engagement Across EV Categories*
   - Scene 5: *Growth Trend in Annual EV Sales (2018–2026)*
   - Scene 6: *Battery Technology Market Share & Chemistry*
   - Scene 7: *Global EV Manufacturing Footprint*
   - Scene 8: *Key Business Insights & Strategic Recommendations*
3. Provide descriptive captions for each scene connecting the findings to Emily, David, and Dr. Sarah.

---

## 5. Publishing to Tableau Public
1. Click **File $\rightarrow$ Save to Tableau Public As...**
2. Name the workbook: `Electric Vehicle Market Performance & Insights`.
3. In Tableau Public, click the **Share** button and copy:
   - **Link:** Paste into the SkillWallet "Add Demo Link" field.
   - **Embed Code:** Paste into `D:\Minor Project\templates\dashboard.html`.
