from datetime import date, datetime, timedelta, timezone
from html import escape
from base64 import b64encode
from heapq import heappop, heappush
from pathlib import Path
from uuid import uuid4

import streamlit as st


st.set_page_config(
    page_title="Website Pemesanan Tiket Bioskop",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Urutan daftar mempertahankan Avengers di posisi pertama, lalu mengikuti rating IMDb tertinggi.
DAFTAR_FILM = [
    {
        "judul": "Avengers: Doomsday",
        "genre": "Aksi, petualangan, fiksi ilmiah, superhero",
        "durasi_menit": 165,
        "sutradara": "Anthony Russo dan Joe Russo",
        "pemeran": "Robert Downey Jr., Chris Hemsworth, Pedro Pascal, Vanessa Kirby, Anthony Mackie",
        "usia": "13 tahun ke atas",
        "studio": 1,
        "harga_dasar": 60000,
        "warna": ("#172554", "#2563eb"),
        "ikon": "✦",
        "poster_file": "avengers-doomsday",
        "rating_imdb": 8.8,
        "rating_rotten_tomatoes": 85,
        "rating_letterboxd": 4.6,
        "sinopsis": "Ketika ancaman baru mempertemukan para pahlawan dari berbagai dunia, mereka harus mengesampingkan perbedaan dan menghadapi kekuatan yang jauh melampaui kemampuan mereka. Nasib banyak semesta bergantung pada keberhasilan mereka bersatu.",
        "trailer_id": "PyTEUYXVDaU",
    },
    {
        "judul": "The Odyssey",
        "genre": "Aksi, petualangan, fantasi",
        "durasi_menit": 172,
        "sutradara": "Christopher Nolan",
        "pemeran": "Matt Damon, Tom Holland, Anne Hathaway, Robert Pattinson, Lupita Nyong’o",
        "usia": "17 tahun ke atas",
        "studio": 2,
        "harga_dasar": 60000,
        "warna": ("#0f172a", "#b45309"),
        "ikon": "⚔",
        "poster_file": "the-odyssey",
        "rating_imdb": 8.4,
        "rating_rotten_tomatoes": 94,
        "rating_letterboxd": 4.3,
        "sinopsis": "Setelah Perang Troya berakhir, Raja Odysseus memulai perjalanan panjang melintasi laut untuk kembali ke Ithaca dan keluarganya. Monster, badai, dan berbagai ujian menghalangi kepulangannya, sementara setiap pilihan menentukan apakah ia dapat bertahan hidup.",
        "trailer_id": "8lI3f6K7mJk",
    },
    {
        "judul": "Your Name.",
        "genre": "Animasi, drama, romantis, fantasi",
        "durasi_menit": 106,
        "sutradara": "Makoto Shinkai",
        "pemeran": "Ryunosuke Kamiki, Mone Kamishiraishi, Ryo Narita, Aoi Yuki, Nobunaga Shimazaki",
        "label_pemeran": "Pengisi suara",
        "usia": "13 tahun ke atas",
        "studio": 3,
        "harga_dasar": 50000,
        "warna": ("#312e81", "#ec4899"),
        "ikon": "☼",
        "poster_file": "your-name",
        "rating_imdb": 8.4,
        "rating_rotten_tomatoes": 98,
        "rating_letterboxd": 4.3,
        "sinopsis": "Mitsuha, seorang siswi yang tinggal di desa pegunungan, dan Taki, seorang remaja di Tokyo, tiba-tiba terbangun dalam tubuh satu sama lain. Saat pertukaran itu semakin sering terjadi, keduanya berusaha mencari tahu hubungan misterius yang menghubungkan hidup mereka.",
        "trailer_id": "i1Fs8KdPvxQ",
    },
    {
        "judul": "Demon Slayer: Kimetsu No Yaiba Infinity Castle",
        "genre": "Animasi, aksi, fantasi",
        "durasi_menit": 155,
        "sutradara": "Haruo Sotozaki",
        "pemeran": "Natsuki Hanae, Akari Kito, Hiro Shimono, Yoshitsugu Matsuoka, Reina Ueda",
        "label_pemeran": "Pengisi suara",
        "usia": "17 tahun ke atas",
        "studio": 4,
        "harga_dasar": 50000,
        "warna": ("#312e81", "#be123c"),
        "ikon": "⚔",
        "poster_file": "demon-slayer-infinity-castle",
        "rating_imdb": 8.3,
        "rating_rotten_tomatoes": 98,
        "rating_letterboxd": 4.1,
        "sinopsis": "Tanjiro dan Korps Pembasmi Iblis terseret ke dalam Infinity Castle, markas labirin milik Muzan Kibutsuji. Di tengah pertarungan melawan para iblis tingkat atas, mereka harus bertahan dan bekerja sama untuk membuka jalan menuju pertempuran penentuan.",
        "trailer_id": "Ti6p4vnKsH8",
    },
    {
        "judul": "Chainsaw Man – The Movie: Reze Arc",
        "genre": "Animasi, aksi, fantasi gelap",
        "durasi_menit": 100,
        "sutradara": "Tatsuya Yoshihara",
        "pemeran": "Kikunosuke Toya, Reina Ueda, Tomori Kusunoki, Shogo Sakata, Fairouz Ai",
        "label_pemeran": "Pengisi suara",
        "usia": "17 tahun ke atas",
        "studio": 5,
        "harga_dasar": 50000,
        "warna": ("#7f1d1d", "#f97316"),
        "ikon": "⛓",
        "poster_file": "chainsaw-man-reze-arc",
        "rating_imdb": 8.3,
        "rating_rotten_tomatoes": 96,
        "rating_letterboxd": 4.4,
        "sinopsis": "Di tengah hidupnya sebagai pemburu iblis, Denji bertemu Reze, seorang gadis yang bekerja di sebuah kafe dan membuatnya merasakan kehidupan yang lebih biasa. Namun, kedekatan mereka menyimpan rahasia yang menyeret Denji ke dalam konflik berbahaya antara manusia dan iblis.",
        "trailer_id": "KVNghVuTMkg",
    },
    {
        "judul": "Spider-Man: Brand New Day",
        "genre": "Aksi, petualangan, superhero",
        "durasi_menit": 145,
        "sutradara": "Destin Daniel Cretton",
        "pemeran": "Tom Holland, Zendaya, Sadie Sink, Jacob Batalon, Jon Bernthal",
        "usia": "13 tahun ke atas",
        "studio": 6,
        "harga_dasar": 60000,
        "warna": ("#7f1d1d", "#1d4ed8"),
        "ikon": "🕸",
        "poster_file": "spider-man-brand-new-day",
        "rating_imdb": 7.9,
        "rating_rotten_tomatoes": 90,
        "rating_letterboxd": 4.0,
        "sinopsis": "Setelah dunia melupakan identitas Peter Parker, ia menjalani hidup baru sebagai Spider-Man tanpa dukungan orang-orang terdekatnya. Ketika ancaman baru muncul di New York, Peter harus mengandalkan dirinya sendiri dan menghadapi konsekuensi dari pilihannya.",
        "trailer_id": "n7n5aU1a1G8",
    },
    {
        "judul": "The Batman",
        "genre": "Aksi, kriminal, drama",
        "durasi_menit": 176,
        "sutradara": "Matt Reeves",
        "pemeran": "Robert Pattinson, Zoë Kravitz, Paul Dano, Jeffrey Wright, Colin Farrell",
        "usia": "17 tahun ke atas",
        "studio": 7,
        "harga_dasar": 60000,
        "warna": ("#111827", "#7f1d1d"),
        "ikon": "🦇",
        "poster_file": "the-batman",
        "rating_imdb": 7.8,
        "rating_rotten_tomatoes": 85,
        "rating_letterboxd": 4.1,
        "sinopsis": "Pada tahun-tahun awalnya sebagai pelindung Gotham, Batman menyelidiki serangkaian pembunuhan yang dilakukan oleh Riddler. Petunjuk demi petunjuk membawanya pada jaringan korupsi yang meresap ke dalam kota dan menyentuh sejarah keluarganya sendiri.",
        "trailer_id": "Wsw1lfHQIhs",
    },
    {
        "judul": "Resident Evil",
        "genre": "Horor, aksi, zombie",
        "durasi_menit": 94,
        "sutradara": "Zach Cregger",
        "pemeran": "Austin Abrams, Zach Cherry, Kali Reis, Paul Walter Hauser",
        "usia": "17 tahun ke atas",
        "studio": 8,
        "harga_dasar": 50000,
        "warna": ("#052e16", "#991b1b"),
        "ikon": "☣",
        "poster_file": "resident-evil",
        "rating_imdb": 7.4,
        "rating_rotten_tomatoes": 96,
        "rating_letterboxd": 3.8,
        "sinopsis": "Dalam satu malam yang berubah menjadi bencana, kurir medis Bryan terjebak di tengah wabah yang menyebar cepat. Ia harus mencari cara untuk bertahan hidup ketika kekacauan menguasai kota dan bahaya mengintai di setiap langkah.",
        "trailer_id": "LR1s3l_fGXQ",
    },
    {
        "judul": "Attack on Titan: The Last Attack",
        "genre": "Animasi, aksi, fantasi",
        "durasi_menit": 144,
        "sutradara": "Yuichiro Hayashi",
        "pemeran": "Yuki Kaji, Yui Ishikawa, Marina Inoue, Yoshimasa Hosoya, Hiroshi Kamiya",
        "label_pemeran": "Pengisi suara",
        "usia": "17 tahun ke atas",
        "studio": 9,
        "harga_dasar": 50000,
        "warna": ("#172554", "#dc2626"),
        "ikon": "⚔",
        "poster_file": "attack-on-titan-last-attack",
        "rating_imdb": 8.9,
        "rating_rotten_tomatoes": None,
        "rating_letterboxd": 4.7,
        "sinopsis": "Dua tahun setelah konflik mencapai titik puncaknya, Eren memulai Rumbling dan mengancam kehidupan di luar Pulau Paradis. Mikasa, Armin, dan sekutu lama maupun baru berpacu menghentikannya, sementara masa depan umat manusia ditentukan oleh pertempuran terakhir mereka.",
        "trailer_id": "MYclcUjyfw8",
    },
    {
        "judul": "Interstellar",
        "genre": "Fiksi ilmiah, petualangan, drama",
        "durasi_menit": 169,
        "sutradara": "Christopher Nolan",
        "pemeran": "Matthew McConaughey, Anne Hathaway, Jessica Chastain, Michael Caine, Matt Damon",
        "usia": "13 tahun ke atas",
        "studio": 10,
        "harga_dasar": 60000,
        "warna": ("#0f172a", "#0e7490"),
        "ikon": "✦",
        "poster_file": "interstellar",
        "rating_imdb": 8.7,
        "rating_rotten_tomatoes": 73,
        "rating_letterboxd": 4.5,
        "sinopsis": "Ketika perubahan iklim membuat Bumi semakin sulit dihuni, mantan pilot Cooper bergabung dengan misi antariksa untuk mencari tempat tinggal baru bagi umat manusia. Perjalanan melewati wormhole membawanya jauh dari keluarganya dan menguji batas waktu, pengorbanan, serta harapan untuk pulang.",
        "trailer_id": "sDcFsRmRECE",
    },
]

# Urutan mengikuti rating IMDb; Avengers tetap di posisi pertama dan Attack on Titan setelah The Odyssey.
film_pengecualian = DAFTAR_FILM[0]
film_lain_urut = sorted(
    [film for film in DAFTAR_FILM[1:] if film["judul"] != "Attack on Titan: The Last Attack"],
    key=lambda film: film["rating_imdb"] or 0,
    reverse=True,
)
film_aot = next(film for film in DAFTAR_FILM if film["judul"] == "Attack on Titan: The Last Attack")
posisi_odyssey = next(
    posisi for posisi, film in enumerate(film_lain_urut)
    if film["judul"] == "The Odyssey"
)
film_lain_urut.insert(posisi_odyssey + 1, film_aot)
DAFTAR_FILM = [film_pengecualian, *film_lain_urut]
# Jadwal tetap dengan jarak antartayang yang realistis.
JADWAL_5_TAYANG = ["10:00", "13:00", "16:00", "19:00", "22:00"]
JADWAL_4_TAYANG = ["11:00", "14:00", "17:00", "20:00"]
JADWAL_3_TAYANG = ["12:00", "16:00", "20:00"]
for posisi, film in enumerate(DAFTAR_FILM, start=1):
    if posisi <= 3:
        film["jam"] = JADWAL_5_TAYANG
    elif posisi <= 8:
        film["jam"] = JADWAL_4_TAYANG
    else:
        film["jam"] = JADWAL_3_TAYANG

BARIS_KURSI = list("ABCDEFGH")
KOLOM_KURSI = 12
TAMBAHAN_AKHIR_PEKAN = 10000
ZONA_WAKTU = timezone(timedelta(hours=7), "WIB")
FOLDER_POSTER = Path(__file__).resolve().parent / "posters"
FOLDER_ASSET = Path(__file__).resolve().parent / "assets"
EKSTENSI_POSTER = (".png", ".jpg", ".jpeg", ".webp")
NAMA_BULAN = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember",
]
NAMA_HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]


def format_rupiah(angka):
    return "Rp " + f"{angka:,}".replace(",", ".")


def format_durasi(menit):
    jam, sisa_menit = divmod(menit, 60)
    if sisa_menit == 0:
        return f"{jam} jam"
    if jam == 0:
        return f"{sisa_menit} menit"
    return f"{jam} jam {sisa_menit} menit"


def waktu_selesai(jam_mulai, durasi_menit):
    selesai = datetime.strptime(jam_mulai, "%H:%M") + timedelta(minutes=durasi_menit)
    sisa_menit = selesai.minute % 5
    if sisa_menit:
        selesai += timedelta(minutes=5 - sisa_menit)
    return selesai.strftime("%H:%M")


def harga_tiket(film, tanggal_tayang):
    harga = film["harga_dasar"]
    if tanggal_tayang.weekday() in (5, 6):
        harga += TAMBAHAN_AKHIR_PEKAN
    return harga


def semua_kursi():
    return [f"{baris}{kolom}" for baris in BARIS_KURSI for kolom in range(1, KOLOM_KURSI + 1)]


def rute_terpendek_ke_kursi(tujuan):
    """Terapkan teori graf dan algoritma Dijkstra pada denah auditorium.

    Model yang digunakan:
    - Simpul (vertex): pintu masuk dan setiap posisi kursi, misalnya A1 atau H12.
    - Sisi (edge): hubungan antara posisi kursi yang bertetangga secara horizontal
      atau vertikal. Pintu berada di sisi kiri denah dan terhubung ke H1.
    - Bobot sisi: 1 unit untuk perpindahan biasa dan 3 unit saat melintasi lorong
      pemisah blok 3-6-3. Nilai ini adalah bobot simulasi, bukan ukuran meter.

    Dijkstra memulai jarak pintu dari 0, lalu berulang kali memproses simpul dengan
    jarak terkecil. Jarak tetangga diperbarui jika rute baru lebih murah. Setelah
    kursi tujuan tercapai, kamus `sebelumnya` dipakai untuk menyusun kembali rute.

    Args:
        tujuan: Kode kursi tujuan yang ada pada denah, misalnya "H8".

    Returns:
        Pasangan (daftar simpul rute dari PINTU, total bobot rute).
    """
    # Bentuk graf tak berarah: hubungan berjalan berlaku dua arah.
    graf = {"PINTU": []}
    for indeks_baris, baris in enumerate(BARIS_KURSI):
        for kolom in range(1, KOLOM_KURSI + 1):
            asal = f"{baris}{kolom}"
            graf.setdefault(asal, [])

            if kolom < KOLOM_KURSI:
                kanan = f"{baris}{kolom + 1}"
                # Penyeberangan celah antarblok dibuat lebih berat daripada langkah biasa.
                bobot = 3 if kolom in (3, 9) else 1
                graf[asal].append((kanan, bobot))
                graf.setdefault(kanan, []).append((asal, bobot))

            if indeks_baris < len(BARIS_KURSI) - 1:
                bawah = f"{BARIS_KURSI[indeks_baris + 1]}{kolom}"
                graf[asal].append((bawah, 1))
                graf.setdefault(bawah, []).append((asal, 1))

    # Pintu masuk dimodelkan di sisi kiri denah, dekat kursi H1.
    graf["PINTU"] = [("H1", 1)]

    # Tahap 1 Dijkstra: inisialisasi jarak semua simpul dengan tak hingga,
    # kecuali simpul awal PINTU yang jaraknya nol.
    jarak = {titik: float("inf") for titik in graf}
    sebelumnya = {}
    jarak["PINTU"] = 0
    antrean = [(0, "PINTU")]

    # Tahap 2: pilih simpul berjarak terkecil dan lakukan relaksasi sisi-sisinya.
    while antrean:
        biaya, titik = heappop(antrean)
        if biaya != jarak[titik]:
            continue
        if titik == tujuan:
            break
        for tetangga, bobot in graf[titik]:
            biaya_baru = biaya + bobot
            if biaya_baru < jarak[tetangga]:
                jarak[tetangga] = biaya_baru
                sebelumnya[tetangga] = titik
                heappush(antrean, (biaya_baru, tetangga))

    # Tahap 3: telusuri simpul sebelumnya dari tujuan untuk membentuk rute akhir.
    rute = [tujuan]
    while rute[-1] != "PINTU":
        rute.append(sebelumnya[rute[-1]])
    rute.reverse()
    return rute, int(jarak[tujuan])


def tampilkan_kursi(kode, kunci_jadwal, kursi_terpesan, kolom):
    sudah_dipesan = kode in kursi_terpesan
    dipilih = kode in st.session_state.kursi_dipilih
    if kolom.button(
        kode,
        key=f"kursi-{kode}",
        disabled=sudah_dipesan,
        use_container_width=True,
    ):
        if dipilih:
            st.session_state.kursi_dipilih.remove(kode)
        else:
            st.session_state.kursi_dipilih.add(kode)
        st.rerun()


def gambar_poster(film):
    """Poster ilustrasi vektor buatan aplikasi, tidak memerlukan file gambar eksternal."""
    warna_atas, warna_bawah = film["warna"]
    judul = escape(film["judul"])
    genre = escape(film["genre"].upper())
    ikon = escape(film["ikon"])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="420" height="600" viewBox="0 0 420 600">
      <defs>
        <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="{warna_atas}"/><stop offset="100%" stop-color="{warna_bawah}"/>
        </linearGradient>
        <radialGradient id="glow"><stop stop-color="#ffffff" stop-opacity=".65"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>
      </defs>
      <rect width="420" height="600" rx="28" fill="url(#bg)"/>
      <circle cx="315" cy="165" r="145" fill="url(#glow)"/>
      <circle cx="90" cy="430" r="105" fill="url(#glow)" opacity=".45"/>
      <path d="M0 395 Q105 330 210 400 T420 380 V600 H0Z" fill="#020617" opacity=".35"/>
      <path d="M35 80 H385 M35 520 H385" stroke="#ffffff" stroke-opacity=".48" stroke-width="2"/>
      <text x="210" y="275" text-anchor="middle" fill="#fff" font-size="118" font-family="Arial,sans-serif">{ikon}</text>
      <text x="210" y="440" text-anchor="middle" fill="#fff" font-size="25" font-weight="700" font-family="Arial,sans-serif">{judul}</text>
      <text x="210" y="474" text-anchor="middle" fill="#e2e8f0" font-size="13" letter-spacing="2" font-family="Arial,sans-serif">{genre}</text>
      <text x="210" y="555" text-anchor="middle" fill="#ffffff" fill-opacity=".72" font-size="11" letter-spacing="3" font-family="Arial,sans-serif">ILUSTRASI PROYEK MATDIS</text>
    </svg>'''


def poster_data_uri(film):
    svg = gambar_poster(film).encode("utf-8")
    return "data:image/svg+xml;base64," + b64encode(svg).decode("ascii")


def logo_rating_data_uri(nama_file):
    file_logo = FOLDER_ASSET / nama_file
    if not file_logo.is_file():
        return ""
    return "data:image/png;base64," + b64encode(file_logo.read_bytes()).decode("ascii")


def cari_file_poster(film):
    for ekstensi in EKSTENSI_POSTER:
        kandidat = FOLDER_POSTER / f"{film['poster_file']}{ekstensi}"
        if kandidat.is_file():
            return kandidat
    return None


def html_kartu_film(film):
    file_poster = cari_file_poster(film)
    if file_poster:
        mime = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".webp": "image/webp",
        }.get(file_poster.suffix.lower(), "image/png")
        isi_gambar = b64encode(file_poster.read_bytes()).decode("ascii")
        sumber_gambar = f"data:{mime};base64,{isi_gambar}"
    else:
        sumber_gambar = poster_data_uri(film)

    judul = escape(film["judul"])
    jadwal = escape(", ".join(film["jam"]))
    return f'''<a class="film-card" href="?film={film['studio']}" target="_self" aria-label="Pilih film {judul}">
      <img class="film-poster" src="{sumber_gambar}" alt="Poster {judul}">
      <div class="film-info">
        <h3>{judul}</h3>
        <p><strong>Genre:</strong> {escape(film['genre'])}</p>
        <p><strong>Durasi:</strong> {format_durasi(film['durasi_menit'])}</p>
        <p><strong>Sutradara:</strong> {escape(film['sutradara'])}</p>
        <p><strong>Rating usia:</strong> {escape(film['usia'])}</p>
        <p><strong>Jadwal:</strong> {jadwal}</p>
        <p><strong>Harga tiket:</strong> {format_rupiah(film['harga_dasar'])}</p>
      </div>
    </a>'''


CSS_PATH = Path(__file__).resolve().with_name("styles.css")
st.markdown(
    f"<style>{CSS_PATH.read_text(encoding='utf-8')}</style>",
    unsafe_allow_html=True,
)

st.markdown(
    """<header class="hero">
      <h1>🎬 Website Pemesanan Tiket Bioskop</h1>
      <p>Pilih film, jadwal tayang, dan kursi favorit Anda.</p>
    </header>""",
    unsafe_allow_html=True,
)

if "kursi_terpesan" not in st.session_state:
    st.session_state.kursi_terpesan = {}
if "riwayat" not in st.session_state:
    st.session_state.riwayat = []
if "pesanan_terakhir" not in st.session_state:
    st.session_state.pesanan_terakhir = None
if "jadwal_kursi_aktif" not in st.session_state:
    st.session_state.jadwal_kursi_aktif = None
if "kursi_dipilih" not in st.session_state:
    st.session_state.kursi_dipilih = set()

if "halaman" not in st.session_state:
    st.session_state.halaman = "daftar_film"
if "film_aktif" not in st.session_state:
    st.session_state.film_aktif = None
if "trailer_film" not in st.session_state:
    st.session_state.trailer_film = None

# Tautan kartu mengirim nomor studio melalui query URL untuk membuka pemesanan.
film_dari_url = st.query_params.get("film")
if film_dari_url:
    film_terpilih = next(
        (item for item in DAFTAR_FILM if str(item["studio"]) == str(film_dari_url)),
        None,
    )
    if film_terpilih:
        film_berubah = st.session_state.film_aktif != film_terpilih["judul"]
        st.session_state.film_aktif = film_terpilih["judul"]
        st.session_state.halaman = "pemesanan"
        if film_berubah:
            st.session_state.kursi_dipilih = set()
            st.session_state.jadwal_kursi_aktif = None
            st.session_state.trailer_film = None


def tiket_individu_pesanan(pesanan):
    return pesanan.get("tiket_individu") or [
        {
            "kursi": kursi,
            "kode": f"TIX-S{pesanan['studio']}-{pesanan['tanggal'].replace('/', '')}-{kursi}",
            "harga": pesanan["harga"],
        }
        for kursi in pesanan["kursi"]
    ]


def html_kartu_tiket(pesanan, tiket, nomor_tiket, jumlah_tiket):
    kode_tiket = escape(str(tiket["kode"]))
    kursi_tiket = escape(str(tiket["kursi"]))
    film_tiket = escape(str(pesanan["film"]))
    nama_tiket = escape(str(pesanan["nama"]))
    tanggal_tiket = escape(str(pesanan["tanggal"]))
    jam_tiket = escape(str(pesanan["jam"]).split("-")[0])
    studio_tiket = escape(str(pesanan["studio"]))
    harga_tiket_individu = format_rupiah(tiket["harga"])
    return (
        '<article class="ticket-card">'
        '<div class="ticket-main">'
        '<header class="ticket-head"><span class="ticket-brand">BIOSKOP MATDIS</span>'
        f'<span class="ticket-type">TIKET {nomor_tiket}</span></header>'
        f'<h3 class="ticket-title">{film_tiket}</h3>'
        '<div class="ticket-info">'
        f'<div class="ticket-field"><span class="ticket-field-label">Nama pemesan</span><span class="ticket-field-value">{nama_tiket}</span></div>'
        f'<div class="ticket-field"><span class="ticket-field-label">Tanggal</span><span class="ticket-field-value">{tanggal_tiket}</span></div>'
        f'<div class="ticket-field"><span class="ticket-field-label">Jam tayang</span><span class="ticket-field-value">{jam_tiket}</span></div>'
        f'<div class="ticket-field"><span class="ticket-field-label">Studio</span><span class="ticket-field-value">Studio {studio_tiket}</span></div>'
        '</div>'
        f'<footer class="ticket-foot"><span class="ticket-code">KODE · {kode_tiket}</span>'
        f'<span class="ticket-payment">Tiket {nomor_tiket} dari {jumlah_tiket}</span></footer>'
        '</div>'
        '<aside class="ticket-stub">'
        '<span class="ticket-seat-label">KURSI</span>'
        f'<strong class="ticket-seat">{kursi_tiket}</strong>'
        f'<span class="ticket-studio">Studio {studio_tiket}</span>'
        f'<span class="ticket-price">{harga_tiket_individu}</span>'
        '<span class="ticket-barcode" aria-hidden="true"></span>'
        '</aside></article>'
    )


def html_qr_contoh(seed):
    """Gambar QR dekoratif untuk contoh tampilan, bukan kode yang dapat dipindai."""
    ukuran = 21
    nilai_seed = sum((indeks + 1) * ord(karakter) for indeks, karakter in enumerate(str(seed)))
    modul = []
    for y in range(ukuran):
        for x in range(ukuran):
            di_penanda = False
            for kiri, atas in ((0, 0), (ukuran - 7, 0), (0, ukuran - 7)):
                if kiri <= x < kiri + 7 and atas <= y < atas + 7:
                    dx, dy = x - kiri, y - atas
                    gelap = dx in (0, 6) or dy in (0, 6) or (2 <= dx <= 4 and 2 <= dy <= 4)
                    di_penanda = True
                    if gelap:
                        modul.append(f'<rect x="{x}" y="{y}" width="1" height="1"/>')
                    break
            if not di_penanda and (nilai_seed * (x + 3) + y * 17 + x * y * 7) % 11 < 5:
                modul.append(f'<rect x="{x}" y="{y}" width="1" height="1"/>')
    return (
        '<svg viewBox="-1 -1 23 23" role="img" aria-label="QR contoh dekoratif">'
        '<rect x="-1" y="-1" width="23" height="23" fill="white"/>'
        '<g fill="#111827">' + "".join(modul) + "</g></svg>"
    )


def html_konfirmasi_pesanan(pesanan):
    kode_booking = escape(str(pesanan.get("kode_booking") or "BOOK-CONTOH"))
    return (
        '<section class="booking-confirmation">'
        '<div><span class="booking-status">✓ PEMESANAN BERHASIL</span>'
        '<h3>Terima kasih telah memesan!</h3>'
        '<p>Kode booking adalah nomor referensi unik pesanan Anda. Simpan kode ini atau '
        'ambil tangkapan layar halaman sebagai bukti pemesanan.</p>'
        '<p><strong>Kegunaan kode booking:</strong></p>'
        '<ul><li>Masukkan kode di mesin tiket mandiri untuk mencetak tiket fisik.</li>'
        '<li>Tunjukkan kode kepada petugas untuk verifikasi jika tiket sulit dibuka.</li>'
        '<li>Sertakan kode saat menghubungi layanan pelanggan untuk melacak kendala pesanan '
        'atau mengajukan pembatalan dan pengembalian dana.</li></ul>'
        '<p>Datang 15 menit sebelum film dimulai. Siapkan kode booking saat mencetak tiket '
        'atau ketika petugas meminta verifikasi.</p>'
        f'<div class="booking-code">{kode_booking}</div>'
        '</div><div class="booking-qr">'
        + html_qr_contoh(kode_booking)
        + '<small>QR CONTOH · TIDAK UNTUK DIPINDAI</small></div></section>'
    )


def tampilkan_riwayat():
    st.subheader("Riwayat Transaksi")
    if not st.session_state.riwayat:
        st.info("Belum ada transaksi. Pilih film yang sedang tayang untuk mulai memesan tiket.")
        return

    for nomor, pesanan in enumerate(st.session_state.riwayat, start=1):
        with st.expander(f"{nomor}. {pesanan['nama']} — {pesanan['film']} ({pesanan['tanggal']})"):
            st.write(f"**Total tiket:** {format_rupiah(pesanan['total'])}")
            st.markdown(html_konfirmasi_pesanan(pesanan), unsafe_allow_html=True)
            tiket_individu = tiket_individu_pesanan(pesanan)
            for nomor_tiket, tiket in enumerate(tiket_individu, start=1):
                st.markdown(
                    html_kartu_tiket(pesanan, tiket, nomor_tiket, len(tiket_individu)),
                    unsafe_allow_html=True,
                )


def tampilkan_form_pemesanan(film):
    st.subheader("Pemesanan Tiket")
    with st.container(border=True):
        poster_col, info_col, sinopsis_col = st.columns([1, 1.35, 1.55], gap="large")
        with poster_col:
            file_poster = cari_file_poster(film)
            if file_poster:
                mime_poster = {
                    ".png": "image/png",
                    ".jpg": "image/jpeg",
                    ".jpeg": "image/jpeg",
                    ".webp": "image/webp",
                }.get(file_poster.suffix.lower(), "image/png")
                data_poster = b64encode(file_poster.read_bytes()).decode("ascii")
                st.markdown(
                    f'<img src="data:{mime_poster};base64,{data_poster}" '
                    f'alt="Poster {escape(film["judul"])}" '
                    'style="display:block;width:100%;max-width:280px;height:auto;'
                    'image-rendering:auto;border-radius:16px;box-shadow:0 8px 24px #0f172a26;" />',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<img src="{poster_data_uri(film)}" alt="Poster {escape(film["judul"])}" '
                    'style="display:block;width:100%;max-width:280px;border-radius:16px;'
                    'box-shadow:0 8px 24px #0f172a26;" />',
                    unsafe_allow_html=True,
                )
            trailer_sedang_dibuka = st.session_state.trailer_film == film["judul"]
            label_tombol_trailer = "✕ Tutup trailer" if trailer_sedang_dibuka else "▶ Tonton trailer"
            if st.button(
                label_tombol_trailer,
                key="trailer_toggle",
                use_container_width=True,
            ):
                st.session_state.trailer_film = None if trailer_sedang_dibuka else film["judul"]
                st.rerun()
        with info_col:
            st.markdown(f"### {film['judul']}")
            st.write(f"**Genre:** {film['genre']}")
            st.write(f"**Durasi:** {format_durasi(film['durasi_menit'])}")
            st.write(f"**Sutradara:** {film['sutradara']}")
            st.write(f"**{film.get('label_pemeran', 'Pemeran')}:** {film['pemeran']}")
            st.write(f"**Rating usia:** {film['usia']}")
            st.write("**Jadwal:** " + ", ".join(film["jam"]))
            st.write(f"**Harga tiket:** {format_rupiah(film['harga_dasar'])}")
            st.caption("Harga akhir pekan (Sabtu–Minggu) dikenakan tambahan Rp 10.000 per tiket.")
            rating = film.get("rating_imdb")
            rating_tampilan = f"{rating:.1f}/10" if rating is not None else "—"
            rating_rt = film.get("rating_rotten_tomatoes")
            rating_rt_tampilan = f"{rating_rt}%" if rating_rt is not None else "—"
            rating_lb = film.get("rating_letterboxd")
            rating_lb_tampilan = f"{rating_lb:.1f}/5" if rating_lb is not None else "—"
            logo_imdb = logo_rating_data_uri("imdb-logo.png")
            logo_rotten = logo_rating_data_uri("rotten-tomatoes.png")
            logo_letterboxd = logo_rating_data_uri("letterboxd-logo.png")
            st.markdown(
                '<div class="ratings-row">'
                '<div class="rating-card rating-imdb">'
                f'<div class="rating-brand"><img class="rating-logo-imdb" src="{logo_imdb}" alt="IMDb"></div>'
                f'<div class="rating-value">{rating_tampilan}</div></div>'
                '<div class="rating-card rating-rotten">'
                f'<div class="rating-brand"><img class="rating-logo-icon" src="{logo_rotten}" alt="">'
                '</div>'
                f'<div class="rating-value">{rating_rt_tampilan}</div></div>'
                '<div class="rating-card rating-letterboxd">'
                f'<div class="rating-brand"><img class="rating-logo-icon" src="{logo_letterboxd}" alt="">'
                '</div>'
                f'<div class="rating-value">{rating_lb_tampilan}</div></div>'
                '</div>',
                unsafe_allow_html=True,
            )
        with sinopsis_col:
            st.markdown(
                '<div class="sinopsis-panel">'
                '<h3>Sinopsis cerita</h3>'
                f'<p>{escape(film.get("sinopsis", "Sinopsis belum tersedia."))}</p>'
                '</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<section class="booking-guide"><h3>Cara Memesan</h3>'
                '<div class="booking-step"><span class="booking-step-number">1</span>'
                '<span>Pilih tanggal dan jam tayang yang tersedia.</span></div>'
                '<div class="booking-step"><span class="booking-step-number">2</span>'
                '<span>Pilih kursi yang Anda inginkan pada denah.</span></div>'
                '<div class="booking-step"><span class="booking-step-number">3</span>'
                '<span>Konfirmasi pesanan untuk mendapatkan e-tiket.</span></div>'
                '<p class="booking-guide-note">Datang 15 menit sebelum film dimulai.</p></section>',
                unsafe_allow_html=True,
            )
    if st.session_state.trailer_film == film["judul"]:
        st.markdown("#### Trailer " + film["judul"])
        video_id = film.get("trailer_id")
        if video_id:
            st.video(f"https://www.youtube.com/watch?v={video_id}")
        else:
            st.info("Trailer untuk film ini belum tersedia.")
    nama = st.text_input("Nama pemesan", placeholder="Masukkan nama Anda", key="nama_pemesan")

    tanggal_pemesanan = datetime.now(ZONA_WAKTU).date()
    tanggal_yang_bisa_dipilih = [
        tanggal_pemesanan + timedelta(days=selisih) for selisih in range(4)
    ]
    st.caption("Pilih tanggal tayang yang tersedia dalam tiga hari ke depan.")

    bulan_tersedia = sorted({(tanggal.year, tanggal.month) for tanggal in tanggal_yang_bisa_dipilih})
    opsi_bulan = [""] + [f"{tahun}-{bulan:02d}" for tahun, bulan in bulan_tersedia]
    kolom_tahun, kolom_bulan, kolom_hari = st.columns([1, 1.5, 1])
    with kolom_bulan:
        bulan_dipilih = st.selectbox(
            "Bulan",
            options=opsi_bulan,
            format_func=lambda nilai: "Pilih bulan" if not nilai else NAMA_BULAN[int(nilai[5:7]) - 1],
            key="pilih_bulan_tayang",
        )
    with kolom_tahun:
        tahun_otomatis = int(bulan_dipilih[:4]) if bulan_dipilih else tanggal_pemesanan.year
        st.text_input("Tahun (otomatis)", value=str(tahun_otomatis), disabled=True)
    with kolom_hari:
        tahun_bulan_dipilih = tuple(map(int, bulan_dipilih.split("-"))) if bulan_dipilih else None
        label_hari = {
            tanggal.day: f"{tanggal.day} ({NAMA_HARI[tanggal.weekday()]})"
            for tanggal in tanggal_yang_bisa_dipilih
        }
        hari_tersedia = [
            tanggal.day for tanggal in tanggal_yang_bisa_dipilih
            if tahun_bulan_dipilih and (tanggal.year, tanggal.month) == tahun_bulan_dipilih
        ]
        hari_dipilih = st.selectbox(
            "Tanggal",
            options=[""] + hari_tersedia,
            format_func=lambda nilai: "Pilih tanggal" if nilai == "" else label_hari[nilai],
            key="pilih_hari_tayang",
        )

    tanggal_tayang = None
    if bulan_dipilih and hari_dipilih:
        tanggal_tayang = date(tahun_bulan_dipilih[0], tahun_bulan_dipilih[1], hari_dipilih)

    pilihan_jam = st.selectbox(
        "Jam tayang",
        options=[""] + film["jam"],
        format_func=lambda nilai: "— Pilih jam tayang —" if nilai == "" else nilai,
        key=f"pilihan_jam_{film['studio']}",
    )
    jadwal_lengkap = bool(tanggal_tayang and pilihan_jam)

    if jadwal_lengkap:
        st.markdown(
            f"**Studio {film['studio']}** · {pilihan_jam}–"
            f"{waktu_selesai(pilihan_jam, film['durasi_menit'])}"
        )
        st.markdown("#### Pilih kursi")
        st.caption("🟩 Tersedia  ·  🟦 Pilihan Anda  ·  🟥 Tidak tersedia")

        kunci_jadwal = (film["judul"], tanggal_tayang.isoformat(), pilihan_jam)
        if st.session_state.jadwal_kursi_aktif != kunci_jadwal:
            st.session_state.jadwal_kursi_aktif = kunci_jadwal
            st.session_state.kursi_dipilih = set()
        kursi_terpesan = st.session_state.kursi_terpesan.get(kunci_jadwal, set())

        with st.container(key="denah-kursi"):
            st.markdown(
                "<div style='text-align:center;background:#dbeafe;padding:.65rem;border-radius:12px;"
                "font-weight:700;letter-spacing:.18em;margin:.5rem 0 .45rem'>LAYAR</div>",
                unsafe_allow_html=True,
            )
            kolom_pintu = st.columns(
                [1, 1, 1, 0.55, 1, 1, 1, 1, 1, 1, 0.55, 1, 1, 1],
                gap="small",
            )
            with kolom_pintu[0]:
                st.markdown(
                    "<div class='auditorium-entrance auditorium-entrance-seat'>PINTU MASUK</div>",
                    unsafe_allow_html=True,
                )
            st.caption("Baris H berada paling dekat dengan layar. Susunan kursi setiap baris: 3–6–3.")
            aturan_warna_kursi = ["<style>"]
            for kode in semua_kursi():
                if kode in kursi_terpesan:
                    warna_kursi = ("#e11d48", "#be123c")
                elif kode in st.session_state.kursi_dipilih:
                    warna_kursi = ("#2563eb", "#1d4ed8")
                else:
                    warna_kursi = ("#22a06b", "#16804f")
                aturan_warna_kursi.append(
                    f".st-key-kursi-{kode} button{{background:{warna_kursi[0]}!important;"
                    f"border:1px solid {warna_kursi[1]}!important;color:#fff!important;"
                    "font-weight:700!important;min-height:42px!important;padding:.2rem!important;}"
                )
            aturan_warna_kursi.append("</style>")
            st.markdown("".join(aturan_warna_kursi), unsafe_allow_html=True)

            for baris in reversed(BARIS_KURSI):
                kolom_denah = st.columns(
                    [1, 1, 1, 0.55, 1, 1, 1, 1, 1, 1, 0.55, 1, 1, 1],
                    gap="small",
                )
                for nomor in range(1, 4):
                    tampilkan_kursi(
                        f"{baris}{nomor}", kunci_jadwal, kursi_terpesan, kolom_denah[nomor - 1]
                    )
                for nomor in range(4, 10):
                    tampilkan_kursi(
                        f"{baris}{nomor}", kunci_jadwal, kursi_terpesan, kolom_denah[nomor]
                    )
                for nomor in range(10, 13):
                    tampilkan_kursi(
                        f"{baris}{nomor}", kunci_jadwal, kursi_terpesan, kolom_denah[nomor + 1]
                    )

        kursi_dipilih = sorted(st.session_state.kursi_dipilih)
        harga = harga_tiket(film, tanggal_tayang)
        total = harga * len(kursi_dipilih)
        st.info("Kursi pilihan: " + (", ".join(kursi_dipilih) if kursi_dipilih else "belum dipilih"))
        if kursi_dipilih:
            with st.expander("Penerapan Matematika Diskrit · Graf dan Dijkstra"):
                st.markdown(
                    "**Tujuan:** mencari rute dengan total bobot paling kecil dari pintu "
                    "auditorium ke kursi yang dipilih.\n\n"
                    "**Model graf:** simpul adalah pintu di sisi kiri dekat H1 dan posisi kursi; "
                    "sisi menghubungkan kursi yang berdekatan. Setiap langkah biasa berbobot 1, "
                    "sedangkan perpindahan melintasi lorong antarblok berbobot 3. Bobot ini "
                    "merupakan satuan simulasi, bukan jarak dalam meter.\n\n"
                    "**Cara kerja:** Dijkstra membandingkan akumulasi bobot dari pintu, "
                    "memperbarui rute yang lebih murah, lalu menampilkan jalur menuju kursi."
                )
                for kursi in kursi_dipilih:
                    rute, bobot = rute_terpendek_ke_kursi(kursi)
                    st.caption(
                        f"Rute terpendek ke {kursi}: {' → '.join(rute)} · "
                        f"total bobot {bobot} unit"
                    )
        metode_bayar = st.selectbox("Metode pembayaran", ["Tunai", "Kartu debit/kredit", "QRIS"])
        kiri_total, kanan_total = st.columns(2)
        kiri_total.metric("Harga per tiket", format_rupiah(harga))
        kanan_total.metric("Total pembayaran", format_rupiah(total))

        if st.button("Konfirmasi pemesanan", type="primary", use_container_width=True):
            if not nama.strip():
                st.error("Masukkan nama pemesan untuk melanjutkan.")
            elif not kursi_dipilih:
                st.error("Pilih setidaknya satu kursi pada denah.")
            else:
                sudah_dipesan_sekarang = st.session_state.kursi_terpesan.setdefault(kunci_jadwal, set())
                bentrok = set(kursi_dipilih) & sudah_dipesan_sekarang
                if bentrok:
                    st.error("Kursi berikut sudah tidak tersedia. Silakan pilih kursi lain: " + ", ".join(sorted(bentrok)))
                else:
                    sudah_dipesan_sekarang.update(kursi_dipilih)
                    tiket_individu = [
                        {
                            "kursi": kursi,
                            "kode": f"TIX-{uuid4().hex[:8].upper()}",
                            "harga": harga,
                        }
                        for kursi in kursi_dipilih
                    ]
                    pesanan = {
                        "nama": nama.strip().title(),
                        "kode_booking": f"BOOK-{uuid4().hex[:8].upper()}",
                        "film": film["judul"],
                        "tanggal": tanggal_tayang.strftime("%d/%m/%Y"),
                        "jam": f"{pilihan_jam}-{waktu_selesai(pilihan_jam, film['durasi_menit'])}",
                        "studio": film["studio"],
                        "kursi": kursi_dipilih,
                        "tiket_individu": tiket_individu,
                        "harga": harga,
                        "total": total,
                        "pembayaran": metode_bayar,
                    }
                    st.session_state.riwayat.append(pesanan)
                    st.session_state.pesanan_terakhir = pesanan
                    st.session_state.kursi_dipilih = set()
                    st.success("Pemesanan berhasil. E-tiket Anda telah diterbitkan.")
                    st.rerun()
    else:
        st.markdown(
            "<div style='background:#e0f2fe;color:#0c4a6e;border:1px solid #7dd3fc;"
            "border-radius:12px;padding:1rem;font-weight:600'>"
            "Pilih tanggal dan jam tayang untuk melihat denah kursi yang tersedia."
            "</div>",
            unsafe_allow_html=True,
        )

    if st.session_state.pesanan_terakhir:
        pesanan_terakhir = st.session_state.pesanan_terakhir
        st.subheader("E-Tiket Anda")
        st.markdown(html_konfirmasi_pesanan(pesanan_terakhir), unsafe_allow_html=True)
        tiket_individu = tiket_individu_pesanan(pesanan_terakhir)
        for nomor_tiket, tiket in enumerate(tiket_individu, start=1):
            st.markdown(
                html_kartu_tiket(pesanan_terakhir, tiket, nomor_tiket, len(tiket_individu)),
                unsafe_allow_html=True,
            )


if st.session_state.halaman == "pemesanan" and st.session_state.film_aktif:
    with st.container():
        if st.button("← Kembali ke film yang sedang tayang"):
            st.session_state.halaman = "daftar_film"
            st.query_params.clear()
            st.rerun()
        film_booking = next(
            (item for item in DAFTAR_FILM if item["judul"] == st.session_state.film_aktif),
            None,
        )
        if film_booking:
            tampilkan_form_pemesanan(film_booking)
else:
    tab_film, tab_riwayat = st.tabs(["🎞️  Sedang Tayang", "📋  Riwayat Transaksi"])
    with tab_film:
        st.subheader("Film yang Sedang Tayang")
        st.caption("Pilih film untuk melihat informasi dan melanjutkan pemesanan tiket.")
        kartu_html = "".join(html_kartu_film(film) for film in DAFTAR_FILM)
        st.markdown(f'<div class="film-grid">{kartu_html}</div>', unsafe_allow_html=True)
    with tab_riwayat:
        tampilkan_riwayat()

st.markdown(
    '<div class="identitas-mahasiswa"><strong>M. Bintang Al Akbar. M</strong><br><strong>F1E126032</strong></div>',
    unsafe_allow_html=True,
)



