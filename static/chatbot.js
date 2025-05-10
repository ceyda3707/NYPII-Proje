document.addEventListener("DOMContentLoaded", function () {
  const button = document.getElementById("chatbot-button");
  const windowEl = document.getElementById("chatbot-window");
  const input = document.getElementById("chat-input");
  const sendBtn = document.getElementById("chat-submit");
  const chatBody = document.getElementById("chat-body");
  const closeBtn = document.querySelector(".chatbot-close");

  closeBtn.addEventListener("click", () => {
    windowEl.classList.add("hidden");
  });


  
   // Sadece ilk açılışta 1 kere "Merhaba" eklensin
  const greeting = document.createElement("div");
  greeting.className = "message bot";
  greeting.innerHTML = `Merhaba! Size nasıl yardımcı olabilirim?<br>
  🧠 Örnek: <em>çorba</em>, <em>tatlı</em> ya da <em>pirinç, süt</em gibi malzemeler yazabilirsin.`;
  chatBody.appendChild(greeting);
 
  button.addEventListener("click", () => {
    windowEl.classList.toggle("hidden");
  });

  sendBtn.addEventListener("click", async () => {
    const userMessage = input.value.trim();
    if (userMessage === "") return;

    const userDiv = document.createElement("div");
    userDiv.className = "message user";
    userDiv.textContent = userMessage;
    chatBody.appendChild(userDiv);
    input.value = "";

    try {
      const response = await fetch("/chatbot", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-Requested-With": "XMLHttpRequest"
        },
        body: `soru=${encodeURIComponent(userMessage)}`
      });

      const html = await response.text();
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, "text/html");
      const botMessage = doc.querySelector(".message.bot");

      if (botMessage) {
        chatBody.appendChild(botMessage);
      } else {
        const fallback = document.createElement("div");
        fallback.className = "message bot";
        fallback.textContent = "Bot'tan cevap alınamadı.";
        chatBody.appendChild(fallback);
      }

      chatBody.scrollTop = chatBody.scrollHeight;
    } catch (err) {
      const errDiv = document.createElement("div");
      errDiv.className = "message bot";
      errDiv.textContent = "Sunucu hatası: " + err;
      chatBody.appendChild(errDiv);
    }
  });
});
