# VirtuBox Data Analyst Assessment

## Project Overview

This project was completed as part of the Data Analyst assessment for VirtuBox Infotech Private Limited.

The analysis uses the UCI Online Retail II dataset to understand sales performance, customer value, product performance, geographical markets and transaction patterns.

## Dataset

Dataset: UCI Online Retail II

Source: UCI Machine Learning Repository

The dataset contains two years of online retail transaction data from a UK-based online retailer.

Raw dataset: 1,067,371 transaction records and 8 columns.

## Business Problem

The objective is to understand the sales and customer performance of the online retail business and identify opportunities to improve revenue, customer value and market performance.

## Analysis Performed

The analysis included:

- Data cleaning and preprocessing
- Missing-value handling
- Duplicate removal
- Cancellation and return identification
- Revenue calculation
- Time-based analysis
- Country-level analysis
- Product-level analysis
- Customer-level analysis
- Transaction-status analysis
- Business recommendations

## Key Findings

- November 2011 was the strongest month by revenue at approximately £1.50M.
- February 2011 was the weakest month at approximately £0.52M.
- The United Kingdom contributed approximately 85% of revenue.
- Manual was the highest-revenue product at approximately £339K.
- Customer 18102 was the highest-value customer at approximately £581K.
- Cancelled and return transactions represented significant negative transaction value and should be monitored separately.

## Tools Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Google Sheets
- Looker Studio
- GitHub
- ChatGPT for occasional guidance and structuring support

## Repository Files

- `analysis.py` – Python data processing and analysis script
- `monthly_revenue.csv` – monthly revenue summary
- `country_revenue.csv` – country revenue summary
- `top_products.csv` – top product analysis
- `top_customers.csv` – top customer analysis
- `transaction_status.csv` – transaction-status summary

## Dashboard

Looker Studio dashboard:

https://datastudio.google.com/u/0/reporting/5e867d4f-0ba9-4ad4-9807-375b7e31ac27/page/kTh8F

## Google sheet

Assessment Google Sheet:

https://docs.google.com/spreadsheets/d/1MKXQZKOsUXKsoH00o7k9UDQOtX19kvdUZ7_4h93-oEM/edit?gid=1925713468#gid=1925713468

## Complete Assessment Files

Google Drive folder containing the complete assessment deliverables:

https://drive.google.com/drive/u/0/folders/1EmF4hSg19vXFSj0WGx0a4ozYxwfjqaPB


## Presentation

The management presentation is included in the final assessment submission folder.

## Limitations

- The dataset does not contain product cost or profit information.
- The analysis is observational and does not establish causal relationships.
- Missing customer IDs limit customer-specific analysis for some transactions.
