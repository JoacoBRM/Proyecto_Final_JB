// static/js/scripts.js
function abrir_grafos() {
  window.location.href = "/grafos";
}

document.addEventListener("DOMContentLoaded", function () {
  const btn = document.getElementById("btn-abrir");
  if (btn) {
    btn.addEventListener("click", abrir_grafos);
  }
});

function abrir_inicio() {
  window.location.href = "/";
}

document.addEventListener("DOMContentLoaded", function () {
  const btn = document.getElementById("btn-inicio");
  if (btn) {
    btn.addEventListener("click", abrir_inicio);
  }
});

const mention = document.getElementById('user-mention');
const popup = document.getElementById('user-popup');

mention.addEventListener('click', function(event) {
  popup.style.left = event.pageX + 'px';
  popup.style.top = event.pageY + 'px';
  popup.style.display = 'block';
});

document.addEventListener('click', function(event) {
  if (!mention.contains(event.target) && !popup.contains(event.target)) {
    popup.style.display = 'none';
  }
});