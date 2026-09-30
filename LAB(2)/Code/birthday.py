birthdays = {
        "honeypot": "Jan 15",
        "Shoaib": "May 22",
        "Umer": "Sep 30",
        "Fezan": "Dec 10"
    }
name = input("Enter a name: ")
if name in birthdays:
    print(name + "'s birthday is", birthdays[name])
else:
    print("No entry found for", name)
