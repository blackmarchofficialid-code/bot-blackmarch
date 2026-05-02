from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import json
import os
import asyncio
import requests

# Data Akurat Sensei Ray
API_ID = 32259933
API_HASH = "a996b57d5a6b672eee4bd2a86daead1b"
BOT_TOKEN = "8691858356:AAFKBKbEuM9AjOA5TlXPkaXNUq75eonRXk4"
GROQ_API_KEY = "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"

app = Client("blackmarch_grup", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

DB_FILE = "db_blackmarch_final.json"
cancel_utag = False

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            data = json.load(f)
            data.setdefault("grup", {"tgl": "", "harian": {}, "rekap": {}})
            data.setdefault("personal", {"tgl": "", "harian": {}, "rekap": {}})
            data.setdefault("nama_user", {})
            return data
    return {"grup": {"tgl": "", "harian": {}, "rekap": {}}, "personal": {"tgl": "", "harian": {}, "rekap": {}}, "nama_user": {}}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

# --- 1. FITUR TAG ALL ---
@app.on_message(filters.command("utag") & filters.group)
async def utag_handler(client, message):
    global cancel_utag
    cancel_utag = False
    msg_text = message.text.split(maxsplit=1)[1] if len(message.command) > 1 else "📢 Panggilan untuk semua anggota!"
    mentions, count, total_tagged = "", 0, 0
    starter = message.from_user.first_name or "Admin"
    
    async for member in client.get_chat_members(message.chat.id):
        if cancel_utag: break
        if not member.user.is_bot:
            user_name = member.user.first_name or "User"
            mentions += f"[{user_name}](tg://user?id={member.user.id}) , "
            count += 1
            total_tagged += 1
            if count >= 10:
                await client.send_message(message.chat.id, f"{msg_text}\n\n{mentions.rstrip(' , ')}")
                mentions, count = "", 0
                await asyncio.sleep(1)

    if mentions and not cancel_utag:
        await client.send_message(message.chat.id, f"{msg_text}\n\n{mentions.rstrip(' , ')}")

    status_icon = "❌ **Tag Cancelled !**" if cancel_utag else "✅ **Process Completed !**"
    report_text = f"{status_icon}\n\n👥 **Number of tagged users :** {total_tagged}\n🚫 **By :** {starter}"
    await client.send_message(message.chat.id, report_text)

@app.on_message(filters.command("cancel") & filters.group)
async def cancel_utag_handler(client, message):
    global cancel_utag
    cancel_utag = True
    await message.reply("Permintaan pembatalan tag sedang diproses...")

# --- 2. FITUR TAG ADMIN ---
@app.on_message(filters.command("atag") & filters.group)
async def atag_handler(client, message):
    msg_text = message.text.split(maxsplit=1)[1] if len(message.command) > 1 else "⚠️ Laporan untuk Admin!"
    mentions = ""
    async for member in client.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        if not member.user.is_bot:
            user_name = member.user.first_name or "Admin"
            mentions += f"[{user_name}](tg://user?id={member.user.id}) , "
    if mentions: await client.send_message(message.chat.id, f"{msg_text}\n\n{mentions.rstrip(' , ')}")

# --- 3. FITUR ABSENSI ---
@app.on_message(filters.command(["absen", "daftar"]))
async def sistem_absen_terpisah_total(client, message):
    db = load_db()
    cmd, tgl_skrg, uid = message.command[0], datetime.now().strftime("%d-%m-%Y"), str(message.from_user.id)
    nama = f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip()
    jalur = "grup" if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP] else "personal"
    db["nama_user"][uid] = nama
    if db[jalur]["tgl"] != tgl_skrg:
        db[jalur]["harian"], db[jalur]["tgl"] = {}, tgl_skrg

    if cmd == "absen":
        if uid in db[jalur]["harian"]:
            await message.reply(f"❌ **{nama}**, Anda sudah absen hari ini!")
        else:
            jam = datetime.now().strftime("%H:%M:%S")
            db[jalur]["harian"][uid], db[jalur]["rekap"][uid] = jam, db[jalur]["rekap"].get(uid, 0) + 1
            save_db(db)
            await message.reply(f"✅ **ABSEN BERHASIL**\n👤 **Nama:** {nama}\n⏰ **Waktu:** {tgl_skrg} {jam}")
    elif cmd == "daftar":
        tgl_judul = datetime.now().strftime("%d %B %Y")
        if not db[jalur]["harian"]: return await message.reply(f"📋 Daftar hadir {tgl_judul} masih kosong.")
        teks = f"📋 **Daftar Hadir {tgl_judul}**\n\n"
        for i, (u_id, jam) in enumerate(db[jalur]["harian"].items(), 1):
            disp_name = db["nama_user"].get(u_id, f"User {u_id}")
            rekap = db[jalur]["rekap"].get(u_id, 0)
            teks += f"{i}. {disp_name} [{jam}] ({rekap}x)\n"
        await message.reply(teks)

# --- 4. FITUR RULES ---
@app.on_message(filters.command("rules"))
async def rules_handler(client, message):
    teks = "˹ʙʟᴀᴄᴋᴍᴀʀᴄʜ ᴛᴇᴍᴘᴀᴛ ᴄᴀʀɪ ᴘᴀᴄᴀʀ ꜱʟᴇᴇᴘᴄᴀʟʟ ᴛᴇᴍᴇɴ ᴠɪʀᴛᴜᴀʟ˼\n\n•• ꜱᴀᴛᴜ ꜱᴀᴛᴜ ɴʏᴀ ɢᴄ ʏᴀɴɢ ʟᴜ ᴍᴀᴜ ɴɢᴀᴘᴀɪɴ ᴀᴊᴀ ʙᴇʙᴀꜱ •••"
    tombol = InlineKeyboardMarkup([[InlineKeyboardButton("ᴄʜ", url="https://t.me/CHBlackMarch")], [InlineKeyboardButton("ɢᴀᴍᴇ", url="https://t.me/GGBlackMarch")], [InlineKeyboardButton("ɢᴀʟᴇʀʏ", url="https://t.me/PBBlackMarch")], [InlineKeyboardButton("ᴛᴀɢᴀʟʟ", url="https://t.me/BlackMarchBot")], [InlineKeyboardButton("ᴇɴᴅᴏʀsᴇ/ᴘᴘ", url="https://t.me/FOBlackManagement")]])
    await message.reply(teks, reply_markup=tombol)

# --- 5. FITUR KALKULATOR ---
@app.on_message(filters.command("calc"))
async def kalkulator_handler(client, message):
    if len(message.command) < 2: return await message.reply("Gunakan: `/calc 1.500.000 x 2`")
    raw = message.text.split(maxsplit=1)[1]
    eks = raw.replace(".", "").replace(",", ".").replace("x", "*").replace(":", "/")
    try:
        hasil = eval(eks)
        res = "{:,.2f}".format(hasil).replace(",", "X").replace(".", ",").replace("X", ".")
        if res.endswith(",00"): res = res[:-3]
        await message.reply(f"🔍 **HASIL**\n\n🔢 **Soal:** `{raw}`\n✅ **Jawaban:** `{res}`")
    except: await message.reply("❌ Error format.")

# --- 6. FITUR OTAK AI (STRICT MODE - NO EMOJI) ---
@app.on_message(
    (filters.private & ~filters.command(["absen", "daftar", "utag", "atag", "rules", "calc", "cancel"])) | 
    filters.command("quest") |
    (filters.group & (filters.mentioned | filters.reply))
)
async def ai_handler(client, message):
    if not message.text:
        return

    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        if message.reply_to_message and message.reply_to_message.from_user.is_self:
            user_input = message.text
        elif message.mentioned:
            user_input = message.text.replace(f"@{client.me.username}", "").strip()
        elif message.command and message.command[0] == "quest":
            if len(message.command) < 2:
                return await message.reply("Gunakan format: `/quest pertanyaan anda`")
            user_input = message.text.split(maxsplit=1)[1]
        else:
            return
    else:
        if message.text == "/start":
            return await message.reply("Pusat Komando BlackMarch Aktif!")
        user_input = message.text

    await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system", 
                "content": (
                    "Kamu adalah BlackMarch Support. Berikan jawaban tanpa menggunakan emoji sama sekali. "
                    "Jawablah secara padat, jelas, dan profesional. Jangan gunakan kalimat selamat datang. "
                    "Sesuaikan panjang jawaban dengan kebutuhan input user."
                )
            },
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        res_data = response.json()
        if "choices" in res_data:
            await message.reply(res_data['choices'][0]['message']['content'])
    except:
        pass

print("--- BlackMarch Support Aktif ---")
app.run()
