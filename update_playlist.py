import requests

def ekstrak_playlist(url_sumber, daftar_pencarian, nama_file_output):
    print(f"Mengunduh database dari {url_sumber}...\n")
    
    try:
        # Menambahkan User-Agent agar tidak dicurigai sebagai bot jahat oleh server sumber
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        
        # stream=True menjaga RAM tetap aman jika file sumber berukuran puluhan MB
        response = requests.get(url_sumber, headers=headers, stream=True, timeout=30)
        response.raise_for_status()
        
        tangkap_url = False
        baris_info = ""
        hasil_m3u = ["#EXTM3U\n"]
        total_ditemukan = 0
        
        for baris in response.iter_lines():
            if baris:
                teks_baris = baris.decode('utf-8')
                
                # Memeriksa baris yang berisi metadata/nama channel
                if teks_baris.startswith("#EXTINF"):
                    cocok = False
                    
                    if not daftar_pencarian:
                        cocok = True
                    else:
                        for kata in daftar_pencarian:
                            if kata.lower() in teks_baris.lower():
                                cocok = True
                                break
                    
                    if cocok:
                        baris_info = teks_baris
                        tangkap_url = True
                
                # Menangkap URL di baris selanjutnya
                elif tangkap_url and not teks_baris.startswith("#"):
                    hasil_m3u.append(f"{baris_info}\n{teks_baris}\n")
                    total_ditemukan += 1
                    tangkap_url = False
                    
        # Menyimpan output
        if total_ditemukan > 0:
            with open(nama_file_output, "w", encoding="utf-8") as f:
                f.writelines(hasil_m3u)
            print(f"✅ Selesai! {total_ditemukan} saluran berhasil disimpan ke '{nama_file_output}'.")
        else:
            print("❌ Tidak ada saluran yang cocok dengan kata kunci.")
            
    except Exception as e:
        print(f"Gagal memproses data: {e}")

if __name__ == "__main__":
    # 1. Ganti URL ini dengan sumber M3U mentah apa pun (Pastebin, Github Raw, dll)
    url_target = "https://iptv-org.github.io/iptv/index.m3u"
    
    # 2. Tambahkan kata kunci channel yang ingin Anda saring
    channel_pilihan = ["spotv", "kompas", "cnn indonesia", "tvone", "berita satu"]
    
    # 3. Nama file hasil kompilasi
    file_hasil = "playlist_custom.m3u"
    
    ekstrak_playlist(url_target, channel_pilihan, file_hasil)
