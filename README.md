# ⚡️ BLACKMARCH SUPPORT BOT ⚡️
> **The Ultimate Command Center for BlackMarch Digital Community.**

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white)
![Pyrogram](https://img.shields.io/badge/Framework-Pyrogram-red?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

Sistem asisten otomatis terintegrasi yang dirancang khusus untuk stabilitas, kecepatan, dan fungsionalitas tinggi di platform Telegram. Dibangun dengan logika **Natural Mode** untuk interaksi yang lebih manusiawi.

---

## 🛠 CORE FEATURES

### 🧠 Advanced AI Integration
Menggunakan model **Llama 3.1** melalui Groq API. Respon cepat, profesional, dan bebas dari emoji yang tidak perlu (Strict Mode).

### 📋 Precision Attendance System
Sistem absensi terpisah untuk grup dan personal dengan pencatatan database JSON yang akurat.
* **Auto-Reset**: Reset otomatis setiap hari.
* **Rekapitulasi**: Menghitung total kehadiran setiap anggota secara real-time.

### 🔢 Integrated Smart Calculator
Fitur perhitungan matematika instan langsung di kolom chat. Mendukung format angka besar dan operasi logika kompleks.

### 📢 High-Level Tagging
Sistem pemanggilan anggota grup yang cerdas.
* **UTAG**: Tag seluruh anggota grup.
* **ATAG**: Khusus memanggil jajaran Administrator.
* **Cancel Support**: Fitur pembatalan tag instan jika terjadi kesalahan.

---

## 🚀 INFRASTRUCTURE
* **Engine**: Pyrogram V2.
* **Database**: JSON-based local storage.
* **Stability**: Handled Non-Text Media (Stickers/Photos) to prevent system crashes.
* **Deployment**: Optimized for Termux & Google Cloud (E2-Micro).

---

## 💻 INSTALLATION

```bash
# Clone the repository
git clone [https://github.com/SenseiRay/bot-blackmarch](https://github.com/SenseiRay/bot-blackmarch)

# Enter the directory
cd bot-blackmarch

# Install dependencies
pip install -r requirements.txt

# Run the command center
python bot.py
