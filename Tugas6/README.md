# Final-Project-Pemrograman-Jaringan-C-Kel-5
Final project untuk mata kuliah pemrograman jaringan kelas C semester genap tahun 2022/2023
## Nama Anggota Kelompok 5
<table>
<tr><td>Name</td><td>NRP</td></tr>
<tr><td>Antonio Taifan Montana</td><td> 5025201219</td></tr>
<tr><td>Cahyadi Surya Nugraha</td><td> 5025201184</td></tr>
<tr><td>Frederick Wijayadi Susilo</td><td>5025201111</td></tr>
<tr><td>Marcellino Mahesa Janitra</td><td> 5025201105</td></tr>
<tr><td>Muhammad Afdal Abdallah</td><td> 5025201163</td></tr>
<tr><td>Naufal Ariq Putra Yosyam</td><td>5025201112</td></tr>
</table>

## Deskripsi
Aplikasi ChatKuy merupakan aplikasi chat yang dapat melakukan komunikasi chat yang dapat diteruskan antar realm. ChatKuy memiliki kemampuan untuk melakukan private message, group message, dan mengirimkan file. Aplikasi dibangun dengan dasar arsitektur pada implementasi tugas chat protocol pada tugas 6 Pemrograman Jaringan C. Arsitektur yang dimaksud yaitu arsitektur multi realm, yaitu kemampuan sistem untuk mendukung atau berinteraksi dengan beberapa lingkungan atau domain yang berbeda secara bersamaan. Setiap lingkungan atau domain memiliki protokol, hak akses, atau pengaturan yang berbeda. Dalam implementasinya, konsep multi realm dapat mencakup pengaturan seperti konfigurasi basis data yang berbeda, integrasi dengan direktori yang berbeda, kebijakan keamanan yang berbeda, dan mekanisme otorisasi yang sesuai dengan lingkungan atau domain yang relevan.

## Arsitektur
![arsitektur](https://github.com/Chroax/Final-Project-Pemrograman-Jaringan-C-Kel-5/assets/101288815/1296d100-13c1-45f7-882a-0cd306822cdc)

IP Address pada Server 1 yang digunakan 0.0.0.0 .<br>
Port pada Server 1 yang akan digunakan 8889.<br>
IP Address pada Client 1 yang digunakan 192.168.xx.xx (Sesuai dengan IP Jaringan yang terhubung pada device). <br>
Port pada Client 1 yang akan digunakan 8889.<br>

IP Address pada Server 2 yang digunakan 0.0.0.0. <br>
Port pada Server 2 yang akan digunakan 1234 (Dapat disesuaikan dengan server kelompok lain).<br>
IP Address pada Client 2 yang digunakan 192.168.xx.xx (Sesuai dengan IP Jaringan yang terhubung pada device). <br>
Port pada Client 2 yang akan digunakan 1234 (Dapat disesuaikan dengan client kelompok lain).<br>
<br>
**Jaringan yang digunakan di 2 server atau lebih harus sama.**

## Cara Menjalankan Server dan Client

### Melihat IP address pada device
![image](https://github.com/Chroax/Final-Project-Pemrograman-Jaringan-C-Kel-5/assets/101288815/71b0e752-6569-49f4-bf50-eb20f514c0d1)
- Ketik ipconfig pada command prompt <br>

![image](https://github.com/Chroax/Final-Project-Pemrograman-Jaringan-C-Kel-5/assets/101288815/59b2c7ca-ed89-4aa7-b0ee-22176ec14ad6)
- Lalu lihat IP4v Address pada Wireless LAN adapter Wi-Fi, pada case ini ip yang nanti akan digunakan pada client adalah ***192.168.18.22***


## Protokol
Untuk protokol bisa dilihat pada link berikut :
https://github.com/Chroax/Final-Project-Pemrograman-Jaringan-C-Kel-5/blob/main/PROTOCOL.md
