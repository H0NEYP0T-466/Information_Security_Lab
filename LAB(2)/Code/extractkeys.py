sample_dict = {
        "name": "Fezan",
        "age": 20,
        "roll_no": "Fall-23-BSCS-466",
        "city": "Lahore",
        "department": "Computer Science"
    }
keys = ["name", "roll_no", "department"]
new_dict = {k: sample_dict[k] for k in keys if k in sample_dict}
print("Original dictionary:", sample_dict)
print("Extracted dictionary:", new_dict)
