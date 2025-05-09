document.addEventListener("DOMContentLoaded", () => {
  const tarifler = [ 
    // Buraya 600 tarif gelecek...
    {
      kategori: "Tatlılar",
      isim: "Çikolatalı Brownie",
      hazirlik: "15 dk",
      pisirme: "25 dk",
      malzemeler: ["Bitter Çikolata", "Tereyağı", "Un", "Şeker"],
      puan: 4.9,
      favori: false
    },
        {
      kategori: "Çorbalar",
      isim: "Ezogelin Çorbası",
      hazirlik: "20 dk",
      pisirme: "40 dk",
      malzemeler: ["Kırmızı Mercimek", "Bulgur", "Pirinç", "Domates Salçası"],
      puan: 4.5,
      favori: false // Favori durumu
    },
    {
      kategori: "Ana Yemekler",
      isim: "Fırında Tavuk",
      hazirlik: "30 dk",
      pisirme: "45 dk",
      malzemeler: ["Tavuk But", "Patates", "Soğan", "Baharatlar"],
      puan: 4.7,
      favori: false // Favori durumu
    },
    {
      kategori: "Tatlılar",
      isim: "Kremalı Çilekli Pasta",
      hazirlik: "30 dk",
      pisirme: "35 dk",
      malzemeler: ["Çilek", "Krema", "Bisküvi", "Süt", "Şeker", "Vanilya", "Tereyağı"],
      puan: 4.8,
      favori: false // Favori durumu
    }
    // Devamı...
  ];

  const container = document.getElementById("tarifler-container");
  const aramaInput = document.getElementById("aramaInput");
  const sayfalamaContainer = document.getElementById("sayfalama"); // sayfalama için ek div
  let seciliKategori = "Hepsi";
  let aramaKelimesi = "";
  let mevcutSayfa = 1;
  const tarifSayisiBirSayfada = 20;

  function tarifleriGoster() {
    container.innerHTML = "";

    const filtreliTarifler = tarifler.filter(t => {
      const kategoriEslesme = seciliKategori === "Hepsi" || t.kategori === seciliKategori;
      const isimEslesme = t.isim.toLowerCase().includes(aramaKelimesi.toLowerCase());
      return kategoriEslesme && isimEslesme;
    });

    if (filtreliTarifler.length === 0) {
      container.innerHTML = "<p>Uygun tarif bulunamadı.</p>";
      sayfalamaContainer.innerHTML = "";
      return;
    }

    // Sayfalama mantığı
    const toplamSayfa = Math.ceil(filtreliTarifler.length / tarifSayisiBirSayfada);
    const baslangic = (mevcutSayfa - 1) * tarifSayisiBirSayfada;
    const goruntulenecekTarifler = filtreliTarifler.slice(baslangic, baslangic + tarifSayisiBirSayfada);

    goruntulenecekTarifler.forEach((tarif, index) => {
      const globalIndex = tarifler.indexOf(tarif); // gerçek index
      const ilkUcMalzeme = tarif.malzemeler.slice(0, 3);
      const geriKalanMalzemeler = tarif.malzemeler.slice(3);

      const malzemelerHTML = ilkUcMalzeme
        .map(malzeme => `<span class="malzeme">${malzeme}</span>`)
        .join(" ");

      const ekstraMalzemeHTML = geriKalanMalzemeler.length > 0
        ? `<span class="ekstra-malzemeler" style="cursor:pointer;" data-index="${globalIndex}">+${geriKalanMalzemeler.length} daha</span>`
        : "";

      const favClass = tarif.favori ? "fa-solid" : "fa-regular";

      const cardHTML = `
        <div class="recipe-card" data-index="${globalIndex}">
          <div class="card-top">
            <div class="fav-icon" data-index="${globalIndex}">
              <i class="${favClass} fa-heart"></i>
            </div>
          </div>
          <div class="card-content">
            <span class="difficulty">${tarif.kategori}</span>
            <h3>${tarif.isim}</h3>
            <div class="süre-bilgi">
              <span class="hazirlik"><i class="fa-solid fa-clock"></i> Hazırlık: ${tarif.hazirlik}</span>
              <span class="pisirme"><i class="fa-solid fa-fire"></i> Pişirme: ${tarif.pisirme}</span>
            </div>
            <p class="malzeme-listesi">${malzemelerHTML} ${ekstraMalzemeHTML}</p>
            <div class="card-footer">
              <span>${tarif.malzemeler.length} malzeme</span>
              <a href="#">Tarifi Gör →</a>
            </div>
          </div>
        </div>
      `;
      container.insertAdjacentHTML("beforeend", cardHTML);
    });

    // Favori ikonu tıklama
    document.querySelectorAll(".fav-icon").forEach(icon => {
      icon.addEventListener("click", () => {
        const index = icon.dataset.index;
        tarifler[index].favori = !tarifler[index].favori;
        const heartIcon = icon.querySelector("i");
        heartIcon.classList.toggle("fa-solid");
        heartIcon.classList.toggle("fa-regular");
      });
    });

    // "+X daha" tıklama
    document.querySelectorAll(".ekstra-malzemeler").forEach(span => {
      span.addEventListener("click", () => {
        const index = span.dataset.index;
        const geriKalan = tarifler[index].malzemeler.slice(3);
        const ekstraHTML = geriKalan.map(m => `<span class="malzeme">${m}</span>`).join(" ");
        const malzemeListesi = span.parentElement;
        span.style.display = "none";
        malzemeListesi.innerHTML += ` ${ekstraHTML}`;
      });
    });

    // Sayfa numaraları
    sayfalamaContainer.innerHTML = "";
    for (let i = 1; i <= toplamSayfa; i++) {
      const btn = document.createElement("button");
      btn.innerText = i;
      btn.className = i === mevcutSayfa ? "aktif" : "";
      btn.addEventListener("click", () => {
        mevcutSayfa = i;
        tarifleriGoster();
      });
      sayfalamaContainer.appendChild(btn);
    }
  }

  // Başlangıçta tarifleri göster
  tarifleriGoster();

  // Kategori butonları
  document.querySelectorAll('.kategori-buttons button').forEach(button => {
    button.addEventListener('click', function () {
      document.querySelectorAll('.kategori-buttons button').forEach(btn => btn.classList.remove('active'));
      this.classList.add('active');
      seciliKategori = this.dataset.kategori;
      mevcutSayfa = 1;
      tarifleriGoster();
    });
  });

  // Arama kutusu
  aramaInput.addEventListener("input", () => {
    aramaKelimesi = aramaInput.value.trim();
    mevcutSayfa = 1;
    tarifleriGoster();
  });
});
