from flask import Flask, request, jsonify

app = Flask(__name__)


knowledge_base = {
 
    "cold": "Drink warm fluids, rest well, and try honey with ginger tea.",
    "cough": "Gargle with warm salt water, drink herbal teas, and try honey with turmeric.",
    "fever": "Stay hydrated, rest, and use a cool compress to lower temperature.",
    "headache": "Drink plenty of water, rest in a dark room, and try peppermint oil on your temples.",
    "sore throat": "Gargle with warm salt water, drink chamomile tea, and suck on lozenges.",
    "indigestion": "Drink ginger tea, chew fennel seeds, and avoid heavy meals.",
    "acidity": "Drink cold milk, eat bananas, and avoid spicy food.",
    "constipation": "Increase fiber intake, drink warm lemon water, and stay active.",
    "diarrhea": "Stay hydrated with ORS, eat bananas and rice, and avoid dairy products.",
    "skin rashes": "Apply aloe vera gel, use coconut oil, and avoid irritants.",
    "stress": "Practice deep breathing, meditate, and engage in physical activities.",
    "insomnia": "Try chamomile tea, meditate before bed, and keep a regular sleep schedule.",
    "muscle pain": "Apply warm compress, do gentle stretching, and use turmeric milk.",
    "toothache": "Apply clove oil to the affected area and rinse with salt water.",
    "eye strain": "Rest your eyes frequently, use the 20-20-20 rule, and apply cold compress.",
    "back pain": "Use a heating pad, practice yoga, and maintain proper posture.",
    "nausea": "Drink ginger tea, suck on peppermint candy, and stay hydrated.",
    "burns": "Apply cool water, use aloe vera gel, and avoid breaking blisters.",
    "anemia": "Eat iron-rich foods like spinach, lentils, and pomegranate juice.",
    "allergies": "Avoid triggers, take honey regularly, and use a saline nasal rinse.",
    "hair fall": "Massage scalp with coconut oil, eat protein-rich foods, and use onion juice.",
    "dandruff": "Apply lemon juice, use aloe vera, and massage with coconut oil.",
    "high blood pressure": "Reduce salt intake, exercise regularly, and eat potassium-rich foods.",
    "low blood pressure": "Increase fluid intake, eat small frequent meals, and consume more salt.",
    "joint pain": "Apply turmeric paste, use warm compress, and consume omega-3-rich foods.",
    "acne": "Apply tea tree oil, use aloe vera, and wash your face with mild cleanser.",
    "dark spots": "Apply lemon juice, use vitamin C serum, and exfoliate regularly.",
    "dry skin": "Moisturize with coconut oil, drink plenty of water, and avoid hot showers.",
    "oily skin": "Use a clay mask, wash face with mild cleanser, and avoid fried foods.",
    "wrinkles": "Apply aloe vera gel, use anti-aging serums with retinol, and stay hydrated.",
    "eczema": "Use coconut oil, take oatmeal baths, and avoid harsh soaps.",
    "psoriasis": "Apply aloe vera, use oatmeal baths, and keep skin hydrated.",
    "sunburn": "Apply aloe vera gel, use a cold compress, and stay hydrated.",
    "skin tanning": "Apply yogurt and turmeric, use aloe vera, and exfoliate regularly.",
    "itchy skin": "Use calamine lotion, take an oatmeal bath, and avoid harsh soaps.",
    "pigmentation": "Apply turmeric and yogurt mask, use vitamin C serums, and avoid sun exposure.",
    "split ends": "Apply coconut oil, and use leave-in conditioners.",
    "frizzy hair": "Apply argan oil, use a silk pillowcase, and avoid excessive heat styling.",
    "dry hair": "Use coconut oil, deep condition weekly, and avoid frequent shampooing.",
    "oily scalp": "Use a mild shampoo, apply apple cider vinegar rinse, and avoid heavy oils.",
    "grey hair": "Apply amla oil, eat vitamin B12-rich foods, and use henna as a natural dye.",
    "dull hair": "Use aloe vera gel, rinse with rice water, and consume omega-3 fatty acids.",
    "hair thinning": "Massage scalp with castor oil, eat protein-rich foods, and avoid chemical treatments.",
    "scalp infections": "Apply neem oil, wash hair with antifungal shampoo, and keep scalp clean."
}


def get_answer(query):
    query = query.lower().strip()
    return knowledge_base.get(query, "Sorry, I don't have an answer for that.")

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Home Remedies</title>
        <style>
            body { 
                font-family: 'Arial', sans-serif; 
                text-align: center; 
                background: linear-gradient(135deg, #d3f8e2, #e4c1f9);
                margin: 0;
                padding: 0;
            }
            header { 
                background: #0077b6; 
                color: white; 
                padding: 30px; 
                font-size: 40px; 
                font-weight: bold;
                letter-spacing: 2px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
                text-align: center;
                border-bottom: 5px solid #023e8a;
            }
            #chat-container {
                width: 50%;
                margin: 100px auto;
                padding: 40px;
                background: white;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
                position: relative;
                animation: fadeIn 1s ease-in-out;
            }
            input {
                width: 80%;
                padding: 15px;
                font-size: 18px;
                border: 2px solid #0077b6;
                border-radius: 10px;
                margin-top: 20px;
                outline: none;
                transition: all 0.3s ease-in-out;
            }
            input:focus {
                border-color: #023e8a;
                transform: scale(1.05);
            }
            button {
                padding: 15px 30px;
                margin-top: 20px;
                background: #0077b6;
                color: white;
                font-size: 18px;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                transition: all 0.3s ease-in-out;
                box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
            }
            button:hover {
                background: #023e8a;
                transform: scale(1.1);
            }
            #bot-response {
                margin-top: 20px;
                font-size: 20px;
                font-weight: bold;
                color: #023e8a;
                animation: fadeIn 0.5s ease-in-out;
            }
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            footer {
                margin-top: 50px;
                padding: 20px;
                background: #0077b6;
                color: white;
                text-align: center;
                font-size: 16px;
                border-top: 3px solid #023e8a;
            }
        </style>
    </head>
    <body>
        <header>
            Home Remedies & Medical Advice
        </header>
        <div id="chat-container">
            <p>Welcome to the world of Home Remedies and Medical Assistance.</p>
            <input type="text" id="user-input" placeholder="Enter Disease Name (Example: cold)">
            <button onclick="sendMessage()">Send</button>
            <p id="bot-response"></p>
        </div>
        <footer>
            &copy; 2025 HealthBot | Your Personal Health Assistant
        </footer>
        <script>
            function sendMessage() {
                let userInput = document.getElementById("user-input").value;
                fetch("/get_response", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message: userInput })
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById("bot-response").innerText = data.response;
                });
            }
        </script>
    </body>
    </html>
    '''

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json.get("message")
    bot_reply = get_answer(user_message)
    return jsonify(response=bot_reply)

if __name__ == '__main__':
    app.run(host='127.0.0.2', port=5000, debug=True)
