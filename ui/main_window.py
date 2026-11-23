"""
T.C. TÜBİTAK 2204-B Projesi
TİD-Klavye Resmi Yönetim Paneli ve Ana Penceresi (Official Dashboard & Main Window)
Canlı Kamera Takibi, Görsel Rehber, TÜBİTAK Jüri Bilgi Paneli ve Yüzen Mod Entegrasyonu.
"""

import sys
import time
from typing import Optional
import cv2
import numpy as np

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTabWidget, QFrame, QTextEdit, QProgressBar,
    QCheckBox, QSlider, QComboBox, QScrollArea, QApplication
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap, QFont

from ui.svg_assets import get_tubitak_badge_svg
from ui.guide_widget import TIDGuideWidget, render_svg_to_pixmap
from core.camera import CameraStream
from core.landmark_detector import HandLandmarkDetector
from core.gesture_recognizer import GestureRecognizer
from core.keyboard_injector import KeyboardInjector


class OfficialMainWindow(QMainWindow):
    # Yüzen moda geçiş sinyali
    switch_to_overlay_requested = pyqtSignal()

    def __init__(self, camera: CameraStream, detector: HandLandmarkDetector,
                 recognizer: GestureRecognizer, injector: KeyboardInjector):
        super().__init__()
        self.camera = camera
        self.detector = detector
        self.recognizer = recognizer
        self.injector = injector

        self.target_practice_word: Optional[str] = None
        self.auto_send = False
        self.append_space = True

        self.setWindowTitle("T.C. TÜBİTAK 2204-B | TİD-Klavye (Sign2Key): Türk İşaret Dili Sanal Klavye Asistanı")
        self.resize(1160, 760)
        self.setMinimumSize(960, 640)

        self._init_styles()
        self._init_ui()

    def _init_styles(self):
        """Resmi, modern ve yüksek kontrastlı koyu kurumsal tema."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0f172a;
            }
            QWidget {
                color: #f8fafc;
                font-family: 'Segoe UI', Roboto, Ubuntu, sans-serif;
            }
            QTabWidget::pane {
                border: 1px solid #334155;
                background-color: #0f172a;
                border-radius: 12px;
                top: -1px;
            }
            QTabBar::tab {
                background-color: #1e293b;
                color: #94a3b8;
                font-size: 13px;
                font-weight: 600;
                padding: 10px 20px;
                margin-right: 4px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                border: 1px solid #334155;
                border-bottom: none;
            }
            QTabBar::tab:selected {
                background-color: #0f172a;
                color: #38bdf8;
                border-top: 3px solid #38bdf8;
                border-bottom: 1px solid #0f172a;
            }
            QTabBar::tab:hover:!selected {
                background-color: #334155;
                color: #f1f5f9;
            }
        """)

    def _init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(16, 12, 16, 16)
        main_layout.setSpacing(10)

        # 1. Üst Kurumsal Başlık Çubuğu
        header_bar = self._create_header_bar()
        main_layout.addWidget(header_bar)

        # 2. Ana Sekme Paneli (Tabs)
        self.tabs = QTabWidget(self)

        # Sekme 1: Canlı Asistan & Akıllı Klavye
        self.live_tab = self._create_live_tab()
        self.tabs.addTab(self.live_tab, "🎥 Canlı Klavye & Kamera")

        # Sekme 2: TİD Görsel Rehberi & Sözlük
        self.guide_tab = TIDGuideWidget(self)
        self.guide_tab.try_sign_selected.connect(self._handle_try_sign_from_guide)
        self.tabs.addTab(self.guide_tab, "📖 TİD Görsel Rehberi & Sözlük")

        # Sekme 3: TÜBİTAK 2204-B Proje Raporu (Jüri Paneli)
        self.jury_tab = self._create_jury_tab()
        self.tabs.addTab(self.jury_tab, "📊 TÜBİTAK 2204-B Proje Künyesi")

        # Sekme 4: Ayarlar & Donanım Kalibrasyonu
        self.settings_tab = self._create_settings_tab()
        self.tabs.addTab(self.settings_tab, "⚙️ Ayarlar & Kalibrasyon")

        main_layout.addWidget(self.tabs)

    def _create_header_bar(self) -> QWidget:
        """TÜBİTAK resmi rozeti, başlık ve hızlı eylemleri içeren üst çubuk."""
        header = QFrame(self)
        header.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
            }
        """)
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(14, 8, 14, 8)
        h_layout.setSpacing(14)

        # TÜBİTAK Rozeti
        badge_pixmap = render_svg_to_pixmap(get_tubitak_badge_svg(230, 48), 230, 48)
        badge_label = QLabel(header)
        badge_label.setPixmap(badge_pixmap)
        badge_label.setFixedSize(230, 48)
        h_layout.addWidget(badge_label)

        # Proje Adı ve Açıklaması
        title_box = QVBoxLayout()
        title_box.setSpacing(2)

        main_title = QLabel("TİD-Klavye (Sign2Key): Türk İşaret Dili Destekli Sanal Klavye Asistanı", header)
        main_title.setStyleSheet("color: #f8fafc; font-size: 16px; font-weight: bold; border: none;")

        sub_title = QLabel("T.C. TÜBİTAK 2204-B Ortaokul Öğrencileri Araştırma Projeleri Yarışması | Yazılım & Erişilebilirlik", header)
        sub_title.setStyleSheet("color: #94a3b8; font-size: 11px; border: none;")

        title_box.addWidget(main_title)
        title_box.addWidget(sub_title)
        h_layout.addLayout(title_box)
        h_layout.addStretch()

        # Klavye Durum Düğmesi
        self.toggle_kbd_btn = QPushButton("Klavye: AKTİF", header)
        self.toggle_kbd_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: #0f172a;
                font-weight: bold;
                font-size: 12px;
                padding: 8px 16px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        self.toggle_kbd_btn.clicked.connect(self._toggle_keyboard_state)
        h_layout.addWidget(self.toggle_kbd_btn)

        # Yüzen Mod (WhatsApp) Düğmesi
        float_btn = QPushButton("🪟 Yüzen Moda Geç (WhatsApp)", header)
        float_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc2626;
                color: #ffffff;
                font-weight: bold;
                font-size: 12px;
                padding: 8px 16px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #b91c1c;
            }
        """)
        float_btn.setToolTip("Pencereyi küçülterek ekran köşesinde yüzen asistan olarak çalıştırır.")
        float_btn.clicked.connect(self._on_switch_to_overlay)
        h_layout.addWidget(float_btn)

        return header

    def _create_live_tab(self) -> QWidget:
        """Canlı Kamera, Tespit Edilen Kelimeler ve Cümle Paneli."""
        widget = QWidget(self)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(14)

        # Sol Panel: Kamera Akışı
        left_box = QVBoxLayout()
        left_box.setSpacing(8)

        # Pratik Hedefi Banner (varsa)
        self.practice_banner = QLabel("Tüm TİD kelimeleri algılanmaya hazır. Kameraya doğru işaret yapın.", widget)
        self.practice_banner.setStyleSheet("""
            background-color: #1e293b;
            color: #38bdf8;
            font-size: 12px;
            font-weight: 600;
            padding: 8px 12px;
            border-radius: 8px;
            border: 1px solid #0284c7;
        """)
        left_box.addWidget(self.practice_banner)

        # Video Gösterici
        self.video_label = QLabel(widget)
        self.video_label.setFixedSize(640, 480)
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setStyleSheet("""
            background-color: #020617;
            border-radius: 12px;
            border: 2px solid #334155;
            color: #64748b;
            font-size: 14px;
        """)
        self.video_label.setText("Kamera başlatılıyor...")
        left_box.addWidget(self.video_label)

        layout.addLayout(left_box)

        # Sağ Panel: Tanıma Kartı ve Metin Paneli
        right_box = QVBoxLayout()
        right_box.setSpacing(10)

        # Kart 1: Canlı Tespit
        detect_card = QFrame(widget)
        detect_card.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
                padding: 12px;
            }
        """)
        d_layout = QVBoxLayout(detect_card)
        d_layout.setSpacing(6)

        d_title = QLabel("Canlı TİD Algılama", detect_card)
        d_title.setStyleSheet("color: #94a3b8; font-size: 12px; font-weight: 600; border: none;")
        d_layout.addWidget(d_title)

        self.live_word_label = QLabel("Bekleniyor...", detect_card)
        self.live_word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.live_word_label.setStyleSheet("color: #38bdf8; font-size: 26px; font-weight: 900; border: none; padding: 6px;")
        d_layout.addWidget(self.live_word_label)

        # Güven Barı
        self.conf_bar = QProgressBar(detect_card)
        self.conf_bar.setRange(0, 100)
        self.conf_bar.setValue(0)
        self.conf_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #334155;
                border-radius: 6px;
                background-color: #0f172a;
                text-align: center;
                color: #f8fafc;
                font-size: 11px;
                height: 18px;
            }
            QProgressBar::chunk {
                background-color: #0ea5e9;
                border-radius: 5px;
            }
        """)
        d_layout.addWidget(self.conf_bar)

        self.status_detail_label = QLabel("Kararlılık bekleniyor...", detect_card)
        self.status_detail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_detail_label.setStyleSheet("color: #64748b; font-size: 11px; border: none;")
        d_layout.addWidget(self.status_detail_label)

        right_box.addWidget(detect_card)

        # Kart 2: Metin Geçmişi ve Cümle Tamponu
        text_card = QFrame(widget)
        text_card.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
                padding: 12px;
            }
        """)
        t_layout = QVBoxLayout(text_card)
        t_layout.setSpacing(8)

        t_title = QLabel("Yazılan Metin Tamponu (Cümle Havuzu)", text_card)
        t_title.setStyleSheet("color: #94a3b8; font-size: 12px; font-weight: 600; border: none;")
        t_layout.addWidget(t_title)

        self.sentence_edit = QTextEdit(text_card)
        self.sentence_edit.setPlaceholderText("İşaret diliyle yaptığınız kelimeler buraya ve imlecin olduğu uygulamaya (WhatsApp vb.) otomatik yazılır...")
        self.sentence_edit.setStyleSheet("""
            QTextEdit {
                background-color: #0f172a;
                color: #f8fafc;
                font-size: 14px;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 8px;
            }
        """)
        t_layout.addWidget(self.sentence_edit)

        # Hızlı Metin Kontrol Butonları
        btn_grid = QHBoxLayout()
        btn_grid.setSpacing(6)

        send_btn = QPushButton("📤 WhatsApp'a Gönder", text_card)
        send_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: #0f172a;
                font-weight: bold;
                font-size: 11px;
                padding: 6px 10px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        send_btn.clicked.connect(self._manual_send_enter)
        btn_grid.addWidget(send_btn)

        copy_btn = QPushButton("📋 Kopyala", text_card)
        copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #334155;
                color: #f8fafc;
                font-weight: 600;
                font-size: 11px;
                padding: 6px 10px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #475569;
            }
        """)
        copy_btn.clicked.connect(self._copy_sentence)
        btn_grid.addWidget(copy_btn)

        clear_btn = QPushButton("🗑️ Temizle", text_card)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #334155;
                color: #f87171;
                font-weight: 600;
                font-size: 11px;
                padding: 6px 10px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #475569;
            }
        """)
        clear_btn.clicked.connect(self.sentence_edit.clear)
        btn_grid.addWidget(clear_btn)

        t_layout.addLayout(btn_grid)
        right_box.addWidget(text_card)

        # Seçenekler
        opt_box = QHBoxLayout()
        self.cb_autosend = QCheckBox("Her kelimede otomatik Enter gönder (WhatsApp)", widget)
        self.cb_autosend.setStyleSheet("color: #cbd5e1; font-size: 12px;")
        self.cb_autosend.toggled.connect(lambda v: setattr(self, 'auto_send', v))
        opt_box.addWidget(self.cb_autosend)

        right_box.addLayout(opt_box)
        layout.addLayout(right_box, stretch=1)

        return widget

    def _create_jury_tab(self) -> QWidget:
        """TÜBİTAK 2204-B Jüri Sunumu ve Bilimsel Rapor Sekmesi."""
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        def add_section(title: str, content: str):
            card = QFrame(container)
            card.setStyleSheet("""
                QFrame {
                    background-color: #1e293b;
                    border: 1px solid #334155;
                    border-radius: 12px;
                    padding: 14px;
                }
            """)
            c_layout = QVBoxLayout(card)
            c_layout.setSpacing(8)

            t_label = QLabel(title, card)
            t_label.setStyleSheet("color: #38bdf8; font-size: 16px; font-weight: bold; border: none;")
            c_layout.addWidget(t_label)

            body_label = QLabel(content, card)
            body_label.setWordWrap(True)
            body_label.setStyleSheet("color: #cbd5e1; font-size: 13px; line-height: 1.5; border: none;")
            c_layout.addWidget(body_label)

            layout.addWidget(card)

        add_section(
            "📌 1. Projenin Adı ve Amacı",
            "<b>Proje Adı:</b> TİD-Klavye (Sign2Key): Türk İşaret Dili Destekli Sanal Klavye ve Engelsiz İletişim Asistanı<br><br>"
            "<b>Amacı:</b> İşitme ve konuşma engelli bireylerin günlük hayatta dijital platformlarda (başta WhatsApp, Not Defteri, e-posta, arama motorları olmak üzere) "
            "bağımsız, hızlı ve kesintisiz biçimde yazışabilmelerini sağlamaktır. Kullanıcı herhangi bir özel donanıma veya pahalı sensörlü eldivenlere gerek duymadan, "
            "yalnızca standart bir web kamerası aracılığıyla Türk İşaret Dili jestlerini doğrudan aktif metin kutularına döker."
        )

        add_section(
            "👥 2. Hedef Kitle ve Erişilebilirlik Kapsamı",
            "• İşitme ve konuşma engelli bireyler (çocuklar, gençler ve yetişkinler)<br>"
            "• Özel eğitim kurumları, kaynaştırma öğrencileri ve öğretmenleri<br>"
            "• İşaret dili tercümanları ve işaret dili öğrenmek isteyen herkes<br>"
            "• WCAG (Web Content Accessibility Guidelines) ilkeleri doğrultusunda odağı bozmayan arayüz tasarımı."
        )

        add_section(
            "🔬 3. Kullanılan Bilimsel Yöntem ve Yapay Zeka Mimarisi",
            "<b>1. Bilgisayarlı Görü (Computer Vision):</b> OpenCV ile düşük gecikmeli kamera akışı işlenir.<br>"
            "<b>2. Eklem Tespiti (Landmark Extraction):</b> Google MediaPipe Hand Landmarker kullanılarak her iki el için 21'er adet 3 boyutlu eklem noktası (toplam 42 eklem) eşzamanlı takip edilir.<br>"
            "<b>3. Ölçek ve Konum Normalizasyonu:</b> Kullanıcının kameraya olan uzaklığından ve elin ekrandaki konumundan etkilenmemek adına bilek merkezli bağıl koordinat matrisi çıkartılır.<br>"
            "<b>4. Hibrit Tanıma Motoru:</b><br>"
            "   - <i>Kural Tabanlı Geometrik Analiz:</i> Temel TİD jestleri ve harfleri için yüksek doğruluklu parmak durum analizleri.<br>"
            "   - <i>Makine Öğrenmesi (ML) Modeli:</i> Random Forest sınıflandırıcısı ile çok sınıflı kelime tanıma.<br>"
            "<b>5. Debounce & Kararlılık Filtresi:</b> İşaretler arası geçiş anlarında yanlış veya mükerrer harf basımını engelleyen tutma-onaylama süresi (Hold-to-confirm)."
        )

        add_section(
            "💡 4. Projenin Yenilikçi Yönü (İnovasyon)",
            "Mevcut işaret dili tanıma projeleri çoğunlukla yalnızca izole bir pencerede kelimenin anlamını ekrana yazdırmakla sınırlı kalmaktadır. "
            "<b>TİD-Klavye projesinin en büyük yeniliği;</b> işletim sistemi düzeyinde sanal klavye enjeksiyonu gerçekleştirerek, "
            "arkaplanda çalışan WhatsApp, Telegram, LibreOffice veya Google Chrome gibi gerçek hedef uygulamalara doğrudan metin gönderebilmesi ve "
            "kullanıcıya hem tam bir görsel rehber hem de odağı çalmayan yüzen (floating) asistan sunabilmesidir."
        )

        layout.addStretch()
        scroll.setWidget(container)
        return scroll

    def _create_settings_tab(self) -> QWidget:
        """Ayarlar ve Kalibrasyon Sekmesi."""
        widget = QWidget(self)
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        card = QFrame(widget)
        card.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
                padding: 16px;
            }
        """)
        c_layout = QVBoxLayout(card)
        c_layout.setSpacing(12)

        title = QLabel("⚙️ Sistem ve Algılama Parametreleri", card)
        title.setStyleSheet("color: #38bdf8; font-size: 16px; font-weight: bold; border: none;")
        c_layout.addWidget(title)

        # Kararlılık Süresi (Debounce) Slider
        debounce_row = QHBoxLayout()
        d_lbl = QLabel("İşaret Onay Süresi (Hold Duration):", card)
        d_lbl.setStyleSheet("color: #cbd5e1; font-size: 13px;")
        self.debounce_val_lbl = QLabel(f"{self.recognizer.hold_duration:.2f} sn", card)
        self.debounce_val_lbl.setStyleSheet("color: #38bdf8; font-weight: bold;")

        self.debounce_slider = QSlider(Qt.Orientation.Horizontal, card)
        self.debounce_slider.setRange(20, 100)  # 0.20 - 1.00 sn
        self.debounce_slider.setValue(int(self.recognizer.hold_duration * 100))
        self.debounce_slider.valueChanged.connect(self._on_debounce_changed)

        debounce_row.addWidget(d_lbl)
        debounce_row.addWidget(self.debounce_slider)
        debounce_row.addWidget(self.debounce_val_lbl)
        c_layout.addLayout(debounce_row)

        # Tekrar Engelleme (Cooldown) Slider
        cooldown_row = QHBoxLayout()
        c_lbl = QLabel("Tekrarlama Bekleme Süresi (Cooldown):", card)
        c_lbl.setStyleSheet("color: #cbd5e1; font-size: 13px;")
        self.cooldown_val_lbl = QLabel(f"{self.recognizer.cooldown:.2f} sn", card)
        self.cooldown_val_lbl.setStyleSheet("color: #38bdf8; font-weight: bold;")

        self.cooldown_slider = QSlider(Qt.Orientation.Horizontal, card)
        self.cooldown_slider.setRange(40, 200)  # 0.40 - 2.00 sn
        self.cooldown_slider.setValue(int(self.recognizer.cooldown * 100))
        self.cooldown_slider.valueChanged.connect(self._on_cooldown_changed)

        cooldown_row.addWidget(c_lbl)
        cooldown_row.addWidget(self.cooldown_slider)
        cooldown_row.addWidget(self.cooldown_val_lbl)
        c_layout.addLayout(cooldown_row)

        layout.addWidget(card)
        layout.addStretch()
        return widget

    def _on_debounce_changed(self, val: int):
        sec = val / 100.0
        self.recognizer.hold_duration = sec
        self.debounce_val_lbl.setText(f"{sec:.2f} sn")

    def _on_cooldown_changed(self, val: int):
        sec = val / 100.0
        self.recognizer.cooldown = sec
        self.cooldown_val_lbl.setText(f"{sec:.2f} sn")

    def _toggle_keyboard_state(self):
        new_state = not self.injector.enabled
        self.injector.set_enabled(new_state)
        if new_state:
            self.toggle_kbd_btn.setText("Klavye: AKTİF")
            self.toggle_kbd_btn.setStyleSheet("background-color: #10b981; color: #0f172a; font-weight: bold; font-size: 12px; padding: 8px 16px; border-radius: 8px; border: none;")
        else:
            self.toggle_kbd_btn.setText("Klavye: DURDURULDU")
            self.toggle_kbd_btn.setStyleSheet("background-color: #64748b; color: #ffffff; font-weight: bold; font-size: 12px; padding: 8px 16px; border-radius: 8px; border: none;")

    def _on_switch_to_overlay(self):
        self.switch_to_overlay_requested.emit()

    def _handle_try_sign_from_guide(self, word: str):
        """Rehberden 'Canlı Dene' tıklandığında Canlı Asistan sekmesine geçer ve hedef belirler."""
        self.target_practice_word = word
        self.practice_banner.setText(f"🎯 HEDEF İŞARET: '{word}' — Lütfen kameraya doğru bu işareti yapın!")
        self.practice_banner.setStyleSheet("""
            background-color: #0284c7;
            color: #ffffff;
            font-size: 13px;
            font-weight: bold;
            padding: 10px 14px;
            border-radius: 8px;
            border: 2px solid #38bdf8;
        """)
        # 1. Sekmeye geç
        self.tabs.setCurrentIndex(0)

    def _manual_send_enter(self):
        self.injector.press_enter()

    def _copy_sentence(self):
        text = self.sentence_edit.toPlainText()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)

    def update_frame(self, bgr_frame: np.ndarray):
        """Kamera akışını arayüzde gösterir."""
        if bgr_frame is None or not self.isVisible():
            return
        scaled = cv2.resize(bgr_frame, (640, 480), interpolation=cv2.INTER_AREA)
        rgb = cv2.cvtColor(scaled, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        q_img = QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(q_img))

    def update_detection_state(self, sign: Optional[str], confidence: float, should_type: bool):
        """Canlı tanıma kartı göstergelerini günceller."""
        if sign:
            self.live_word_label.setText(sign)
            self.conf_bar.setValue(int(confidence * 100))

            if should_type:
                self.status_detail_label.setText(f"✅ Onaylandı & Yazıldı: {sign}")
                self.status_detail_label.setStyleSheet("color: #10b981; font-weight: bold;")
                # Metin havuzuna ekle (özel komutlar değilse)
                if not sign.startswith("<"):
                    current = self.sentence_edit.toPlainText()
                    sep = " " if current and not current.endswith(" ") else ""
                    self.sentence_edit.setText(current + sep + sign)
            else:
                self.status_detail_label.setText("İşaret kararlı tutuluyor...")
                self.status_detail_label.setStyleSheet("color: #38bdf8;")

            # Hedef deneme tamamlandı mı?
            if self.target_practice_word and sign.upper() in self.target_practice_word.upper():
                self.practice_banner.setText(f"🎉 TEBRİKLER! '{sign}' işareti başarıyla tespit edildi!")
                self.practice_banner.setStyleSheet("""
                    background-color: #059669;
                    color: #ffffff;
                    font-size: 13px;
                    font-weight: bold;
                    padding: 10px 14px;
                    border-radius: 8px;
                    border: 2px solid #34d399;
                """)
        else:
            self.live_word_label.setText("Bekleniyor...")
            self.conf_bar.setValue(0)
            self.status_detail_label.setText("El tespit bekleniyor...")
            self.status_detail_label.setStyleSheet("color: #64748b;")
