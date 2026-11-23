"""
T.C. TÜBİTAK 2204-B Projesi
🤟 TİD-Klavye (Sign2Key) - Ana Uygulama
Kamera -> MediaPipe Landmark -> TİD Tanıma Motoru -> Klavye Enjeksiyonu
-> Resmi Yönetim Paneli (Official Dashboard) & Yüzen Asistan (Floating Overlay)
"""

import os
import sys
import locale

# Türkçe sistemlerde MediaPipe C++ regex çakışmasını engelle
os.environ["LC_ALL"] = "C"
os.environ["LANG"] = "C"
try:
    locale.setlocale(locale.LC_ALL, "C")
except Exception:
    pass

import time
import argparse
import cv2

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from core.camera import CameraStream
from core.landmark_detector import HandLandmarkDetector
from core.gesture_recognizer import GestureRecognizer
from core.keyboard_injector import KeyboardInjector
from ui.main_window import OfficialMainWindow
from ui.overlay_widget import SignOverlayWidget


class TIDAssistantApp:
    def __init__(self, camera_index: int = 0, no_gui: bool = False, start_as_overlay: bool = False):
        self.camera_index = camera_index
        self.no_gui = no_gui
        self.start_as_overlay = start_as_overlay

        print("[TİD-Klavye | TÜBİTAK 2204-B] Sistem bileşenleri başlatılıyor...")
        self.camera = CameraStream(src=camera_index)
        self.detector = HandLandmarkDetector()
        self.recognizer = GestureRecognizer()
        self.injector = KeyboardInjector()

        self.last_action_msg = ""
        self.action_msg_time = 0.0

        if not self.no_gui:
            self.qt_app = QApplication(sys.argv)
            self.qt_app.setApplicationName("TİD-Klavye (TÜBİTAK 2204-B)")

            # 1. Ana Resmi Pencere (Dashboard & Rehber)
            self.main_window = OfficialMainWindow(
                camera=self.camera,
                detector=self.detector,
                recognizer=self.recognizer,
                injector=self.injector
            )
            self.main_window.switch_to_overlay_requested.connect(self.switch_to_overlay)

            # 2. Yüzen Mini Asistan (WhatsApp Modu)
            self.overlay = SignOverlayWidget(
                on_toggle_active=self.on_toggle_active,
                on_toggle_autosend=self.on_toggle_autosend
            )
            self.overlay.open_main_window_requested.connect(self.switch_to_main_window)

            # Başlangıç konumu: Sağ alt köşe
            screen = self.qt_app.primaryScreen().geometry()
            self.overlay.move(screen.width() - 340, screen.height() - 430)

            if self.start_as_overlay:
                self.overlay.show()
                self.main_window.hide()
            else:
                self.main_window.show()
                self.overlay.hide()

            # Timer döngüsü (~30 FPS)
            self.timer = QTimer()
            self.timer.timeout.connect(self.process_frame)
            self.timer.start(30)
        else:
            self.qt_app = None
            self.main_window = None
            self.overlay = None

    def switch_to_overlay(self):
        """Ana pencereyi gizleyip WhatsApp yüzen kartına geçer."""
        if self.main_window and self.overlay:
            self.main_window.hide()
            self.overlay.show()
            print("[TİD-Klavye] Yüzen moda geçildi (WhatsApp için hazır).")

    def switch_to_main_window(self):
        """Yüzen kartı gizleyip ana resmi pencereyi ve rehberi açar."""
        if self.main_window and self.overlay:
            self.overlay.hide()
            self.main_window.show()
            self.main_window.raise_()
            self.main_window.activateWindow()
            print("[TİD-Klavye] Ana yönetim ve TİD rehberi penceresine dönüldü.")

    def on_toggle_active(self, active: bool):
        self.injector.set_enabled(active)
        if self.main_window:
            self.main_window._toggle_keyboard_state()
        print(f"[TİD-Klavye] Klavye yazımı: {'AKTİF' if active else 'DURDURULDU'}")

    def on_toggle_autosend(self, autosend: bool):
        if self.main_window:
            self.main_window.auto_send = autosend
            self.main_window.cb_autosend.setChecked(autosend)
        print(f"[TİD-Klavye] Otomatik Mesaj Gönderme (Enter): {'AÇIK' if autosend else 'KAPALI'}")

    def start(self):
        if not self.camera.start():
            print("HATA: Kamera açılamadı! Lütfen kamera bağlantınızı kontrol edin.")
            return

        print("================================================================")
        print("  🤟 T.C. TÜBİTAK 2204-B Projesi: TİD-Klavye Başlatıldı!")
        print("  - Ana Pencere & TİD Rehberi Aktif")
        print("  - WhatsApp için 'Yüzen Moda Geç' seçeneğini kullanabilirsiniz.")
        print("================================================================")

        if not self.no_gui:
            sys.exit(self.qt_app.exec())
        else:
            self.run_cli_loop()

    def process_frame(self):
        ret, frame = self.camera.read()
        if not ret or frame is None:
            return

        # El tespiti
        det_result = self.detector.detect(frame)
        hands = det_result.get("hands", [])

        # İskelet çizimi
        if hands:
            self.detector.draw_landmarks(frame, hands)

        # TİD Jest analizi
        sign, confidence, should_type = self.recognizer.process_hands(hands)

        # Klavyeye yazma eylemi
        if should_type and sign:
            auto_send = False
            if self.overlay and self.overlay.isVisible():
                auto_send = self.overlay.auto_send
            elif self.main_window and self.main_window.isVisible():
                auto_send = self.main_window.auto_send

            self._handle_keyboard_action(sign, auto_send)

        # Arayüzleri güncelle
        if self.main_window and self.main_window.isVisible():
            self.main_window.update_detection_state(sign, confidence, should_type)
            self.main_window.update_frame(frame)

        if self.overlay and self.overlay.isVisible():
            msg = self.last_action_msg if time.time() - self.action_msg_time < 2.0 else ""
            self.overlay.update_detection(sign, confidence, msg)
            self.overlay.update_frame(frame)

    def _handle_keyboard_action(self, sign: str, auto_send: bool):
        """Tespit edilen sembole göre klavye eylemini yürütür."""
        if sign == "<SİL>":
            self.injector.backspace()
            self.last_action_msg = "• Geri Silindi"
            print(f"[Klavye] Eylem: Geri Silme (Backspace)")
        elif sign == "<GÖNDER>":
            self.injector.press_enter()
            self.last_action_msg = "• Gönderildi (Enter)"
            print(f"[Klavye] Eylem: Gönderildi (Enter)")
        elif sign == "<BOŞLUK>":
            self.injector.press_space()
            self.last_action_msg = "• Boşluk"
            print(f"[Klavye] Eylem: Boşluk")
        elif sign == "<TEMİZLE>":
            if self.main_window:
                self.main_window.sentence_edit.clear()
            self.last_action_msg = "• Temizlendi"
            print(f"[Klavye] Eylem: Tampon Temizlendi")
        else:
            typed = self.injector.type_text(sign, append_space=True, auto_send=auto_send)
            if typed:
                self.last_action_msg = f"• Yazıldı: {sign}"
                print(f"[Klavye] Metin Yazıldı: '{sign}' (Oto-Gönder: {auto_send})")

        self.action_msg_time = time.time()

    def run_cli_loop(self):
        """Grafik arayüz olmadan CLI penceresi ile çalıştırma."""
        try:
            while True:
                ret, frame = self.camera.read()
                if not ret or frame is None:
                    time.sleep(0.01)
                    continue

                det_result = self.detector.detect(frame)
                hands = det_result.get("hands", [])

                if hands:
                    self.detector.draw_landmarks(frame, hands)

                sign, confidence, should_type = self.recognizer.process_hands(hands)
                if should_type and sign:
                    self._handle_keyboard_action(sign, auto_send=False)

                status_str = f"Kelime: {sign} (%{int(confidence*100)})" if sign else "El Bekleniyor..."
                cv2.putText(frame, status_str, (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                cv2.imshow("TID-Klavye (CLI Modu) - Cikis: Q", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            self.camera.stop()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="T.C. TÜBİTAK 2204-B TİD-Klavye Asistanı")
    parser.add_argument("--camera", type=int, default=0, help="Kamera indeksi (varsayılan: 0)")
    parser.add_argument("--overlay", action="store_true", help="Doğrudan yüzen mini asistan modunda başlat")
    parser.add_argument("--no-gui", action="store_true", help="Grafik arayüz olmadan CLI modu ile başlat")
    args = parser.parse_args()

    app = TIDAssistantApp(camera_index=args.camera, no_gui=args.no_gui, start_as_overlay=args.overlay)
    app.start()
