const selectElement = document.getElementById('choice');
const documentsSection = document.getElementById('documents_section');
const releasesSection = document.getElementById('releases_section');

if (selectElement && documentsSection && releasesSection) {
    selectElement.addEventListener('change', function () {
        console.log("Valeur sélectionnée :", this.value);
        if (this.value === 'doc') {
            documentsSection.style.display = 'block';
            releasesSection.style.display = 'none';
        } else if (this.value === 'notes') {
            documentsSection.style.display = 'none';
            releasesSection.style.display = 'block';
        }
    });
}
// Afficher la première description par défaut
if (selectElement?.value === 'notes') {
    document.getElementById('releases_section').style.display = "block";
    document.getElementById('documents_section').style.display = 'none';
}