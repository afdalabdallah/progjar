### Login

`auth [username] [password]`

- Tujuan: autentikasi pengguna terdaftar
- Parameter:
  - username: username yang digunakan pengguna
  - password: password yang digunakan pengguna

### Register

`register [username] [password] [name] [country]`

- Tujuan: mendaftarkan data pengguna
- Parameter:
  - username: username yang digunakan pengguna
  - password: password yang digunakan pengguna
  - name: nama lengkap pengguna
  - country: negara pengguna

### Logout

`logout`

- Tujuan: untuk keluar dari akun atau aplikasi
- Parameter: -

### Send Private

`sendprivate [receiver] [message] `

- Tujuan: mengirimkan pesan secara privat
- Parameter:
  - receiver: nama penerima
  - message: pesan yang dikirimkan

### Send Private File

`sendprivatefile [receiver] [filepath]`

- Tujuan: mengirimkan file secara privat
- Parameter:
  - receiver: nama penerima
  - filepath: lokasi file yang ingin dikirim

### Send Group

`sendgroup [group_receiver] [message]`

- Tujuan: mengirimkan pesan ke banyak orang
- Parameter:
  - group_receiver: group penerima pesan
  - message: pesan yang dikirimkan

### Send Group File

`sendgroupfile [group_receiver] [message]`

- Tujuan: mengirimkan file ke banyak orang
- Parameter:
  - group_receiver: group penerima pesan
  - message: pesan yang akan dikirimkan

### Inbox

`inbox`

- Tujuan: menampilkan pesan yang belum terbaca
- Parameter: -

### Add Realm

`addrealm [realm_id] [realm_address_to] [realm_port_to]`

- Tujuan: menambahkan jembatan realm baru sebagai penghubung antara 2 server
- Parameter:
  - realm_id: nama jembatan realm yang menjadi identitas
  - realm_address_to: ip address dari server yang ingin disambungkan
  - realm_port_to: port dari server yang ingin disambungkan

### List Connected Realm

`connectedrealm`

- Tujuan: menampilkan semua jembatan realm yang terhubung pada suatu server
- Parameter: -

### Send Private Realm

`sendprivaterealm [realm_id] [receiver] [message]`

- Tujuan: mengirimkan pesan secara privat ke pengguna pada server lain yang telah tersambung
- Parameter:
  - realm_id: nama jembatan realm yang menjadi identitas
  - receiver: penerima pesan yang dikirim
  - message: pesan yang akan dikirimkan

### Send Private File Realm

`sendprivatefilerealm [realm_id] [receiver] [filepath]`

- Tujuan: mengirimkan file secara privat ke pengguna pada server lain yang telah tersambung
- Parameter:
  - realm_id: nama jembatan realm yang menjadi identitas
  - receiver: penerima file yang dikirim
  - filepath: lokasi file yang mau dikirimkan

### Send Group Realm

`sendgrouprealm [realm_id] [group_receiver] [message]`

- Tujuan: mengirimkan pesan ke beberapa orang pada server lain yang telah tersambung
- Parameter:
  - realm_id: nama jembatan realm yang menjadi identitas
  - group_receiver: penerima pesan yang dikirim
  - message: pesan yang akan dikirimkan

### Send Group File Realm

`sendgroupfilerealm [realm_id] [group_receiver] [filepath]`

- Tujuan: mengirimkan file ke beberapa orang pada server lain yang telah tersambung
- Parameter:
  - realm_id: nama jembatan realm yang menjadi identitas
  - group_receiver: penerima file yang dikirim
  - filepath: lokasi file yang ingin dikirimkan

### Inbox Realm

`inboxrealm [realm_id]`

- Tujuan: menampilkan pesan yang belum dibaca pada server yang terhubung pada jembatan realm yang sama
- Parameter:
  - realm_id: nama jembatan realm yang menjadi identitas

### Login Info

`login_info`

- Tujuan: melihat info dari pengguna yang aktif
- Parameter: -
