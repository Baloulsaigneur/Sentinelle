async function startScan() {
    const url = document.getElementById("urlInput").value;
    if (!url) {
        alert("Veuillez entrer une URL !");
        return;
    }

    document.getElementById("status").textContent = "Scan en cours...";
    document.getElementById("result").textContent = "";

    try {
        // Démarrer un scan
        const response = await fetch("http://localhost:8000/scan/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ target: url })
        });
        const data = await response.json();
        const taskId = data.task_id;

        // Vérifier les résultats toutes les 5 secondes
        let result = null;
        while (!result) {
            await new Promise(resolve => setTimeout(resolve, 5000));
            const resultResponse = await fetch(`http://localhost:8000/results/${taskId}`);
            const resultData = await resultResponse.json();
            
            if (resultData.status === "completed") {
                result = resultData.result;
            }
        }

        document.getElementById("status").textContent = "Scan terminé !";
        document.getElementById("result").textContent = JSON.stringify(result, null, 2);
    } catch (error) {
        document.getElementById("status").textContent = "Erreur lors du scan.";
        console.error("Erreur:", error);
    }
}
