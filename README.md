# Zara Stock Tracker (ZST)

Zara ürün stoklarını takip eden, stok geldiğinde Telegram ve E-posta ile bildirim gönderen otomasyon sistemi.

## 🛠 Teknolojiler (Tech Stack)

Proje 3 ana parçadan oluşmaktadır:

### 1. Backend (Java)
*   **Dil:** Java 17
*   **Framework:** Spring Boot 3.4
*   **Veritabanı:** PostgreSQL
*   **Kütüphaneler:** Spring Data JPA, Java Mail Sender, TelegramBots
*   **Konum:** `/backend` klasörü

### 2. Scraper / Kazıyıcı (Python)
*   **Dil:** Python 3.10+
*   **Framework:** FastAPI (Web API arayüzü için)
*   **Araç:** Microsoft Playwright (Headless Browser)
*   **Konum:** `/scraper` klasörü

### 3. Frontend (JavaScript/React)
*   **Dil:** JavaScript (ES6+)
*   **Framework:** React 19 (Vite ile)
*   **Stil:** Tailwind CSS v3
*   **Konum:** `/frontend` klasörü

## 💻 Geliştirme İçin Önerilen IDE'ler

Projeyi geliştirmek için aşağıdaki editörleri kullanabilirsiniz:

### Önerilen: IntelliJ IDEA (Ultimate veya Community)
*   **Backend (Java/Spring)** geliştirmesi için en iyisidir.
*   Frontend ve Python pluginleri ile tüm projeyi tek yerden yönetebilirsiniz.

### Alternatif: Visual Studio Code (VS Code)
*   **Frontend (React)** ve **Scraper (Python)** için çok hafiftir ve mükemmel çalışır.
*   Java eklenti paketi (Extension Pack for Java) yükleyerek Backend'i de açabilirsiniz.
*   *Öneri:* Tüm klasörü (`C:\MyApps\ZaraStockTracker`) VS Code ile açıp geliştirebilirsiniz.

## 🚀 Yerel Çalıştırma (Local Development)

Projeyi bilgisayarınızda (Docker olmadan) tek tek çalıştırmak için:

1.  **Veritabanı:** PostgreSQL'in kurulu ve çalışıyor olması gerekir (veya Docker ile sadece db kaldırılabilir).
2.  **Scraper:**
    ```bash
    cd scraper
    pip install -r requirements.txt
    playwright install
    uvicorn main:app --reload
    ```
3.  **Backend:**
    IntelliJ IDEA ile açıp `ZaraStockTrackerApplication` sınıfını çalıştırın.
4.  **Frontend:**
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

## 🐳 Docker ile Çalıştırma (Kolay Yöntem)

Tüm sistemi tek komutla ayağa kaldırmak için:

```powershell
docker compose up -d --build
```
Bu komut veritabanını, backend'i, scraper'ı ve frontend'i otomatik kurar ve başlatır.
Web Arayüzü: `http://localhost`
