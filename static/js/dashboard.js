if (typeof STATS !== "undefined" && STATS.total > 0) {
  Chart.defaults.color = getComputedStyle(document.body).color;
  Chart.defaults.borderColor = "rgba(128,128,128,.2)";
  Chart.defaults.font.family = "Inter, system-ui, sans-serif";

  const COLORS = {
    cardboard: "#a16207", glass: "#0891b2", metal: "#64748b",
    organic: "#16a34a", other: "#a855f7", paper: "#d97706", plastic: "#2563eb"
  };
  const colors = STATS.classes.map(c => COLORS[c] || "#94a3b8");
  const labels = STATS.classes.map(c => c.charAt(0).toUpperCase() + c.slice(1));

  new Chart(document.getElementById("pieChart"), {
    type: "doughnut",
    data: { labels, datasets: [{ data: STATS.class_counts, backgroundColor: colors, borderWidth: 0 }] },
    options: { cutout: "62%", plugins: { legend: { position: "bottom" } } }
  });

  new Chart(document.getElementById("barChart"), {
    type: "bar",
    data: { labels, datasets: [{ data: STATS.class_counts, backgroundColor: colors, borderRadius: 8 }] },
    options: {
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true, ticks: { precision: 0 } } }
    }
  });

  new Chart(document.getElementById("lineChart"), {
    type: "line",
    data: {
      labels: STATS.days,
      datasets: [{ label: "Classifications", data: STATS.day_counts, borderColor: "#16a34a",
                   backgroundColor: "rgba(34,197,94,.2)", fill: true, tension: 0.35, pointRadius: 3 }]
    },
    options: {
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true, ticks: { precision: 0 } } }
    }
  });
}