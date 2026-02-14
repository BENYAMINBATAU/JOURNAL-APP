# 🚀 Quick Start Guide - BENYAMIN BATAU JOURNAL APP

Panduan cepat untuk menjalankan aplikasi dalam 5 menit!

## ⚡ Super Quick Start (Recommended)

```bash
# 1. Clone repository
git clone https://github.com/benyaminbatau/journal-app.git
cd journal-app

# 2. Jalankan script otomatis
chmod +x run.sh
./run.sh

# 3. Buka browser
# http://localhost:5000
```

Selesai! Aplikasi sudah berjalan. 🎉

---

## 📝 Manual Setup (Jika run.sh tidak bekerja)

### Step 1: Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# Di Linux/Mac:
source venv/bin/activate
# Di Windows:
venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### Step 2: Setup Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env file (optional - untuk AI features)
nano .env  # atau gunakan editor favorit
```

Tambahkan API keys (opsional):
```env
ANTHROPIC_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-xxxxx
```

### Step 3: Run Application

```bash
python app.py
```

### Step 4: Open Browser

Navigate to: **http://localhost:5000**

---

## 🎯 First Time Usage

### 1. Prepare Your Thesis Files

Siapkan file-file berikut (PDF atau DOCX):
- ✅ `SAMPUL.docx` - Cover page dengan judul dan nama
- ✅ `BAB_I.docx` - Pendahuluan
- ✅ `BAB_II.docx` - Kajian Pustaka
- ✅ `BAB_III.docx` - Metode Penelitian
- ✅ `BAB_IV.docx` - Hasil dan Pembahasan
- ✅ `BAB_V.docx` - Kesimpulan
- ✅ `DAFTAR_PUSTAKA.docx` - References

### 2. Upload Files

- Drag & drop semua file ke area upload
- Atau klik untuk browse dan pilih file

### 3. Fill Author Information

```
Nama Penulis: Ahmad Akbar
Co-Authors: Penulis Kedua², Penulis Ketiga³
Afiliasi: Pendidikan Teknologi Kejuruan, Universitas Negeri Makassar
Email: ahmad@example.com
```

### 4. Configure Settings

**Recommended Settings:**
- ✅ Output Format: DOCX
- ✅ AI Provider: Claude (Anthropic)
- ✅ Min References: 15
- ✅ Use AI Enhancement: Checked
- ✅ Include Abstract: Checked

### 5. Generate & Download

Click **"Generate Artikel Jurnal"** → Wait 1-3 minutes → Download!

---

## 🎨 Advanced Options

### Disable AI (Faster Processing)

Jika tidak punya API key atau ingin processing lebih cepat:
- Uncheck **"Gunakan AI Enhancement"**
- Proses akan lebih cepat tapi tanpa AI optimization

### Custom Reference Count

Default: 15 referensi
- Bisa diubah 10-50 referensi
- Aplikasi akan filter dan format otomatis

### PDF Output

Saat ini DOCX lebih stabil.
PDF output masih dalam pengembangan.

---

## 🔧 Common Issues & Solutions

### Issue 1: "Module not found"
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

### Issue 2: "Port already in use"
```bash
# Solution: Change port
export PORT=5001
python app.py
```

### Issue 3: "AI features not working"
```bash
# Solution: Add API keys to .env
ANTHROPIC_API_KEY=your_key_here
```

### Issue 4: "Upload failed"
- Check file size < 50MB
- Check file format (PDF, DOCX, DOC only)
- Try converting to PDF if DOCX fails

---

## 📚 Example Files Structure

```
thesis-files/
├── SAMPUL_DEPAN.docx
├── BAB_I_PENDAHULUAN.docx
├── BAB_II_KAJIAN_PUSTAKA.docx
├── BAB_III_METODE.docx
├── BAB_IV_HASIL.docx
├── BAB_V_KESIMPULAN.docx
└── DAFTAR_PUSTAKA.docx
```

**Tips:** 
- Gunakan nama file yang jelas
- Pisahkan per bab untuk hasil optimal
- Format: Times New Roman, 12pt

---

## 🎓 Sample Output

**Input:** Tesis 100 halaman (7 files)
**Processing Time:** 2-3 minutes
**Output:** Artikel jurnal 10-15 halaman
**Format:** UNM Template (A4, 2 columns, Times New Roman 11pt)
**References:** Auto-formatted APA style

---

## 🚀 Next Steps

After generating your first article:

1. **Review Output** - Check formatting and content
2. **Manual Edits** - Fine-tune as needed
3. **Add Figures/Tables** - Insert from original thesis
4. **Proofread** - Check grammar and flow
5. **Submit!** - Ready for journal submission

---

## 💡 Pro Tips

### Tip 1: File Naming
✅ Use: `BAB_I.docx`, `BAB_II.docx`
❌ Avoid: `Chapter1.docx`, `bab1.docx`

### Tip 2: Content Quality
- Pastikan abstract jelas dan lengkap
- Referensi minimal 15, lebih dari 80% dari jurnal
- Tahun publikasi referensi < 10 tahun

### Tip 3: AI Enhancement
- Claude: Better for academic Indonesian text
- GPT-4: Faster processing
- No AI: Fastest but basic formatting only

### Tip 4: Multiple Attempts
- Try different AI providers
- Adjust reference count
- Re-upload if results not satisfactory

---

## 📞 Need Help?

- 📖 Full Documentation: [README.md](README.md)
- 🚀 Deployment Guide: [DEPLOYMENT.md](DEPLOYMENT.md)
- 🐛 Report Bug: [GitHub Issues](https://github.com/benyaminbatau/journal-app/issues)
- 📧 Email: benyamin.batau@example.com

---

## ✨ Features Checklist

- [x] Multi-file upload (PDF, DOCX, DOC)
- [x] AI-powered abstract enhancement
- [x] Automatic keyword generation
- [x] Smart reference formatting (APA)
- [x] UNM template compliance
- [x] Real-time progress tracking
- [x] One-click download
- [x] Mobile-responsive UI

---

**Happy Converting! 🎉**

Made with ❤️ by **Benyamin Batau**
