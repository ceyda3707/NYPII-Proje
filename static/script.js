// Emoji listesi
const emojiListesi = {
        "Domates": "🍅",
        "Biber": "🌶",
        "Sarımsak": "🧄",
        "Soğan": "🧅",
        "Havuç": "🥕",
        "Patates": "🥔",
        "Patlıcan": "🍆",
        "Kabak": "🥒",
        "Fasulye": "🫘",
        "Mısır": "🌽",
        "Lahana": "🥬",
        "Ispanak": "🍃",
        "Kuşkonmaz": "🌱",
        "Brüksel Lahanası": "🥦",
        "Pırasa": "🥬",
        "Karnabahar": "🥦",
        "Brokoli": "🥦",
        "Zeytinyağı": "🫒",
        "Süt": "🥛",
        "Yumurta": "🥚",
        "Un": "🌾",
        "Şeker": "🍬",
        "Tuz": "🧂",
        "Karabiber": "🧂",
        "Kimyon": "🌿",
        "Zerdeçal": "🌕",
        "Kişniş": "🌿",
        "Pul Biber": "🌶",
        "Paprika": "🌶",
        "Tarçın": "🟤",
        "Yenibahar": "🟤",
        "Vanilya Özütü": "🌼",
        "Defne Yaprağı": "🍃",
        "Kekik": "🌿",
        "Rosemary": "🌿",
        "Adaçayı": "🌿",
        "Kakao": "🍫",
        "Fesleğen": "🌿",
        "Çikolata": "🍫",
        "Beyaz Peynir": "🧀",
        "Mozzarella": "🧀",
        "Cheddar": "🧀",
        "Süzme Yoğurt": "🥣",
        "Ricotta": "🧀",
        "Fıstık Ezmesi": "🥜",
        "Bal": "🍯",
        "Beyaz Ekmek": "🍞",
        "Çavdar Ekmeği": "🍞",
        "Baget": "🥖",
        "Tortilla": "🌮",
        "Pizza Hamuru": "🍕",
        "Pide": "🥙",
        "Simit": "🥯",
        "Kruvasan": "🥐",
        "Poğaça": "🥐",
        "Kek": "🍰",
        "Çörek": "🍞",
        "Pasta": "🍰",
        "Kurabiye": "🍪",
        "Bisküvi": "🍪",
        "Dondurma": "🍦",
        "Çörek": "🍩",
        "Donut": "🍩",
        "Meyve": "🍎",
        "Elma": "🍎",
        "Armut": "🍐",
        "Portakal": "🍊",
        "Muz": "🍌",
        "Üzüm": "🍇",
        "Karpuz": "🍉",
        "Kavun": "🍈",
        "Kiraz": "🍒",
        "Ananas": "🍍",
        "Şeftali": "🍑",
        "Limon": "🍋",
        "Nar": "🍊",
        "Erik": "🍑",
        "Kayısı": "🍑",
        "Yaban Mersini": "🫐",
        "Ceviz": "🌰",
        "Fındık": "🌰",
        "Badem": "🌰",
        "Fıstık": "🥜",
        "Ceviz": "🌰",
        "Kaju": "🥜",
        "Kurutulmuş Meyve": "🍒",
        "Yaban Mersini": "🫐",
        "Karpuz Tohumu": "🌱",
        "Limon Suyu": "🍋",
        "Portakal Suyu": "🍊",
        "Elma Suyu": "🍏",
        "Yaban Mersini Suyu": "🫐",
        "Vişne Suyu": "🍒",
        "Şarap": "🍷",
        "Bira": "🍺",
        "Soda": "🥤",
        "Limonata": "🍋",
        "Su": "💧",
        "Meyve Suyu": "🍊",
        "Zeytin": "🫒",
        "Zeytin Yağı": "🫒",
        "Hindistancevizi Sütü": "🥥",
        "Brokoli Çiçeği": "🥦",
        "Ayçiçek Yağı": "🌻",
        "Margarine": "🧈",
        "Terbiyeli Yoğurt": "🥣",
        "Fırın Tavuk": "🍗",
        "Tavuk Göğsü": "🍗",
        "Izgara Et": "🥩",
        "Köfte": "🍖",
        "Dana Eti": "🥩",
        "Kuzu Eti": "🥩",
        "Balık": "🐟",
        "Somon": "🐟",
        "Ton Balığı": "🐟",
        "Midye": "🦪",
        "Karides": "🦐",
        "Yengeç": "🦀",
        "İstiridye": "🦪",
        "Fıstık Ezmesi": "🥜",
        "Kekik Yağı": "🌿",
        "Vegan Burger": "🍔",
        "Vejetaryen Pizza": "🍕",
        "Kavurma": "🥩",
        "Sütlü Kahve": "☕",
        "Türk Kahvesi": "☕",
        "Sıcak Çikolata": "☕",
        "Kumpir": "🍠",
        "Sosis": "🌭",
        "Tereyağı": "🧈",
        "Yulaf": "🌾",
        "Beyaz Şarap": "🍷",
        "Şampanya": "🍾",
        "Vişne": "🍒",
        "Avokado": "🥑",
        "Karpuz": "🍉",
        "Mango": "🥭",
        "İncir": "🍈",
        "Zencefil": "🧄",
        "Lavanta": "💜",
        "Çam Fıstığı": "🌰"
};

let secilenKategori = "Tümü"; // Varsayılan

document.querySelectorAll('.kategori-btn').forEach(btn => {
  btn.addEventListener('click', function() {
    document.querySelectorAll('.kategori-btn').forEach(b => b.classList.remove('active'));
    this.classList.add('active');
    secilenKategori = this.dataset.kategori;
  });
});


// Malzeme butonlarına tıklayınca seçilen malzemeyi ekler
document.querySelectorAll('.malzeme-listesi button').forEach(button => {
    button.addEventListener('click', function() {
        const malzemeAdi = this.innerText;
        malzemeEkle(malzemeAdi);
    });
});

// "Ekle" butonuna basınca inputtan malzeme ekler
document.querySelector('.ekle-btn').addEventListener('click', function() {
    const input = document.querySelector('.malzeme-ekle input');
    const yeniMalzeme = input.value.trim();

    if (yeniMalzeme !== '') {
        // Girdiği malzemenin baş harfini büyük yapıyoruz, diğerlerini küçük yapıyoruz
        const formatlanmisMalzeme = capitalizeFirstLetter(yeniMalzeme);

        // Emojiyi bul (varsa)
        const emoji = emojiListesi[formatlanmisMalzeme] || "📝"; // Emoji yoksa varsayılan emoji ekle
        malzemeEkle(formatlanmisMalzeme, emoji);
        input.value = ''; // Input'u temizle
    }
});

// Baş harfi büyük, geri kalan harfleri küçük yapma fonksiyonu
function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
}

// Malzeme ekleyen fonksiyon
function malzemeEkle(malzemeAdi, emoji = "") {
    const secilenListesi = document.getElementById('secilen-malzemeler');

    // Aynı malzeme iki kere eklenmesin
    const mevcutMalzeme = Array.from(secilenListesi.children).find(span => 
        span.querySelector('span') && span.querySelector('span').innerText.includes(malzemeAdi)
    );

    if (!mevcutMalzeme) {
        const secilen = document.createElement('div');
        secilen.classList.add('secilen');

        // Emojiyi malzeme adının başına ekliyoruz
        secilen.innerHTML = `
            <span>${emoji} ${malzemeAdi}</span>
            <button class="kapat">&times;</button>
        `;

        secilen.querySelector('.kapat').addEventListener('click', function() {
            secilen.remove();
        });

        secilenListesi.appendChild(secilen);
    }
}



document.addEventListener("DOMContentLoaded", function () {
    const buton = document.getElementById("tarif-bul-btn");
    const tarifListesi = document.getElementById("tarif-listesi");
    const tariflerBolumu = document.getElementById("tarifler");
  
    buton.addEventListener("click", function () {
      const secilenler = document.querySelectorAll('#secilen-malzemeler .secilen span');
      const malzemeler = Array.from(secilenler).map(m =>
        m.innerText.replace(/^[^a-zA-ZçğıöşüÇĞİÖŞÜ]*\s*/, '').trim()
      );
  
      fetch(`/api/tarifler?malzemeler=${malzemeler.join(',')}&kategori=${secilenKategori}`)

        .then(r => r.json())
        .then(tarifler => {
          const unique = new Map(); // 🔥 Tarifleri ID'ye göre sakla
          tarifler.forEach(t => {
              const key = t.isim.toLowerCase().trim();
              if (!unique.has(key)) {
                unique.set(key, t);
      }
          });
  
          tarifListesi.innerHTML = '';
          unique.forEach(tarif => {
            const card = document.createElement('div');
            card.classList.add('tarif-card');
            
            card.innerHTML = `
             <div class="card-top">
                 <img src="${tarif.resim && tarif.resim.length > 5 ? tarif.resim : '/static/placeholder.png'}" alt="${tarif.isim}" class="dinamik-gorsel">



                  <div class="plus">+</div>
                  <div class="time-badge">${tarif.hazirlama_suresi || '30 dk'}</div>
                  <div class="favorite-btn">♡</div>
              </div>
              <div class="card-content">
                 <div class="card-header-alt">
                  <span class="difficulty">${tarif.kategori || 'Genel'}</span>
                  <div class="favorite-btn">♡</div>
                </div>

                  <h3>${tarif.isim}</h3>
                  <p>${tarif.malzemeler ? tarif.malzemeler.split(',').length : 0} malzeme</p>
                  <div class="card-footer">
                      <span>${tarif.bolge || 'Bilinmiyor'}</span>
                      <a href="/tarif/${tarif.id || 1}">Tarifi Gör →</a>
                  </div>
              </div>
              <div class="rating">⭐ 4.8</div>
            `;
            const favBtn = card.querySelector('.favorite-btn');
            favBtn.addEventListener('click', function () {
                  favBtn.classList.toggle('active');
                  favBtn.innerText = favBtn.classList.contains('active') ? '❤️' : '♡';
});

            tarifListesi.appendChild(card);
          });
  
          tariflerBolumu.style.display = 'block';
        })
        .catch(error => {
                console.error("Tarifleri alırken hata:", error);
            });
    });
  });
  