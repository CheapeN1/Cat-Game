import pgzrun  # Bu, pgzero'nun çalışabilmesi için gerekli
from pgzero.actor import Actor
import random

# Oyun ekran boyutları
WIDTH = 800
HEIGHT = 320

# Arka plan
background = "bg_city"  # Arka plan resmi (bg_city.gif)
background_x1 = 0  # İlk arka planın x pozisyonu
background_x2 = -WIDTH  # İkinci arka planın x pozisyonu
background_speed = 2  # Arka planın kayma hızı (sağa doğru)

# Oyun nesneleri
cat_frames = ['cat_run1', 'cat_run2', 'cat_run3', 'cat_run4']  # Kedinin hareket animasyonu için resimler
cat = Actor(cat_frames[0])  # Kediyi ilk poz ile başlat
cat.x = WIDTH - 100  # Kedi ekranın sağında sabit
cat.y = HEIGHT - 50
cat.state = "ready"  # Kedi hazır durumda
cat.dy = 0  # Kediye yukarı doğru hareket için hız ekliyoruz
cat.frame_index = 0  # Animasyon için pozisyon

# Çöp kutusu (engel)
trash_can = Actor('trash_can')  # Çöp kutusunun resmi (trash_can.gif)
trash_can.x = -50  # Çöp kutusunu ekranın solundan başlatıyoruz
trash_can.y = HEIGHT - 50
trash_can.dx = 5.0   # Çöp kutusunun sağa doğru hareket hızını ayarlıyoruz

# Yerçekimi
gravity = -0.7

# Skor
score = 0
game_over = False

# Animasyon hızı kontrolü için sayaç
animation_counter = 0
animation_speed = 5  # Kedinin animasyonu kaç update() çağrısından sonra değişecek

def draw():
    screen.clear()  # Ekranı temizle

    # Hareketli arka planı çiz
    screen.blit(background, (background_x1, 0))
    screen.blit(background, (background_x2, 0))

    # Kedi ve çöp kutusunu çiz
    cat.draw()
    trash_can.draw()
    screen.draw.text(f"Score: {score}", (10, 10), fontsize=30, color="white")
    
    if game_over:
        screen.draw.text("GAME OVER", center=(WIDTH / 2, HEIGHT / 2), fontsize=50, color="red")

def update():
    global score, game_over, animation_counter, background_x1, background_x2

    if game_over:
        return 

     # Kedi animasyonunu güncelle
    animation_counter += 1
    if animation_counter >= animation_speed:
        animation_counter = 0
        cat.frame_index = (cat.frame_index + 1) % len(cat_frames)  # Sıradaki animasyon karesi
        cat.image = cat_frames[cat.frame_index]  # Kedinin görüntüsünü değiştir

    # Kedi yerçekimi etkisi ve zıplama
    if cat.state == "jumping":
        cat.dy += gravity  # Yerçekimi etkisi
        cat.y -= cat.dy  # Kediyi yukarı hareket ettir

    if cat.y >= HEIGHT - 50:  # Yere indiğinde
        cat.y = HEIGHT - 50  # Yere temas ettiğinde konumunu sabitle
        cat.dy = 0  # Yerçekimini sıfırla
        cat.state = "ready"  # Zıplama bitince kedi hazır duruma geçer

    # Çöp kutusunun hareketi
    trash_can.x += trash_can.dx  # Çöp kutusunu sağa hareket ettir
    if trash_can.x > WIDTH + 50:  # Ekranın sağ tarafına geçtiğinde
        trash_can.x = -50  # Yeniden soldan başlat
        trash_can.dx *= 1.05  # Çöp kutusunun hızını artır
        score += 1  # Skoru artır

    # Çöp kutusu ile çarpışma
    if cat.colliderect(trash_can):  # Çarpışma kontrolü
        game_over = True

    # Arka planı ters yöne kaydır
    background_x1 += background_speed
    background_x2 += background_speed

    # Arka planın sonsuz döngüsünü sağla
    if background_x1 >= WIDTH:
        background_x1 = -WIDTH
    if background_x2 >= WIDTH:
        background_x2 = -WIDTH

def on_key_down():
    global game_over

    if keyboard.space and cat.state == "ready" and not game_over:  # Zıplama
        cat.dy = 10  # Zıplama kuvveti
        cat.state = "jumping"  # Kedi zıplama durumuna geçer

pgzrun.go()
