let entries = JSON.parse(localStorage.getItem("entries")) || [];

function renderEntries() {
  const list = document.getElementById("entriesList");
  if (!list) return;
  list.innerHTML = "";
  entries.forEach(entry => {
    const li = document.createElement("li");
    li.textContent = `${entry.date} - ${entry.title} [${(entry.skills||[]).join(", ")}]`;
    list.appendChild(li);
  });
}

function renderSkillCloud() {
  const cloud = document.getElementById("skillCloud");
  if (!cloud) return;
  cloud.innerHTML = "";
  const skillCount = {};
  entries.forEach(e => (e.skills || []).forEach(s => {
    const skill = String(s).trim().toLowerCase();
    if (!skill) return;
    skillCount[skill] = (skillCount[skill] || 0) + 1;
  }));
  Object.entries(skillCount).forEach(([skill, count]) => {
    const span = document.createElement("span");
    span.textContent = skill;
    span.style.margin = "0 8px";
    span.style.display = "inline-block";
    span.style.fontSize = (12 + Math.min(count, 8) * 3) + "px";
    cloud.appendChild(span);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const features = [
    "Progress Tracker",
    "Skill Cloud",
    "Timeline View",
    "Resume Generator",
    "Learning Hub"
  ];

  const featureLinks = {
    "Progress Tracker": "progress-tracker.html",
    "Skill Cloud": "skill-cloud.html",
    "Timeline View": "timeline.html",
    "Resume Generator": "resume-generator.html",
    "Learning Hub": "learning-hub.html"
  };

  const searchBar = document.getElementById("searchBar");
  const suggestionsBox = document.getElementById("suggestions");

  if (searchBar && suggestionsBox) {
    searchBar.addEventListener("input", function () {
      const query = this.value.toLowerCase().trim();
      suggestionsBox.innerHTML = "";
      if (!query) {
        suggestionsBox.style.display = "none";
        return;
      }
      const matches = features.filter(item => item.toLowerCase().includes(query));
      if (matches.length) {
        matches.forEach(match => {
          const div = document.createElement("div");
          div.textContent = match;
          div.addEventListener("click", () => {
            searchBar.value = match;
            suggestionsBox.style.display = "none";
            const link = featureLinks[match];
            if (link) window.location.href = link;
          });
          suggestionsBox.appendChild(div);
        });
        suggestionsBox.style.display = "block";
      } else {
        suggestionsBox.style.display = "none";
      }
    });

    document.addEventListener("click", (e) => {
      if (!suggestionsBox.contains(e.target) && e.target !== searchBar) {
        suggestionsBox.style.display = "none";
      }
    });
  }

  const form = document.getElementById("entryForm");
  if (form) {
    form.addEventListener("submit", e => {
      e.preventDefault();
      const date = document.getElementById("date")?.value || "";
      const title = document.getElementById("title")?.value || "";
      const description = document.getElementById("description")?.value || "";
      const skillsRaw = document.getElementById("skills")?.value || "";
      const skills = skillsRaw.split(",").map(s => s.trim()).filter(Boolean);
      entries.push({ date, title, description, skills });
      localStorage.setItem("entries", JSON.stringify(entries));
      renderEntries();
      renderSkillCloud();
      form.reset();
    });
  }

  const menuIcon = document.querySelector(".menu-icon");
  const sideMenu = document.getElementById("sideMenu");
  if (menuIcon && sideMenu) {
    menuIcon.addEventListener("click", (e) => {
      e.stopPropagation();
      sideMenu.style.width = sideMenu.style.width === "250px" ? "0" : "250px";
    });
    document.addEventListener("click", (event) => {
      if (!sideMenu.contains(event.target) && !menuIcon.contains(event.target)) {
        sideMenu.style.width = "0";
      }
    });
  }

  renderEntries();
  renderSkillCloud();

    // Reveal feature cards with animation
  const featureCards = document.querySelectorAll(".feature-card");
  featureCards.forEach((card, index) => {
    setTimeout(() => {
      card.classList.add("show");
    }, index * 150);
  });

});
