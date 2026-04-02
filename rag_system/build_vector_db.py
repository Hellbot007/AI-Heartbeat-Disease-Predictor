knowledge = [
"High heart rate can indicate stress",
"Low SpO2 may indicate oxygen deficiency",
"Normal heart rate ranges between 60 and 100 bpm"
]

with open("rag_system/vector_db.txt","w") as f:
    for line in knowledge:
        f.write(line+"\n")

print("Knowledge base created")