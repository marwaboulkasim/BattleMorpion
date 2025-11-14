let models = [];
const urlAPI_play = "http://127.0.0.1:8000/play";
let gridHTML;
let controller = null;
let playButton;

(async function initConfig() {
  const res = await fetch("http://127.0.0.1:8000/config");
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const config = await res.json();
  models = config.MODELS || [];
})();


const grid = Array.from({ length: 10 }, () => Array(10).fill(""));

function viewGrid() {
  gridHTML.innerHTML = "";
  for (let i = 0; i < grid.length; i++) {
    for (let j = 0; j < grid[i].length; j++) {
      const cell = document.createElement("div");
      cell.classList.add("cell");
      cell.textContent = grid[i][j];
      gridHTML.appendChild(cell);
    }
  }
  console.log("Grille générée :", gridHTML.children.length);
}


let joueur = "X";  
let playing = false; // La partie commence au clic sur Play
let lock = false;    // Empêche les coups simultanés

// Vérifie la direction pour alignement de 5
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


function getWinningCells(board, player) {
  for (let i = 0; i < 10; i++) {
    for (let j = 0; j < 10; j++) {
      if (board[i][j] === player) {
        const dirs = [
          [1, 0],  // horizontal
          [0, 1],  // vertical
          [1, 1],  // diagonal \
          [1, -1]  // diagonal /
        
        ];

        for (let [dx, dy] of dirs) {
          const cells = [];
          for (let k = 0; k < 5; k++) {
            const nx = j + dx * k;
            const ny = i + dy * k;
            if (nx >= 0 && nx < 10 && ny >= 0 && ny < 10 && board[ny][nx] === player) {
              cells.push([nx, ny]);
            } else {
              break;
            }
          }
          if (cells.length === 5) return cells;
        }
      }
    }
  }
  return null;
}

// Vérifie s’il y a un gagnant
function checkWinner(board, player) {
  return getWinningCells(board, player) !== null;
}

// Fonction principale qui joue un tour
async function playTurn() {
  if (!playing || lock) return;
  lock = true;

  controller = new AbortController();
  const signal = controller.signal;

  try {
    const res = await fetch(urlAPI_play, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        player: joueur.toLowerCase(),
        model: joueur === "X" ? models[0] : models[1],
        board: grid
      }),
      signal,
    });

    const data = await res.json();
    let [x, y] = data.move;
    if (grid[y][x] !== "") {
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

   
    if (checkWinner(grid, joueur)) {
      const winningCells = getWinningCells(grid, joueur);
      if (winningCells) {
        winningCells.forEach(([wx, wy]) => {
          const index = wy * 10 + wx;
          gridHTML.children[index].classList.add("winner");
        });
      }

      alert(`${joueur === "X" ? models[0] : models[1]} a gagné !`);
      playing = false;
      lock = false;
      playButton = document.getElementById("play");
      playButton.textContent = "Relancer?";
      console.log("Play → Relancer?");
      return;
    }

    // Vérifie match nul
    if (grid.flat().every(cell => cell !== "")) {
      alert("Match nul !");
      playing = false;
      lock = false;
      playButton = document.getElementById("play");
      playButton.textContent = "Relancer?";
      console.log("Play → Relancer?");
      return;
    }

    // Changer de joueur
    joueur = joueur === "X" ? "O" : "X";

    // Relance le tour après un délai
    setTimeout(() => {
      lock = false;
      playTurn();
    }, 700);

  } catch (err) {
    if (err.name === "AbortError") {
      console.warn("Requête annulée !");
    } else {
      console.error("Erreur API :", err);
    }
    lock = false;
  }
}

// Lancement au clic sur le bouton Play
document.addEventListener("DOMContentLoaded", () => {
  gridHTML = document.querySelector("#grid");
  viewGrid();

  playButton = document.getElementById("play");
  console.log("Bouton trouvé :", playButton);

  playButton.addEventListener("click", () => {
    if (!playing) {
    // Lancer la partie
    grid.forEach(row => row.fill(""));
    viewGrid();
    playing = true;
    lock = false;
    playButton.textContent = "Bataille en cours... Annuler ?";
    console.log("Play → Bataille en cours... Annuler?");
    playTurn();
  } else {
    // Annuler la partie
    playing = false;
    lock = false;

    if (controller) {
      controller.abort();
      controller = null;
    }
    clearTimeout();
    playButton.textContent = "Play";
    console.warn("Partie annulée !");
  }
  });
});