const buttons = document.querySelectorAll('.dropdown-item');

// Liste des sections
const sections = [
    "tasks_section",
    "documents_section",
    "pv_section",
    "releases_section"
];

// Fonction pour afficher la bonne section et cacher les autres
function showSection(selectedSection) {
    sections.forEach(sectionId => {
        const section = document.getElementById(sectionId);
        if (section) {
            section.style.display = (sectionId === selectedSection) ? "table" : "none";
        }
    });
}

// Ajouter l'événement de clic aux boutons
buttons.forEach(button => {
    button.addEventListener("click", function () {
        const sectionId = this.getAttribute("data-section");
        if (sectionId) {
            showSection(sectionId);
        }
    });
});

// Afficher uniquement "Tasks" au chargement
showSection("tasks_section");