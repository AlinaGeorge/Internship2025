import pandas as pd
import matplotlib.pyplot as plt

class Sales:
    def __init__(self, fileName):
        self.fileName = fileName
        self.data = pd.read_csv(fileName)
        print("Data read successfully")

    def show_head(self):
        print("\nHead:")
        print(self.data.head())

    def describe_data(self):
        print("\nDescription:")
        print(self.data.describe(include='all'))

    def total_revenue(self):
        totrevenue = self.data['TotalPrice'].sum()
        print(f"\nTotal Revenue: ${totrevenue:.2f}")

    def revenue_by_category(self):
        revenue = self.data.groupby('Category')['TotalPrice'].sum()
        print("\nRevenue by Category:")
        print(revenue)
        return revenue  # Return for plotting use

    def orders_by_region(self):
        ordersRegion = self.data['Region'].value_counts()
        print("\nOrders by Region:")
        print(ordersRegion)

    def average_unit_price(self):
        avg = self.data.groupby('Product')['UnitPrice'].mean()
        print("\nAverage Unit Price by Product:")
        print(avg)

    def electronics_sales(self):
        electronics = self.data[self.data['Category'] == 'Electronics']
        print("\nElectronics Sales:")
        print(electronics)

    def add_discount_column(self, discount=0.10):
        self.data['DiscountedPrice'] = self.data['TotalPrice'] * (1 - discount)
        print("\nDiscounted Price Column Added:")
        print(self.data[['OrderID', 'TotalPrice', 'DiscountedPrice']])

    def sort_by_total_price(self):
        sorted_df = self.data.sort_values(by='TotalPrice', ascending=False)
        print("\nSorted by TotalPrice:")
        print(sorted_df[['OrderID', 'TotalPrice']])

    def plot_revenue_by_category(self):
        revenue = self.revenue_by_category()  # Reuse method
        revenue.plot(kind='bar', title='Revenue by Category')
        plt.figure(figsize=(5,5)) 
        plt.ylabel('Revenue')
        plt.xlabel('Category')
        plt.show()

# === Main driver code ===
if __name__ == "__main__":
    path = input("Enter the path to your Sales CSV file: ")
    analyzer = Sales(path)
    analyzer.show_head()
    analyzer.describe_data()
    analyzer.total_revenue()
    analyzer.revenue_by_category()
    analyzer.orders_by_region()
    analyzer.average_unit_price()
    analyzer.electronics_sales()
    analyzer.add_discount_column()
    analyzer.sort_by_total_price()
    analyzer.plot_revenue_by_category()  # 📊 Plot called here
