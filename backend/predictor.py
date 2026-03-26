def predict_disease(bpm):

    bpm = int(bpm)

    if bpm < 60:
        return {
            "condition": "Bradycardia Risk",
            "severity": "Medium"
        }

    elif 60 <= bpm <= 100:
        return {
            "condition": "Normal Heart Rate",
            "severity": "Low"
        }

    else:
        return {
            "condition": "Tachycardia Risk",
            "severity": "High"
        }