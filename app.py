from datetime import date, datetime, timedelta

import streamlit as st


st.set_page_config(page_title="Bioskop Kelompok 2", page_icon="🎬", layout="centered")

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
    },
]

BARIS_KURSI = list("ABCDEFGH")
KOLOM_KURSI = 8
TAMBAHAN_AKHIR_PEKAN = 10000


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
    mulai = datetime.strptime(jam_mulai, "%H:%M")
    selesai = mulai + timedelta(minutes=durasi_menit)
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
    return [
        f"{baris}{kolom}"
        for baris in BARIS_KURSI
        for kolom in range(1, KOLOM_KURSI + 1)
    ]


if "kursi_terpesan" not in st.session_state:
    st.session_state.kursi_terpesan = {}
if "riwayat" not in st.session_state:
    st.session_state.riwayat = []
if "pesanan_terakhir" not in st.session_state:
    st.session_state.pesanan_terakhir = None


st.title("🎬 Bioskop Kelompok 2")
st.caption("Aplikasi pemesanan tiket bioskop")
tab_pesan, tab_film, tab_riwayat = st.tabs(
    ["Pesan tiket", "Daftar film", "Riwayat pemesanan"]
)


with tab_film:
    st.subheader("Daftar film")
    tanggal_info = date.today()
    for film in DAFTAR_FILM:
        with st.expander(film["judul"]):
            st.write(f"**Genre:** {film['genre']}")
            st.write(f"**Durasi:** {format_durasi(film['durasi_menit'])}")
            st.write(f"**Sutradara:** {film['sutradara']}")
            st.write(f"**Rating usia:** {film['usia']}")
            st.write(f"**Studio:** {film['studio']}")
            st.write(
                "**Jam tayang:** "
                + ", ".join(
                    f"{jam}-{waktu_selesai(jam, film['durasi_menit'])}"
                    for jam in film["jam"]
                )
            )
            st.write(f"**Harga hari ini:** {format_rupiah(harga_tiket(film, tanggal_info))}")


with tab_pesan:
    st.subheader("Formulir pemesanan")
    nama = st.text_input("Nama pemesan")
    judul_film = st.selectbox("Pilih film", [film["judul"] for film in DAFTAR_FILM])
    film = next(item for item in DAFTAR_FILM if item["judul"] == judul_film)

    st.write(f"**Genre:** {film['genre']}  ")
    st.write(f"**Durasi:** {format_durasi(film['durasi_menit'])}  ")
    st.write(f"**Rating usia:** {film['usia']}  ")

    tanggal_tayang = st.date_input("Tanggal menonton", value=date.today())
    jam_mulai = st.selectbox("Pilih jam tayang", film["jam"])
    kunci_jadwal = (film["judul"], str(tanggal_tayang), jam_mulai)
    terpesan = st.session_state.kursi_terpesan.get(kunci_jadwal, [])
    kursi_tersedia = [kursi for kursi in semua_kursi() if kursi not in terpesan]

    st.write(f"**Studio:** {film['studio']}")
    st.write(f"**Jam tayang:** {jam_mulai}-{waktu_selesai(jam_mulai, film['durasi_menit'])}")
    st.markdown("**Denah kursi** (O = tersedia, X = terpesan)")
    st.code(
        "        LAYAR\n\n"
        + "       KIRI       LORONG       KANAN\n"
        + "       1 2 3 4      ||      5 6 7 8\n"
        + "\n".join(
            f"{baris}      "
            + " ".join("X" if f"{baris}{kolom}" in terpesan else "O" for kolom in range(1, 5))
            + "       ||       "
            + " ".join("X" if f"{baris}{kolom}" in terpesan else "O" for kolom in range(5, 9))
            for baris in BARIS_KURSI
        ),
        language=None,
    )

    kursi_dipilih = st.multiselect(
        "Pilih kursi",
        options=kursi_tersedia,
        help="Kursi yang sudah dipesan untuk film, tanggal, dan jadwal ini tidak dapat dipilih.",
    )
    metode_bayar = st.selectbox("Metode pembayaran", ["Tunai", "Kartu debit", "QRIS"])
    harga = harga_tiket(film, tanggal_tayang)
    total_bayar = harga * len(kursi_dipilih)

    st.write(f"**Harga per tiket:** {format_rupiah(harga)}")
    st.write(f"**Jumlah tiket:** {len(kursi_dipilih)}")
    st.write(f"**Total bayar:** {format_rupiah(total_bayar)}")
    if tanggal_tayang.weekday() in (5, 6):
        st.info("Harga sudah termasuk tambahan akhir pekan sebesar Rp 10.000 per tiket.")

    if st.button("Konfirmasi pemesanan", type="primary", use_container_width=True):
        if not nama.strip():
            st.error("Nama pemesan tidak boleh kosong.")
        elif not kursi_dipilih:
            st.error("Pilih minimal satu kursi.")
        else:
            # Cek ulang sebelum menyimpan agar kursi tidak tercatat dua kali.
            kursi_terbaru = st.session_state.kursi_terpesan.get(kunci_jadwal, [])
            bentrok = [kursi for kursi in kursi_dipilih if kursi in kursi_terbaru]
            if bentrok:
                st.error("Kursi sudah dipesan: " + ", ".join(bentrok))
            else:
                st.session_state.kursi_terpesan.setdefault(kunci_jadwal, []).extend(kursi_dipilih)
                pesanan = {
                    "nama": nama.strip().title(),
                    "film": film["judul"],
                    "jam_mulai": jam_mulai,
                    "jam": f"{jam_mulai}-{waktu_selesai(jam_mulai, film['durasi_menit'])}",
                    "studio": film["studio"],
                    "kursi": list(kursi_dipilih),
                    "tanggal": tanggal_tayang.strftime("%d-%m-%Y"),
                    "harga_per_tiket": harga,
                    "total": total_bayar,
                    "pembayaran": metode_bayar,
                }
                st.session_state.riwayat.append(pesanan)
                st.session_state.pesanan_terakhir = pesanan
                st.success("Pemesanan berhasil!")

    if st.session_state.pesanan_terakhir:
        pesanan = st.session_state.pesanan_terakhir
        st.divider()
        st.subheader("Tiket terakhir")
        st.success(
            f"{pesanan['nama']} | {pesanan['film']} | {pesanan['tanggal']} "
            f"| {pesanan['jam']} | Studio {pesanan['studio']}"
        )
        for nomor, kursi in enumerate(pesanan["kursi"], start=1):
            st.markdown(
                f"**Tiket {nomor}**  \n"
                f"Film: {pesanan['film']}  \n"
                f"Tanggal: {pesanan['tanggal']}  \n"
                f"Jam: {pesanan['jam']}  \n"
                f"Studio: {pesanan['studio']}  \n"
                f"Kursi: {kursi}  \n"
                f"Harga: {format_rupiah(pesanan['harga_per_tiket'])}"
            )


with tab_riwayat:
    st.subheader("Riwayat pemesanan")
    if not st.session_state.riwayat:
        st.info("Belum ada pemesanan tiket.")
    else:
        for nomor, pesanan in enumerate(st.session_state.riwayat, start=1):
            with st.expander(f"{nomor}. {pesanan['nama']} - {pesanan['film']} ({pesanan['tanggal']})"):
                st.write(f"**Jam:** {pesanan['jam']}")
                st.write(f"**Studio:** {pesanan['studio']}")
                st.write(f"**Kursi:** {', '.join(pesanan['kursi'])}")
                st.write(f"**Pembayaran:** {pesanan['pembayaran']}")
                st.write(f"**Total:** {format_rupiah(pesanan['total'])}")

st.caption("Data pemesanan disimpan selama sesi aplikasi berjalan.")
