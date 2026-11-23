"""
TİD-Klavye Modül Testleri
"""

import os
import sys
import unittest
import numpy as np

# Proje ana dizinini ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.keyboard_injector import KeyboardInjector
from core.landmark_detector import HandLandmarkDetector
from core.gesture_recognizer import GestureRecognizer


class TestTIDKeyboard(unittest.TestCase):

    def setUp(self):
        self.injector = KeyboardInjector(char_delay=0.001, word_delay=0.05)
        self.detector = HandLandmarkDetector()
        self.recognizer = GestureRecognizer(hold_duration=0.05, cooldown=0.1)

    def test_keyboard_injector_state(self):
        """Klavye açma/kapama durumunu test eder."""
        self.assertTrue(self.injector.enabled)
        self.injector.set_enabled(False)
        self.assertFalse(self.injector.enabled)
        # Kapalıyken yazım reddedilmeli
        self.assertFalse(self.injector.type_text("Test"))
        self.injector.set_enabled(True)

    def test_landmark_detector_dummy_frame(self):
        """Boş görüntüde dedektörün çökmeden doğru formatta yanıt verdiğini test eder."""
        blank_img = np.zeros((480, 640, 3), dtype=np.uint8)
        result = self.detector.detect(blank_img)
        self.assertIn("hands", result)
        self.assertEqual(len(result["hands"]), 0)

    def test_gesture_recognizer_rules(self):
        """Kural tabanlı jest tanıma mantığını simüle edilmiş landmarklar ile test eder."""
        # 21 tane landmark oluştur
        landmarks = [(0.5, 0.5, 0.0)] * 21
        # MERHABA için parmaklar açık ve aralıklı
        merhaba_lms = list(landmarks)
        merhaba_lms[4] = (0.2, 0.4, 0.0)  # Başparmak ucu
        merhaba_lms[8] = (0.5, 0.2, 0.0)  # İşaret ucu (aralıklı)

        # Parmak durumları simülasyonu: Tüm parmaklar açık (MERHABA)
        hand_data_merhaba = [{
            "landmarks": merhaba_lms,
            "relative_landmarks": merhaba_lms,
            "finger_states": {
                "thumb": True,
                "index": True,
                "middle": True,
                "ring": True,
                "pinky": True
            }
        }]

        sign, conf, _ = self.recognizer.process_hands(hand_data_merhaba)
        self.assertEqual(sign, "MERHABA")
        self.assertGreater(conf, 0.8)

        # Parmak durumları simülasyonu: Sadece başparmak açık (EVET)
        # Başparmak ucu (4) eklemden (2) yukarıda (y daha küçük)
        evet_lms = list(landmarks)
        evet_lms[4] = (0.5, 0.3, 0.0)
        evet_lms[2] = (0.5, 0.5, 0.0)

        hand_data_evet = [{
            "landmarks": evet_lms,
            "relative_landmarks": evet_lms,
            "finger_states": {
                "thumb": True,
                "index": False,
                "middle": False,
                "ring": False,
                "pinky": False
            }
        }]

        sign_evet, conf_evet, _ = self.recognizer.process_hands(hand_data_evet)
        self.assertEqual(sign_evet, "EVET")


if __name__ == "__main__":
    unittest.main()
