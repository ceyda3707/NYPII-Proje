document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("tarifler-container");
  const aramaInput = document.getElementById("aramaInput");
  const sayfalamaContainer = document.getElementById("sayfalama");
  let seciliKategori = "Tümü";
  let aramaKelimesi = "";
  let mevcutSayfa = 1;
  const tarifSayisiBirSayfada = 20;

  let tarifler = [];
  
  async function tarifleriYukle() {
    try {
      const response = await fetch("/api/tum_tarifler");
      const veri = await response.json();

      tarifler = veri.map(t => ({
        ...t,
        malzemeler: t.malzemeler.split(','),

        favori: t.favori === 1
      }));

      tarifleriGoster();
    } catch (err) {
      console.error("Tarifler yüklenemedi:", err);
      container.innerHTML = "<p>Tarifler yüklenirken hata oluştu.</p>";
    }
  }

  function tarifleriGoster() {
    console.log("Görünen tarif sayısı:", document.querySelectorAll(".recipe-card").length);

    container.innerHTML = "";

    const filtreliTarifler = tarifler.filter(t => {
     const kategoriEslesme = seciliKategori === "Tümü" || !seciliKategori || t.kategori === seciliKategori;
      const isimEslesme = t.isim.toLowerCase().includes(aramaKelimesi.toLowerCase());
      return kategoriEslesme && isimEslesme;
    });

    if (filtreliTarifler.length === 0) {
      container.innerHTML = "<p>Uygun tarif bulunamadı.</p>";
      sayfalamaContainer.innerHTML = "";
      return;
    }

    const toplamSayfa = Math.ceil(filtreliTarifler.length / tarifSayisiBirSayfada);
    const baslangic = (mevcutSayfa - 1) * tarifSayisiBirSayfada;
    const goruntulenecekTarifler = filtreliTarifler.slice(baslangic, baslangic + tarifSayisiBirSayfada);

    goruntulenecekTarifler.forEach((tarif, index) => {
      const globalIndex = tarifler.indexOf(tarif);
      const ilkUcMalzeme = tarif.malzemeler.slice(0, 3);
      const geriKalanMalzemeler = tarif.malzemeler.slice(3);

      const malzemelerHTML = ilkUcMalzeme
        .map(malzeme => `<span class="malzeme">${malzeme}</span>`)
        .join(" ");

      const ekstraMalzemeHTML = geriKalanMalzemeler.length > 0
        ? `<span class="ekstra-malzemeler" style="cursor:pointer;" data-index="${globalIndex}">+${geriKalanMalzemeler.length} daha</span>`
        : "";

      const favClass = tarif.favori ? "fa-solid" : "fa-regular";

      const slug = tarif.isim.toLowerCase().replaceAll(" ", "-").replaceAll("ı", "i").replaceAll("ç", "c").replaceAll("ş", "s").replaceAll("ğ", "g").replaceAll("ü", "u").replaceAll("ö", "o");

      const imgPath = `/static/uploads/${slug}.png`;


      const cardHTML = `
        <div class="recipe-card" data-index="${globalIndex}">
          <div class="card-top">
            <img src="${imgPath}" alt="${tarif.isim}" onerror="this.src='/static/uploads/placeholder.png'" style="width:100%; height:200px; object-fit:cover; border-radius: 12px 12px 0 0;">
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

    document.querySelectorAll(".fav-icon").forEach(icon => {
      icon.addEventListener("click", () => {
        const index = icon.dataset.index;
        tarifler[index].favori = !tarifler[index].favori;
        const heartIcon = icon.querySelector("i");
        heartIcon.classList.toggle("fa-solid");
        heartIcon.classList.toggle("fa-regular");
      });
    });

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

  document.querySelectorAll('.kategori-buttons button').forEach(button => {
    button.addEventListener('click', function () {
      document.querySelectorAll('.kategori-buttons button').forEach(btn => btn.classList.remove('active'));
      this.classList.add('active');
      seciliKategori = this.dataset.kategori;
      mevcutSayfa = 1;
      tarifleriGoster();
    });
  });

  aramaInput.addEventListener("input", () => {
    aramaKelimesi = aramaInput.value.trim();
    mevcutSayfa = 1;
    tarifleriGoster();
  });

  tarifleriYukle(); // Sayfa yüklendiğinde API'den verileri çek
});
