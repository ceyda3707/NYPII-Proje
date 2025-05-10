document.addEventListener("DOMContentLoaded", function () {
  const button = document.getElementById("chatbot-button");
  const windowEl = document.getElementById("chatbot-window");

  button.addEventListener("click", () => {
    windowEl.classList.toggle("hidden");
  });
});
