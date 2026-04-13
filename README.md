# 🛒 Online Retail Analysis

> Exploratory data analysis of **7,243 customers** and **42,000 transactions** to uncover churn patterns, retention trends, and high-value product segments.

---

## 📌 Project Overview

This project analyses a synthetic online retail dataset spanning **January 2023 – December 2024**. The goal is to extract actionable business insights around customer churn, retention segments, product performance, and acquisition channel effectiveness — the kind of analysis a data analyst would deliver to a retail or e-commerce product team.

| Metric | Value |
|---|---|
| Customers | 7,243 |
| Transactions | 42,000 |
| Date Range | Jan 2023 – Dec 2024 |
| Total Revenue | ~$3.53M |
| Categories | 6 (Electronics, Clothing, Home & Kitchen, Books, Beauty, Sports) |

---

## 🔍 Key Business Insights

1. **Home & Kitchen** is the highest-grossing category across all regions, contributing the largest share of total revenue.
2. Only **~18% of customers** made a purchase within the last 30 days — a substantial portion sits in "at-risk" or "churned" buckets, indicating strong re-engagement opportunities.
3. **Mobile App** outperforms all other acquisition channels in total revenue generated.
4. **Platinum-tier** members represent a high-leverage upsell segment; loyalty program investment shows measurable spend differentiation.
5. **~7% return rate** is within acceptable industry benchmarks but warrants ongoing product quality monitoring in high-ticket categories.
6. The **RFM scatter plot** reveals a long tail of infrequent, low-spend customers — a latent growth segment for targeted promotions.
7. **Saturday afternoons and Wednesday evenings** show the highest purchase activity (Day × Hour heatmap).

---

## 📊 Visualizations (11 total)

| # | Plot | Type |
|---|---|---|
| 01 | Monthly Revenue Trend (2023–2024) | Line + Fill |
| 02 | Total Revenue by Product Category | Horizontal Bar |
| 03 | Revenue Heatmap — Day of Week × Hour | Heatmap |
| 04 | Revenue Heatmap — Category × Region | Heatmap (annotated) |
| 05 | Customer Lifetime Spend Distribution | Histogram |
| 06 | Order Value Distribution | Histogram |
| 07 | Customer Spend by Membership Tier | Boxplot |
| 08 | Order Value by Acquisition Channel | Boxplot |
| 09 | Customer Retention Segments (Recency) | Bar |
| 10 | RFM Scatter — Recency vs. Frequency | Scatter |
| 11 | Top 15 Products by Revenue | Horizontal Bar |

All plots are saved to `outputs/plots/`.

---

## 🗂️ Project Structure

```
online-retail-analysis/
│
├── data/
│   ├── customers.csv          # 7,243 customer records
│   └── transactions.csv       # 42,000 transaction records
│
├── notebooks/
│   └── retail_analysis.ipynb  # Full interactive analysis notebook
│
├── src/
│   ├── generate_data.py       # Synthetic data generator (run once)
│   └── analysis.py            # Main analysis script (11 plots + insights)
│
├── outputs/
│   └── plots/                 # All 11 generated PNG visualizations
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/online-retail-analysis.git
cd online-retail-analysis
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate the dataset
```bash
python src/generate_data.py
```

### 4. Run the full analysis
```bash
python src/analysis.py
```

### 5. Or explore interactively
```bash
jupyter notebook notebooks/retail_analysis.ipynb
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **Python 3.11+** | Core language |
| **Pandas** | Data loading, cleaning, aggregation |
| **NumPy** | Numerical operations, RFM computation |
| **Matplotlib** | Line charts, histograms, bar charts |
| **Seaborn** | Heatmaps, boxplots, statistical plots |
| **Jupyter** | Interactive exploration |

---

## 📈 Analysis Methodology

### Churn Segmentation (Recency-Based)
Customers are segmented into five buckets based on **days since last purchase**:

| Segment | Days Since Last Purchase |
|---|---|
| Active | ≤ 30 days |
| Recent | 31 – 90 days |
| At Risk | 91 – 180 days |
| Churning | 181 – 365 days |
| Churned | > 365 days |

### RFM Analysis
Each customer is profiled on three dimensions:
- **Recency** — How recently did they purchase?
- **Frequency** — How many purchases have they made?
- **Monetary** — How much have they spent in total?

The RFM scatter plot (Plot 10) visually maps customers in the Recency × Frequency space, with colour encoding monetary value, enabling instant identification of high-value vs. lapsed customers.

---

## 📁 Dataset Schema

**customers.csv**
| Column | Type | Description |
|---|---|---|
| `customer_id` | string | Unique customer identifier |
| `age` | int | Customer age (18–75) |
| `gender` | string | Male / Female / Other |
| `region` | string | North / South / East / West / Central |
| `membership_tier` | string | Bronze / Silver / Gold / Platinum |
| `signup_date` | datetime | Account creation date |

**transactions.csv**
| Column | Type | Description |
|---|---|---|
| `transaction_id` | string | Unique transaction identifier |
| `customer_id` | string | FK → customers |
| `date` | datetime | Purchase timestamp |
| `category` | string | Product category |
| `product` | string | Product name |
| `unit_price` | float | Price per unit ($) |
| `quantity` | int | Units purchased |
| `discount_pct` | int | Discount applied (%) |
| `total_amount` | float | Final order value ($) |
| `channel` | string | Acquisition channel |
| `payment_method` | string | Payment type |
| `returned` | int | 1 if returned, 0 otherwise |


