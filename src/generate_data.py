"""
generate_data.py
Generates a realistic synthetic online retail dataset with 7,000+ customers.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

# --- Config ---
N_CUSTOMERS = 7_243
N_TRANSACTIONS = 42_000
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)

PRODUCTS = {
    "Electronics":    ["Wireless Earbuds", "Smart Watch", "USB-C Hub", "Webcam HD", "Power Bank", "Bluetooth Speaker"],
    "Clothing":       ["Casual T-Shirt", "Denim Jacket", "Running Shoes", "Sports Socks", "Hoodie", "Formal Shirt"],
    "Home & Kitchen": ["Coffee Maker", "Air Fryer", "Blender", "Cookware Set", "Knife Set", "Toaster"],
    "Books":          ["Python Programming", "Data Science Guide", "Self-Help Bestseller", "Mystery Novel", "Cook Book", "Finance 101"],
    "Beauty":         ["Face Serum", "Moisturizer SPF50", "Hair Mask", "Lipstick Set", "Eye Cream", "Body Lotion"],
    "Sports":         ["Yoga Mat", "Resistance Bands", "Dumbbells 5kg", "Jump Rope", "Water Bottle", "Gym Gloves"],
}

PRICE_RANGES = {
    "Electronics":    (15, 120),
    "Clothing":       (10, 80),
    "Home & Kitchen": (20, 150),
    "Books":          (8, 35),
    "Beauty":         (12, 60),
    "Sports":         (8, 75),
}

REGIONS = ["North", "South", "East", "West", "Central"]
CHANNELS = ["Website", "Mobile App", "Email Campaign", "Social Media", "Direct"]
PAYMENT_METHODS = ["Credit Card", "Debit Card", "PayPal", "UPI", "Net Banking"]

def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days),
                             hours=random.randint(0, 23),
                             minutes=random.randint(0, 59))

def generate_customers():
    ages = np.random.normal(38, 12, N_CUSTOMERS).clip(18, 75).astype(int)
    genders = np.random.choice(["Male", "Female", "Other"], N_CUSTOMERS, p=[0.47, 0.50, 0.03])
    regions = np.random.choice(REGIONS, N_CUSTOMERS)
    membership = np.random.choice(["Bronze", "Silver", "Gold", "Platinum"], N_CUSTOMERS, p=[0.40, 0.30, 0.20, 0.10])
    signup_dates = [random_date(START_DATE - timedelta(days=365*3), START_DATE) for _ in range(N_CUSTOMERS)]

    customers = pd.DataFrame({
        "customer_id": [f"CUST{str(i).zfill(5)}" for i in range(1, N_CUSTOMERS + 1)],
        "age": ages,
        "gender": genders,
        "region": regions,
        "membership_tier": membership,
        "signup_date": signup_dates,
    })
    return customers

def generate_transactions(customers):
    records = []
    customer_ids = customers["customer_id"].tolist()

    # Skew: top 20% customers generate ~60% of transactions
    weights = np.random.pareto(1.5, N_CUSTOMERS) + 1
    weights = weights / weights.sum()

    for _ in range(N_TRANSACTIONS):
        cid = np.random.choice(customer_ids, p=weights)
        category = random.choice(list(PRODUCTS.keys()))
        product = random.choice(PRODUCTS[category])
        lo, hi = PRICE_RANGES[category]
        price = round(random.uniform(lo, hi), 2)
        qty = np.random.choice([1, 2, 3, 4, 5], p=[0.55, 0.25, 0.10, 0.06, 0.04])
        discount = np.random.choice([0, 5, 10, 15, 20], p=[0.45, 0.20, 0.20, 0.10, 0.05])
        final_price = round(price * qty * (1 - discount / 100), 2)
        date = random_date(START_DATE, END_DATE)
        channel = random.choice(CHANNELS)
        payment = random.choice(PAYMENT_METHODS)
        returned = np.random.choice([0, 1], p=[0.93, 0.07])

        records.append({
            "transaction_id": f"TXN{str(len(records)+1).zfill(7)}",
            "customer_id": cid,
            "date": date,
            "category": category,
            "product": product,
            "unit_price": price,
            "quantity": qty,
            "discount_pct": discount,
            "total_amount": final_price,
            "channel": channel,
            "payment_method": payment,
            "returned": returned,
        })

    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    return df

if __name__ == "__main__":
    print("Generating customers...")
    customers = generate_customers()
    customers.to_csv("data/customers.csv", index=False)
    print(f"  -> {len(customers):,} customers saved to data/customers.csv")

    print("Generating transactions...")
    transactions = generate_transactions(customers)
    transactions.to_csv("data/transactions.csv", index=False)
    print(f"  -> {len(transactions):,} transactions saved to data/transactions.csv")
    print("Done.")
