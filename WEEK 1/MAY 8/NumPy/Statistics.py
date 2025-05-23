import numpy as np

# Sample dataset
data = np.array([10, 20, 30, 40, 50, 60, 70])

# Basic statistics
mean = np.mean(data)
median = np.median(data)
std_dev = np.std(data)

# Display the results
print("Dataset:", data)
print("Mean:", mean)
print("Median:", median)
print("Standard Deviation:", std_dev)

# Additional functions 
print("Minimum:", np.min(data)) 
print("Maximum:", np.max(data)) 
print("Range:", np.ptp(data))   #ptp takes the difference between peaks
print("Sorted:", np.sort(data))
print("Sum:", np.sum(data))
print("Size of dataset:", data.size)
