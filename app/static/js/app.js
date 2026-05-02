/**
 * Frontend Application Logic for Fitness Assistant
 * Handles UI interactions, API calls, and navigation
 */

let currentUserId = null;

/**
 * Navigate between pages
 */
function navigateTo(pageId) {
  // Hide all pages
  const pages = document.querySelectorAll(".page");
  pages.forEach((page) => page.classList.remove("active"));

  // Show selected page
  const selectedPage = document.getElementById(pageId);
  if (selectedPage) {
    selectedPage.classList.add("active");

    // Load dashboard data if navigating to dashboard
    if (pageId === "dashboard" && currentUserId) {
      loadDashboard();
    }
  }
}

/**
 * Switch between authentication tabs
 */
function switchAuthTab(tabName) {
  // Hide all auth forms
  document.querySelectorAll(".auth-form").forEach((form) => {
    form.classList.remove("active");
  });
  document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.classList.remove("active");
  });

  // Show selected form
  const formId = `${tabName}-tab`;
  const btnSelector = event.target;
  document.getElementById(formId).classList.add("active");
  btnSelector.classList.add("active");
}

/**
 * Switch between dashboard tabs
 */
function switchDashboardTab(tabName) {
  // Hide all tab contents
  document.querySelectorAll(".tab-content").forEach((tab) => {
    tab.classList.remove("active");
  });

  // Show selected tab
  const tabId = `${tabName}-tab`;
  const tab = document.getElementById(tabId);
  if (tab) {
    tab.classList.add("active");

    // Load specific data based on tab
    if (tabName === "view-plan") {
      loadFitnessPlan();
    } else if (tabName === "track-progress") {
      loadProgressData();
    } else if (tabName === "recommendations") {
      loadRecommendations();
    } else if (tabName === "user-info") {
      loadUserProfile();
    }
  }
}

/**
 * Show message to user
 */
function showMessage(elementId, message, type = "success") {
  const element = document.getElementById(elementId);
  if (element) {
    element.textContent = message;
    element.className = `message show ${type}`;
    setTimeout(() => {
      element.classList.remove("show");
    }, 5000);
  }
}

/**
 * Handle user registration
 */
async function handleRegister(event) {
  event.preventDefault();

  const formData = {
    username: document.getElementById("username").value,
    email: document.getElementById("email").value,
    age: document.getElementById("age").value,
    height: document.getElementById("height").value,
    weight: document.getElementById("weight").value,
    gender: document.getElementById("gender").value,
    fitness_goal: document.getElementById("fitness_goal").value,
    experience_level: document.getElementById("experience_level").value,
    diet_preference: document.getElementById("diet_preference").value,
    daily_budget: document.getElementById("daily_budget").value,
    workout_preference: document.getElementById("workout_preference").value,
  };

  try {
    const response = await fetch("/api/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });

    const data = await response.json();

    if (data.success) {
      currentUserId = data.user_id;
      document.getElementById("logoutBtn").style.display = "block";
      showMessage(
        "register-message",
        "Registration successful! Welcome!",
        "success",
      );
      setTimeout(() => navigateTo("dashboard"), 1500);
    } else {
      showMessage("register-message", data.error, "error");
    }
  } catch (error) {
    showMessage("register-message", "Error: " + error.message, "error");
  }
}

/**
 * Handle user login
 */
async function handleLogin(event) {
  event.preventDefault();

  const username = document.getElementById("login-username").value;

  try {
    const response = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username }),
    });

    const data = await response.json();

    if (data.success) {
      currentUserId = data.user_id;
      document.getElementById("logoutBtn").style.display = "block";
      showMessage("login-message", "Login successful!", "success");
      setTimeout(() => navigateTo("dashboard"), 1500);
    } else {
      showMessage("login-message", data.error, "error");
    }
  } catch (error) {
    showMessage("login-message", "Error: " + error.message, "error");
  }
}

/**
 * Handle logout
 */
async function logout() {
  try {
    await fetch("/api/logout", { method: "POST" });
    currentUserId = null;
    document.getElementById("logoutBtn").style.display = "none";
    navigateTo("home");
  } catch (error) {
    console.error("Logout error:", error);
  }
}

/**
 * Load user profile
 */
async function loadUserProfile() {
  if (!currentUserId) return;

  try {
    const response = await fetch(`/api/user/${currentUserId}`);
    const data = await response.json();

    if (data.success === false) {
      showMessage("", data.error, "error");
      return;
    }

    const profileHtml = `
            <div class="profile-item">
                <div class="profile-label">Age</div>
                <div class="profile-value">${data.age} years</div>
            </div>
            <div class="profile-item">
                <div class="profile-label">Height</div>
                <div class="profile-value">${data.height} cm</div>
            </div>
            <div class="profile-item">
                <div class="profile-label">Weight</div>
                <div class="profile-value">${data.weight} kg</div>
            </div>
            <div class="profile-item">
                <div class="profile-label">Gender</div>
                <div class="profile-value">${data.gender}</div>
            </div>
            <div class="profile-item">
                <div class="profile-label">Fitness Goal</div>
                <div class="profile-value">${data.fitness_goal.replace("_", " ")}</div>
            </div>
            <div class="profile-item">
                <div class="profile-label">Experience</div>
                <div class="profile-value">${data.experience_level}</div>
            </div>
            <div class="profile-item">
                <div class="profile-label">Diet Preference</div>
                <div class="profile-value">${data.diet_preference}</div>
            </div>
            <div class="profile-item">
                <div class="profile-label">Daily Budget</div>
                <div class="profile-value">₹${data.daily_budget}/day</div>
            </div>
        `;

    document.getElementById("user-profile").innerHTML = profileHtml;
  } catch (error) {
    console.error("Error loading profile:", error);
  }
}

/**
 * Handle plan generation
 */
async function handleGeneratePlan(event) {
  event.preventDefault();

  if (!currentUserId) {
    showMessage("generate-plan-message", "Please login first", "error");
    return;
  }

  const activityLevel = parseFloat(
    document.getElementById("activity_level").value,
  );

  try {
    const response = await fetch("/api/generate-plan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ activity_level: activityLevel }),
    });

    const data = await response.json();

    if (data.success) {
      showMessage(
        "generate-plan-message",
        "Plan generated successfully!",
        "success",
      );
      setTimeout(() => {
        switchDashboardTab("view-plan");
      }, 1000);
    } else {
      showMessage("generate-plan-message", data.error, "error");
    }
  } catch (error) {
    showMessage("generate-plan-message", "Error: " + error.message, "error");
  }
}

/**
 * Load and display fitness plan
 */
async function loadFitnessPlan() {
  if (!currentUserId) return;

  try {
    const response = await fetch(`/api/plans/${currentUserId}`);
    const data = await response.json();

    if (!data.success || data.plans.length === 0) {
      document.getElementById("fitness-plan").innerHTML =
        "<p>No plans generated yet. Generate a plan first!</p>";
      return;
    }

    const plan = data.plans[0]; // Show latest plan

    let planHtml = `
            <div class="plan-section">
                <h3>📊 Nutrition Summary</h3>
                <div class="plan-item">
                    <div class="plan-item-title">Daily Calories Target</div>
                    <div class="plan-item-detail">${Math.round(plan.daily_calories)} kcal</div>
                </div>
                <div class="plan-item">
                    <div class="plan-item-title">Daily Protein Target</div>
                    <div class="plan-item-detail">${Math.round(plan.daily_protein)}g</div>
                </div>
            </div>
        `;

    // Workout Plan
    planHtml += '<div class="plan-section"><h3>🏋️ Workout Plan</h3>';
    const workoutPlan = plan.workout_plan;
    for (const [day, exercises] of Object.entries(workoutPlan)) {
      planHtml += `<div class="plan-item"><div class="plan-item-title">${day}</div>`;
      for (const [muscle, details] of Object.entries(exercises)) {
        planHtml += `
                    <div class="plan-item-detail">
                        <strong>${muscle}:</strong> ${details.exercise} - ${details.sets}x${details.reps} (Rest: ${details.rest})
                    </div>
                `;
      }
      planHtml += "</div>";
    }
    planHtml += "</div>";

    // Diet Plan
    planHtml += '<div class="plan-section"><h3>🥗 Diet Plan</h3>';
    const dietPlan = plan.diet_plan;
    const meals = ["breakfast", "lunch", "dinner", "snacks"];
    meals.forEach((meal) => {
      if (dietPlan[meal] && dietPlan[meal].length > 0) {
        planHtml += `<div class="plan-item"><div class="plan-item-title" style="text-transform: capitalize;">${meal}</div>`;
        dietPlan[meal].forEach((item) => {
          planHtml += `<div class="plan-item-detail">${item.item} (${item.quantity}) - ${item.calories} cal, ${item.protein}g protein - ₹${item.cost}</div>`;
        });
        planHtml += "</div>";
      }
    });
    planHtml += `<div class="plan-item">
            <div class="plan-item-title">Daily Totals</div>
            <div class="plan-item-detail">Calories: ${Math.round(dietPlan.total_calories)} | Protein: ${Math.round(dietPlan.total_protein)}g | Cost: ₹${Math.round(dietPlan.total_cost)}</div>
        </div>`;
    planHtml += "</div>";

    document.getElementById("fitness-plan").innerHTML = planHtml;
  } catch (error) {
    console.error("Error loading plan:", error);
  }
}

/**
 * Handle weight logging
 */
async function handleLogWeight(event) {
  event.preventDefault();

  if (!currentUserId) {
    showMessage("progress-message", "Please login first", "error");
    return;
  }

  const weight = parseFloat(document.getElementById("log-weight").value);
  const notes = document.getElementById("log-notes").value;

  try {
    const response = await fetch("/api/log-weight", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ weight, notes }),
    });

    const data = await response.json();

    if (data.success) {
      showMessage("progress-message", "Weight logged successfully!", "success");
      document.getElementById("log-weight").value = "";
      document.getElementById("log-notes").value = "";
      loadProgressData();
    } else {
      showMessage("progress-message", data.error, "error");
    }
  } catch (error) {
    showMessage("progress-message", "Error: " + error.message, "error");
  }
}

/**
 * Load and display progress data
 */
async function loadProgressData() {
  if (!currentUserId) return;

  try {
    const response = await fetch(`/api/progress/${currentUserId}`);
    const data = await response.json();

    if (!data.success || data.progress.length === 0) {
      document.getElementById("progress-chart").innerHTML =
        "<p>No progress logged yet. Start by logging your weight!</p>";
      return;
    }

    const progress = data.progress;
    const dates = progress.map((p) => p.date);
    const weights = progress.map((p) => p.weight);

    // Create simple ASCII chart
    let chartHtml =
      '<h3>Weight Progress</h3><pre style="background: #f5f5f5; padding: 1rem; border-radius: 5px; overflow-x: auto;">';
    chartHtml += `Date: ${dates.join(" → ")}\n`;
    chartHtml += `Weight: ${weights.map((w) => w.toFixed(1) + " kg").join(" → ")}\n\n`;

    // Simple graph
    const minWeight = Math.min(...weights);
    const maxWeight = Math.max(...weights);
    const range = maxWeight - minWeight || 1;

    weights.forEach((w, i) => {
      const level = Math.round(((w - minWeight) / range) * 20);
      chartHtml += `${dates[i]}: ${"█".repeat(level)} ${w.toFixed(1)}kg\n`;
    });

    chartHtml += "</pre>";
    chartHtml += `<p><strong>Weight Change:</strong> ${(weights[0] - weights[weights.length - 1]).toFixed(1)} kg</p>`;
    chartHtml += `<p><strong>Total Logs:</strong> ${data.total_logs}</p>`;

    document.getElementById("progress-chart").innerHTML = chartHtml;
  } catch (error) {
    console.error("Error loading progress:", error);
  }
}

/**
 * Load AI recommendations
 */
async function loadRecommendations() {
  if (!currentUserId) return;

  try {
    const response = await fetch(`/api/recommendations/${currentUserId}`);
    const data = await response.json();

    if (!data.success) {
      document.getElementById("recommendations-list").innerHTML =
        "<p>Error loading recommendations</p>";
      return;
    }

    if (data.recommendations.length === 0) {
      document.getElementById("recommendations-list").innerHTML = `
                <p>${data.message}</p>
            `;
      return;
    }

    let html = "";
    data.recommendations.forEach((rec) => {
      html += `
                <div class="recommendation-card">
                    <div class="recommendation-type">${rec.type.replace("_", " ")}</div>
                    <div class="recommendation-message">${rec.message}</div>
                    <div class="recommendation-action">${rec.action}</div>
                </div>
            `;
    });

    if (data.progress_summary) {
      html += `
                <div style="background: #f5f5f5; padding: 1rem; border-radius: 5px; margin-top: 1rem;">
                    <h4>Progress Summary</h4>
                    <p>Weight Change: <strong>${data.progress_summary.weight_change} kg</strong></p>
                    <p>Weeks Elapsed: <strong>${data.progress_summary.weeks_elapsed}</strong></p>
                    <p>Total Logs: <strong>${data.progress_summary.logs_count}</strong></p>
                </div>
            `;
    }

    document.getElementById("recommendations-list").innerHTML = html;
  } catch (error) {
    console.error("Error loading recommendations:", error);
  }
}

/**
 * Load dashboard
 */
async function loadDashboard() {
  loadUserProfile();
}

// Initialize app on page load
document.addEventListener("DOMContentLoaded", () => {
  console.log("Fitness Assistant loaded");
});
