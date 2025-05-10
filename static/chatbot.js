document.addEventListener("DOMContentLoaded", function () {
  const button = document.getElementById("chatbot-button");
  const windowEl = document.getElementById("chatbot-window");
  const input = document.querySelector(".chatbot-input input");
  const sendBtn = document.querySelector(".chatbot-input button");
  const chatBody = document.getElementById("chat-body");

  button.addEventListener("click", () => {
    windowEl.classList.toggle("hidden");
  });

  sendBtn.addEventListener("click", () => {
    const userMessage = input.value.trim();
    if (userMessage !== "") {
      const userDiv = document.createElement("div");
      userDiv.className = "message user";
      userDiv.textContent = userMessage;
      chatBody.appendChild(userDiv);
      input.value = "";

      // Simüle bot cevabı
      setTimeout(() => {
        const botDiv = document.createElement("div");
        botDiv.className = "message bot";
        botDiv.textContent = "Bu sadece bir örnek cevaptır.";
        chatBody.appendChild(botDiv);
        chatBody.scrollTop = chatBody.scrollHeight;
      }, 800);
    }
  });
});

