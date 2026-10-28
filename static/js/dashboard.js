/**
 * EV Market Performance & Insights - Interactive Dashboard Engine
 * Uses Chart.js with dynamic API integration & live cross-filtering
 */

let categoryChart, mfgChart, trendChart, batteryChart, countryChart;

document.addEventListener('DOMContentLoaded', async () => {
    await populateFilters();
    await loadInitialData();
    setupEventListeners();
});

async function populateFilters() {
    try {
        const res = await fetch('/api/filters');
        const data = await res.json();

        const countrySel = document.getElementById('filterCountry');
        const catSel = document.getElementById('filterCategory');
        const mfgSel = document.getElementById('filterMfg');

        data.countries.forEach(c => {
            const opt = document.createElement('option');
            opt.value = c;
            opt.textContent = c;
            countrySel.appendChild(opt);
        });

        data.categories.forEach(c => {
            const opt = document.createElement('option');
            opt.value = c;
            opt.textContent = c;
            catSel.appendChild(opt);
        });

        data.manufacturers.forEach(m => {
            const opt = document.createElement('option');
            opt.value = m;
            opt.textContent = m;
            mfgSel.appendChild(opt);
        });
    } catch (err) {
        console.error("Failed to load filters:", err);
    }
}

async function loadInitialData() {
    try {
        const res = await fetch('/api/metrics');
        const data = await res.json();
        renderAllCharts(data);
    } catch (err) {
        console.error("Failed to load metrics:", err);
    }
}

function setupEventListeners() {
    const filterBtn = document.getElementById('applyFilterBtn');
    const resetBtn = document.getElementById('resetFilterBtn');

    if (filterBtn) {
        filterBtn.addEventListener('click', applyFilters);
    }

    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            document.getElementById('filterCountry').value = 'All';
            document.getElementById('filterCategory').value = 'All';
            document.getElementById('filterMfg').value = 'All';
            loadInitialData();
        });
    }
}

async function applyFilters() {
    const country = document.getElementById('filterCountry').value;
    const category = document.getElementById('filterCategory').value;
    const manufacturer = document.getElementById('filterMfg').value;

    const url = `/api/query?country=${encodeURIComponent(country)}&category=${encodeURIComponent(category)}&manufacturer=${encodeURIComponent(manufacturer)}`;

    try {
        const res = await fetch(url);
        const data = await res.json();

        // Update KPIs
        document.getElementById('kpiRecords').textContent = Number(data.kpis.total_records).toLocaleString();
        document.getElementById('kpiManufacturers').textContent = Number(data.kpis.total_manufacturers).toLocaleString();
        document.getElementById('kpiSales').textContent = data.kpis.total_sales_display;
        document.getElementById('kpiRating').textContent = `${data.kpis.avg_customer_rating} / 5`;
        document.getElementById('kpiRange').textContent = `${data.kpis.avg_driving_range_km} km`;
        document.getElementById('kpiCapacity').textContent = `${data.kpis.avg_battery_capacity_kwh} kWh`;

        // Update Chart Data
        updateChart(categoryChart, Object.keys(data.categories), Object.values(data.categories));
        updateChart(mfgChart, Object.keys(data.manufacturers), Object.values(data.manufacturers));
        updateChart(trendChart, Object.keys(data.trend), Object.values(data.trend));
        updateChart(batteryChart, Object.keys(data.battery), Object.values(data.battery));
    } catch (err) {
        console.error("Filter query failed:", err);
    }
}

function updateChart(chart, labels, data) {
    if (!chart) return;
    chart.data.labels = labels;
    chart.data.datasets[0].data = data;
    chart.update();
}

function renderAllCharts(metrics) {
    const isDark = true;
    const gridColor = 'rgba(255, 255, 255, 0.06)';
    const textColor = '#9ca3af';

    // 1. Category Distribution Bar Chart
    const ctxCat = document.getElementById('categoryChart');
    if (ctxCat) {
        if (categoryChart) categoryChart.destroy();
        const catLabels = Object.keys(metrics.category_distribution);
        const catData = Object.values(metrics.category_distribution);

        categoryChart = new Chart(ctxCat, {
            type: 'bar',
            data: {
                labels: catLabels,
                datasets: [{
                    label: 'Models / Records',
                    data: catData,
                    backgroundColor: '#10b981',
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { ticks: { color: textColor, maxRotation: 45, minRotation: 25 }, grid: { display: false } },
                    y: { ticks: { color: textColor }, grid: { color: gridColor } }
                }
            }
        });
    }

    // 2. Manufacturer Market Share Horizontal Bar Chart
    const ctxMfg = document.getElementById('mfgChart');
    if (ctxMfg) {
        if (mfgChart) mfgChart.destroy();
        const mfgLabels = Object.keys(metrics.manufacturer_market_share);
        const mfgData = Object.values(metrics.manufacturer_market_share).map(v => (v / 1e6).toFixed(2));

        mfgChart = new Chart(ctxMfg, {
            type: 'bar',
            data: {
                labels: mfgLabels,
                datasets: [{
                    label: 'Annual Sales ($M)',
                    data: mfgData,
                    backgroundColor: '#f59e0b',
                    borderRadius: 4
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { ticks: { color: textColor, callback: v => `$${v}M` }, grid: { color: gridColor } },
                    y: { ticks: { color: textColor }, grid: { display: false } }
                }
            }
        });
    }

    // 3. Annual Sales Trend Line Chart (2018-2026)
    const ctxTrend = document.getElementById('trendChart');
    if (ctxTrend) {
        if (trendChart) trendChart.destroy();
        const trendLabels = Object.keys(metrics.annual_sales_trend);
        const trendData = Object.values(metrics.annual_sales_trend).map(v => (v / 1e6).toFixed(2));

        trendChart = new Chart(ctxTrend, {
            type: 'line',
            data: {
                labels: trendLabels,
                datasets: [{
                    label: 'Sales Units (Millions)',
                    data: trendData,
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    borderWidth: 2.5,
                    fill: true,
                    tension: 0.35,
                    pointBackgroundColor: '#60a5fa',
                    pointRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { ticks: { color: textColor }, grid: { display: false } },
                    y: { ticks: { color: textColor, callback: v => `${v}M` }, grid: { color: gridColor } }
                }
            }
        });
    }

    // 4. Battery Technology Donut Chart
    const ctxBattery = document.getElementById('batteryChart');
    if (ctxBattery) {
        if (batteryChart) batteryChart.destroy();
        const battLabels = Object.keys(metrics.battery_technology_percentage);
        const battData = Object.values(metrics.battery_technology_percentage);

        batteryChart = new Chart(ctxBattery, {
            type: 'doughnut',
            data: {
                labels: battLabels,
                datasets: [{
                    data: battData,
                    backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#ec4899', '#8b5cf6'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: textColor, boxWidth: 12, padding: 14 }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(item) {
                                return ` ${item.label}: ${item.raw}%`;
                            }
                        }
                    }
                },
                cutout: '68%'
            }
        });
    }

    // 5. Country Distribution Bar Chart
    const ctxCountry = document.getElementById('countryChart');
    if (ctxCountry) {
        if (countryChart) countryChart.destroy();
        const cLabels = Object.keys(metrics.country_distribution).slice(0, 8);
        const cData = Object.values(metrics.country_distribution).slice(0, 8);

        countryChart = new Chart(ctxCountry, {
            type: 'bar',
            data: {
                labels: cLabels,
                datasets: [{
                    label: 'Manufactured EV Records',
                    data: cData,
                    backgroundColor: '#8b5cf6',
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { ticks: { color: textColor }, grid: { display: false } },
                    y: { ticks: { color: textColor }, grid: { color: gridColor } }
                }
            }
        });
    }
}
