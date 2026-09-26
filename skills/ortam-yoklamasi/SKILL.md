---
name: ortam-yoklamasi
description: Bir işe girmeden önce o işin dayandığı ortam gerçeklerini tek çağrıda yoklar — nerede çalışıyor, hangi yetki var, hangi kabuk, süreci kim başlatmalı. Varsayımla teşhise girmeyi ve imkânsız yolları sırayla denemeyi önler. "çalışmıyor", "açılmıyor", "bozuldu", "şuna bak", "sistemde şunu yap", "servisi başlat", "masaüstünü değiştir" dendiğinde veya uzaktan oturumda, sistem düzeyinde, uzun ömürlü bir süreçle ya da eski bir nota dayanarak işe başlarken kullan.
---

# Ortam yoklaması

Tek ilke: **varsayım bir kanıt değil, bir borçtur.** İşe girmeden önce tek çağrıda ödenirse
ucuz; ödenmezse teşhisin ortasında faiziyle çıkar.

Bu, `kabul-kontrolu` skill'inin aynadaki kardeşidir. O "iş bittiğinde sonucu kendi elinle
ölç" der; bu "işe başlamadan önce zemini kendi elinle yokla" der. İkisinin ortak düşmanı
aynı: ekranda doğru görünen, gerçekte yanlış olan bir cümle.

## Yoklama tablosu

| Durum | Başlamadan önce yokla | Nereden geldi |
| --- | --- | --- |
| Kullanıcı "çalışmıyor / açılmıyor" dedi | **Tam olarak nerede?** Hangi adres, hangi cihaz, hangi tarayıcı. Yerel sunucu mu, GitHub Pages mi, telefon mu | 0031 |
| Elinde eski bir proje notu var | Not **varsayım kaynağıdır, kanıt değil**. Teşhise girmeden önce notun hâlâ doğru olduğunu tek komutla doğrula | 0031 |
| Sistem düzeyinde iş (servis, güç, ağ, paket) | Tek çağrıda: `sudo -n true`, `loginctl list-sessions`, kabuk türü. Yetki yoksa imkânsız yollar baştan elenir | 0033 |
| Uzaktan oturum | Grafik oturum var mı, ekran kilitli mi, hangi kullanıcı. Uzaktan çalışan bir komut masaüstünü göremez | 0033 |
| Kabuk fish | `&`, `export`, `$(...)` bash'ten farklı davranır. Arka plana atma ve değişken atama sözdizimini yazmadan önce kontrol et | 0033 |
| Uzun ömürlü süreç başlatma (masaüstü, servis, daemon) | **Ajan kabuğundan başlatma.** Kendi yöneticisinden başlat: `systemctl --user restart plasma-plasmashell.service` | 0017 |
| Araç veya MCP "bulunamadı" | Önce o işi yürüten skill dosyasının "doğrulanmış gerçekler" bölümüne bak. Paket flatpak/snap olabilir; yokluk sanılan şey çoğu zaman farklı yerde duruyordur | 0009, 0013 |

## Miras alınan ortam sessizce yayılır

Ajan kabuğundan başlatılan bir süreç, o kabuğun bütün ortamını (`LC_ALL`, `PATH`, `DISPLAY`)
miras alır ve **kendinden sonra açılan her şeye geçirir**. plasmashell böyle yeniden
başlatıldığında `LC_ALL=C` mirası bütün masaüstünü İngilizceye çevirdi; kullanıcı saatler sonra
fark etti, aynı dönemde simge teması da sessizce değişmişti.

Bu yüzden bir masaüstü veya sistem ayarı değiştirildikten sonra yalnızca **değiştirilen**
ayar değil, **çevresindeki** ayarlar da bir kez doğrulanır: dil, tema, simge, klavye.

## Maliyet sınırı

Yoklama **tek çağrıdır**, keşif turu değil. Birden fazla kontrol gerekiyorsa aynı komuta
birleştirilir. Beş ayrı yoklama çağrısı, önlediği yanlış teşhisten pahalıya gelir —
gözlem 0033'te beş yol sırayla denendi, tek çağrılık yoklama dördünü baştan elerdi.

Geri alınabilir, tek adımlı ve zemini zaten bilinen işlerde atlanır.
