import ollama

import ollama

def generate_explanation(bpm, condition):
    
    prompt = f"""
    A patient has a heart rate of {bpm} BPM.
    The predicted condition is {condition}.
    Explain the possible health risk in 2 simple sentences.
    """

    response = ollama.chat(
        model='phi3',
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response['message']['content']