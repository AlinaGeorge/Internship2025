import pandas as pd
import matplotlib.pyplot as plt

# Sample data
data = {
    'Items': ['Apples', 'Bananas', 'Cherries', 'Dates'],
    'Quantity': [10, 15, 7, 12]
}

df = pd.DataFrame(data)     #creating dataframe

# Plot a bar chart
plt.figure(figsize=(5,3))                    # Setting the figure size
plt.bar(df['Items'], df['Quantity'])  # Plotting

# Adding title and labels
plt.title('Fruit Inventory')
plt.xlabel('Fruit')
plt.ylabel('Quantity')

# Displaying the plot
plt.show()
