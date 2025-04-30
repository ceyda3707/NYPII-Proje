// Emoji listesi
const emojiListesi = {
    "Domates": "🍅",
    "Biber": "🌶️",
    "Sarımsak": "🧄",
    "Soğan": "🧅",
    // Diğer malzemeler ve emojiler...  // !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
};

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