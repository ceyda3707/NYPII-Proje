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

document.getElementById('yumurta').addEventListener('click', function() {
    alert('Yumurta seçildi!');
});

document.getElementById('peynir').addEventListener('click', function() {
    alert('Peynir seçildi!');
});