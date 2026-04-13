"""
analysis.py
Online Retail Analysis — Churn, Retention, Segmentation & Product Insights
Generates 11 visualizations and prints a full business insights summary.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from pathlib import Path
import warnings

warnings.filterwarnings("ignore")

# ── Paths ────────────────────────────────────────────────────────────────────
ROOT   = Path(__file__).resolve().parent.parent
DATA   = ROOT / "data"
PLOTS  = ROOT / "outputs" / "plots"
PLOTS.mkdir(parents=True, exist_ok=True)

# ── Style ─────────────────────────────────────────────────────────────────────
PALETTE   = ["#2D6A4F", "#40916C", "#52B788", "#74C69D", "#95D5B2", "#B7E4C7"]
ACCENT    = "#F4845F"
DARK_BG   = "#0D1117"
CARD_BG   = "#161B22"
TEXT_CLR  = "#E6EDF3"
GRID_CLR  = "#21262D"

plt.rcParams.update({
    "figure.facecolor":  DARK_BG,
    "axes.facecolor":    CARD_BG,
    "axes.edgecolor":    GRID_CLR,
    "axes.labelcolor":   TEXT_CLR,
    "axes.titlecolor":   TEXT_CLR,
    "axes.titlesize":    14,
    "axes.labelsize":    11,
    "xtick.color":       TEXT_CLR,
    "ytick.color":       TEXT_CLR,
    "grid.color":        GRID_CLR,
    "text.color":        TEXT_CLR,
    "legend.facecolor":  CARD_BG,
    "legend.edgecolor":  GRID_CLR,
    "legend.labelcolor": TEXT_CLR,
    "font.family":       "monospace",
    "figure.dpi":        150,
})

def save(fig, name):
    path = PLOTS / name
    fig.savefig(path, bbox_inches="tight", facecolor=DARK_BG)
    plt.close(fig)
    print(f"  [saved] {path.name}")


# ── Load Data ─────────────────────────────────────────────────────────────────
print("Loading data...")
customers = pd.read_csv(DATA / "customers.csv", parse_dates=["signup_date"])
txn       = pd.read_csv(DATA / "transactions.csv", parse_dates=["date"])

txn["month"]       = txn["date"].dt.to_period("M")
txn["year"]        = txn["date"].dt.year
txn["day_of_week"] = txn["date"].dt.day_name()
txn["hour"]        = txn["date"].dt.hour

merged = txn.merge(customers, on="customer_id", how="left")
print(f"  -> {len(customers):,} customers | {len(txn):,} transactions")


# ═══════════════════════════════════════════════════════════════════════════════
# PLOT 1 — Monthly Revenue Trend (Line)
# ═══════════════════════════════════════════════════════════════════════════════
print("\n[1/11] Monthly Revenue Trend")
monthly_rev = txn.groupby("month")["total_amount"].sum().reset_index()
monthly_rev["month_dt"] = monthly_rev["month"].dt.to_timestamp()

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(monthly_rev["month_dt"], monthly_rev["total_amount"] / 1000,
        color=PALETTE[1], linewidth=2.5, marker="o", markersize=5)
ax.fill_between(monthly_rev["month_dt"], monthly_rev["total_amount"] / 1000,
                alpha=0.15, color=PALETTE[1])
ax.set_title("Monthly Revenue Trend (2023–2024)", pad=15)
ax.set_xlabel("Month")
ax.set_ylabel("Revenue ($ thousands)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}K"))
ax.grid(axis="y", linestyle="--", alpha=0.4)
fig.tight_layout()
save(fig, "01_monthly_revenue_trend.png")


# ═══════════════════════════════════════════════════════════════════════════════
# PLOT 2 — Revenue by Category (Bar)
# ═══════════════════════════════════════════════════════════════════════════════
print("[2/11] Revenue by Category")
cat_rev = txn.groupby("category")["total_amount"].sum().sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(9, 6))
bars = ax.barh(cat_rev.index, cat_rev.values / 1000, color=PALETTE[:len(cat_rev)], edgecolor="none")
for bar, val in zip(bars, cat_rev.values):
    ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2,
            f"${val/1000:,.1f}K", va="center", fontsize=10)
ax.set_title("Total Revenue by Product Category")
ax.set_xlabel("Revenue ($ thousands)")
ax.set_xlim(0, cat_rev.max() / 1000 * 1.18)
ax.grid(axis="x", linestyle="--", alpha=0.4)
fig.tight_layout()
save(fig, "02_revenue_by_category.png")


# ═══════════════════════════════════════════════════════════════════════════════
# PLOT 3 — Heatmap: Revenue by Day-of-Week × Hour
# ═══════════════════════════════════════════════════════════════════════════════
print("[3/11] Heatmap — Day × Hour Revenue")
dow_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
heat_data = (txn.groupby(["day_of_week", "hour"])["total_amount"]
               .sum()
               .unstack(fill_value=0)
               .reindex(dow_order))

fig, ax = plt.subplots(figsize=(14, 5))
sns.heatmap(heat_data / 1000, ax=ax,
            cmap="YlGn", linewidths=0.3, linecolor=DARK_BG,
            cbar_kws={"label": "Revenue ($K)", "shrink": 0.8},
            annot=False)
ax.set_title("Revenue Heatmap — Day of Week × Hour of Day", pad=12)
ax.set_xlabel("Hour of Day")
ax.set_ylabel("")
fig.tight_layout()
save(fig, "03_heatmap_dow_hour.png")


# ═══════════════════════════════════════════════════════════════════════════════
# PLOT 4 — Heatmap: Category × Region Revenue
# ═══════════════════════════════════════════════════════════════════════════════
print("[4/11] Heatmap — Category × Region")
cat_region = (merged.groupby(["category", "region"])["total_amount"]
                    .sum()
                    .unstack(fill_value=0))

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(cat_region / 1000, ax=ax,
            cmap="mako", linewidths=0.4, linecolor=DARK_BG,
            annot=True, fmt=".0f",
            cbar_kws={"label": "Revenue ($K)", "shrink": 0.85})
ax.set_title("Revenue Heatmap — Category × Region ($K)", pad=12)
ax.set_xlabel("Region")
ax.set_ylabel("")
fig.tight_layout()
save(fig, "04_heatmap_category_region.png")


# ═══════════════════════════════════════════════════════════════════════════════
# PLOT 5 — Histogram: Customer Spend Distribution
# ═══════════════════════════════════════════════════════════════════════════════
print("[5/11] Histogram — Customer Spend")
cust_spend = txn.groupby("customer_id")["total_amount"].sum()

fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(cust_spend.clip(upper=np.percentile(cust_spend, 97)),
        bins=60, color=PALETTE[2], edgecolor=DARK_BG, linewidth=0.5)
ax.axvline(cust_spend.median(), color=ACCENT, linewidth=2, linestyle="--",
           label=f"Median: ${cust_spend.median():,.0f}")
ax.axvline(cust_spend.mean(), color="#FFD166", linewidth=2, linestyle=":",
           label=f"Mean: ${cust_spend.mean():,.0f}")
ax.set_title("Distribution of Total Spend per Customer (top 97th pct clipped)")
ax.set_xlabel("Total Spend ($)")
ax.set_ylabel("Number of Customers")
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.4)
fig.tight_layout()
save(fig, "05_histogram_customer_spend.png")


# ═══════════════════════════════════════════════════════════════════════════════
# PLOT 6 — Histogram: Order Value Distribution
# ═══════════════════════════════════════════════════════════════════════════════
print("[6/11] Histogram — Order Value")
fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(txn["total_amount"].clip(upper=300), bins=70,
        color=PALETTE[3], edgecolor=DARK_BG, linewidth=0.4)
ax.axvline(txn["total_amount"].median(), color=ACCENT, linewidth=2, linestyle="--",
           label=f"Median: ${txn['total_amount'].median():.2f}")
ax.set_title("Order Value Distribution (clipped at $300)")
ax.set_xlabel("Order Value ($)")
ax.set_ylabel("Transaction Count")
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.4)
fig.tight_layout()
save(fig, "06_histogram_order_value.png")


# ═══════════════════════════════════════════════════════════════════════════════
# PLOT 7 — Boxplot: Spend Distribution by Membership Tier
# ═══════════════════════════════════════════════════════════════════════════════
print("[7/11] Boxplot — Spend by Membership Tier")
tier_order = ["Bronze", "Silver", "Gold", "Platinum"]
tier_spend = merged.groupby(["customer_id", "membership_tier"])["total_amount"].sum().reset_index()
tier_spend = tier_spend[tier_spend["membership_tier"].isin(tier_order)]

fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=tier_spend, x="membership_tier", y="total_amount",
            order=tier_order, palette=PALETTE[:4], ax=ax,
            flierprops={"marker": ".", "color": ACCENT, "alpha": 0.4, "markersize": 4},
            width=0.5)
ax.set_title("Customer Lifetime Spend by Membership Tier")
ax.set_xlabel("Membership Tier")
ax.set_ylabel("Total Spend ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.grid(axis="y", linestyle="--", alpha=0.4)
fig.tight_layout()
save(fig, "07_boxplot_spend_by_tier.png")


# ═══════════════════════════════════════════════════════════════════════════════
# PLOT 8 — Boxplot: Order Value by Acquisition Channel
# ═══════════════════════════════════════════════════════════════════════════════
print("[8/11] Boxplot — Order Value by Channel")
fig, ax = plt.subplots(figsize=(11, 6))
channel_order = txn.groupby("channel")["total_amount"].median().sort_values(ascending=False).index
sns.boxplot(data=txn[txn["total_amount"] < txn["total_amount"].quantile(0.97)],
            x="channel", y="total_amount",
            order=channel_order, palette=PALETTE[:5], ax=ax,
            flierprops={"marker": ".", "color": ACCENT, "alpha": 0.3, "markersize": 3},
            width=0.5)
ax.set_title("Order Value Distribution by Acquisition Channel")
ax.set_xlabel("Channel")
ax.set_ylabel("Order Value ($)")
ax.grid(axis="y", linestyle="--", alpha=0.4)
fig.tight_layout()
save(fig, "08_boxplot_order_by_channel.png")


# ═══════════════════════════════════════════════════════════════════════════════
# PLOT 9 — Churn Analysis: Recency Buckets (Bar)
# ═══════════════════════════════════════════════════════════════════════════════
print("[9/11] Churn — Recency Buckets")
snapshot = txn["date"].max()
recency  = txn.groupby("customer_id")["date"].max().reset_index()
recency["days_since"] = (snapshot - recency["date"]).dt.days
recency["segment"] = pd.cut(
    recency["days_since"],
    bins=[0, 30, 90, 180, 365, 9999],
    labels=["Active (≤30d)", "Recent (31–90d)", "At Risk (91–180d)",
            "Churning (181–365d)", "Churned (>365d)"]
)

seg_counts = recency["segment"].value_counts().reindex(
    ["Active (≤30d)", "Recent (31–90d)", "At Risk (91–180d)",
     "Churning (181–365d)", "Churned (>365d)"]
)

fig, ax = plt.subplots(figsize=(10, 5))
colors = [PALETTE[1], PALETTE[2], "#FFD166", ACCENT, "#E63946"]
bars = ax.bar(seg_counts.index, seg_counts.values, color=colors, edgecolor="none")
for bar, val in zip(bars, seg_counts.values):
    pct = val / seg_counts.sum() * 100
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 20,
            f"{val:,}\n({pct:.1f}%)", ha="center", fontsize=9)
ax.set_title("Customer Retention Segments by Recency")
ax.set_xlabel("Segment")
ax.set_ylabel("Number of Customers")
ax.set_ylim(0, seg_counts.max() * 1.2)
ax.tick_params(axis="x", labelrotation=15)
ax.grid(axis="y", linestyle="--", alpha=0.4)
fig.tight_layout()
save(fig, "09_churn_recency_segments.png")


# ═══════════════════════════════════════════════════════════════════════════════
# PLOT 10 — RFM Scatter: Recency vs Frequency (coloured by Monetary)
# ═══════════════════════════════════════════════════════════════════════════════
print("[10/11] RFM Scatter")
rfm = txn.groupby("customer_id").agg(
    recency   = ("date",         lambda x: (snapshot - x.max()).days),
    frequency = ("transaction_id", "count"),
    monetary  = ("total_amount",  "sum"),
).reset_index()

sample = rfm.sample(min(2000, len(rfm)), random_state=42)
fig, ax = plt.subplots(figsize=(10, 7))
sc = ax.scatter(sample["recency"], sample["frequency"],
                c=sample["monetary"], cmap="YlGn", alpha=0.65,
                s=20, edgecolors="none", vmax=np.percentile(sample["monetary"], 95))
cbar = fig.colorbar(sc, ax=ax, shrink=0.85)
cbar.set_label("Monetary Value ($)")
ax.set_title("RFM Analysis — Recency vs. Frequency (color = Spend)")
ax.set_xlabel("Recency (days since last purchase)")
ax.set_ylabel("Purchase Frequency")
ax.grid(linestyle="--", alpha=0.3)
fig.tight_layout()
save(fig, "10_rfm_scatter.png")


# ═══════════════════════════════════════════════════════════════════════════════
# PLOT 11 — Top 15 Products by Revenue (Horizontal Bar)
# ═══════════════════════════════════════════════════════════════════════════════
print("[11/11] Top Products by Revenue")
top_products = (txn.groupby("product")["total_amount"]
                   .sum()
                   .sort_values(ascending=False)
                   .head(15))

fig, ax = plt.subplots(figsize=(10, 7))
colors_grad = [PALETTE[1] if i < 3 else PALETTE[3] for i in range(len(top_products))]
bars = ax.barh(top_products.index[::-1], top_products.values[::-1] / 1000,
               color=colors_grad[::-1], edgecolor="none")
for bar, val in zip(bars, top_products.values[::-1]):
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
            f"${val/1000:,.1f}K", va="center", fontsize=9)
ax.set_title("Top 15 Products by Total Revenue")
ax.set_xlabel("Revenue ($ thousands)")
ax.set_xlim(0, top_products.max() / 1000 * 1.18)
ax.grid(axis="x", linestyle="--", alpha=0.4)
fig.tight_layout()
save(fig, "11_top15_products_revenue.png")


# ═══════════════════════════════════════════════════════════════════════════════
# BUSINESS INSIGHTS SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═" * 65)
print("  BUSINESS INSIGHTS SUMMARY")
print("═" * 65)

total_rev   = txn["total_amount"].sum()
avg_order   = txn["total_amount"].mean()
top_cat     = txn.groupby("category")["total_amount"].sum().idxmax()
top_product = txn.groupby("product")["total_amount"].sum().idxmax()
active_pct  = seg_counts["Active (≤30d)"] / seg_counts.sum() * 100
churned_pct = seg_counts["Churned (>365d)"] / seg_counts.sum() * 100
best_chan    = txn.groupby("channel")["total_amount"].sum().idxmax()
return_rate = txn["returned"].mean() * 100
plat_spend  = tier_spend[tier_spend["membership_tier"]=="Platinum"]["total_amount"].mean()
bronze_spend= tier_spend[tier_spend["membership_tier"]=="Bronze"]["total_amount"].mean()

print(f"\n{'Total Revenue:':<40} ${total_rev:>12,.2f}")
print(f"{'Average Order Value:':<40} ${avg_order:>12,.2f}")
print(f"{'Top Revenue Category:':<40} {top_cat:>14}")
print(f"{'Top Revenue Product:':<40} {top_product:>14}")
print(f"{'Best Acquisition Channel:':<40} {best_chan:>14}")
print(f"{'Active Customers (≤30 days):':<40} {active_pct:>13.1f}%")
print(f"{'Churned Customers (>365 days):':<40} {churned_pct:>13.1f}%")
print(f"{'Return/Refund Rate:':<40} {return_rate:>13.1f}%")
print(f"{'Avg Platinum Lifetime Spend:':<40} ${plat_spend:>12,.2f}")
print(f"{'Avg Bronze Lifetime Spend:':<40} ${bronze_spend:>12,.2f}")
print(f"{'Platinum vs Bronze Multiplier:':<40} {plat_spend/bronze_spend:>13.1f}x")

print("\n── Key Findings ─────────────────────────────────────────────")
print(f"  1. {top_cat} is the highest-grossing category.")
print(f"  2. Only {active_pct:.1f}% of customers are active within 30 days —")
print(f"     a re-engagement campaign for at-risk segments is recommended.")
print(f"  3. Platinum members spend {plat_spend/bronze_spend:.1f}x more than Bronze members;")
print(f"     loyalty upgrades represent significant revenue leverage.")
print(f"  4. {best_chan} drives the most revenue — budget allocation should")
print(f"     prioritise this channel.")
print(f"  5. {return_rate:.1f}% return rate is within acceptable range but warrants")
print(f"     product quality monitoring in {top_cat}.")
print("═" * 65)
print(f"\n✓ All 11 plots saved to:  {PLOTS}\n")
