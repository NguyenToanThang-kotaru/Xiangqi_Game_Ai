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
        self.sound_folder = os.path.abspath(sound_folder)  # Đảm bảo đường dẫn tuyệt đối
        self.music_volume = 0.5 # Mặc định 50%
        self.last_music_volume = self.music_volume
        self.sound_enabled = True # Trạng thái âm thanh (True: bật, False: tắt)

        # Đường dẫn file nhạc nền
        self.music_file = os.path.join(self.sound_folder, "Theme_menu.mp3")

        # Nạp âm thanh click chuột
        self.click_sound_path = os.path.join(self.sound_folder, "click_sound.wav")
        self.click_sound = pygame.mixer.Sound(self.click_sound_path) if os.path.exists(self.click_sound_path) else None
        
        # Phát nhạc nền mặc định
        self.play_music()
    
    def play_music(self):
        # Phát nhạc nền theo vòng lặp
        if os.path.exists(self.music_file):
            pygame.mixer.music.load(self.music_file)
            pygame.mixer.music.set_volume(self.music_volume) # Cài đặt âm lượng 50%
            pygame.mixer.music.play(-1) # Lặp vô hạn
        else: 
            print("Không tìm thấy file nhạc nền: {self.music_file}")

    def play_click_sound(self):
        # Phát âm thanh khi bấm chuột
        if self.click_sound:
            self.click_sound.play()

    def set_music_volume(self, volume):
        # Thay đổi âm lượng nhạc nền
        self.music_volume = max(0.0, min(1.0, volume/100))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def stop_music(self):
        # Dừng nhạc nền
        pygame.mixer.music.stop()

    def mute(self):
        if self.sound_enabled:
            self.last_music_volume = self.music_volume
            pygame.mixer.music.set_volume(0)
            self.sound_enabled = False

    def unmute(self):
        if not self.sound_enabled:
            pygame.mixer.music.set_volume(self.last_music_volume)
            self.music_volume = self.last_music_volume
            self.sound_enabled = True
            if not pygame.mixer.music.get_busy():
                self.play_music()