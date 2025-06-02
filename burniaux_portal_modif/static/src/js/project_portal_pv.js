const selectElements = document.getElementById("update_choice");
const descriptions = document.querySelectorAll(".update-desc");

selectElements?.addEventListener("change", function () {
    descriptions.forEach(desc => desc.style.display = "none"); // Cacher toutes les descriptions
    const selectedId = selectElements.value;
    const selectedDesc = document.getElementById("update_desc_" + selectedId);
    if (selectedDesc) {
        selectedDesc.style.display = ""; // Afficher seulement la description sélectionnée
    }
});

// Afficher la première description par défaut
if (selectElements?.value) {
    document.getElementById("update_desc_" + selectElements.value).style.display = "";
}