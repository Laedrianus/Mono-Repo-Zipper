TR & EN

# MonoRepoZipper

A modern web tool to bundle multiple code files into a ZIP archive while preserving folder structure. Ideal for developers who work with multiple languages and need fast, organized packaging.

---

## 🌐 Features / Özellikler

**English:**
- Paste or upload multiple code files
- Preview file structure before download
- Lint and check syntax for:
  - TypeScript & React/Next.js
  - Solidity
  - Rust
  - WebAssembly
  - Nix
- Generate ZIP with nested folders according to file paths
- Dark / Light mode toggle
- Modern and responsive UI
- Optional code formatting/beautifier
- Detailed per-file error/warning/info report
- Starter presets for common frameworks and languages

**Türkçe:**
- Birden çok kod dosyasını yapıştır veya yükle
- İndirmeden önce dosya yapısını önizle
- Kodları kontrol et ve lint uygula:
  - TypeScript & React/Next.js
  - Solidity
  - Rust
  - WebAssembly
  - Nix
- Dosya yollarına göre ZIP içinde klasör yapısı oluştur
- Koyu / Açık tema seçeneği
- Modern ve responsive arayüz
- Opsiyonel kod formatlama
- Dosya başına detaylı hata/uyarı/bilgi raporu
- Hazır starter presetler ile hızlı başlama

---

## 🚀 Installation / Kurulum

**English:**

1. Clone the repository:
```bash
git clone https://github.com/Laedrianus/Mono-Repo-Zipper.git
cd Mono-Repo-Zipper
Set up Python virtual environment:


python -m venv venv
# Windows
venv\Scripts\activate
# Linux / Mac
source venv/bin/activate
Install dependencies:


pip install -r requirements.txt
Run the app:

python app.py
Türkçe:

Repo’yu klonla:

git clone https://github.com/Laedrianus/Mono-Repo-Zipper.git
cd Mono-Repo-Zipper
Python sanal ortamını kur:

python -m venv venv
# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
Gerekli paketleri yükle:


pip install -r requirements.txt
Uygulamayı çalıştır:


python app.py
🖥️ Usage / Kullanım
English:

Open your browser and navigate to the local URL (usually http://127.0.0.1:5000).

Paste or upload code files.

Preview the file structure.

Run lint checks on individual files.

Click Generate ZIP to prepare the archive.

Use the Download button to save the ZIP manually.

Türkçe:

Tarayıcını aç ve uygulamanın yerel URL’sine git (genellikle http://127.0.0.1:5000).

Kod dosyalarını yapıştır veya yükle.

Dosya yapısını önizle.

Her dosya için lint kontrolü yap.

Generate ZIP butonuna basarak arşivi hazırla.

Download butonunu kullanarak ZIP’i kaydet.

🌟 Demo / Canlı Örnek
Replit (Python backend demo):
https://replit.com/@username/MonoRepoZipper

💻 Supported Languages / Desteklenen Diller
TypeScript

React/Next.js

Solidity

Rust

WebAssembly

Nix

📂 Folder Structure / Klasör Yapısı
vbnet

MonoRepoZipper/
├─ app.py
├─ requirements.txt
├─ components/
│  ├─ FileList.tsx
│  └─ ResultView.tsx
├─ lib/
│  ├─ types.ts
│  ├─ repoStore.ts
│  └─ linters/
└─ ...
⚙️ Configuration / Konfigürasyon
Light / Dark theme toggle available in UI.

ZIP folder structure respects file paths.

Starter presets can be configured in lib/presets.ts.

🔧 Contributing / Katkıda Bulunma
English:

Fork the repo

Create a branch for your feature

Make changes and test

Submit a pull request

Türkçe:

Repo’yu forkla

Özelliğin için bir branch oluştur

Değişiklikleri yap ve test et

Pull request gönder

📄 License / Lisans
MIT License.
