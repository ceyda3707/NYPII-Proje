document.addEventListener("DOMContentLoaded", () => {
  const tarifler = [
    {
      kategori: "Tatlılar",
      isim: "Çikolatalı Brownie",
      hazirlik: "15 dk",
      pisirme: "25 dk",
      malzemeler: ["Bitter Çikolata", "Tereyağı", "Un", "Şeker"],
      puan: 4.9,
      favori: false // Favori durumu
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
  ];

  const container = document.getElementById("tarifler-container");
  const aramaInput = document.getElementById("aramaInput");
  let seciliKategori = "Hepsi";
  let aramaKelimesi = "";

  function tarifleriGoster() {
    container.innerHTML = "";

    const filtreliTarifler = tarifler.filter(t => {
      const kategoriEslesme = seciliKategori === "Hepsi" || t.kategori === seciliKategori;
      const isimEslesme = t.isim.toLowerCase().includes(aramaKelimesi.toLowerCase());
      return kategoriEslesme && isimEslesme;
    });

      // Favori boş mesajını göster/gizle
  const favoriBosDiv = document.querySelector("#favoriBosMesaji .favori-bos");
  if (filtreliTarifler.length === 0) {
    favoriBosDiv.style.display = "block";
  } else {
    favoriBosDiv.style.display = "none";
  }

    if (filtreliTarifler.length === 0) {
      container.innerHTML = "<p>Uygun tarif bulunamadı.</p>";
      return;
    }

    filtreliTarifler.forEach(tarif => {
      const ilkUcMalzeme = tarif.malzemeler.slice(0, 3);
      const geriKalanMalzemeler = tarif.malzemeler.slice(3);
      const malzemelerHTML = ilkUcMalzeme
        .map(malzeme => `<span class="malzeme">${malzeme}</span>`)
        .join(" ");
        
      let ekstraMalzemeler = '';
      if (geriKalanMalzemeler.length > 0) {
        ekstraMalzemeler = `<span class="ekstra-malzemeler" style="cursor:pointer;">+${geriKalanMalzemeler.length} daha</span>`;
      }

      const cardHTML = `
        <div class="recipe-card">
          <div class="card-top">
            <div class="fav-icon" data-index="${tarifler.indexOf(tarif)}">
              <i class="fa-solid fa-heart"></i>
            </div>
          </div>
          <div class="card-content">
            <span class="difficulty">${tarif.kategori}</span>
            <h3>${tarif.isim}</h3>
            <div class="süre-bilgi">
              <span class="hazirlik"><i class="fa-solid fa-clock"></i> Hazırlık: ${tarif.hazirlik}</span>
              <span class="pisirme"><i class="fa-solid fa-fire"></i> Pişirme: ${tarif.pisirme}</span>
            </div>
            <p>${malzemelerHTML} ${ekstraMalzemeler}</p>
            <div class="card-footer">
              <span>${tarif.malzemeler.length} malzeme</span>
              <a href="#">Tarifi Gör →</a>
            </div>
          </div>
        </div>
      `;
      container.insertAdjacentHTML("beforeend", cardHTML);

      // "+X daha" tıklama olayını dinleyin
      const ekstraMalzemeLinki = container.querySelectorAll('.ekstra-malzemeler');
      ekstraMalzemeLinki.forEach((ekstraLink, index) => {
        if (geriKalanMalzemeler.length > 0) {
          ekstraLink.addEventListener('click', () => {
            const ekstraMalzemelerHTML = geriKalanMalzemeler
              .map(malzeme => `<span class="malzeme">${malzeme}</span>`)
              .join(" ");
            
            ekstraLink.style.display = 'none';
            const malzemeP = ekstraLink.parentElement;
            malzemeP.innerHTML += ` ${ekstraMalzemelerHTML}`;
            malzemeP.parentElement.style.height = 'auto';
          });
        }
      });
    });

    // Favori ikonuna tıklama işlevi ekleyin
    const favIcons = document.querySelectorAll(".fav-icon");
    favIcons.forEach(icon => {
      icon.addEventListener("click", () => {
        const index = icon.dataset.index;

        // Favori olan tarifi sil
        tarifler.splice(index, 1); // Favori tarif siliniyor
        tarifleriGoster(); // Tarifleri tekrar göster
      });
    });
  }

  // Sayfa yüklendiğinde tüm tarifleri göster
  tarifleriGoster();

  // Kategori butonlarını dinle
  document.querySelectorAll('.kategori-buttons button').forEach(button => {
    button.addEventListener('click', function () {
      document.querySelectorAll('.kategori-buttons button').forEach(btn => btn.classList.remove('active'));
      this.classList.add('active');
      seciliKategori = this.dataset.kategori;
      tarifleriGoster();
    });
  });

  // Arama kutusunu dinle
  aramaInput.addEventListener("input", () => {
    aramaKelimesi = aramaInput.value.trim();
    tarifleriGoster();
  });

  




});
