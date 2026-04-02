from retrieve_context import retrieve

query = "high heart rate"

context = retrieve(query)

print("Analysis:")
print(context)