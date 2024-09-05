const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
canvas.width = 800;
canvas.height = 600;

// Player settings
const player = {
    x: canvas.width / 2 - 20,
    y: canvas.height - 40,
    width: 40,
    height: 20,
    color: 'green',
    speed: 5,
    bullets: []
};

// Invaders settings
const invaders = [];
const rows = 5;
const cols = 8;
const invaderWidth = 40;
const invaderHeight = 20;

for (let row = 0; row < rows; row++) {
    for (let col = 0; col < cols; col++) {
        invaders.push({
            x: col * (invaderWidth + 10) + 50,
            y: row * (invaderHeight + 10) + 30,
            width: invaderWidth,
            height: invaderHeight,
            color: 'red'
        });
    }
}

// Gamepad support
let gamepadIndex = null;

function updateGamepad() {
    const gamepads = navigator.getGamepads();
    if (gamepads[gamepadIndex]) {
        const gamepad = gamepads[gamepadIndex];
        const axisX = gamepad.axes[0];

        if (axisX < -0.1) {
            player.x -= player.speed;
        } else if (axisX > 0.1) {
            player.x += player.speed;
        }

        // Fire button (A button)
        if (gamepad.buttons[0].pressed) {
            fireBullet();
        }
    }
}

window.addEventListener("gamepadconnected", (event) => {
    gamepadIndex = event.gamepad.index;
    console.log("Gamepad connected at index", gamepadIndex);
});

window.addEventListener("gamepaddisconnected", () => {
    gamepadIndex = null;
    console.log("Gamepad disconnected");
});

// Player controls
const keys = {};

window.addEventListener('keydown', (e) => {
    keys[e.key] = true;
    if (e.key === " ") fireBullet();
});

window.addEventListener('keyup', (e) => {
    keys[e.key] = false;
});

function fireBullet() {
    player.bullets.push({
        x: player.x + player.width / 2 - 2,
        y: player.y,
        width: 4,
        height: 10,
        color: 'white',
        speed: 7
    });
}

function update() {
    // Player movement
    if (keys['ArrowLeft'] && player.x > 0) player.x -= player.speed;
    if (keys['ArrowRight'] && player.x + player.width < canvas.width) player.x += player.speed;

    // Update bullets
    player.bullets = player.bullets.filter(bullet => bullet.y > 0);
    player.bullets.forEach(bullet => bullet.y -= bullet.speed);

    // Update invaders
    invaders.forEach((invader, index) => {
        player.bullets.forEach((bullet, bulletIndex) => {
            if (bullet.x < invader.x + invader.width &&
                bullet.x + bullet.width > invader.x &&
                bullet.y < invader.y + invader.height &&
                bullet.y + bullet.height > invader.y) {
                // Bullet hits invader
                invaders.splice(index, 1);
                player.bullets.splice(bulletIndex, 1);
            }
        });
    });

    // Gamepad update
    if (gamepadIndex !== null) updateGamepad();
}

function draw() {
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw player
    ctx.fillStyle = player.color;
    ctx.fillRect(player.x, player.y, player.width, player.height);

    // Draw bullets
    player.bullets.forEach(bullet => {
        ctx.fillStyle = bullet.color;
        ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
    });

    // Draw invaders
    invaders.forEach(invader => {
        ctx.fillStyle = invader.color;
        ctx.fillRect(invader.x, invader.y, invader.width, invader.height);
    });
}

function gameLoop() {
    update();
    draw();
    requestAnimationFrame(gameLoop);
}

gameLoop();

