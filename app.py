from datetime import date, datetime, timedelta, timezone
from html import escape
from base64 import b64encode
from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="Aplikasi Pemesanan Tiket Bioskop",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Data film. Silakan ubah atau tambah data pada daftar ini.
DAFTAR_FILM = [
    {
        "judul": "Avengers: Doomsday",
        "genre": "Aksi, petualangan, fiksi ilmiah, superhero",
        "durasi_menit": 150,
        "sutradara": "Anthony Russo dan Joe Russo",
        "usia": "13 tahun ke atas",
        "studio": 1,
        "harga_dasar": 60000,
        "jam": ["10:00", "13:00", "16:00", "19:00", "22:00"],
        "warna": ("#172554", "#2563eb"),
        "ikon": "✦",
        "poster_file": "avengers-doomsday",
    },
    {
        "judul": "The Conjuring: Last Rites",
        "genre": "Horor",
        "durasi_menit": 135,
        "sutradara": "Michael Chaves",
        "usia": "17 tahun ke atas",
        "studio": 2,
        "harga_dasar": 60000,
        "jam": ["10:00", "13:00", "16:00", "19:00", "22:00"],
        "warna": ("#111827", "#7f1d1d"),
        "ikon": "☾",
        "poster_file": "the-conjuring-last-rites",
    },
    {
        "judul": "Your Name. (Kimi no Na wa)",
        "genre": "Animasi, drama, romantis, fantasi",
        "durasi_menit": 106,
        "sutradara": "Makoto Shinkai",
        "usia": "13 tahun ke atas",
        "studio": 3,
        "harga_dasar": 50000,
        "jam": ["11:00", "15:00", "19:00"],
        "warna": ("#312e81", "#ec4899"),
        "ikon": "☼",
        "poster_file": "your-name",
    },
    {
        "judul": "Train to Busan",
        "genre": "Aksi, horor, thriller, drama",
        "durasi_menit": 118,
        "sutradara": "Yeon Sang-ho",
        "usia": "17 tahun ke atas",
        "studio": 4,
        "harga_dasar": 50000,
        "jam": ["11:00", "15:00", "19:00"],
        "warna": ("#0f172a", "#0f766e"),
        "ikon": "▰",
        "poster_file": "train-to-busan",
    },
    {
        "judul": "Warkop DKI: Viralin Doooong..!!",
        "genre": "Drama, komedi, horor",
        "durasi_menit": 120,
        "sutradara": "Herwin Novianto",
        "usia": "13 tahun ke atas",
        "studio": 5,
        "harga_dasar": 30000,
        "jam": ["14:00"],
        "warna": ("#14532d", "#eab308"),
        "ikon": "✦",
        "poster_file": "warkop-dki",
    },
]

BARIS_KURSI = list("ABCDEFGH")
KOLOM_KURSI = 8
TAMBAHAN_AKHIR_PEKAN = 10000
ZONA_WAKTU = timezone(timedelta(hours=7), "WIB")
FOLDER_POSTER = Path(__file__).resolve().parent / "posters"
EKSTENSI_POSTER = (".png", ".jpg", ".jpeg", ".webp")
NAMA_BULAN = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember",
]


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


def tampilkan_kursi(kode, kunci_jadwal, kursi_terpesan, kolom):
    sudah_dipesan = kode in kursi_terpesan
    dipilih = kode in st.session_state.kursi_dipilih
    ikon = "🟥🪑" if sudah_dipesan else ("🟦🪑" if dipilih else "🟩🪑")
    if kolom.button(
        f"{ikon} {kode}",
        key=f"seat_{kunci_jadwal}_{kode}",
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


def cari_file_poster(film):
    for ekstensi in EKSTENSI_POSTER:
        kandidat = FOLDER_POSTER / f"{film['poster_file']}{ekstensi}"
        if kandidat.is_file():
            return kandidat
    return None


st.markdown(
    """
    <style>
      .stApp {background: linear-gradient(135deg,#f5f7ff 0%,#eef6ff 48%,#f5f3ff 100%); color:#172033;}
      .block-container {padding-top: 2rem; max-width: 1180px;}
      .hero {padding: 1.5rem 1.8rem; border-radius: 24px; color: white;
        background: linear-gradient(110deg,#111827,#1d4ed8 65%,#7c3aed);
        box-shadow: 0 14px 36px rgba(30,64,175,.20); margin-bottom: 1rem;}
      .hero h1 {margin: 0; color: white; font-size: 2.2rem;}
      .hero p {margin: .45rem 0 0; color: #dbeafe;}
      /* Pastikan label dan teks tetap terbaca ketika browser memakai tema gelap. */
      .stApp h1, .stApp h2, .stApp h3, .stApp h4,
      .stApp p, .stApp li, .stApp label, .stApp [data-testid="stWidgetLabel"],
      .stApp [data-testid="stWidgetLabel"] p,
      .stApp [data-testid="stCaptionContainer"], .stApp [data-testid="stCaptionContainer"] p,
      .stApp [data-testid="stMarkdownContainer"], .stApp [data-testid="stMarkdownContainer"] p,
      .stApp [data-testid="stMetricLabel"], .stApp [data-testid="stMetricValue"] {
        color: #172033 !important;
      }
      .stApp .hero h1, .stApp .hero p {color: white !important;}
      .stApp [data-baseweb="tab"] p, .stApp [data-baseweb="tab"] div {
        color: #334155 !important;
      }
      .stApp [data-baseweb="input"] > div,
      .stApp [data-baseweb="select"] > div,
      .stApp [data-testid="stTextInput"] input,
      .stApp [data-testid="stDateInput"] input {
        background-color: #ffffff !important;
        color: #172033 !important;
        border-color: #cbd5e1 !important;
      }
      /* Atur kolom nama secara terpisah agar tidak mengubah kolom tahun. */
      .stApp [data-testid="stTextInput"]:has(input[aria-label="Nama pemesan"]) [data-baseweb="input"],
      .stApp [data-testid="stTextInput"]:has(input[aria-label="Nama pemesan"]) [data-baseweb="input"] > div,
      .stApp [data-testid="stTextInput"]:has(input[aria-label="Nama pemesan"]) [data-rac][role="group"],
      .stApp [data-testid="stTextInput"]:has(input[aria-label="Nama pemesan"]) [data-rac][role="group"] > div {
        background: #ffffff !important;
        background-color: #ffffff !important;
      }
      .stApp input[aria-label="Nama pemesan"],
      .stApp input[aria-label="Nama pemesan"]:focus,
      .stApp input[aria-label="Nama pemesan"]:active {
        background: #ffffff !important;
        background-color: #ffffff !important;
        color: #172033 !important;
        -webkit-text-fill-color: #172033 !important;
        caret-color: #172033 !important;
      }
      /* Kolom tahun hanya-baca selalu putih dan menggunakan teks abu gelap. */
      .stApp [data-testid="stTextInput"]:has(input[aria-label="Tahun (otomatis)"]) [data-baseweb="input"],
      .stApp [data-testid="stTextInput"]:has(input[aria-label="Tahun (otomatis)"]) [data-baseweb="input"] > div,
      .stApp [data-testid="stTextInput"]:has(input[aria-label="Tahun (otomatis)"]) [data-rac][role="group"],
      .stApp [data-testid="stTextInput"]:has(input[aria-label="Tahun (otomatis)"]) [data-rac][role="group"] > div,
      .stApp input[aria-label="Tahun (otomatis)"] {
        background: #ffffff !important;
        background-color: #ffffff !important;
        color: #475569 !important;
        -webkit-text-fill-color: #475569 !important;
      }
      /* Samakan bingkai kolom teks dengan bingkai dropdown. */
      .stApp [data-testid="stTextInput"] [data-baseweb="input"] > div,
      .stApp [data-testid="stTextInput"] [data-rac][role="group"] {
        border: 1px solid #94a3b8 !important;
        border-radius: 6px !important;
        box-shadow: none !important;
      }
      .stApp [data-testid="stTextInput"] [data-baseweb="input"]:focus-within > div,
      .stApp [data-testid="stTextInput"] [data-rac][role="group"]:focus-within {
        border: 1px solid #94a3b8 !important;
        box-shadow: none !important;
      }
      .stApp [data-testid="stTextInput"] input {
        border: 0 !important;
        outline: 0 !important;
        box-shadow: none !important;
      }
      /* Streamlit menyimpan garis luar teks pada wrapper ini, bukan pada input. */
      .stApp [data-testid="stTextInputRootElement"],
      .stApp [data-testid="stTextInputRootElement"]:focus-within,
      .stApp [data-testid="stTextInputRootElement"]:has(input:not(:placeholder-shown)) {
        background: #ffffff !important;
        background-color: #ffffff !important;
        border: 1px solid #94a3b8 !important;
        border-radius: 6px !important;
        box-shadow: none !important;
      }
      .stApp input[aria-label="Nama pemesan"]:-webkit-autofill,
      .stApp input[aria-label="Nama pemesan"]:-webkit-autofill:hover,
      .stApp input[aria-label="Nama pemesan"]:-webkit-autofill:focus {
        -webkit-box-shadow: 0 0 0 1000px #ffffff inset !important;
        box-shadow: 0 0 0 1000px #ffffff inset !important;
        -webkit-text-fill-color: #172033 !important;
        caret-color: #172033 !important;
      }
      /* Paksa seluruh bidang select dan kalender memakai permukaan putih. */
      .stApp [data-testid="stSelectbox"] [data-baseweb="select"] > div,
      .stApp [data-testid="stSelectbox"] [data-baseweb="select"] [role="combobox"],
      .stApp [data-testid="stDateInput"] [data-baseweb="input"],
      .stApp [data-testid="stDateInput"] [data-baseweb="input"] > div,
      .stApp [data-testid="stDateInput"] button {
        background: #ffffff !important;
        color: #172033 !important;
      }
      /* Samakan kontrol dropdown dengan kolom nama pemesan. */
      .stApp [data-testid="stSelectbox"] [data-baseweb="select"] > div {
        background: #ffffff !important;
        border: 1px solid #94a3b8 !important;
        border-radius: 6px !important;
        min-height: 40px;
      }
      /* BaseWeb membungkus selectbox dalam beberapa lapisan; target langsung
         pada kontrol agar tidak mewarisi latar gelap dari tema browser. */
      .stApp div[data-baseweb="select"] > div,
      .stApp div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        background-image: none !important;
        border: 1px solid #94a3b8 !important;
        border-radius: 6px !important;
      }
      .stApp div[data-baseweb="select"] > div > div,
      .stApp div[data-baseweb="select"] [role="combobox"] {
        background-color: transparent !important;
        color: #172033 !important;
        -webkit-text-fill-color: #172033 !important;
      }
      /* Streamlit versi baru menggunakan React Aria untuk selectbox,
         bukan BaseWeb. Warna gelap muncul pada grup yang membungkus input. */
      .stApp [data-rac][role="group"] {
        background: #ffffff !important;
        background-color: #ffffff !important;
        color: #172033 !important;
        border: 1px solid #94a3b8 !important;
        border-radius: 6px !important;
      }
      .stApp [data-rac][role="group"] input[role="combobox"] {
        background: transparent !important;
        background-color: transparent !important;
        color: #172033 !important;
        -webkit-text-fill-color: #172033 !important;
      }
      .stApp [data-rac][role="group"] button {
        background: transparent !important;
        color: #334155 !important;
      }
      .stApp [data-rac][role="group"][data-disabled="true"] input[role="combobox"] {
        color: #64748b !important;
        -webkit-text-fill-color: #64748b !important;
      }
      .stApp [data-rac][role="listbox"],
      .stApp [data-rac][role="option"] {
        background: #ffffff !important;
        color: #172033 !important;
      }
      .stApp select {
        background: #ffffff !important;
        color: #172033 !important;
        border: 1px solid #94a3b8 !important;
        border-radius: 6px !important;
      }
      .stApp [data-testid="stSelectbox"] [data-baseweb="select"] > div > div,
      .stApp [data-testid="stSelectbox"] [data-baseweb="select"] [role="combobox"],
      .stApp [data-testid="stSelectbox"] [data-baseweb="select"] span {
        background: transparent !important;
        color: #172033 !important;
        -webkit-text-fill-color: #172033 !important;
      }
      .stApp [data-baseweb="popover"],
      .stApp [data-baseweb="menu"],
      .stApp [role="listbox"] {
        background: #ffffff !important;
        color: #172033 !important;
      }
      .stApp [role="option"] {background:#ffffff !important;color:#172033 !important;}
      .stApp [role="option"]:hover {background:#dbeafe !important;}
      .stApp [data-testid="stSelectbox"] [data-baseweb="select"] span,
      .stApp [data-testid="stDateInput"] input {
        color: #172033 !important;
        -webkit-text-fill-color: #172033 !important;
      }
      .stApp [data-testid="stExpander"] details,
      .stApp [data-testid="stExpander"] details > summary {
        background: #ffffff !important;
        color: #172033 !important;
        border-color: #cbd5e1 !important;
      }
      .stApp [data-testid="stExpander"] details > summary:hover {background:#f1f5f9 !important;}
      .stApp [data-testid="stExpander"] details > summary p,
      .stApp [data-testid="stExpander"] details > summary span,
      .stApp [data-testid="stExpander"] details > summary svg {
        color: #172033 !important;
        fill: #172033 !important;
      }
      .stApp input::placeholder {color: #64748b !important; opacity: 1;}
      .stApp [data-baseweb="select"] [role="option"] {color: #172033 !important;}
      .stApp [data-testid="stAlert"] > div {background:#e0f2fe !important;}
      .stApp [data-testid="stAlert"] p,
      .stApp [data-testid="stAlert"] span {color:#0c4a6e !important;}
      div[data-testid="stVerticalBlockBorderWrapper"] {border-radius: 18px;}
      div.stButton > button {border-radius: 12px; min-height: 42px; font-weight: 650;
        color: #172033; border-color: #cbd5e1; background-color: #ffffff;}
      div.stButton > button:hover {border-color: #2563eb; color: #1d4ed8;}
      .stApp div[data-testid="stButton"] button[kind="primary"],
      .stApp div[data-testid="stButton"] button[data-testid="stBaseButton-primary"] {
        background: #16a34a !important;
        background-color: #16a34a !important;
        color: #ffffff !important;
        border: 1px solid #15803d !important;
      }
      .stApp div[data-testid="stButton"] button[kind="primary"]:hover,
      .stApp div[data-testid="stButton"] button[data-testid="stBaseButton-primary"]:hover {
        background: #15803d !important;
        background-color: #15803d !important;
        border-color: #166534 !important;
        color: #ffffff !important;
      }
      div.stButton > button:disabled {opacity: .78;}
      [data-testid="stImage"] img {border-radius: 16px; box-shadow: 0 8px 24px #0f172a26;}
    </style>
    <div class="hero"><h1>🎬 Aplikasi Pemesanan Tiket Bioskop</h1>
    <p>Aplikasi pemesanan tiket bioskop · Proyek Matematika Diskrit</p></div>
    """,
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

tab_film, tab_pesan, tab_riwayat = st.tabs(["🎞️  Daftar film", "🎟️  Pesan tiket", "📋  Riwayat"])


with tab_film:
    st.subheader("Film yang tersedia")
    st.caption("Tambahkan poster sendiri ke folder posters untuk mengganti ilustrasi bawaan.")
    for awal in range(0, len(DAFTAR_FILM), 2):
        kolom_kartu = st.columns(2, gap="large")
        for kolom, film in zip(kolom_kartu, DAFTAR_FILM[awal:awal + 2]):
            with kolom:
                with st.container(border=True):
                    kiri, kanan = st.columns([0.8, 1.2], gap="medium")
                    with kiri:
                        file_poster = cari_file_poster(film)
                        if file_poster:
                            st.image(str(file_poster), width=190)
                        else:
                            st.markdown(
                                f'<img src="{poster_data_uri(film)}" '
                                'style="width:100%;max-width:190px;border-radius:16px;'
                                'box-shadow:0 8px 24px #0f172a26;" />',
                                unsafe_allow_html=True,
                            )
                    with kanan:
                        st.markdown(f"### {film['judul']}")
                        st.write(f"**Genre:** {film['genre']}")
                        st.write(f"**Durasi:** {format_durasi(film['durasi_menit'])}")
                        st.write(f"**Sutradara:** {film['sutradara']}")
                        st.write(f"**Rating:** {film['usia']}")
                        st.write(f"**Studio:** {film['studio']}")
                        st.write("**Jadwal:** " + ", ".join(film["jam"]))
                        st.write(f"**Harga dasar:** {format_rupiah(film['harga_dasar'])}")


with tab_pesan:
    st.subheader("Buat pemesanan")
    nama = st.text_input("Nama pemesan", placeholder="Masukkan nama Anda")

    pilihan_film = st.selectbox(
        "Pilih film",
        options=[""] + [film["judul"] for film in DAFTAR_FILM],
        index=0,
        format_func=lambda nilai: "— Pilih film —" if nilai == "" else nilai,
        key="pilihan_film",
    )

    tanggal_pemesanan = datetime.now(ZONA_WAKTU).date()
    tanggal_yang_bisa_dipilih = [
        tanggal_pemesanan + timedelta(days=selisih) for selisih in range(4)
    ]
    st.write(f"**Tanggal pemesanan otomatis:** {tanggal_pemesanan.strftime('%d/%m/%Y')}")
    st.caption("Tanggal menonton dapat dipilih dari hari ini sampai tiga hari ke depan.")

    bulan_tersedia = sorted({(tanggal.year, tanggal.month) for tanggal in tanggal_yang_bisa_dipilih})
    opsi_bulan = [""] + [f"{tahun}-{bulan:02d}" for tahun, bulan in bulan_tersedia]
    kolom_tahun, kolom_bulan, kolom_hari = st.columns([1, 1.5, 1])
    with kolom_bulan:
        bulan_dipilih = st.selectbox(
            "Bulan",
            options=opsi_bulan,
            format_func=lambda nilai: (
                "Pilih bulan" if not nilai else NAMA_BULAN[int(nilai[5:7]) - 1]
            ),
            key="pilih_bulan_tayang",
        )
    with kolom_tahun:
        tahun_otomatis = int(bulan_dipilih[:4]) if bulan_dipilih else tanggal_pemesanan.year
        st.text_input("Tahun (otomatis)", value=str(tahun_otomatis), disabled=True)
    with kolom_hari:
        tahun_bulan_dipilih = tuple(map(int, bulan_dipilih.split("-"))) if bulan_dipilih else None
        hari_tersedia = [
            tanggal.day for tanggal in tanggal_yang_bisa_dipilih
            if tahun_bulan_dipilih and (tanggal.year, tanggal.month) == tahun_bulan_dipilih
        ]
        hari_dipilih = st.selectbox(
            "Tanggal",
            options=[""] + hari_tersedia,
            format_func=lambda nilai: "Pilih tanggal" if nilai == "" else str(nilai),
            key="pilih_hari_tayang",
        )

    tanggal_tayang = None
    if bulan_dipilih and hari_dipilih:
        tanggal_tayang = date(tahun_bulan_dipilih[0], tahun_bulan_dipilih[1], hari_dipilih)

    film = next((item for item in DAFTAR_FILM if item["judul"] == pilihan_film), None)
    pilihan_jam = ""
    if film:
        pilihan_jam = st.selectbox(
            "Jam tayang",
            options=[""] + film["jam"],
            index=0,
            format_func=lambda nilai: "— Pilih jam tayang —" if nilai == "" else nilai,
            key=f"pilihan_jam_{film['studio']}",
        )
    else:
        st.selectbox("Jam tayang", options=[""], format_func=lambda _: "— Pilih film terlebih dahulu —", disabled=True)

    jadwal_lengkap = bool(film and tanggal_tayang and pilihan_jam)

    if jadwal_lengkap:
        st.markdown(
            f"**Studio {film['studio']}** · {pilihan_jam}–"
            f"{waktu_selesai(pilihan_jam, film['durasi_menit'])} · {film['usia']}"
        )
        st.markdown("#### Pilih kursi")
        st.caption("🟩🪑 Tersedia  ·  🟦🪑 Pilihan Anda  ·  🟥🪑 Sudah dipesan")

        kunci_jadwal = (film["judul"], tanggal_tayang.isoformat(), pilihan_jam)
        if st.session_state.jadwal_kursi_aktif != kunci_jadwal:
            st.session_state.jadwal_kursi_aktif = kunci_jadwal
            st.session_state.kursi_dipilih = set()
        kursi_terpesan = st.session_state.kursi_terpesan.get(kunci_jadwal, set())

        st.markdown(
            "<div style='text-align:center;background:#dbeafe;padding:.55rem;border-radius:12px;"
            "font-weight:700;letter-spacing:.18em;margin:.5rem 0 1rem'>LAYAR</div>",
            unsafe_allow_html=True,
        )

        for baris in BARIS_KURSI:
            kiri, lorong, kanan = st.columns([4, 0.7, 4], gap="small")
            kiri_atas, kiri_bawah = kiri.columns(2, gap="small")
            kanan_atas, kanan_bawah = kanan.columns(2, gap="small")
            # Baris visual atas: 1-2 di kiri lorong, 3-4 di kanan lorong.
            for nomor, kolom_kursi in zip((1, 2), (kiri_atas, kiri_bawah)):
                tampilkan_kursi(f"{baris}{nomor}", kunci_jadwal, kursi_terpesan, kolom_kursi)
            for nomor, kolom_kursi in zip((5, 6), (kiri_atas, kiri_bawah)):
                tampilkan_kursi(f"{baris}{nomor}", kunci_jadwal, kursi_terpesan, kolom_kursi)
            for nomor, kolom_kursi in zip((3, 4), (kanan_atas, kanan_bawah)):
                tampilkan_kursi(f"{baris}{nomor}", kunci_jadwal, kursi_terpesan, kolom_kursi)
            for nomor, kolom_kursi in zip((7, 8), (kanan_atas, kanan_bawah)):
                tampilkan_kursi(f"{baris}{nomor}", kunci_jadwal, kursi_terpesan, kolom_kursi)
            with lorong:
                st.markdown("<div style='text-align:center;padding-top:.6rem;color:#64748b'>│</div>", unsafe_allow_html=True)

        kursi_dipilih = sorted(st.session_state.kursi_dipilih)
        harga = harga_tiket(film, tanggal_tayang)
        total = harga * len(kursi_dipilih)
        st.info("Kursi dipilih: " + (", ".join(kursi_dipilih) if kursi_dipilih else "belum ada"))
        if tanggal_tayang.weekday() in (5, 6):
            st.caption("Harga akhir pekan sudah termasuk tambahan Rp 10.000 per tiket.")

        metode_bayar = st.selectbox("Metode pembayaran", ["Tunai", "Kartu debit", "QRIS"])
        kiri_total, kanan_total = st.columns(2)
        kiri_total.metric("Harga per tiket", format_rupiah(harga))
        kanan_total.metric("Total pembayaran", format_rupiah(total))

        if st.button("Konfirmasi pemesanan", type="primary", use_container_width=True):
            if not nama.strip():
                st.error("Nama pemesan belum diisi.")
            elif not kursi_dipilih:
                st.error("Pilih minimal satu kursi pada denah.")
            else:
                sudah_dipesan_sekarang = st.session_state.kursi_terpesan.setdefault(kunci_jadwal, set())
                bentrok = set(kursi_dipilih) & sudah_dipesan_sekarang
                if bentrok:
                    st.error("Kursi berikut baru saja dipesan: " + ", ".join(sorted(bentrok)))
                else:
                    sudah_dipesan_sekarang.update(kursi_dipilih)
                    pesanan = {
                        "nama": nama.strip().title(),
                        "film": film["judul"],
                        "tanggal": tanggal_tayang.strftime("%d/%m/%Y"),
                        "jam": f"{pilihan_jam}-{waktu_selesai(pilihan_jam, film['durasi_menit'])}",
                        "studio": film["studio"],
                        "kursi": kursi_dipilih,
                        "harga": harga,
                        "total": total,
                        "pembayaran": metode_bayar,
                    }
                    st.session_state.riwayat.append(pesanan)
                    st.session_state.pesanan_terakhir = pesanan
                    st.session_state.kursi_dipilih = set()
                    st.success("Pemesanan berhasil. Tiket Anda siap.")
                    st.rerun()
    else:
        st.markdown(
            "<div style='background:#e0f2fe;color:#0c4a6e;border:1px solid #7dd3fc;"
            "border-radius:12px;padding:1rem;font-weight:600'>"
            "Pilih film, tanggal menonton, dan jam tayang untuk menampilkan denah kursi."
            "</div>",
            unsafe_allow_html=True,
        )

    pesanan_terakhir = st.session_state.pesanan_terakhir
    if pesanan_terakhir:
        with st.container(border=True):
            st.subheader("Tiket terakhir")
            st.write(f"**{pesanan_terakhir['film']}** · {pesanan_terakhir['tanggal']} · {pesanan_terakhir['jam']}")
            st.write(f"Studio {pesanan_terakhir['studio']} · Kursi {', '.join(pesanan_terakhir['kursi'])}")
            st.write(f"Pembayaran: {pesanan_terakhir['pembayaran']} · Total: {format_rupiah(pesanan_terakhir['total'])}")


with tab_riwayat:
    st.subheader("Riwayat pemesanan")
    if not st.session_state.riwayat:
        st.info("Belum ada pemesanan dalam sesi ini.")
    else:
        for nomor, pesanan in enumerate(st.session_state.riwayat, start=1):
            with st.expander(f"{nomor}. {pesanan['nama']} — {pesanan['film']} ({pesanan['tanggal']})"):
                st.write(f"**Jadwal:** {pesanan['jam']} · Studio {pesanan['studio']}")
                st.write(f"**Kursi:** {', '.join(pesanan['kursi'])}")
                st.write(f"**Metode pembayaran:** {pesanan['pembayaran']}")
                st.write(f"**Total:** {format_rupiah(pesanan['total'])}")

st.caption("Aplikasi tugas proyek Matematika Diskrit · Data pesanan tersimpan selama sesi aplikasi aktif.")
