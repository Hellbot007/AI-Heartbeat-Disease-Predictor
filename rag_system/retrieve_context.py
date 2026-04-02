def retrieve(query):

    with open("rag_system/vector_db.txt","r") as f:
        data = f.readlines()

    for line in data:
        if "heart rate" in query.lower():
            return line

    return "No context found"