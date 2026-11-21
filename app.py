from datetime import date, datetime, timedelta
from html import escape

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
    },
]

BARIS_KURSI = list("ABCDEFGH")
KOLOM_KURSI = 8
TAMBAHAN_AKHIR_PEKAN = 10000
TANGGAL_MINIMUM = date(2026, 1, 1)
TANGGAL_MAKSIMUM = date(2027, 12, 31)


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


st.markdown(
    """
    <style>
      .stApp {background: linear-gradient(135deg,#f5f7ff 0%,#eef6ff 48%,#f5f3ff 100%);}
      .block-container {padding-top: 2rem; max-width: 1180px;}
      .hero {padding: 1.5rem 1.8rem; border-radius: 24px; color: white;
        background: linear-gradient(110deg,#111827,#1d4ed8 65%,#7c3aed);
        box-shadow: 0 14px 36px rgba(30,64,175,.20); margin-bottom: 1rem;}
      .hero h1 {margin: 0; color: white; font-size: 2.2rem;}
      .hero p {margin: .45rem 0 0; color: #dbeafe;}
      div[data-testid="stVerticalBlockBorderWrapper"] {border-radius: 18px;}
      div.stButton > button {border-radius: 12px; min-height: 42px; font-weight: 650;}
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

tab_pesan, tab_film, tab_riwayat = st.tabs(["🎟️  Pesan tiket", "🎞️  Daftar film", "📋  Riwayat"])


with tab_film:
    st.subheader("Film yang tersedia")
    st.caption("Poster di bawah adalah ilustrasi vektor khusus untuk proyek ini.")
    for awal in range(0, len(DAFTAR_FILM), 2):
        kolom_kartu = st.columns(2, gap="large")
        for kolom, film in zip(kolom_kartu, DAFTAR_FILM[awal:awal + 2]):
            with kolom:
                with st.container(border=True):
                    kiri, kanan = st.columns([0.8, 1.2], gap="medium")
                    with kiri:
                        st.image(gambar_poster(film).encode("utf-8"), width=190)
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

    tanggal_tayang = st.date_input(
        "Tanggal menonton (hanya tahun 2026–2027)",
        value=None,
        min_value=TANGGAL_MINIMUM,
        max_value=TANGGAL_MAKSIMUM,
        format="DD/MM/YYYY",
        key="tanggal_tayang",
    )

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

    tanggal_valid = isinstance(tanggal_tayang, date) and TANGGAL_MINIMUM <= tanggal_tayang <= TANGGAL_MAKSIMUM
    jadwal_lengkap = bool(film and tanggal_valid and pilihan_jam)

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
            for offset in range(4):
                kolom_nomor = offset + 1
                kode = f"{baris}{kolom_nomor}"
                sudah_dipesan = kode in kursi_terpesan
                dipilih = kode in st.session_state.kursi_dipilih
                ikon = "🟥🪑" if sudah_dipesan else ("🟦🪑" if dipilih else "🟩🪑")
                with kiri:
                    if st.button(
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

                kolom_nomor_kanan = offset + 5
                kode_kanan = f"{baris}{kolom_nomor_kanan}"
                sudah_dipesan_kanan = kode_kanan in kursi_terpesan
                dipilih_kanan = kode_kanan in st.session_state.kursi_dipilih
                ikon_kanan = "🟥🪑" if sudah_dipesan_kanan else ("🟦🪑" if dipilih_kanan else "🟩🪑")
                with kanan:
                    if st.button(
                        f"{ikon_kanan} {kode_kanan}",
                        key=f"seat_{kunci_jadwal}_{kode_kanan}",
                        disabled=sudah_dipesan_kanan,
                        use_container_width=True,
                    ):
                        if dipilih_kanan:
                            st.session_state.kursi_dipilih.remove(kode_kanan)
                        else:
                            st.session_state.kursi_dipilih.add(kode_kanan)
                        st.rerun()
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
        st.info("Pilih film, tanggal menonton, dan jam tayang untuk menampilkan denah kursi.")

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
