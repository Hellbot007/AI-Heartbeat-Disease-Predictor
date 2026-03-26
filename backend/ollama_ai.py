import ollama

def generate_explanation(bpm, condition):

    prompt = f"""
    A user has a heart rate of {bpm} BPM.

    Predicted condition: {condition}

    Explain what this means for the person's health in simple terms
    and suggest basic precautions.
    """

    response = ollama.chat(
        model='llama3',
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response['message']['content']