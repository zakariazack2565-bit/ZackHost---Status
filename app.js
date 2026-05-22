const ctx = document.getElementById("latencyChart");

const chart = new Chart(ctx, {

    type: "line",

    data: {
        labels: [],
        datasets: [{
            label: "Latency (ms)",
            data: [],
            tension: 0.3
        }]
    },

    options: {
        responsive: true
    }
});

async function updateDashboard() {

    // Get API data
    const response = await fetch("/api/status");

    const data = await response.json();

    // Stop if empty
    if(data.length === 0){
        return;
    }

    // Latest check
    const latest = data[data.length - 1];

    // Update UI
    document.getElementById("status").innerText =
        latest.state;

    document.getElementById("latency").innerText =
        latest.latency + " ms";

    document.getElementById("last-check").innerText =
        latest.time;

    // Update graph
    chart.data.labels =
        data.map(item => item.time);

    chart.data.datasets[0].data =
        data.map(item => item.latency);

    chart.update();
}

// Refresh every 5 sec
setInterval(updateDashboard, 5000);

// First load
updateDashboard();