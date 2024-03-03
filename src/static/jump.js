const jumpingText = document.getElementById("jumping-text");

let position = 0;
let velocity = 1;

function updatePosition() {
  position += velocity;
  if (position <= 0) {
    velocity = 1;
  }
  if (position >= 20) {
    velocity = -1;
  }
  jumpingText.style.transform = `translateY(${position}px)`;
}

setInterval(updatePosition, 50);
