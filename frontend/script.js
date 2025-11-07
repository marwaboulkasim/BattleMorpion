const urlAPI = "http://127.0.0.1:8000/play";
const grid = Array.from({ length: 10 }, () => Array(10).fill(""));
const gridHTML = document.querySelector("#grid");

function viewGrid() {
    gridHTML.innerHTML = "";
    for (let i = 0; i < grid.length; i++) {
        for (let j = 0; j < grid[i].length; j++) {
            const cellHTML = document.createElement("div");
            cellHTML.classList.add("cell");
            cellHTML.textContent = grid[i][j]; // Affiche le symbole du joueur
            gridHTML.appendChild(cellHTML);
        }
    }
}

let joueur = "X"; // X = Ollama, O = Azure
let playing = true; // Variable pour contrôler l'état du jeu
let lock = false; // Variable de verrouillage pour empêcher des mouvements trop rapides

// Fonction pour vérifier la victoire
function checkWinner(board, player) {
    for (let i = 0; i < 10; i++) {
        for (let j = 0; j < 10; j++) {
            if (board[i][j] === player) {
                if (checkDirection(board, player, i, j, 1, 0) || // Horizontal
                    checkDirection(board, player, i, j, 0, 1) || // Vertical
                    checkDirection(board, player, i, j, 1, 1) || // Diagonal \
                    checkDirection(board, player, i, j, 1, -1)) { // Diagonal /
                    return true; // Victoire si une direction est valide
                }
            }
        }
    }
    return false;
}

function checkDirection(board, player, x, y, dx, dy) {
    let count = 0;
    for (let i = 0; i < 5; i++) {
        let nx = x + dx * i;
        let ny = y + dy * i;
        if (nx >= 0 && nx < 10 && ny >= 0 && ny < 10 && board[ny][nx] === player) {
            count++;
        } else {
            break;
        }
    }
    return count === 5; // 5 symboles consécutifs
}

// Fonction de gestion des tours
async function playTurn() {
    if (!playing || lock) return; // Empêche de jouer si la partie est terminée ou si un verrou est activé
    lock = true; // Active le verrou pour éviter plusieurs coups simultanés

    try {
        // Envoi du coup pour le joueur actuel
        const res = await fetch(urlAPI, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                player: joueur.toLowerCase(),
                model: joueur === "X" ? "llama3" : "o4-mini",
                board: grid
            })
        });

        const data = await res.json();

        // Vérification que la réponse du modèle est correcte
        const [x, y] = data.move;
        if (grid[y][x] === "") { // Si la case est vide, on place le symbole du joueur
            grid[y][x] = joueur;
            viewGrid(); // Met à jour l'affichage de la grille
        }

        // Vérification si le joueur a gagné
        if (checkWinner(grid, joueur)) {
            alert(`${joueur === "X" ? "Ollama" : "Azure"} a gagné ! 🎉`);
            playing = false; // Met fin à la partie si un joueur gagne
            return;
        }

        // Changer de joueur après avoir joué un coup
        joueur = joueur === "X" ? "O" : "X";
        
        setTimeout(() => {
            lock = false; // Déverrouille le jeu pour permettre au joueur suivant de jouer
            playTurn(); // Rejoue après un petit délai pour respecter les tours
        }, 700); // Délai de 700ms pour simuler une petite pause entre les coups

    } catch (err) {
        console.error("Erreur API :", err);
        lock = false; // Si une erreur se produit, le verrou est désactivé
        setTimeout(playTurn, 1000); // Réessayer après un délai de 1 seconde
    }
}

// Lancer le duel automatiquement dès le chargement de la page
document.addEventListener("DOMContentLoaded", () => {
    viewGrid(); // Afficher la grille vide au début
    playTurn(); // Démarrer le jeu
});
