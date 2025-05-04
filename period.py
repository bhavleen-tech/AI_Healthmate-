#WORKING
from flask import Flask, render_template_string, request, jsonify
from datetime import datetime

app = Flask(__name__)

# In-memory storage of marked period dates
marked_dates = set()

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Women's Health Tracker</title>
  <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
  <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
  <style>
    .marked {
      background-color: #ec4899;
      color: white;
      font-weight: bold;
    }
    button {
      transition: background-color 0.2s ease;
    }
  </style>
</head>
<body class="bg-pink-50 text-gray-800 font-sans">
  <div class="max-w-4xl mx-auto px-6 py-10">
    <h1 class="text-5xl font-bold text-center text-pink-700 mb-12">🩺 Women's Health Tracker</h1>

    <!-- Period Calendar -->
    <section class="mb-12">
      <h2 class="text-3xl font-semibold text-pink-600 mb-6">📅 Period Calendar</h2>
      <div class="bg-white shadow-md rounded-lg p-6">
        <div class="flex items-center justify-between mb-4">
          <button onclick="prevMonth()" class="bg-pink-500 text-white px-4 py-2 rounded hover:bg-pink-600">&larr;</button>
          <h2 id="monthYear" class="text-xl font-semibold text-pink-600"></h2>
          <button onclick="nextMonth()" class="bg-pink-500 text-white px-4 py-2 rounded hover:bg-pink-600">&rarr;</button>
        </div>
        <div class="grid grid-cols-7 gap-2 text-center font-semibold text-gray-700 mb-2">
          <div>Sun</div><div>Mon</div><div>Tue</div><div>Wed</div><div>Thu</div><div>Fri</div><div>Sat</div>
        </div>
        <div id="calendar" class="grid grid-cols-7 gap-2 mb-4"></div>
        <button onclick="showMarkedDates()" class="mt-4 bg-pink-600 text-white px-4 py-2 rounded hover:bg-pink-700">Show My Marked Dates</button>
        <div id="markedList" class="mt-4 text-sm text-gray-700"></div>
      </div>
    </section>

    <!-- Diet During Periods -->
    <section class="mb-10">
      <h2 class="text-2xl font-semibold text-pink-600 mb-4">🥗 Diet During Periods</h2>
      <ul class="list-disc list-inside space-y-2 pl-4">
        <li><strong>Hydration:</strong> Drink warm water and herbal teas (like chamomile) to reduce bloating and cramps.</li>
        <li><strong>Iron-rich foods:</strong> Eat spinach, lentils, tofu, and beets to replenish iron lost during menstruation.</li>
        <li><strong>Magnesium sources:</strong> Dark chocolate, bananas, and avocados help reduce mood swings and cramps.</li>
        <li><strong>Vitamin B6:</strong> Include oats, eggs, and salmon to ease irritability and fatigue.</li>
        <li><strong>Avoid:</strong> Processed foods, caffeine, and excess salt to reduce water retention and discomfort.</li>
      </ul>
    </section>

    <!-- PMS Awareness -->
    <section class="mb-10">
      <h2 class="text-2xl font-semibold text-pink-600 mb-4">🌙 Premenstrual Syndrome (PMS)</h2>
      <p class="mb-2">PMS occurs before menstruation and includes symptoms like mood swings, bloating, fatigue, and irritability.</p>
      <p class="mb-2">Tips to ease PMS:</p>
      <ul class="list-disc list-inside space-y-2 pl-4">
        <li>Exercise regularly to improve mood and reduce bloating</li>
        <li>Follow a healthy diet rich in complex carbs and magnesium</li>
        <li>Sleep at least 7–8 hours to reduce fatigue and irritability</li>
        <li>Practice relaxation techniques like deep breathing or meditation</li>
      </ul>
    </section>

    <!-- PCOD & PCOS Info -->
    <section class="mb-10">
      <h2 class="text-2xl font-semibold text-pink-600 mb-4">🧬 PCOD & PCOS Awareness</h2>
      <p class="mb-2">PCOD and PCOS are common hormonal disorders affecting women. Symptoms include irregular periods, weight gain, acne, and hair growth.</p>
      <p class="mb-2">Management tips:</p>
      <ul class="list-disc list-inside space-y-2 pl-4">
        <li>Maintain a balanced diet (low GI, anti-inflammatory)</li>
        <li>Exercise for at least 30 minutes daily</li>
        <li>Manage stress through mindfulness or yoga</li>
        <li>Consult with a healthcare provider for regular checkups</li>
      </ul>
    </section>

    <!-- Exercises -->
    <section class="mb-10">
      <h2 class="text-2xl font-semibold text-pink-600 mb-4">🏃‍♀️ Exercises During Periods</h2>
      <ul class="list-disc list-inside space-y-2 pl-4">
        <li>Light yoga poses: Child’s Pose, Cat-Cow, Reclined Twist</li>
        <li>Gentle walking or stretching to boost circulation</li>
        <li>Breathing techniques for relaxation and stress relief</li>
      </ul>
    </section>

    <!-- Additional Tips -->
    <section>
      <h2 class="text-2xl font-semibold text-pink-600 mb-4">💡 Additional Tips</h2>
      <ul class="list-disc list-inside space-y-2 pl-4">
        <li>Use a hot water bag or heating pad to relieve cramps</li>
        <li>Keep a cycle journal or use the calendar above</li>
        <li>Maintain proper hygiene</li>
        <li>Seek professional help if experiencing unusual symptoms</li>
      </ul>
    </section>
  </div>

  <script>
    let today = new Date();
    let currentYear = today.getFullYear();
    let currentMonth = today.getMonth();
    let marked = new Set({{ marked_dates|tojson }});

    function renderCalendar() {
      const calendar = document.getElementById('calendar');
      const monthYear = document.getElementById('monthYear');
      calendar.innerHTML = '';

      const firstDay = new Date(currentYear, currentMonth, 1).getDay();
      const lastDate = new Date(currentYear, currentMonth + 1, 0).getDate();

      monthYear.textContent = new Date(currentYear, currentMonth).toLocaleString('default', { month: 'long', year: 'numeric' });

      for (let i = 0; i < firstDay; i++) {
        const blank = document.createElement('div');
        calendar.appendChild(blank);
      }

      for (let d = 1; d <= lastDate; d++) {
        const dateStr = `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
        const btn = document.createElement('button');
        btn.textContent = d;
        btn.className = `p-2 border rounded ${marked.has(dateStr) ? 'marked' : 'hover:bg-pink-200'}`;
        btn.onclick = () => toggleDate(dateStr);
        calendar.appendChild(btn);
      }
    }

    function toggleDate(date) {
      axios.post('/mark-date', { date }).then(res => {
        marked = new Set(res.data.marked);
        renderCalendar();
      });
    }

    function prevMonth() {
      currentMonth--;
      if (currentMonth < 0) {
        currentMonth = 11;
        currentYear--;
      }
      renderCalendar();
    }

    function nextMonth() {
      currentMonth++;
      if (currentMonth > 11) {
        currentMonth = 0;
        currentYear++;
      }
      renderCalendar();
    }

    function showMarkedDates() {
      const listDiv = document.getElementById('markedList');
      if (marked.size === 0) {
        listDiv.textContent = 'No dates marked yet.';
        return;
      }
      const sorted = Array.from(marked).sort();
      const avgGap = calculateAverageGap(sorted);
      listDiv.innerHTML = '<strong>Marked Period Dates:</strong><ul class="list-disc list-inside">' +
        sorted.map(date => `<li>${date}</li>`).join('') + '</ul>' +
        `<p class='mt-2 text-sm text-pink-700'>Average days between periods: <strong>${avgGap}</strong></p>`;
    }

    function calculateAverageGap(dates) {
      if (dates.length < 2) return 'N/A';
      const gaps = [];
      for (let i = 1; i < dates.length; i++) {
        const prev = new Date(dates[i - 1]);
        const curr = new Date(dates[i]);
        gaps.push((curr - prev) / (1000 * 60 * 60 * 24));
      }
      const avg = gaps.reduce((a, b) => a + b, 0) / gaps.length;
      return Math.round(avg);
    }

    renderCalendar();
  </script>
</body>
</html>
"""


@app.route('/')
def index():
    return render_template_string(HTML_PAGE, marked_dates=list(marked_dates))

@app.route('/mark-date', methods=['POST'])
def mark_date():
    date = request.json.get('date')
    if date in marked_dates:
        marked_dates.remove(date)
    else:
        marked_dates.add(date)
    return jsonify(success=True, marked=list(marked_dates))

if __name__ == '__main__':
    app.run(host='127.0.0.4', port=5000, debug=True)