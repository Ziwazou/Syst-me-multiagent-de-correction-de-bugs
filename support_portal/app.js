/**
 * Logique JavaScript du Portail Support Utilisateur (support_portal/app.js)
 * Gère l'envoi asynchrone HTTP POST au serveur FastAPI backend (http://localhost:8000/api/trigger-fix)
 */

document.getElementById('support-form').addEventListener('submit', async function(e) {
  e.preventDefault();

  // 1. Récupération des données du formulaire HTML
  const ticketId = document.getElementById('ticket-id').value;
  const userReport = document.getElementById('user-report').value;
  const targetRepo = "programiz/Calculator";
  
  // 2. Éléments DOM d'affichage du statut
  const submitBtn = document.getElementById('btn-submit');
  const statusCard = document.getElementById('status-card');
  const statusTitle = document.getElementById('status-title');
  const statusBadge = document.getElementById('status-badge');
  const statusDetails = document.getElementById('status-details');
  const resultBox = document.getElementById('result-box');
  const prLink = document.getElementById('pr-link');
  const codeOutput = document.getElementById('code-output');

  // 3. Mise à jour de l'interface en mode "Chargement / En cours"
  submitBtn.disabled = true;
  submitBtn.innerHTML = '<span>Traitement en cours...</span>';
  statusCard.style.display = 'block';
  resultBox.style.display = 'none';
  statusTitle.textContent = 'Traitement en cours par le système...';
  statusBadge.className = 'badge badge-pending';
  statusBadge.textContent = 'EN COURS';

  const sampleSourceCode = `
def evaluer_expression_calculatrice(expression: str) -> str:
    # Code source actuel de l'application
    return str(eval(expression))
`;

  // 4. Envoi de la requête HTTP POST asynchrone (fetch) à l'API FastAPI
  try {
    const response = await fetch('http://localhost:8000/api/trigger-fix', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        ticket_id: ticketId,
        user_report: userReport,
        source_code: sampleSourceCode,
        repository: targetRepo
      })
    });

    const data = await response.json();

    if (data.success) {
      statusTitle.textContent = 'Bug résolu et Pull Request GitHub ouverte !';
      statusBadge.className = 'badge badge-success';
      statusBadge.textContent = 'SUCCÈS';
      statusDetails.textContent = `Résolution validée en ${data.tentatives} tentative(s). Statut final : ${data.statut_final}`;
      
      prLink.href = data.pr_github_url;
      prLink.textContent = data.pr_github_url;
      codeOutput.textContent = data.code_final_corrige;
      resultBox.style.display = 'block';
    } else {
      statusTitle.textContent = 'Échec de la résolution automatique';
      statusDetails.textContent = data.detail || 'Erreur lors du traitement.';
    }
  } catch (error) {
    statusTitle.textContent = 'En attente du serveur API FastAPI (http://localhost:8000)';
    statusDetails.textContent = `Le frontend est prêt ! Lancez le serveur FastAPI pour tester la communication. (${error.message})`;
  } finally {
    submitBtn.disabled = false;
    submitBtn.innerHTML = '<span>Soumettre l\'Incident</span>';
  }
});
