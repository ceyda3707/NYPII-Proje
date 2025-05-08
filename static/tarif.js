document.addEventListener("DOMContentLoaded", function () {
    const tarifId = window.location.pathname.split("/").pop();

    fetch(`/api/tarif/${tarifId}`)
        .then(response => response.json())
        .then(data => {
            console.log("Gelen hazırlanış:", data.hazirlanis);
            
            // Kategori ve başlık
            document.getElementById("kategoriBaslik").textContent = data.kategori;
            document.getElementById("tarifBaslik").textContent = data.isim;

            // Detaylar
            const detaylar = document.querySelectorAll(".detay-deger");
            detaylar[0].textContent = data.hazirlik_suresi;
            detaylar[1].textContent = data.pisirme_suresi;
            detaylar[2].textContent = data.porsiyon;
            detaylar[3].textContent = data.kalori;

            // Malzemeler
            const liste = document.getElementById("malzeme-listesi");
            data.malzemeler.forEach(malzeme => {
                const li = document.createElement("li");
                li.classList.add("ingredient-item");

                const circleContainer = document.createElement("span");
                circleContainer.classList.add("circle-container");

                const checkmark = document.createElement("span");
                checkmark.classList.add("checkmark");
                checkmark.textContent = "✓";

                const text = document.createElement("span");
                text.classList.add("malzeme-text");
                text.textContent = malzeme;

                circleContainer.appendChild(checkmark);
                li.appendChild(circleContainer);
                li.appendChild(text);
                liste.appendChild(li);

    });

   

            const container = document.getElementById("hazirlanis-adimlari");

            // Veri diziyse ve içinde tek bir uzun cümle varsa:
            let adimlar = [];
            
              // Gelen veri array ise ve içinde tek bir uzun string varsa:
              if (Array.isArray(data.hazirlanis) && data.hazirlanis.length === 1 && typeof data.hazirlanis[0] === "string") {
                // Örneğin: ["1. Şunu yap. 2. Bunu yap. 3. Sonra şunu yap."]
                adimlar = data.hazirlanis[0]
                    .split(/\d+\.\s+/)                     // 1. 2. 3. ile ayır
                    .map(adim => adim.trim())               // boşlukları temizle
                    .filter(adim => adim.length > 0);       // boş olanları çıkar
            } else {
                adimlar = data.hazirlanis;
            }
            
            // DOM’a her adımı sırayla ekle
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
            
        })
        .catch(error => {
            console.error("Tarif verisi alınamadı:", error);
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
    yildizYaziElementi.textContent = "Değerlendirin";

    yildizlar.forEach((yildiz, index) => {
        yildiz.addEventListener("mouseover", function () {
            yildizlar.forEach(star => star.classList.remove('hovered'));
            yildiz.classList.add('hovered');
        });
        yildiz.addEventListener("mouseout", function () {
            yildiz.classList.remove('hovered');
        });
        yildiz.addEventListener("click", function () {
            yildizlar.forEach(star => star.classList.remove('selected'));
            for (let i = 0; i <= index; i++) {
                yildizlar[i].classList.add('selected');
            }
            yildizYaziElementi.textContent = `${yildizYazilari[index]}`;
        });
    });
});
