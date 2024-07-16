const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

canvas.width = 800;
canvas.height = 600;

const player = {
    x: canvas.width / 2 - 15,
    y: canvas.height - 50,
    width: 30,
    height: 30,
    dx: 5,
    bullets: []
};

const aliens = [];
const alienRows = 5;
const alienCols = 11;
const alienWidth = 30;
const alienHeight = 30;
const alienPadding = 10;
const alienOffsetTop = 50;
const alienOffsetLeft = 50;
let alienDx = 1; // Horizontal movement speed
let alienDy = 10; // Vertical movement speed
let alienDirection = 1; // 1 for right, -1 for left

let rightPressed = false;
let leftPressed = false;
let spacePressed = false;

function drawPlayer() {
    ctx.fillStyle = 'green';
    ctx.fillRect(player.x, player.y, player.width, player.height);
}

function drawAliens() {
    ctx.fillStyle = 'white';
    for (let r = 0; r < alienRows; r++) {
        for (let c = 0; c < alienCols; c++) {
            if (!aliens[r][c].destroyed) {
                const x = aliens[r][c].x;
                const y = aliens[r][c].y;
                ctx.fillRect(x, y, alienWidth, alienHeight);
            }
        }
    }
}

function drawBullets() {
    ctx.fillStyle = 'white';
    player.bullets.forEach(bullet => {
        ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
    });
}

function movePlayer() {
    if (rightPressed && player.x < canvas.width - player.width) {
        player.x += player.dx;
    }
    if (leftPressed && player.x > 0) {
        player.x -= player.dx;
    }
}

function moveBullets() {
    player.bullets.forEach((bullet, index) => {
        bullet.y -= bullet.dy;
        if (bullet.y < 0) {
            player.bullets.splice(index, 1);
        }
    });
}

function detectCollisions() {
    player.bullets.forEach((bullet, bIndex) => {
        aliens.forEach((row, rIndex) => {
            row.forEach((alien, aIndex) => {
                if (!alien.destroyed && bullet.x < alien.x + alienWidth &&
                    bullet.x + bullet.width > alien.x &&
                    bullet.y < alien.y + alienHeight &&
                    bullet.y + bullet.height > alien.y) {
                    player.bullets.splice(bIndex, 1);
                    alien.destroyed = true;
                }
            });
        });
    });
}

function initAliens() {
    for (let r = 0; r < alienRows; r++) {
        aliens[r] = [];
        for (let c = 0; c < alienCols; c++) {
            const x = c * (alienWidth + alienPadding) + alienOffsetLeft;
            const y = r * (alienHeight + alienPadding) + alienOffsetTop;
            aliens[r][c] = { x, y, destroyed: false };
        }
    }
}

function moveAliens() {
    let atEdge = false;
    aliens.forEach(row => {
        row.forEach(alien => {
            if (!alien.destroyed) {
                alien.x += alienDx * alienDirection;
                if (alien.x + alienWidth >= canvas.width || alien.x <= 0) {
                    atEdge = true;
                }
            }
        });
    });

    if (atEdge) {
        alienDirection *= -1;
        aliens.forEach(row => {
            row.forEach(alien => {
                alien.y += alienDy;
            });
        });
    }
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawPlayer();
    drawAliens();
    drawBullets();
    movePlayer();
    moveBullets();
    moveAliens();
    detectCollisions();
    requestAnimationFrame(draw);
}

function keyDownHandler(e) {
    if (e.key === 'Right' || e.key === 'ArrowRight') {
        rightPressed = true;
    }
    if (e.key === 'Left' || e.key === 'ArrowLeft') {
        leftPressed = true;
    }
    if (e.key === ' ' || e.key === 'Spacebar') {
        spacePressed = true;
        player.bullets.push({
            x: player.x + player.width / 2 - 2.5,
            y: player.y,
            width: 5,
            height: 10,
            dy: 7
        });
    }
}

function keyUpHandler(e) {
    if (e.key === 'Right' || e.key === 'ArrowRight') {
        rightPressed = false;
    }
    if (e.key === 'Left' || e.key === 'ArrowLeft') {
        leftPressed = false;
    }
    if (e.key === ' ' || e.key === 'Spacebar') {
        spacePressed = false;
    }
}

document.addEventListener('keydown', keyDownHandler);
document.addEventListener('keyup', keyUpHandler);

initAliens();
draw();
