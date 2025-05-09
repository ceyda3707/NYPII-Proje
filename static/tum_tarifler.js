document.addEventListener("DOMContentLoaded", () => {
  const tarifler = [];
  const container = document.getElementById("tarifler-container");
  const aramaInput = document.getElementById("aramaInput");
  const sayfalamaContainer = document.getElementById("sayfalama");
  let seciliKategori = "Hepsi";
  let aramaKelimesi = "";
  let mevcutSayfa = 1;
  const tarifSayisiBirSayfada = 20;

  // Flask API'den tarifleri çekme
  function fetchTarifler() {
    fetch('/tarifler')
      .then(response => response.json())
      .then(data => {
        tarifler.length = 0; // Eski tarifleri temizle
        tarifler.push(...data.tarifler); // Yeni tarifleri ekle
        tarifleriGoster(); // Tarifleri ekranda göster
      })
      .catch(error => {
        console.error('Hata:', error);
        container.innerHTML = "<p>Veriler alınırken bir hata oluştu.</p>";
      });
  }

  // Tarifleri filtrele ve sayfalama yap
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

    goruntulenecekTarifler.forEach(tarif => {
      const malzemelerHTML = tarif.malzemeler.slice(0, 3)
        .map(malzeme => `<span class="malzeme">${malzeme}</span>`)
        .join(" ");

      const ekstraMalzemeHTML = tarif.malzemeler.length > 3
        ? `<span class="ekstra-malzemeler" style="cursor:pointer;">+${tarif.malzemeler.length - 3} daha</span>`
        : "";

      const favClass = tarif.favori ? "fa-solid" : "fa-regular";

      const cardHTML = `
        <div class="recipe-card">
          <div class="card-top">
            <div class="fav-icon">
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

    // Sayfa numaralarını ekle
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

  fetchTarifler(); // Sayfa yüklendiğinde tarifleri çek

  // Kategori ve arama işlemleri
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
});
