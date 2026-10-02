import cv2
import os


# ========================================================
# TAHAP 1 — CROP 9 GAMBAR
# ========================================================

dataset_folder = "dataset"
crop_folder = "hasil/crop"

os.makedirs(crop_folder, exist_ok=True)

files = [
    "01_HighQuality_Enhanced.jpg",
    "02_LowContrast.jpg",
    "03_Blurred.jpg",
    "04_HighNoise.jpg",
    "05_LowResolution_Upsampled.jpg",
    "06_Faded_Underexposed.jpg",
    "07_ColorShift_WarmTint.jpg",
    "08_JPEGCompression_Artifacts.jpg",
    "09_CombinedDegradation.jpg"
]


for nomor, filename in enumerate(files, start=1):

    print()
    print("========================================")
    print(f"TAHAP 1 - CROP GAMBAR {nomor} DARI 9")
    print(f"{filename}")
    print("========================================")

    image_path = os.path.join(
        dataset_folder,
        filename
    )

    image = cv2.imread(image_path)

    if image is None:
        print("Gambar tidak ditemukan!")
        continue

    # ROTASI
    rotated = cv2.rotate(
        image,
        cv2.ROTATE_90_CLOCKWISE
    )

    # PERBESAR
    scale = 4

    enlarged = cv2.resize(
        rotated,
        None,
        fx=scale,
        fy=scale,
        interpolation=cv2.INTER_CUBIC
    )

    # TAMPILKAN FOTO SECARA UTUH
    max_width = 700
    max_height = 500

    h, w = enlarged.shape[:2]

    display_scale = min(
        max_width / w,
        max_height / h,
        1
    )

    display_w = int(w * display_scale)
    display_h = int(h * display_scale)

    display = cv2.resize(
        enlarged,
        (display_w, display_h),
        interpolation=cv2.INTER_AREA
    )

    # CROP MANUAL
    window = f"GAMBAR {nomor} - CROP TANDA TANGAN"

    x, y, crop_w, crop_h = cv2.selectROI(
        window,
        display,
        showCrosshair=True,
        fromCenter=False
    )

    cv2.destroyAllWindows()

    if crop_w == 0 or crop_h == 0:
        print(f"Crop gambar {nomor} dibatalkan.")
        continue

    # KEMBALIKAN KOORDINAT
    x = int(x / display_scale)
    y = int(y / display_scale)
    crop_w = int(crop_w / display_scale)
    crop_h = int(crop_h / display_scale)

    # CROP
    crop = enlarged[
        y:y + crop_h,
        x:x + crop_w
    ]

    # SIMPAN CROP
    output_path = os.path.join(
        crop_folder,
        f"{nomor:02d}_crop.jpg"
    )

    cv2.imwrite(
        output_path,
        crop
    )

    print(f"✓ Gambar {nomor} berhasil di-crop.")


print()
print("========================================")
print("TAHAP 1 SELESAI")
print("9 GAMBAR SUDAH DI-CROP")
print("========================================")


# ========================================================
# TAHAP 2 — GRAYSCALE 9 GAMBAR
# ========================================================

grayscale_folder = "hasil/grayscale"

os.makedirs(
    grayscale_folder,
    exist_ok=True
)


for nomor in range(1, 10):

    print()
    print("========================================")
    print(f"TAHAP 2 - GRAYSCALE GAMBAR {nomor} DARI 9")
    print("========================================")

    # BACA HASIL CROP
    input_path = os.path.join(
        crop_folder,
        f"{nomor:02d}_crop.jpg"
    )

    image = cv2.imread(input_path)

    if image is None:
        print(f"File tidak ditemukan: {input_path}")
        continue

    # KONVERSI GRAYSCALE
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # SIMPAN GRAYSCALE
    output_path = os.path.join(
        grayscale_folder,
        f"{nomor:02d}_grayscale.jpg"
    )

    cv2.imwrite(
        output_path,
        gray
    )

    # TAMPILKAN
    cv2.imshow(
        f"GRAYSCALE GAMBAR {nomor}",
        gray
    )

    print(f"✓ Gambar {nomor} berhasil grayscale.")
    print("Tekan tombol apa saja untuk lanjut.")

    cv2.waitKey(0)
    cv2.destroyAllWindows()


print()
print("========================================")
print("TAHAP 2 SELESAI")
print("9 GAMBAR SUDAH MENJADI GRAYSCALE")
print("========================================")

# ========================================================
# TAHAP 3 — THRESHOLDING
# GLOBAL THRESHOLD DAN OTSU
# ========================================================

global_folder = "hasil/global_threshold"
otsu_folder = "hasil/otsu_threshold"

os.makedirs(
    global_folder,
    exist_ok=True
)

os.makedirs(
    otsu_folder,
    exist_ok=True
)


for nomor in range(1, 10):

    print()
    print("========================================")
    print(f"THRESHOLD GAMBAR {nomor} DARI 9")
    print("========================================")

    # ----------------------------------------------------
    # BACA GAMBAR GRAYSCALE
    # ----------------------------------------------------

    input_path = os.path.join(
        grayscale_folder,
        f"{nomor:02d}_grayscale.jpg"
    )

    gray = cv2.imread(
        input_path,
        cv2.IMREAD_GRAYSCALE
    )

    if gray is None:
        print(f"File tidak ditemukan: {input_path}")
        continue

    # ====================================================
    # 1. GLOBAL THRESHOLD
    # ====================================================

    _, global_threshold = cv2.threshold(
        gray,
        127,
        255,
        cv2.THRESH_BINARY
    )

    global_output = os.path.join(
        global_folder,
        f"{nomor:02d}_global.jpg"
    )

    cv2.imwrite(
        global_output,
        global_threshold
    )

    # ====================================================
    # 2. OTSU THRESHOLD
    # ====================================================

    otsu_value, otsu_threshold = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    otsu_output = os.path.join(
        otsu_folder,
        f"{nomor:02d}_otsu.jpg"
    )

    cv2.imwrite(
        otsu_output,
        otsu_threshold
    )

    # ====================================================
    # TAMPILKAN HASIL GLOBAL
    # ====================================================

    cv2.imshow(
        f"GLOBAL THRESHOLD - GAMBAR {nomor}",
        global_threshold
    )

    print("Global Threshold selesai.")
    print("Tekan tombol untuk melihat Otsu.")

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # ====================================================
    # TAMPILKAN HASIL OTSU
    # ====================================================

    cv2.imshow(
        f"OTSU THRESHOLD - GAMBAR {nomor}",
        otsu_threshold
    )

    print(f"Otsu selesai. Nilai Otsu = {otsu_value}")
    print("Tekan tombol untuk lanjut ke gambar berikutnya.")

    cv2.waitKey(0)
    cv2.destroyAllWindows()


# ========================================================
# SELESAI TAHAP 3
# ========================================================

print()
print("========================================")
print("TAHAP 3 SELESAI")
print("GLOBAL + OTSU UNTUK 9 GAMBAR")
print("========================================")
print("Hasil Global:")
print("hasil/global_threshold/")
print()
print("Hasil Otsu:")
print("hasil/otsu_threshold/")
print("========================================")

# ========================================================
# TAHAP 4 — MORPHOLOGICAL OPENING DAN CLOSING
# ========================================================

opening_folder = "hasil/morphology/opening"
closing_folder = "hasil/morphology/closing"

os.makedirs(
    opening_folder,
    exist_ok=True
)

os.makedirs(
    closing_folder,
    exist_ok=True
)


# KERNEL MORFOLOGI
kernel = cv2.getStructuringElement(
    cv2.MORPH_RECT,
    (3, 3)
)


for nomor in range(1, 10):

    print()
    print("========================================")
    print(f"MORFOLOGI GAMBAR {nomor} DARI 9")
    print("========================================")

    # ====================================================
    # BACA HASIL OTSU
    # ====================================================

    input_path = os.path.join(
        otsu_folder,
        f"{nomor:02d}_otsu.jpg"
    )

    otsu = cv2.imread(
        input_path,
        cv2.IMREAD_GRAYSCALE
    )

    if otsu is None:
        print(f"❌ File tidak ditemukan: {input_path}")
        continue

    # ====================================================
    # 1. OPENING
    # ====================================================

    opening = cv2.morphologyEx(
        otsu,
        cv2.MORPH_OPEN,
        kernel
    )

    opening_output = os.path.join(
        opening_folder,
        f"{nomor:02d}_opening.jpg"
    )

    cv2.imwrite(
        opening_output,
        opening
    )

    print("✓ Opening berhasil.")
    print("✓ Disimpan:", opening_output)

    # TAMPILKAN OPENING
    cv2.imshow(
        f"OPENING - GAMBAR {nomor}",
        opening
    )

    print("Opening sedang ditampilkan.")
    print("Tekan tombol untuk melihat Closing.")

    cv2.waitKey(0)
    cv2.destroyAllWindows()


    # ====================================================
    # 2. CLOSING
    # ====================================================

    closing = cv2.morphologyEx(
        otsu,
        cv2.MORPH_CLOSE,
        kernel
    )

    closing_output = os.path.join(
        closing_folder,
        f"{nomor:02d}_closing.jpg"
    )

    cv2.imwrite(
        closing_output,
        closing
    )

    print("✓ Closing berhasil.")
    print("✓ Disimpan:", closing_output)

    # TAMPILKAN CLOSING
    cv2.imshow(
        f"CLOSING - GAMBAR {nomor}",
        closing
    )

    print("👉 Closing sedang ditampilkan.")
    print("👉 Tekan tombol untuk lanjut ke gambar berikutnya.")

    cv2.waitKey(0)
    cv2.destroyAllWindows()


# ========================================================
# SELESAI TAHAP 4
# ========================================================

print()
print("========================================")
print("TAHAP 4 SELESAI")
print("OPENING + CLOSING UNTUK 9 GAMBAR")
print("========================================")
print("Hasil Opening:")
print("hasil/morphology/opening/")
print()
print("Hasil Closing:")
print("hasil/morphology/closing/")
print("========================================")

# ========================================================
# TAHAP 5 — MENGHITUNG LUAS AREA TANDA TANGAN
# ========================================================

area_folder = "hasil/area"

os.makedirs(
    area_folder,
    exist_ok=True
)


# FILE UNTUK MENYIMPAN HASIL AREA
area_file = os.path.join(
    area_folder,
    "hasil_area.txt"
)


with open(area_file, "w") as file:

    file.write("HASIL LUAS AREA TANDA TANGAN\n")
    file.write("========================================\n\n")


    for nomor in range(1, 10):

        print()
        print("========================================")
        print(f"AREA GAMBAR {nomor} DARI 9")
        print("========================================")

        # ====================================================
        # BACA HASIL CLOSING
        # ====================================================

        input_path = os.path.join(
            closing_folder,
            f"{nomor:02d}_closing.jpg"
        )

        image = cv2.imread(
            input_path,
            cv2.IMREAD_GRAYSCALE
        )

        if image is None:
            print(f"❌ File tidak ditemukan: {input_path}")
            continue

        # ====================================================
        # HITUNG JUMLAH PIXEL
        # ====================================================

        total_pixels = image.shape[0] * image.shape[1]

        # Karena hasil threshold menggunakan THRESH_BINARY,
        # tanda tangan berwarna hitam dan background putih.
        # Jadi kita hitung pixel hitam sebagai area tanda tangan.

        black_pixels = total_pixels - cv2.countNonZero(image)

        # Persentase area tanda tangan
        area_percentage = (
            black_pixels / total_pixels
        ) * 100

        # ====================================================
        # TAMPILKAN HASIL
        # ====================================================

        print(f"Total pixel       : {total_pixels}")
        print(f"Pixel tanda tangan: {black_pixels}")
        print(f"Persentase area   : {area_percentage:.2f}%")

        # ====================================================
        # SIMPAN HASIL
        # ====================================================

        file.write(
            f"Gambar {nomor:02d}\n"
        )

        file.write(
            f"Total pixel       : {total_pixels}\n"
        )

        file.write(
            f"Pixel tanda tangan: {black_pixels}\n"
        )

        file.write(
            f"Persentase area   : {area_percentage:.2f}%\n"
        )

        file.write(
            "----------------------------------------\n"
        )


# ========================================================
# SELESAI TAHAP 5
# ========================================================

print()
print("========================================")
print("TAHAP 5 SELESAI")
print("PERHITUNGAN AREA TANDA TANGAN SELESAI")
print("========================================")
print("Hasil disimpan di:")
print("hasil/area/hasil_area.txt")
print("========================================")

# ========================================================
# TAHAP 6 — DETEKSI SIGNATURE PRESENT / ABSENT
# ========================================================

detection_folder = "hasil/detection"

os.makedirs(
    detection_folder,
    exist_ok=True
)


# ========================================================
# BATAS AREA
# ========================================================
# Nilai ini digunakan sebagai batas awal.
# Nanti dapat disesuaikan setelah diuji dengan
# gambar yang memiliki dan tidak memiliki tanda tangan.

AREA_THRESHOLD = 1.0


# FILE HASIL DETEKSI
detection_file = os.path.join(
    detection_folder,
    "hasil_deteksi.txt"
)


with open(detection_file, "w") as file:

    file.write("HASIL DETEKSI TANDA TANGAN\n")
    file.write("========================================\n")
    file.write(
        f"Area Threshold = {AREA_THRESHOLD:.2f}%\n\n"
    )


    for nomor in range(1, 10):

        print()
        print("========================================")
        print(f"DETEKSI GAMBAR {nomor} DARI 9")
        print("========================================")

        # BACA HASIL CLOSING
        input_path = os.path.join(
            closing_folder,
            f"{nomor:02d}_closing.jpg"
        )

        image = cv2.imread(
            input_path,
            cv2.IMREAD_GRAYSCALE
        )

        if image is None:
            print(f"❌ File tidak ditemukan: {input_path}")
            continue

        # ====================================================
        # HITUNG AREA TANDA TANGAN
        # ====================================================

        total_pixels = image.shape[0] * image.shape[1]

        black_pixels = (
            total_pixels -
            cv2.countNonZero(image)
        )

        area_percentage = (
            black_pixels /
            total_pixels
        ) * 100

        # ====================================================
        # ATURAN DETEKSI
        # ====================================================

        if area_percentage >= AREA_THRESHOLD:

            result = "SIGNATURE PRESENT"

        else:

            result = "SIGNATURE ABSENT"

        # ====================================================
        # TAMPILKAN HASIL
        # ====================================================

        print(
            f"Area tanda tangan : {area_percentage:.2f}%"
        )

        print(
            f"Hasil deteksi     : {result}"
        )

        # ====================================================
        # SIMPAN HASIL
        # ====================================================

        file.write(
            f"Gambar {nomor:02d}\n"
        )

        file.write(
            f"Area tanda tangan : "
            f"{area_percentage:.2f}%\n"
        )

        file.write(
            f"Hasil deteksi     : {result}\n"
        )

        file.write(
            "----------------------------------------\n"
        )


# ========================================================
# SELESAI TAHAP 6
# ========================================================

print()
print("========================================")
print("TAHAP 6 SELESAI")
print("DETEKSI SIGNATURE PRESENT / ABSENT")
print("========================================")
print("Area Threshold:", AREA_THRESHOLD, "%")
print("Hasil disimpan di:")
print("hasil/detection/hasil_deteksi.txt")
print("========================================")

# ========================================================
# TAHAP 7 — TABEL HASIL PENGUJIAN
# ========================================================

testing_folder = "hasil/testing"

os.makedirs(
    testing_folder,
    exist_ok=True
)

# Kondisi 9 gambar
conditions = [
    "High Quality",
    "Low Contrast",
    "Blurred",
    "High Noise",
    "Low Resolution",
    "Faded / Underexposed",
    "Color Shift / Warm Tint",
    "JPEG Compression",
    "Combined Degradation"
]

# ========================================================
# BACA HASIL AREA DARI TAHAP 5
# ========================================================

area_file = "hasil/area/hasil_area.txt"

area_data = {}

with open(
    area_file,
    "r",
    encoding="utf-8"
) as file:

    current_number = None

    for line in file:

        line = line.strip()

        # Contoh:
        # Gambar 01
        if line.startswith("Gambar"):

            current_number = line.replace(
                "Gambar",
                ""
            ).strip()

        # Contoh:
        # Persentase area   : 2.20%
        elif line.startswith("Persentase area"):

            if current_number is not None:

                nilai = line.split(":")[1].strip()

                nilai = nilai.replace(
                    "%",
                    ""
                )

                area_data[current_number] = nilai


# ========================================================
# BACA HASIL DETEKSI DARI TAHAP 6
# ========================================================

detection_file = "hasil/detection/hasil_deteksi.txt"

detection_data = {}

with open(
    detection_file,
    "r",
    encoding="utf-8"
) as file:

    current_number = None

    for line in file:

        line = line.strip()

        # Contoh:
        # Gambar 01
        if line.startswith("Gambar"):

            current_number = line.replace(
                "Gambar",
                ""
            ).strip()

        # Contoh:
        # Hasil deteksi : SIGNATURE PRESENT
        elif line.startswith("Hasil deteksi"):

            if current_number is not None:

                hasil = line.split(":")[1].strip()

                detection_data[current_number] = hasil


# ========================================================
# BUAT TABEL MARKDOWN
# ========================================================

markdown_file = os.path.join(
    testing_folder,
    "tabel_hasil_pengujian.md"
)

with open(
    markdown_file,
    "w",
    encoding="utf-8"
) as file:

    file.write("# Tabel Hasil Pengujian\n\n")

    file.write(
        "| No | Kondisi Gambar | Area Tanda Tangan (%) | "
        "Ground Truth | Hasil Deteksi | Keterangan |\n"
    )

    file.write(
        "|---|---|---:|---|---|---|\n"
    )

    for nomor in range(1, 10):

        no = f"{nomor:02d}"

        area = area_data.get(
            no,
            "-"
        )

        hasil = detection_data.get(
            no,
            "-"
        )

        # Karena 9 dataset yang digunakan
        # semuanya memiliki tanda tangan
        ground_truth = "SIGNATURE PRESENT"

        if hasil == ground_truth:

            keterangan = "Benar"

        else:

            keterangan = "Salah"

        file.write(
            f"| {no} | {conditions[nomor - 1]} | "
            f"{area} | {ground_truth} | "
            f"{hasil} | {keterangan} |\n"
        )


# ========================================================
# SELESAI
# ========================================================

print()
print("========================================")
print("TAHAP 7 SELESAI")
print("========================================")

print("Tabel hasil pengujian berhasil dibuat.")

print(f"Lokasi:")
print(markdown_file)

# ========================================================
# TAHAP 8 — PENGUJIAN CITRA TANPA TANDA TANGAN
# ========================================================

import glob
import numpy as np

print()
print("========================================")
print("TAHAP 8 — PENGUJIAN CITRA TANPA TANDA TANGAN")
print("========================================")

# Folder hasil
testing_absent_folder = "hasil/testing_absent"

os.makedirs(
    testing_absent_folder,
    exist_ok=True
)

# ========================================================
# CARI FILE 10, 11, DAN 12 SECARA OTOMATIS
# ========================================================

absent_files = []

for nomor in range(10, 13):

    pola = os.path.join(
        dataset_folder,
        f"{nomor:02d}_NoSignature_*"
    )

    hasil_cari = glob.glob(pola)

    if len(hasil_cari) > 0:

        absent_files.append(
            hasil_cari[0]
        )

    else:

        print()
        print(f"File gambar {nomor} tidak ditemukan.")

# ========================================================
# THRESHOLD DETEKSI
# ========================================================

AREA_THRESHOLD = 1.0


# ========================================================
# PROSES GAMBAR 10-12
# ========================================================

for nomor, path in enumerate(
    absent_files,
    start=10
):

    filename = os.path.basename(path)

    print()
    print("----------------------------------------")
    print(f"PENGUJIAN GAMBAR {nomor}")
    print(f"File: {filename}")
    print("----------------------------------------")

    # ====================================================
    # BACA GAMBAR
    # ====================================================

    try:

        data = np.fromfile(
            path,
            dtype=np.uint8
        )

        image = cv2.imdecode(
            data,
            cv2.IMREAD_COLOR
        )

    except Exception as error:

        print("Gagal membaca gambar.")
        print(error)
        continue

    if image is None:

        print("Gambar tidak dapat dibaca OpenCV.")
        continue

    print("✓ Gambar berhasil dibaca.")

    # ====================================================
    # ROTASI
    # ====================================================

    rotated = cv2.rotate(
        image,
        cv2.ROTATE_90_CLOCKWISE
    )

    # ====================================================
    # PERBESAR
    # ====================================================

    scale = 4

    enlarged = cv2.resize(
        rotated,
        None,
        fx=scale,
        fy=scale,
        interpolation=cv2.INTER_CUBIC
    )

    # ====================================================
    # TAMPILKAN FOTO FULL
    # ====================================================

    max_width = 700
    max_height = 500

    h, w = enlarged.shape[:2]

    display_scale = min(
        max_width / w,
        max_height / h,
        1
    )

    display_w = int(
        w * display_scale
    )

    display_h = int(
        h * display_scale
    )

    display = cv2.resize(
        enlarged,
        (display_w, display_h),
        interpolation=cv2.INTER_AREA
    )

    window = f"GAMBAR {nomor} - CROP"

    cv2.namedWindow(
        window,
        cv2.WINDOW_AUTOSIZE
    )

    # ====================================================
    # CROP MANUAL
    # ====================================================

    x, y, crop_w, crop_h = cv2.selectROI(
        window,
        display,
        showCrosshair=True,
        fromCenter=False
    )

    cv2.destroyWindow(window)

    if crop_w == 0 or crop_h == 0:

        print("Crop dibatalkan.")
        continue

    # ====================================================
    # KEMBALIKAN KOORDINAT
    # ====================================================

    x = int(
        x / display_scale
    )

    y = int(
        y / display_scale
    )

    crop_w = int(
        crop_w / display_scale
    )

    crop_h = int(
        crop_h / display_scale
    )

    # ====================================================
    # CROP
    # ====================================================

    crop = enlarged[
        y:y + crop_h,
        x:x + crop_w
    ]

    # ====================================================
    # GRAYSCALE
    # ====================================================

    gray = cv2.cvtColor(
        crop,
        cv2.COLOR_BGR2GRAY
    )

    # ====================================================
    # OTSU THRESHOLD
    # ====================================================

    _, otsu = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # ====================================================
    # MORPHOLOGY CLOSING
    # ====================================================

    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (3, 3)
    )

    closing = cv2.morphologyEx(
        otsu,
        cv2.MORPH_CLOSE,
        kernel
    )

    # ====================================================
    # HITUNG AREA
    # ====================================================

    total_pixels = (
        closing.shape[0] *
        closing.shape[1]
    )

    black_pixels = (
        total_pixels -
        cv2.countNonZero(closing)
    )

    area_percentage = (
        black_pixels /
        total_pixels *
        100
    )

    # ====================================================
    # DETEKSI
    # ====================================================

    if area_percentage >= AREA_THRESHOLD:

        result = "SIGNATURE PRESENT"

    else:

        result = "SIGNATURE ABSENT"

    # ====================================================
    # SIMPAN HASIL
    # ====================================================

    output_image = os.path.join(
        testing_absent_folder,
        f"{nomor:02d}_hasil.jpg"
    )

    cv2.imwrite(
        output_image,
        closing
    )

    # ====================================================
    # TAMPILKAN HASIL
    # ====================================================

    cv2.imshow(
        f"HASIL DETEKSI {nomor}",
        closing
    )

    print()
    print(f"Area tanda tangan : {area_percentage:.2f}%")
    print(f"Hasil deteksi     : {result}")
    print()
    print("Tekan tombol apa saja untuk lanjut.")

    cv2.waitKey(0)
    cv2.destroyAllWindows()


# ========================================================
# SELESAI TAHAP 8
# ========================================================

print()
print("========================================")
print("TAHAP 8 SELESAI")
print("========================================")

print(
    f"Hasil disimpan di: {testing_absent_folder}"
)

# ========================================================
# CEK FILE 10-12
# ========================================================

import os

print()
print("========================================")
print("CEK FILE 10-12")
print("========================================")

for nomor in range(10, 13):

    pola = os.path.join(
        "dataset",
        f"{nomor:02d}_NoSignature_*"
    )

    import glob

    files = glob.glob(pola)

    print()
    print(f"Gambar {nomor}")

    if len(files) == 0:
        print("❌ File tidak ditemukan")
        continue

    for file in files:

        print("Nama :", file)
        print("Ada  :", os.path.exists(file))
        print("Size :", os.path.getsize(file), "bytes")