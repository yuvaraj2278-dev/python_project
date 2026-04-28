// 🔐 Firebase Config
const firebaseConfig = {
    apiKey: "AIzaSyA9CXDiGXm1-P86mn-2qrVeAAV6GlKuJXI",
    authDomain: "shopper-ai-ff808.firebaseapp.com",
    projectId: "shopper-ai-ff808",
    storageBucket: "shopper-ai-ff808.firebasestorage.app",
    messagingSenderId: "461841307458",
    appId: "1:461841307458:web:5c4ecd59c170dd3bfadadb",
    measurementId: "G-N0KDSVCNB4"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();

// 🛡️ Protect Dashboard + Welcome Message
auth.onAuthStateChanged(user => {
    if (!user) {
        window.location.href = "login.html";
    } else {
        const msg = document.getElementById("welcomeMsg");
        if (msg) {
            msg.innerText = "👋 Welcome, " + user.email;
        }
    }
});

// 🔄 Navigation (3 Pages)
function showPage(page) {
    document.getElementById("welcomePage").style.display = "none";
    document.getElementById("predictPage").style.display = "none";
    document.getElementById("graphPage").style.display = "none";

    document.getElementById(page + "Page").style.display = "block";

    // 🔥 Fix: redraw graph when opening graph page
    if (page === "graph" && lastConfidence !== null) {
        createCharts(lastConfidence);
    }
}

// 🔓 Logout
function logout() {
    auth.signOut().then(() => {
        window.location.href = "login.html";
    });
}

// 📊 Graph variables
let barChart = null;
let pieChart = null;


let lastConfidence = null;

// 🤖 Prediction Function
async function getPrediction() {
    const data = {
        PageValues: parseFloat(document.getElementById('pageValues').value),
        Month: document.getElementById('month').value,
        VisitorType: document.getElementById('visitorType').value,
        Weekend: document.getElementById('weekend').value === 'true'
    };

    const resultDiv = document.getElementById("result");
    resultDiv.innerText = "⏳ Predicting...";

    try {
        const response = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(data)
        });

        const result = await response.json();

        // Show result
        resultDiv.innerText = result.prediction ? "✅ PURCHASE" : "❌ NO PURCHASE";

        // Save confidence
        lastConfidence = result.confidence;

        // Create graphs
        createCharts(result.confidence);

    } catch (error) {
        console.error(error);
        resultDiv.innerText = "⚠️ Backend error!";
    }
}

// 📊 Create Charts
function createCharts(confidence) {

    const purchase = confidence * 100;
    const noPurchase = (1 - confidence) * 100;

    // BAR CHART
    const barCanvas = document.getElementById("barChart");
    const barCtx = barCanvas.getContext("2d");

    if (barChart) barChart.destroy();

    barChart = new Chart(barCtx, {
        type: "bar",
        data: {
            labels: ["Purchase", "No Purchase"],
            datasets: [{
                label: "Probability (%)",
                data: [purchase, noPurchase],
                backgroundColor: ["#2563eb", "#60a5fa"]
            }]
        },
        options: {
            responsive: true
        }
    });

    // PIE CHART
    const pieCanvas = document.getElementById("pieChart");
    const pieCtx = pieCanvas.getContext("2d");

    if (pieChart) pieChart.destroy();

    pieChart = new Chart(pieCtx, {
        type: "pie",
        data: {
            labels: ["Purchase", "No Purchase"],
            datasets: [{
                data: [purchase, noPurchase],
                backgroundColor: ["#2563eb", "#60a5fa"]
            }]
        },
        options: {
            responsive: true
        }
    });
}