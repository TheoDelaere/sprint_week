// document.addEventListener("DOMContentLoaded", function() {
var emptyChart = document.getElementById("myChart")
if (emptyChart != null) {
    var ctx = emptyChart.getContext("2d");
    var data = JSON.parse(document.getElementById("myChart").getAttribute("data-total-hours"));
    var reversedData = [...data].reverse();

    var myChart = new Chart(ctx, {
        type: "bar",  // Type de graphique (barres, ligne, etc.)
        data: {
            labels: ["-5", "-4", "-3", "-2", "-1", "0"], // Labels des données
            datasets: [{
                label: "Valeurs",
                data: reversedData, // Données
                backgroundColor: "rgba(54, 162, 235, 0.6)",
                borderColor: "rgba(54, 162, 235, 1)",
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
// });
