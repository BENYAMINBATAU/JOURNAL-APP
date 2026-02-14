# BENYAMIN BATAU JOURNAL APP

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

**Aplikasi Powerful untuk Mengkonversi Tesis menjadi Artikel Jurnal Berkualitas Tinggi**

Dikembangkan oleh **Benyamin Batau** untuk memudahkan mahasiswa dan peneliti dalam mengubah tesis menjadi artikel jurnal yang siap dipublikasikan, dengan bantuan AI (Claude & GPT-4).

## 🌟 Fitur Utama

### 1. **AI-Powered Enhancement**
- ✅ Automatic abstract improvement (English & Indonesian)
- ✅ Keyword generation otomatis
- ✅ Section summarization
- ✅ Content optimization
- ✅ Support Claude (Anthropic) dan GPT-4 (OpenAI)

### 2. **Multi-Format Support**
- 📄 Input: PDF, DOCX, DOC
- 📝 Output: DOCX (Word), PDF
- 🎯 Template: Universitas Negeri Makassar (UNM)

### 3. **Advanced Document Processing**
- 🔍 Smart content extraction
- 📚 Automatic chapter detection
- 📖 Reference management (APA format)
- 🏷️ Metadata extraction
- 🎨 Professional formatting

### 4. **User-Friendly Interface**
- 🖱️ Drag & drop file upload
- 📊 Real-time progress tracking
- 👁️ Preview before download
- 📱 Responsive design
- ⚡ Fast processing

## 🚀 Quick Start

### Instalasi

```bash
# Clone repository
git clone https://github.com/benyaminbatau/journal-app.git
cd journal-app

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env dan tambahkan API keys
```

### Konfigurasi Environment Variables

Buat file `.env` di root directory:

```env
# API Keys (Optional - untuk fitur AI)
ANTHROPIC_API_KEY=your_claude_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Flask Configuration
SECRET_KEY=your_secret_key_here
FLASK_ENV=development

# File Upload Configuration
MAX_FILE_SIZE=52428800  # 50MB in bytes
UPLOAD_FOLDER=uploads
OUTPUT_FOLDER=outputs
```

### Menjalankan Aplikasi

```bash
# Development mode
python app.py

# Production mode (menggunakan Gunicorn)
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Buka browser dan akses: `http://localhost:5000`

## 📖 Cara Penggunaan

### 1. Upload File Tesis

Upload file-file berikut (dalam format PDF atau DOCX):
- ✅ Sampul/Cover
- ✅ BAB I (Pendahuluan)
- ✅ BAB II (Kajian Pustaka)
- ✅ BAB III (Metode Penelitian)
- ✅ BAB IV (Hasil dan Pembahasan)
- ✅ BAB V (Kesimpulan)
- ✅ Daftar Pustaka

> **Tips**: Beri nama file dengan jelas, misalnya: `BAB_I.docx`, `BAB_II.pdf`, `DAFTAR_PUSTAKA.docx`

### 2. Isi Informasi Penulis

- **Nama Penulis**: Nama lengkap penulis utama
- **Co-Authors**: Nama penulis kedua, ketiga (opsional)
- **Afiliasi**: Program Studi dan Universitas
- **Email**: Email korespondensi

### 3. Pilih Pengaturan

- **Output Format**: DOCX atau PDF
- **AI Provider**: Claude (recommended) atau GPT-4
- **Min. References**: Jumlah minimal referensi (default: 15)
- **AI Enhancement**: Aktifkan untuk kualitas terbaik
- **Include Abstract**: Sertakan abstract dalam 2 bahasa

### 4. Generate & Download

Klik tombol **"Generate Artikel Jurnal"** dan tunggu proses selesai (biasanya 1-3 menit).

## 🏗️ Arsitektur Aplikasi

```
benyamin_journal_app/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── README.md                   # Documentation
│
├── utils/                      # Core modules
│   ├── __init__.py
│   ├── document_processor.py  # Extract content from PDF/DOCX
│   ├── ai_processor.py        # AI enhancement (Claude/GPT-4)
│   ├── journal_generator.py   # Generate journal article
│   └── reference_manager.py   # Format & validate references
│
├── templates/                  # HTML templates
│   └── index.html             # Main interface
│
├── static/                     # Static assets
│   ├── js/
│   │   └── app.js             # Frontend JavaScript
│   └── css/
│       └── style.css          # Custom styles
│
├── uploads/                    # Uploaded files (gitignored)
└── outputs/                    # Generated articles (gitignored)
```

## 🔧 Advanced Features

### 1. Reference Management

Aplikasi secara otomatis:
- ✅ Memformat referensi ke APA style
- ✅ Validasi tahun publikasi (minimal 10 tahun terakhir)
- ✅ Memastikan minimal 80% dari jurnal
- ✅ Mengurutkan alfabetis
- ✅ Menghapus duplikasi

### 2. AI Enhancement Options

#### Claude (Anthropic) - Recommended
- Model: `claude-sonnet-4-20250514`
- Keunggulan: Lebih akurat untuk konten akademik
- Kecepatan: Moderate
- Cost: Moderate

#### GPT-4 (OpenAI)
- Model: `gpt-4-turbo-preview`
- Keunggulan: Lebih cepat
- Kecepatan: Fast
- Cost: Higher

### 3. Template Customization

Saat ini mendukung template UNM dengan format:
- ✅ A4, 2 kolom
- ✅ Times New Roman 11pt
- ✅ Margin: Top 3cm, Others 2.5cm
- ✅ Single spacing
- ✅ APA reference format

## 📊 API Endpoints

### POST `/upload`
Upload dan proses file tesis

**Request:**
```javascript
FormData:
  - files[]: Multiple files
  - author_name: string
  - affiliation: string
  - email: string
  - output_format: 'docx' | 'pdf'
  - ai_provider: 'claude' | 'gpt4'
  - use_ai: boolean
```

**Response:**
```json
{
  "success": true,
  "message": "Artikel jurnal berhasil dibuat!",
  "filename": "artikel_jurnal_20260214_123456.docx",
  "download_url": "/download",
  "preview_data": {
    "title": "...",
    "abstract": "...",
    "word_count": 3500,
    "reference_count": 18
  }
}
```

### GET `/download`
Download generated journal article

### POST `/api/enhance-abstract`
Enhance abstract using AI

### POST `/api/check-references`
Validate references

### GET `/health`
Health check endpoint

## 🐛 Troubleshooting

### Error: "ANTHROPIC_API_KEY not set"
**Solusi**: Tambahkan API key di file `.env` atau disable AI enhancement

### Error: "File too large"
**Solusi**: Compress PDF atau pecah file menjadi beberapa bagian

### Error: "Invalid file format"
**Solusi**: Pastikan file dalam format PDF, DOCX, atau DOC

### Proses terlalu lama
**Solusi**: 
- Reduce file size
- Disable AI enhancement
- Check internet connection

## 🔒 Security

- ✅ File size validation (max 50MB)
- ✅ File type validation
- ✅ Secure filename handling
- ✅ Session-based file storage
- ✅ Auto cleanup temporary files
- ⚠️ **Note**: Jangan upload data sensitif atau rahasia

## 📈 Performance

- Average processing time: 1-3 minutes
- Supported file size: up to 50MB
- Concurrent users: up to 10 (adjust gunicorn workers)
- Memory usage: ~500MB per process

## 🤝 Contributing

Kontribusi sangat diterima! Silakan:

1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Developer

**Benyamin Batau**
- Email: benyamin.batau@example.com
- GitHub: [@benyaminbatau](https://github.com/benyaminbatau)
- LinkedIn: [Benyamin Batau](https://linkedin.com/in/benyaminbatau)

## 🙏 Acknowledgments

- Universitas Negeri Makassar untuk template jurnal
- Anthropic (Claude AI)
- OpenAI (GPT-4)
- Flask Framework
- All contributors and users

## 📞 Support

Jika menemukan bug atau ingin request fitur:
- 🐛 [Report Bug](https://github.com/benyaminbatau/journal-app/issues)
- 💡 [Request Feature](https://github.com/benyaminbatau/journal-app/issues)
- 📧 Email: benyamin.batau@example.com

---

**Made with ❤️ by Benyamin Batau | © 2026**
