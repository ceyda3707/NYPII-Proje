document.addEventListener("DOMContentLoaded", function () {
    // Dinamik başlık yükleme
    fetch('/kategori')  // Flask route'undan veri alıyoruz
        .then(response => response.json())
        .then(data => {
            const kategoriBaslik = document.getElementById('kategoriBaslik');
            kategoriBaslik.textContent = data.kategori || "Kategori";
        })
        .catch(error => {
            console.error("Başlık yüklenemedi:", error);
        });

    // Tarif başlığı verisini al
    fetch('/tarif')
        .then(response => response.json())
        .then(data => {
            const tarifBaslik = document.getElementById('tarifBaslik');
            tarifBaslik.textContent = data.tarif || "Tarif";
        })
        .catch(error => {
            console.error("Tarif başlığı yüklenemedi:", error);
        });

    // Yıldızlı değerlendirme sistemi
    const yildizlar = document.querySelectorAll('.yildiz');
    const yildizYazilari = [
        "Beğenmedim",
        "Fena değil",
        "İyi",
        "Çok iyi",
        "Mükemmel!"
    ];
    const yildizYaziElementi = document.querySelector('.yildiz-yazi');

    // Başlangıçta yazıyı "Değerlendirin" olarak ayarla
    yildizYaziElementi.textContent = "Değerlendirin";

    yildizlar.forEach((yildiz, index) => {
        // Hover durumunda sadece o yıldızın turuncu olması
        yildiz.addEventListener("mouseover", function () {
            yildizlar.forEach(star => star.classList.remove('hovered'));
            yildiz.classList.add('hovered');
        });

        yildiz.addEventListener("mouseout", function () {
            yildiz.classList.remove('hovered');
        });

        // Tıklama durumunda yazı ve yıldızları güncelleme
        yildiz.addEventListener("click", function () {
            // Tüm yıldızlardan "selected" sınıfını kaldır
            yildizlar.forEach(star => star.classList.remove('selected'));

            // Bu yıldızla birlikte önceki yıldızlara da "selected" sınıfı ekle
            for (let i = 0; i <= index; i++) {
                yildizlar[i].classList.add('selected');
            }

            // Yazıyı değiştirme
            yildizYaziElementi.textContent = `${yildizYazilari[index]}`;
        });
    });


    const malzemeler = [
        "1 kg olgun domates",
        "2 yemek kaşığı tereyağı",
        "1 adet orta boy soğan",
        "2 diş sarımsak",
        "1 yemek kaşığı un",
        "5 su bardağı sıcak su veya et suyu",
        "1 tatlı kaşığı toz şeker",
        "Tuz ve karabiber",
        "Süslemek için krema ve kıyılmış maydanoz"
    ];
    
    const liste = document.getElementById("malzeme-listesi");
    
    malzemeler.forEach(malzeme => {
        const li = document.createElement("li");
        li.classList.add("ingredient-item"); // ingredient-item sınıfı ekleniyor
    
        // Daire kutusu
        const circleContainer = document.createElement("span");
        circleContainer.classList.add("circle-container");
    
        // Tik işareti
        const checkmark = document.createElement("span");
        checkmark.classList.add("checkmark");
        checkmark.textContent = "✓"; // Tik işaretini ekliyoruz
    
        circleContainer.appendChild(checkmark); // Tik işaretini daireye ekle
    
        // Malzeme metnini ekle
        const text = document.createElement("span");
        text.classList.add("malzeme-text");
        text.textContent = malzeme;
    
        // Liste öğesine daireyi ve metni ekle
        li.appendChild(circleContainer);
        li.appendChild(text);
    
        liste.appendChild(li);
    });
    
    const adimlar = [
        "Domatesleri yıkayın ve kabuklarını soyun. Daha sonra küp küp doğrayın.",
        "Soğanı ve sarımsağı ince ince doğrayın.",
        "Derin bir tencerede tereyağını eritin. Soğanları ekleyip pembeleşene kadar kavurun.",
        "Sarımsakları ekleyip 1 dakika daha kavurun.",
        "Unu ekleyip kokusu çıkana kadar karıştırarak kavurun.",
        "Doğranmış domatesleri ekleyin ve 5 dakika kadar pişirin.",
        "Tuz ve karabiberle tatlandırın.",
        "Üzerine su ekleyin, kaynamaya bırakın.",
        "Çorba kıvamına gelene kadar kısık ateşte pişirin.",
        "Blender ile pürüzsüz hale getirin ve sıcak servis yapın."
      ];
    
      const container = document.getElementById("hazirlanis-adimlari");
    
      adimlar.forEach((adim, index) => {
        const li = document.createElement("li");
        li.className = "hazirlanis-adimi";
    
        const numara = document.createElement("span");
        numara.className = "hazirlanis-numara";
        numara.textContent = index + 1;
    
        const metin = document.createElement("p");
        metin.className = "hazirlanis-metin";
        metin.textContent = adim;
    
        li.appendChild(numara);
        li.appendChild(metin);
        container.appendChild(li);
      });
    
    
      
});