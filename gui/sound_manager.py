# move.wav Tiếng di chuyển quân cờ nhẹ
# capture.wav Tiếng ăn quân cờ
# check.wav Âm báo khi chiếu tướng
# draw.wav Âm thanh hòa cờ
# win.wav Âm chiến thắng
# lose.wav Âm báo thua cuộc
# resign.wav Âm báo nhận thua
# menu_close.wav Âm đóng menu

# Dùng pygame.mixer

import pygame 
import os

class SoundManager:
    def __init__(self, sound_folder = "assets/sound/"):
        pygame.mixer.init()
        self.sound_folder = sound_folder
        self.sound_folder = os.path.abspath(sound_folder)  # Đảm bảo đường dẫn tuyệt đối
        self.music_volume = 0.5 # Mặc định 50%

        # Đường dẫn file nhạc nền
        self.music_file = os.path.join(self.sound_folder, "Theme_menu.mp3")

        # Phát nhạc nền khi khởi động
        self.play_music()

    def play_music(self):
        # Phát nhạc nền theo vòng lặp
        if os.path.exists(self.music_file):
            pygame.mixer.music.load(self.music_file)
            pygame.mixer.music.set_volume(self.music_volume) # Cài đặt âm lượng 50%
            pygame.mixer.music.play(-1) # Lặp vô hạn
        else: 
            print("Không tìm thấy file nhạc nền: {self.music_file}")

    def set_music_volume(self, volume):
        # Thay đổi âm lượng nhạc nền
        self.music_volume = max(0.0, min(1.0, volume/100))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def stop_music(self):
        # Dừng nhạc nền
        pygame.mixer.music.stop()
