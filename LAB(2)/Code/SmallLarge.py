list1 = [int(x) for x in input("Enter first list of numbers: ").replace(",", " ").split()]
list2 = [int(x) for x in input("Enter second list of numbers: ").replace(",", " ").split()]
merged = sorted(list1 + list2)
print("Merged list:", merged)
print("Smallest element:", min(merged))
print("Largest element:", max(merged))
