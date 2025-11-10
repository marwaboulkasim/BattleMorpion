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
let playing = true; // Contrôle l'état du jeu
let lock = false; // Empêche les coups trop rapides

// Vérifie si un joueur a gagné (alignement de 5)
function checkWinner(board, player) {
    for (let i = 0; i < 10; i++) {
        for (let j = 0; j < 10; j++) {
            if (board[i][j] === player) {
                if (checkDirection(board, player, i, j, 1, 0) || // Horizontal
                    checkDirection(board, player, i, j, 0, 1) || // Vertical
                    checkDirection(board, player, i, j, 1, 1) || // Diagonal \
                    checkDirection(board, player, i, j, 1, -1)) { // Diagonal /
                    return true;
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
    return count === 5;
}

// Gestion d’un tour
async function playTurn() {
    if (!playing || lock) return;
    lock = true;

    try {
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
        let [x, y] = data.move;

        // Vérifier si la case est libre, sinon choisir une case vide aléatoire
        if (grid[y][x] !== "") {
            console.warn(`Coup invalide du joueur ${joueur} sur [${x},${y}]`);
            const empty = [];
            for (let i = 0; i < 10; i++) {
                for (let j = 0; j < 10; j++) {
                    if (grid[i][j] === "") empty.push([j, i]);
                }
            }
            if (empty.length > 0) {
                [x, y] = empty[Math.floor(Math.random() * empty.length)];
            }
        }

        grid[y][x] = joueur;
        viewGrid();

        // Vérifie victoire
        if (checkWinner(grid, joueur)) {
            alert(`${joueur === "X" ? "Ollama" : "Azure"} a gagné ! `);
            playing = false;
            return;
        }

        // Vérifie match nul
        if (grid.flat().every(cell => cell !== "")) {
            alert("Match nul !");
            playing = false;
            return;
        }

        // Changer de joueur
        joueur = joueur === "X" ? "O" : "X";

        setTimeout(() => {
            lock = false;
            playTurn();
        }, 700);

    } catch (err) {
        console.error("Erreur API :", err);
        lock = false;
        setTimeout(playTurn, 1000);
    }
}

// Lancer la partie dès le chargement
document.addEventListener("DOMContentLoaded", () => {
    viewGrid();
    playTurn();
});
