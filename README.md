# deteksi-tanda-tangan
Deteksi tanda tangan Rektor menggunakan Python dan OpenCV
NAMA : RISMA DWI AZ-ZAHRA
NIM : F1G124016
KELAS : B

# Mini-Project: Deteksi Tanda Tangan Rektor (Signature Detection)

Proyek ini merupakan implementasi sederhana dari pengolahan citra untuk mendeteksi keberadaan tanda tangan Rektor pada dokumen menggunakan Python dan OpenCV. Proses deteksi dilakukan dengan mengambil area tanda tangan dari dokumen, kemudian melakukan beberapa tahap pengolahan citra seperti grayscale, thresholding, dan morphology. Hasil dari proses tersebut digunakan untuk menghitung luas area tanda tangan dan menentukan apakah tanda tangan terdeteksi atau tidak.

## Alur Pemrosesan (Pipeline)

1. Rotasi dan Perbesaran: Citra diputar 90° searah jarum jam agar posisi dokumen sesuai dengan kebutuhan proses. Setelah itu, citra diperbesar 4 kali untuk mempermudah proses melihat dan menentukan area tanda tangan saat melakukan cropping.

2. Region of Interest (ROI) Cropping: Memotong area tanda tangan pada masing-masing gambar secara manual. Tahap ini dilakukan agar proses pengolahan hanya berfokus pada bagian dokumen yang terdapat tanda tangan dan tidak memproses seluruh bagian dokumen.

3. Grayscale Conversion: Mengubah citra hasil crop dari citra berwarna menjadi citra grayscale. Dengan menggunakan grayscale, citra hanya memiliki satu nilai intensitas piksel sehingga lebih mudah digunakan untuk proses thresholding.

4. Thresholding (Global & Otsu): Mengubah citra grayscale menjadi citra biner untuk memisahkan tanda tangan dari latar belakang. Digunakan Global Threshold dengan nilai 127 dan Otsu Threshold secara otomatis. Global Threshold menggunakan nilai batas yang sudah ditentukan, sedangkan Otsu menentukan nilai threshold berdasarkan distribusi intensitas piksel pada gambar.

5. Morphological Operations:
   - Opening digunakan untuk membantu mengurangi noise atau titik-titik kecil yang muncul setelah proses thresholding.
   - Closing digunakan untuk membantu menyambungkan bagian tanda tangan yang terputus atau memiliki celah kecil sehingga bentuk tanda tangan menjadi lebih jelas.

6. Area Calculation: Menghitung persentase area tanda tangan berdasarkan jumlah piksel objek terhadap total piksel pada area crop. Hasil perhitungan digunakan untuk mengetahui seberapa besar bagian area crop yang dianggap sebagai tanda tangan.

7. Signature Detection: Hasil perhitungan area digunakan untuk menentukan keberadaan tanda tangan. Jika luas area tanda tangan ≥ 1%, sistem menyimpulkan SIGNATURE PRESENT. Jika luas area kurang dari 1%, sistem menyimpulkan SIGNATURE ABSENT.

## Hasil Pengujian

Sistem diuji menggunakan 9 citra yang memiliki tanda tangan dengan kondisi kualitas gambar yang berbeda. Setiap gambar memiliki kondisi yang berbeda, seperti kualitas tinggi, kontras rendah, blur, noise, resolusi rendah, gambar pudar, perubahan warna, artefak kompresi JPEG, dan gabungan beberapa kondisi degradasi.

Dari hasil eksekusi program, diperoleh data sebagai berikut:

- 01_HighQuality_Enhanced: 2.18% (PRESENT)
- 02_LowContrast: 2.12% (PRESENT)
- 03_Blurred: 3.58% (PRESENT)
- 04_HighNoise: 1.73% (PRESENT)
- 05_LowResolution_Upsampled: 2.53% (PRESENT)
- 06_Faded_Underexposed: 2.13% (PRESENT)
- 07_ColorShift_WarmTint: 2.08% (PRESENT)
- 08_JPEGCompression_Artifacts: 2.06% (PRESENT)
- 09_CombinedDegradation: 2.58% (PRESENT)

Dari 9 citra yang diuji, seluruh gambar berhasil terdeteksi sebagai SIGNATURE PRESENT. Persentase area tanda tangan yang diperoleh berada pada kisaran 1.73% sampai 3.58%. Nilai tersebut kemudian dibandingkan dengan batas area sebesar 1% untuk menentukan hasil deteksi.

## Analisis & Kesimpulan

1. Mengapa thresholding diperlukan sebelum melakukan analisis keberadaan tanda tangan?

Thresholding diperlukan untuk mengubah citra grayscale menjadi citra biner sehingga tanda tangan dapat dipisahkan dari latar belakang. Dengan hasil biner tersebut, piksel yang dianggap sebagai bagian dari tanda tangan dapat dihitung sehingga luas area tanda tangan dapat diperoleh dalam bentuk persentase.

Pada project ini digunakan Global Threshold dan Otsu Threshold. Hasil thresholding kemudian digunakan untuk proses morphology dan perhitungan area. Dengan tahapan tersebut, sistem dapat menggunakan luas area sebagai salah satu dasar untuk menentukan apakah tanda tangan terdapat pada area yang telah dipotong.

2. Apa masalah yang terjadi jika threshold terlalu tinggi atau terlalu rendah?

- Jika Threshold Terlalu Rendah: Bagian tanda tangan yang tipis, kurang jelas, atau pudar dapat hilang dan dianggap sebagai background. Hal ini dapat membuat jumlah piksel tanda tangan menjadi lebih sedikit sehingga luas area yang dihitung menjadi terlalu kecil. Jika hasilnya berada di bawah batas yang ditentukan, tanda tangan dapat dianggap tidak ada (False Negative).

- Jika Threshold Terlalu Tinggi: Noise, tekstur kertas, tulisan, atau bagian lain dari dokumen dapat ikut dianggap sebagai objek tanda tangan. Hal ini dapat menyebabkan jumlah piksel objek menjadi terlalu banyak dan luas area menjadi lebih besar dari kondisi sebenarnya. Akibatnya, sistem dapat mendeteksi tanda tangan meskipun objek yang terdeteksi bukan tanda tangan (False Positive).

- Solusi yang Diterapkan: Penggunaan Global Threshold dan Otsu Threshold, kemudian dilanjutkan dengan proses morphology dan perhitungan area. Pada project ini digunakan batas area sebesar 1% sebagai dasar untuk menentukan hasil deteksi. Berdasarkan hasil pengujian, seluruh 9 gambar berhasil terdeteksi sebagai SIGNATURE PRESENT dengan luas area berada pada kisaran 1.73%–3.58%.

Secara keseluruhan, tahapan pengolahan citra yang digunakan dapat membantu sistem dalam memisahkan area tanda tangan dari background dan melakukan deteksi berdasarkan luas area yang diperoleh.
