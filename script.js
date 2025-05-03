function searchDoctor() {
  const location = document.getElementById("location").value;
  const specialty = document.getElementById("specialty").value;

  fetch("http://localhost:5000/api/doctors", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ location, specialty }),
  })
    .then((res) => res.json())
    .then((data) => displayDoctors(data))
    .catch((err) => console.error("Error:", err));
}

function displayDoctors(doctors) {
  const results = document.getElementById("results");
  results.innerHTML = "";

  if (doctors.length === 0) {
    results.innerHTML = "<p>No doctors found.</p>";
    return;
  }

  doctors.forEach((doc) => {
    const card = document.createElement("div");
    card.className = "doctor-card";
    card.innerHTML = `
      <h3>${doc.name}</h3>
      <p><strong>Clinic:</strong> ${doc.clinic}</p>
      <p><strong>Experience:</strong> ${doc.experience}</p>
      <p><strong>Location:</strong> ${doc.location}</p>
      <p><strong>Specialty:</strong> ${doc.specialty}</p>
      <p><a href="${doc.maps_link}" target="_blank">📍 View on Google Maps</a></p>
      <button class="book-btn">Book Now & Get 20% OFF</button>
    `;
    results.appendChild(card);
  });
}
