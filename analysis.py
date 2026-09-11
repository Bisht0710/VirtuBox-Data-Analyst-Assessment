import pandas as pd

file_path = r"C:\Users\HP\Downloads\online+retail+ii\online_retail_II.xlsx"

print("Reading 2009-2010...")
df_2009 = pd.read_excel(file_path, sheet_name="Year 2009-2010")

print("Reading 2010-2011...")
df_2010 = pd.read_excel(file_path, sheet_name="Year 2010-2011")

print("Combining datasets...")

df = pd.concat([df_2009, df_2010], ignore_index=True)

print("Total rows:", len(df))
print("Total columns:", len(df.columns))

print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())
print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nData types:")
print(df.dtypes)
print("\nCancelled transactions:")

cancelled = df["Invoice"].astype(str).str.startswith("C")

print("Cancelled rows:", cancelled.sum())
print("Normal rows:", (~cancelled).sum())

print("\nNegative quantities:")
print((df["Quantity"] < 0).sum())

print("\nNegative prices:")
print((df["Price"] < 0).sum())
print("\nRecords with negative price:")
print(df[df["Price"] < 0][[
    "Invoice",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "Price",
    "Customer ID",
    "Country"
]])
# ==============================
# DATA CLEANING
# ==============================

print("\nStarting data cleaning...")

# 1. Remove exact duplicate rows
df_clean = df.drop_duplicates().copy()

print("Rows after removing duplicates:", len(df_clean))

# 2. Remove invalid negative-price accounting adjustments
df_clean = df_clean[df_clean["Price"] >= 0].copy()

print("Rows after removing negative prices:", len(df_clean))

# 3. Create cancellation flag
df_clean["IsCancelled"] = df_clean["Invoice"].astype(str).str.startswith("C")

# 4. Create return flag
df_clean["IsReturn"] = df_clean["Quantity"] < 0

# 5. Calculate revenue
df_clean["Revenue"] = df_clean["Quantity"] * df_clean["Price"]

print("Cleaning completed.")

print("\nProcessed data preview:")
print(df_clean.head())

print("\nProcessed rows:", len(df_clean))
print("Processed columns:", len(df_clean.columns))
# ==============================
# ADD ANALYSIS FIELDS
# ==============================

# Fill missing product descriptions
df_clean["Description"] = df_clean["Description"].fillna("Unknown Product")

# Convert Customer ID to string-friendly format
df_clean["Customer ID"] = df_clean["Customer ID"].fillna("Unknown")

# Create date-related fields
df_clean["Year"] = df_clean["InvoiceDate"].dt.year
df_clean["Month"] = df_clean["InvoiceDate"].dt.month
df_clean["Month_Name"] = df_clean["InvoiceDate"].dt.month_name()
df_clean["Day"] = df_clean["InvoiceDate"].dt.day
df_clean["Day_Name"] = df_clean["InvoiceDate"].dt.day_name()

# Create year-month field for monthly trend analysis
df_clean["Year_Month"] = df_clean["InvoiceDate"].dt.to_period("M").astype(str)

print("\nNew columns:")
print(df_clean.columns.tolist())

print("\nMissing values after processing:")
print(df_clean.isnull().sum())
# ==============================
# SAVE PROCESSED DATA
# ==============================

output_file = r"C:\Users\HP\Desktop\VirtuBox Data Analyst Assesment\Python\processed_retail_data.csv"

df_clean.to_csv(output_file, index=False)

print("\nProcessed dataset saved successfully!")
print(output_file)
# ==============================
# Q4 - OVERALL BUSINESS KPIs
# ==============================

print("\n==============================")
print("OVERALL BUSINESS KPIs")
print("==============================")

# Normal sales transactions only
sales_df = df_clean[
    (df_clean["IsCancelled"] == False) &
    (df_clean["IsReturn"] == False)
].copy()

total_revenue = sales_df["Revenue"].sum()
total_quantity = sales_df["Quantity"].sum()
unique_invoices = sales_df["Invoice"].nunique()
unique_products = sales_df["StockCode"].nunique()
unique_customers = sales_df[
    sales_df["Customer ID"] != "Unknown"
]["Customer ID"].nunique()

print("Total Revenue:", round(total_revenue, 2))
print("Total Quantity Sold:", total_quantity)
print("Total Invoices:", unique_invoices)
print("Unique Products:", unique_products)
print("Unique Customers:", unique_customers)
# ==============================
# Q4 - INSIGHT 1: MONTHLY REVENUE
# ==============================

monthly_revenue = (
    sales_df.groupby("Year_Month")["Revenue"]
    .sum()
    .reset_index()
)

print("\n==============================")
print("MONTHLY REVENUE")
print("==============================")

print(monthly_revenue.to_string(index=False))

print("\nHighest revenue month:")
print(monthly_revenue.loc[
    monthly_revenue["Revenue"].idxmax()
])

print("\nLowest revenue month:")
print(monthly_revenue.loc[
    monthly_revenue["Revenue"].idxmin()
])
# ==============================
# Q4 - INSIGHT 2: TOP PRODUCTS
# ==============================

top_products = (
    sales_df.groupby("Description")
    .agg(
        Revenue=("Revenue", "sum"),
        Quantity=("Quantity", "sum")
    )
    .sort_values("Revenue", ascending=False)
    .head(10)
    .reset_index()
)

print("\n==============================")
print("TOP 10 PRODUCTS BY REVENUE")
print("==============================")

print(top_products.to_string(index=False))
# ==============================
# Q4 - INSIGHT 3: COUNTRY PERFORMANCE
# ==============================

country_sales = (
    sales_df.groupby("Country")
    .agg(
        Revenue=("Revenue", "sum"),
        Quantity=("Quantity", "sum"),
        Invoices=("Invoice", "nunique")
    )
    .sort_values("Revenue", ascending=False)
    .head(10)
    .reset_index()
)

print("\n==============================")
print("TOP 10 COUNTRIES BY REVENUE")
print("==============================")

print(country_sales.to_string(index=False))
# ==============================
# Q4 - INSIGHT 4: CUSTOMER PERFORMANCE
# ==============================

customer_sales = (
    sales_df[sales_df["Customer ID"] != "Unknown"]
    .groupby("Customer ID")
    .agg(
        Revenue=("Revenue", "sum"),
        Quantity=("Quantity", "sum"),
        Invoices=("Invoice", "nunique")
    )
    .sort_values("Revenue", ascending=False)
    .head(10)
    .reset_index()
)

print("\n==============================")
print("TOP 10 CUSTOMERS BY REVENUE")
print("==============================")

print(customer_sales.to_string(index=False))
# ==============================
# Q4 - INSIGHT 5: RETURNS AND CANCELLATIONS
# ==============================

cancelled_count = df_clean["IsCancelled"].sum()
return_count = df_clean["IsReturn"].sum()

cancelled_revenue = df_clean.loc[
    df_clean["IsCancelled"] == True, "Revenue"
].sum()

return_revenue = df_clean.loc[
    df_clean["IsReturn"] == True, "Revenue"
].sum()

print("\n==============================")
print("RETURNS AND CANCELLATIONS")
print("==============================")

print("Cancelled transactions:", cancelled_count)
print("Return transactions:", return_count)
print("Cancelled transaction revenue:", round(cancelled_revenue, 2))
print("Return transaction revenue:", round(return_revenue, 2))
# ==============================
# Q5 - SURPRISING RESULT
# ==============================

total_revenue = sales_df["Revenue"].sum()

uk_revenue = sales_df.loc[
    sales_df["Country"] == "United Kingdom", "Revenue"
].sum()

uk_share = (uk_revenue / total_revenue) * 100

print("\n==============================")
print("Q5 - UK REVENUE SHARE")
print("==============================")

print("Total Revenue:", round(total_revenue, 2))
print("UK Revenue:", round(uk_revenue, 2))
print("UK Revenue Share:", round(uk_share, 2), "%")
# ==============================
# CREATE GOOGLE SHEETS VERSION
# ==============================

processed_for_sheets = df_clean[
    [
        "Invoice",
        "StockCode",
        "Description",
        "Quantity",
        "InvoiceDate",
        "Price",
        "Customer ID",
        "Country",
        "Revenue"
    ]
].copy()

processed_for_sheets.to_csv(
    "processed_retail_data_google_sheets.csv",
    index=False
)

print("\nGoogle Sheets file created successfully.")
print("Rows:", len(processed_for_sheets))
print("Columns:", len(processed_for_sheets.columns))
# ==============================
# DASHBOARD SUMMARY DATA
# ==============================

# 1. Monthly Revenue
monthly_revenue = (
    sales_df.groupby("Year_Month")
    .agg(Revenue=("Revenue", "sum"))
    .reset_index()
)

# 2. Country Revenue
country_revenue = (
    sales_df.groupby("Country")
    .agg(Revenue=("Revenue", "sum"))
    .sort_values("Revenue", ascending=False)
    .reset_index()
)

# 3. Top Products
product_revenue = (
    sales_df.groupby("Description")
    .agg(
        Revenue=("Revenue", "sum"),
        Quantity=("Quantity", "sum")
    )
    .sort_values("Revenue", ascending=False)
    .head(20)
    .reset_index()
)

# 4. Top Customers
customer_revenue = (
    sales_df[sales_df["Customer ID"] != "Unknown"]
    .groupby("Customer ID")
    .agg(
        Revenue=("Revenue", "sum"),
        Quantity=("Quantity", "sum"),
        Invoices=("Invoice", "nunique")
    )
    .sort_values("Revenue", ascending=False)
    .head(20)
    .reset_index()
)

# 5. Returns and Cancellations
status_summary = pd.DataFrame({
    "Category": [
        "Normal Sales",
        "Cancelled Transactions",
        "Return Transactions"
    ],
    "Count": [
        len(sales_df),
        int(df_clean["IsCancelled"].sum()),
        int(df_clean["IsReturn"].sum())
    ]
})

# Save files
monthly_revenue.to_csv("monthly_revenue.csv", index=False)
country_revenue.to_csv("country_revenue.csv", index=False)
product_revenue.to_csv("top_products.csv", index=False)
customer_revenue.to_csv("top_customers.csv", index=False)
status_summary.to_csv("transaction_status.csv", index=False)

print("\n==============================")
print("DASHBOARD FILES CREATED")
print("==============================")
print("monthly_revenue.csv")
print("country_revenue.csv")
print("top_products.csv")
print("top_customers.csv")
print("transaction_status.csv")
