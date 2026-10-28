# Project Presentation & Viva Voce Defense Guide
## Electric Vehicle Market Performance & Insights

This guide provides the exact script for your **5–7 minute video presentation** (required by SkillWallet) and answers to the most frequent **Viva Voce examination questions**.

---

## Part 1: 5–7 Minute Screen-Recording Video Script

Use OBS Studio, Loom, or Windows Game Bar (`Win + Alt + R`) to record your screen and microphone.

### Timestamp Breakdown:
* **0:00 – 1:00:** Introduction & Problem Statement
* **1:00 – 2:00:** Dataset Description & Preprocessing
* **2:00 – 4:00:** Live Dashboard Demonstration & Filter Testing
* **4:00 – 5:15:** Tableau Data Story Walkthrough (Emily, David & Sarah scenarios)
* **5:15 – 6:15:** Flask Web Application Showcase
* **6:15 – 7:00:** Conclusion & Business Recommendations

---

### Verbatim Presentation Script

#### 0:00 – 1:00 | Introduction & Problem Statement
> *"Hello everyone. My name is Siddharth Yadav, and today I am excited to present my capstone project titled **'Electric Vehicle Market Performance & Insights'**, completed as part of the Data Analytics track on SkillWallet by SmartBridge.*
>
> *The electric vehicle industry is currently the fastest-growing sector in global automotive manufacturing. However, automotive executives, consultants, and researchers face a massive challenge: how to distill hundreds of thousands of complex records into strategic, actionable business decisions. Our project addresses this challenge by providing an end-to-end analytical solution designed for three key decision-makers: Emily Johnson, an EV Market Strategy Director; David Chen, an Automotive BI Consultant; and Dr. Sarah Williams, a Sustainable Mobility Researcher."*

#### 1:00 – 2:00 | Dataset & Preprocessing
> *"Our project is powered by an extensive dataset comprising **200,000 vehicle records across 39 distinct attributes**. This includes vehicle specifications, pricing, battery chemistries, annual sales units, customer ratings, driving range, and global manufacturing countries.*
>
> *During the data preparation phase in Tableau, we standardized data types, assigned geographic roles to country fields, and verified that all numeric measures were properly classified. Crucially, to ensure high responsiveness and zero performance lag, we relied on Tableau's optimized native aggregation engine—`SUM`, `AVG`, `COUNT`, and `COUNTD`—avoiding costly calculated string expressions."*

#### 2:00 – 4:00 | Live Dashboard Demonstration
*(Action: Open the Tableau Dashboard / Flask Dashboard on your screen)*
> *"Now, let's examine our interactive executive dashboard.*
>
> *At the top, we immediately see our six core KPI scorecards: **200 manufacturers**, **17,980 vehicle models**, **$1,550.7 million in annual sales**, an average customer satisfaction of **4.01 out of 5**, an average driving range of **324.54 kilometers**, and an average battery capacity of **78.24 kilowatt-hours**.*
>
> *Looking at our categorical breakdown, **Two-Wheeler Scooters and Hatchbacks** represent the highest volume of vehicle adoption, showing that consumers prioritize affordable urban transit.*
>
> *In our OEM market share analysis, **AmpereWorks** leads the market with $9.45 million in annual sales, followed closely by CircuitWorks, MomentumMobility, SurgeDynamics, and TerraMotors. The top five OEMs are separated by less than 8%, highlighting an intensely competitive landscape.*
>
> *Notice our battery technology chart: **NMC and LFP chemistry** account for two-thirds of the entire market, while **Sodium-ion** has emerged strongly with over 10% share.*
>
> *Now, let me demonstrate our interactive filtering:*
> *(Action: Click a filter dropdown—e.g., select country 'USA' or category 'Hatchback')*
> *Notice how all seven visualizations update synchronously in real-time, providing deep segment-level clarity."*

#### 4:00 – 5:15 | Data Story Walkthrough
*(Action: Click the 'Story' tab)*
> *"To bridge technical analytics with executive decision-making, we structured an 8-scene Data Story.*
>
> *Scene 1 establishes the macroeconomic overview. Scenes 2 and 3 address **Emily Johnson's** strategic requirements by pinpointing the most lucrative form factors and OEM market share spreads. Scenes 4 and 5 track customer satisfaction and longitudinal sales growth, showing our trajectory toward peak sales in 2026.*
>
> *Scenes 6 and 7 speak directly to **Dr. Sarah Williams** and **David Chen**, evaluating battery degradation rates and illustrating the balanced global manufacturing footprint across India, the United States, China, South Korea, and Sweden. Finally, Scene 8 synthesizes our actionable recommendations."*

#### 5:15 – 6:15 | Full-Stack Flask Web Integration
*(Action: Switch to the browser tab running `http://127.0.0.1:5000`)*
> *"To make these insights accessible to any executive worldwide, we built and deployed a responsive web application using Python and the Flask framework.*
>
> *The application features an executive dark theme with a hero landing section, KPI scorecards, and a dedicated scenarios page. On our web dashboard, users can interact with live charts powered by an in-memory SQLite analytical engine, or toggle directly to view the embedded, cloud-hosted Tableau Public dashboard."*

#### 6:15 – 7:00 | Conclusion & Recommendations
> *"In conclusion, our analysis yields three strategic recommendations:*
> *First, OEMs should prioritize modular LFP battery platforms for hatchbacks and compact SUVs to dominate urban volume.*
> *Second, new entrants should target partnerships in high-density production hubs like India and the US to circumvent tariff barriers.*
> *And third, governments should incentivize sodium-ion adoption to alleviate lithium supply chain strains.*
>
> *Thank you very much for your time. All project source code, Tableau workbooks, and documentation have been uploaded to GitHub."*

---

## Part 2: Viva Voce Examination Questions & Answers

### Q1: Why did you choose Tableau for this analytics project?
**Answer:** Tableau was chosen because of its enterprise-grade data visualization capabilities, high-speed in-memory data engine (Hyper), and built-in geographic mapping. It allows rapid exploratory analysis, seamless dashboard creation with cross-filtering, and intuitive narrative storytelling through Tableau Story Points without requiring complex frontend visualization programming.

### Q2: Why are there no custom calculated fields in this project?
**Answer:** The dataset already provides well-structured numerical measures for all key attributes (such as annual sales, driving range, battery capacity, and customer ratings). By utilizing Tableau's native aggregation functions (`SUM`, `AVG`, `COUNTD`), we eliminate row-level computation overhead, ensuring that 200,000 records filter and render in under 200 milliseconds.

### Q3: How did you ensure the dashboard performs smoothly with 200,000 rows?
**Answer:** We implemented three performance optimization strategies:
1. Used a Tableau Data Extract (`.hyper`) instead of a live file connection.
2. Filtered at the database/data source level where appropriate and avoided heavy string calculations.
3. In the Flask web application, we leveraged an in-memory SQLite database indexed on categorical columns, which answers aggregated queries in milliseconds.

### Q4: What is the significance of the 8-scene Data Story?
**Answer:** A dashboard shows *what* is happening at a specific moment, while a Data Story explains *why* it is happening and *what action* should be taken. Our 8 scenes guide the viewer logically from global sales totals to category adoption, manufacturer benchmarking, battery technology trade-offs, and geographic footprints, directly answering the needs of Emily Johnson, David Chen, and Dr. Sarah Williams.

### Q5: How is the Flask web integration implemented?
**Answer:** The Flask application (`app.py`) serves as the full-stack controller. It exposes REST API endpoints (`/api/metrics`, `/api/query`) that query the pre-aggregated data or in-memory SQLite database. The frontend uses modern semantic HTML5, responsive CSS, and Chart.js for native visualization, alongside an embedded iframe/object script communicating with the Tableau Public JavaScript API.
