import re

def analyze_report(text):
    patterns = {
        'Hemoglobin': r'Hemoglobin[\s:]*([\d.]+)',
        'WBC': r'WBC[\s:]*([\d.]+)',
        'Platelets': r'Platelets[\s:]*([\d,]+)',
        'RBC': r'RBC[\s:]*([\d.]+)',
        'Glucose': r'Glucose[\s:]*([\d.]+)',
        'SGPT': r'SGPT[\s:]*([\d.]+)',
        'Bilirubin': r'Bilirubin[\s:]*([\d.]+)'
    }

    normal_ranges = {
        'Hemoglobin': (13.0, 17.0),
        'WBC': (4000, 11000),
        'Platelets': (150000, 450000),
        'RBC': (4.5, 6.0),
        'Glucose': (70, 140),
        'SGPT': (7, 56),
        'Bilirubin': (0.1, 1.2)
    }

    comments = {
        'Hemoglobin': "Maintain a balanced diet to support red blood cell production.",
        'WBC': "Good immunity. Stay hydrated and maintain hygiene.",
        'Platelets': "Your platelet count is healthy. Keep monitoring during illnesses.",
        'RBC': "Your RBC count is fine. Regular exercise helps improve blood health.",
        'Glucose': "Maintain a balanced diet, avoid excess sugar.",
        'SGPT': "Your liver function is within limits. Avoid alcohol and fatty foods.",
        'Bilirubin': "Normal liver function. Stay hydrated and eat liver-friendly foods."
    }

    results = []
    for metric, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                value = float(match.group(1).replace(',', ''))
                low, high = normal_ranges[metric]
                status = "Normal" if low <= value <= high else "Abnormal"
                suggestion = comments[metric] if status == "Normal" else f"{metric} is out of normal range. Please consult a doctor."
                results.append(f"{metric}: {value} ({status})\n→ Suggestion: {suggestion}\n")
            except:
                results.append(f"{metric}: Value could not be parsed.\n")
        else:
            results.append(f"{metric}: Not Found in the report.\n")

    return "\n".join(results)
