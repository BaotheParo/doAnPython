import pygame
import os


class SoundManager:
    def __init__(self, game_state=None):
        pygame.mixer.init()
        self.game_state = game_state
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        self.sound_dir = os.path.join(self.base_dir, "assets", "soundeffect")
        self.is_sound_enabled = self.game_state.is_sound_enabled if self.game_state else True

        # Tải các âm thanh
        self.sounds = {
            'water': self.load_sound('water.wav'),
            'plant': self.load_sound('plant.wav'),
            'remove': self.load_sound('remove.wav'),
            'harvest': self.load_sound('harvest.wav'),
            'fishing': self.load_sound('fishing.mp3'),
            'success': self.load_sound('success.wav'),
            'fail': self.load_sound('fail.wav'),
            'complete': self.load_sound('complete.wav'),
            'click': self.load_sound('click.wav'),
            'teleport': self.load_sound('teleport.wav'),
            'splash': self.load_sound('splash.mp3'),  # Thêm splash.mp3
            'reel': self.load_sound('reel.mp3'),  # Thêm reel.mp3
        }

        # Thiết lập âm lượng mặc định
        for sound in self.sounds.values():
            if sound:
                sound.set_volume(0.5)

    def load_sound(self, filename):
        """Tải một file âm thanh, trả về None nếu không tìm thấy."""
        try:
            return pygame.mixer.Sound(os.path.join(self.sound_dir, filename))
        except FileNotFoundError:
            print(f"Error: Sound file {filename} not found in {self.sound_dir}")
            return None

    def play_sound(self, sound_name, loops=0):
        """
        Phát một hiệu ứng âm thanh nếu âm thanh được bật.
        loops: Số lần lặp lại âm thanh (mặc định là 0 - phát 1 lần, -1 để lặp vô hạn).
        Trả về channel của âm thanh để có thể dừng hoặc kiểm soát sau này.
        """
        if self.is_sound_enabled and sound_name in self.sounds and self.sounds[sound_name]:
            channel = self.sounds[sound_name].play(loops=loops)
            return channel
        return None

    def toggle_sound(self):
        """Bật/tắt âm thanh."""
        self.is_sound_enabled = not self.is_sound_enabled
        if self.game_state:
            self.game_state.is_sound_enabled = self.is_sound_enabled  # Đồng bộ với game_state