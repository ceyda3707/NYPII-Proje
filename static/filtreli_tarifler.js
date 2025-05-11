function toggleHeart(btn) {
  btn.classList.toggle('active');
  const icon = btn.querySelector('i');
  if (btn.classList.contains('active')) {
    icon.classList.remove('fa-regular');
    icon.classList.add('fa-solid');
  } else {
    icon.classList.remove('fa-solid');
    icon.classList.add('fa-regular');
  }
}


function toggleMalzemeler(button) {
    const gizliListe = button.nextElementSibling;
    if (gizliListe.style.display === "none") {
        gizliListe.style.display = "inline";
        button.style.display = "none"; // butonu gizle (isteğe bağlı)
    }
}


document.addEventListener("DOMContentLoaded", function () {
  const kategoriButtons = document.querySelectorAll(".kategori-buttons button");
  const tarifler = document.querySelectorAll(".recipe-card");

  kategoriButtons.forEach(button => {
    button.addEventListener("click", function () {
      const secilenKategori = this.getAttribute("data-kategori");

      // Aktif butonu işaretle
      kategoriButtons.forEach(btn => btn.classList.remove("active"));
      this.classList.add("active");

      tarifler.forEach(tarif => {
        const kategori = tarif.querySelector(".difficulty").textContent.trim();

        if (secilenKategori === "Tümü" || kategori === secilenKategori) {
          tarif.style.display = "block";
        } else {
          tarif.style.display = "none";
        }
      });
    });
  });
});


document.addEventListener("DOMContentLoaded", function () {
  const aramaInput = document.getElementById("aramaInput");
  const tarifler = document.querySelectorAll(".recipe-card");

  aramaInput.addEventListener("input", function () {
    const aranan = this.value.toLowerCase();

    tarifler.forEach(tarif => {
      const tarifIsmi = tarif.querySelector("h3").textContent.toLowerCase();

      if (tarifIsmi.includes(aranan)) {
        tarif.style.display = "block";
      } else {
        tarif.style.display = "none";
      }
    });
  });
});




document.addEventListener("DOMContentLoaded", function () {
  const tarifler = Array.from(document.querySelectorAll(".recipe-card"));
  const sayfalama = document.getElementById("sayfalama");
  const tariflerPerPage = 21;
  let aktifSayfa = 1;

  function sayfalariOlustur() {
    const toplamSayfa = Math.ceil(tarifler.length / tariflerPerPage);
    sayfalama.innerHTML = "";

    for (let i = 1; i <= toplamSayfa; i++) {
      const btn = document.createElement("button");
      btn.textContent = i;
      if (i === aktifSayfa) btn.classList.add("aktif");

      btn.addEventListener("click", function () {
        aktifSayfa = i;
        tarifleriGoster();
        sayfalariOlustur();
      });

      sayfalama.appendChild(btn);
    }
  }

  function tarifleriGoster() {
    const start = (aktifSayfa - 1) * tariflerPerPage;
    const end = start + tariflerPerPage;

    tarifler.forEach((tarif, index) => {
      tarif.style.display = (index >= start && index < end) ? "block" : "none";
    });
  }

  tarifleriGoster();
  sayfalariOlustur();
});
