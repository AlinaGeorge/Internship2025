import pandas as pd

# Load the CSV file
df = pd.read_csv('Sales.csv')

# Show first 5 rows
print("🔹 Head:")
print(df.head())

# Summary statistics
print("\n🔹 Description:")
print(df.describe(include='all'))

# Total revenue
totrevenue = df['TotalPrice'].sum()
print(f"\n Total Revenue: ${totrevenue}")

# Revenue by Category
revenue= df.groupby('Category')['TotalPrice'].sum()
print("\n Revenue by Category:")
print(revenue)

# Number of orders per region
ordersRegion = df['Region'].value_counts()
print("\n Orders by Region:")
print(ordersRegion)

# Average Unit Price by Product
avg = df.groupby('Product')['UnitPrice'].mean()
print("\n Average Price by Product:")
print(avg)

# Filter: Show only Electronics sales
electronics_sales = df[df['Category'] == 'Electronics']
print("\n Electronics Sales:")
print(electronics_sales)

# Add a new column: Discounted Total (10% discount on TotalPrice)
df['DiscountedPrice'] = df['TotalPrice'] * 0.9
print("\n Added DiscountedPrice Column:")
print(df[['OrderID', 'TotalPrice', 'DiscountedPrice']])

# Sort data by TotalPrice
sorted_df = df.sort_values(by='TotalPrice', ascending=False)
print("\n Sorted by TotalPrice:")
print(sorted_df[['OrderID', 'TotalPrice']])

