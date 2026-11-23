"""
T.C. TÜBİTAK 2204-B Projesi
Vektörel Grafik ve SVG İllüstrasyon Üreteci (SVG Assets)
El şekilleri, yönlendirme okları ve resmi TÜBİTAK rozetleri.
"""

from typing import Dict


def get_tubitak_badge_svg(width: int = 240, height: int = 50) -> str:
    """Resmi TÜBİTAK 2204-B Proje Rozeti (Vektörel SVG)"""
    return f"""<svg width="{width}" height="{height}" viewBox="0 0 240 50" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="tubitakGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#b91c1c" />
      <stop offset="100%" stop-color="#991b1b" />
    </linearGradient>
    <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#f87171" stop-opacity="0.8" />
      <stop offset="100%" stop-color="#ef4444" stop-opacity="0.3" />
    </linearGradient>
  </defs>
  <!-- Background Pill -->
  <rect x="2" y="2" width="236" height="46" rx="10" fill="url(#tubitakGrad)" stroke="url(#borderGrad)" stroke-width="1.5" />
  
  <!-- Emblem Circle -->
  <circle cx="26" cy="25" r="15" fill="#ffffff" />
  <!-- Crescent & Star / Science Emblem -->
  <circle cx="26" cy="25" r="11" fill="#b91c1c" />
  <circle cx="28" cy="25" r="9" fill="#ffffff" />
  <circle cx="29" cy="25" r="8" fill="#b91c1c" />
  <polygon points="23,23 24.5,21.5 25,23.5 23.5,24.5" fill="#ffffff" />

  <!-- Text Header -->
  <text x="50" y="21" font-family="'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="12" font-weight="900" fill="#ffffff" letter-spacing="1">TÜBİTAK 2204-B</text>
  <!-- Subtitle -->
  <text x="50" y="36" font-family="'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="9" font-weight="600" fill="#fecaca" letter-spacing="0.5">ARAŞTIRMA PROJESİ</text>
</svg>"""


def get_hand_svg(hand_shape: str, width: int = 140, height: int = 140, primary_color: str = "#38bdf8", accent_color: str = "#f43f5e") -> str:
    """Verilen el şekline göre yüksek kaliteli vektörel SVG üretir."""
    
    # Varsayılan el gövdesi ve eklemler
    svg_header = f'<svg width="{width}" height="{height}" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'
    svg_footer = '</svg>'

    # 1. Açık El / Merhaba (Open Palm)
    if hand_shape in ("open_palm_wave", "open_palm", "flat_open_four", "bye_wave"):
        content = f"""
        <g stroke="{primary_color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none">
          <!-- Avuç içi -->
          <path d="M35 50 Q35 78 50 78 Q65 78 65 50 Z" fill="{primary_color}" fill-opacity="0.2" />
          <!-- Başparmak -->
          <path d="M35 55 Q20 48 24 38 Q28 35 36 45" />
          <!-- İşaret -->
          <path d="M38 45 L38 20 Q41 17 44 20 L44 45" />
          <!-- Orta -->
          <path d="M46 45 L46 15 Q49 12 52 15 L52 45" />
          <!-- Yüzük -->
          <path d="M54 45 L54 18 Q57 15 60 18 L60 45" />
          <!-- Serçe -->
          <path d="M62 48 L62 26 Q65 23 68 26 L68 50" />
          <!-- Bilek -->
          <line x1="42" y1="78" x2="42" y2="92" />
          <line x1="58" y1="78" x2="58" y2="92" />
        </g>
        <!-- Hareket Dalgası -->
        <path d="M16 28 Q20 22 16 16" stroke="{accent_color}" stroke-width="2" fill="none" stroke-linecap="round" />
        <path d="M12 32 Q18 22 12 12" stroke="{accent_color}" stroke-width="2" fill="none" stroke-linecap="round" />
        <path d="M84 28 Q80 22 84 16" stroke="{accent_color}" stroke-width="2" fill="none" stroke-linecap="round" />
        """

    # 2. Onay / Evet / A Harfi (Thumbs Up)
    elif hand_shape in ("thumbs_up", "fist_thumb_side", "fist_thumb_front"):
        content = f"""
        <g stroke="{primary_color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none">
          <!-- Yumruk tabanı -->
          <rect x="35" y="45" width="34" height="32" rx="8" fill="{primary_color}" fill-opacity="0.2" />
          <!-- Başparmak dimdik yukarı -->
          <path d="M35 55 L35 25 Q39 16 45 20 Q48 24 45 45" fill="{accent_color}" fill-opacity="0.25" stroke="{accent_color}" stroke-width="3.5" />
          <!-- Parmak kıvrımları -->
          <line x1="45" y1="52" x2="65" y2="52" />
          <line x1="45" y1="60" x2="65" y2="60" />
          <line x1="45" y1="68" x2="65" y2="68" />
          <!-- Bilek -->
          <line x1="42" y1="77" x2="42" y2="92" />
          <line x1="62" y1="77" x2="62" y2="92" />
        </g>
        <!-- Yukarı yönlü onay oku -->
        <path d="M22 36 L22 20 M18 24 L22 20 L26 24" stroke="{accent_color}" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round" />
        """

    # 3. Sil / Kötü / Thumbs Down
    elif hand_shape in ("thumbs_down", "thumbs_down_frown"):
        content = f"""
        <g stroke="{primary_color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none">
          <!-- Yumruk tabanı -->
          <rect x="35" y="24" width="34" height="32" rx="8" fill="{primary_color}" fill-opacity="0.2" />
          <!-- Başparmak dimdik aşağı -->
          <path d="M35 45 L35 75 Q39 84 45 80 Q48 76 45 55" fill="{accent_color}" fill-opacity="0.25" stroke="{accent_color}" stroke-width="3.5" />
          <!-- Parmak kıvrımları -->
          <line x1="45" y1="32" x2="65" y2="32" />
          <line x1="45" y1="40" x2="65" y2="40" />
          <line x1="45" y1="48" x2="65" y2="48" />
          <!-- Bilek -->
          <line x1="42" y1="24" x2="42" y2="12" />
          <line x1="62" y1="24" x2="62" y2="12" />
        </g>
        <!-- Aşağı yönlü silme oku -->
        <path d="M22 64 L22 80 M18 76 L22 80 L26 76" stroke="{accent_color}" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round" />
        """

    # 4. Tamam / OK Halka Jesti / F Harfi
    elif hand_shape in ("ok_sign", "d_shape", "o_shape", "o_shape_dots"):
        content = f"""
        <g stroke="{primary_color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none">
          <!-- Avuç İçi Tabanı -->
          <path d="M40 55 Q40 76 56 76 Q70 76 68 55 Z" fill="{primary_color}" fill-opacity="0.2" />
          <!-- Başparmak ve işaret parmağı halkası -->
          <circle cx="34" cy="46" r="12" fill="{accent_color}" fill-opacity="0.2" stroke="{accent_color}" stroke-width="3" />
          <!-- Orta parmak dik -->
          <path d="M48 45 L48 18 Q51 14 54 18 L54 48" />
          <!-- Yüzük parmak dik -->
          <path d="M56 46 L56 22 Q59 18 62 22 L62 50" />
          <!-- Serçe parmak dik -->
          <path d="M64 48 L64 28 Q67 25 70 28 L70 55" />
          <!-- Bilek -->
          <line x1="46" y1="76" x2="46" y2="92" />
          <line x1="62" y1="76" x2="62" y2="92" />
        </g>
        <circle cx="34" cy="46" r="4" fill="{accent_color}" />
        """

    # 5. Zafer / V Harfi / Gönder (Victory / Peace)
    elif hand_shape in ("v_shape", "victory_peace", "two_fingers_horizontal", "two_fingers_eyes_forward"):
        content = f"""
        <g stroke="{primary_color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none">
          <!-- Yumruk -->
          <path d="M35 50 Q35 76 52 76 Q65 76 65 50 Z" fill="{primary_color}" fill-opacity="0.2" />
          <!-- İşaret Parmağı (V'nin sol kolu) -->
          <path d="M42 48 L32 18 Q35 14 39 16 L48 46" stroke="{accent_color}" stroke-width="3.5" fill="{accent_color}" fill-opacity="0.2" />
          <!-- Orta Parmak (V'nin sağ kolu) -->
          <path d="M50 46 L60 16 Q64 14 67 18 L57 48" stroke="{accent_color}" stroke-width="3.5" fill="{accent_color}" fill-opacity="0.2" />
          <!-- Başparmak diğer parmakların üstünü kapatır -->
          <path d="M35 56 Q50 56 58 60" />
          <!-- Kıvrık yüzük ve serçe -->
          <path d="M56 60 Q62 60 62 68" />
          <!-- Bilek -->
          <line x1="44" y1="76" x2="44" y2="92" />
          <line x1="58" y1="76" x2="58" y2="92" />
        </g>
        """

    # 6. Hayır / İşaret Parmağı Tek (Index Wag / Point)
    elif hand_shape in ("index_wag", "index_straight", "point_search", "chin_tap"):
        content = f"""
        <g stroke="{primary_color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none">
          <!-- Yumruk tabanı -->
          <rect x="36" y="44" width="30" height="32" rx="8" fill="{primary_color}" fill-opacity="0.2" />
          <!-- Tek işaret parmağı yukarı -->
          <path d="M42 44 L42 16 Q46 12 50 16 L50 44" stroke="{accent_color}" stroke-width="3.5" fill="{accent_color}" fill-opacity="0.25" />
          <!-- Başparmak önü kapatır -->
          <path d="M36 54 Q48 50 54 56" />
          <line x1="52" y1="62" x2="64" y2="62" />
          <line x1="52" y1="69" x2="64" y2="69" />
          <!-- Bilek -->
          <line x1="42" y1="76" x2="42" y2="92" />
          <line x1="58" y1="76" x2="58" y2="92" />
        </g>
        <!-- İki yana sallanma okları -->
        <path d="M30 22 L24 22 M26 19 L23 22 L26 25" stroke="{accent_color}" stroke-width="2" fill="none" stroke-linecap="round" />
        <path d="M62 22 L68 22 M66 19 L69 22 L66 25" stroke="{accent_color}" stroke-width="2" fill="none" stroke-linecap="round" />
        """

    # 7. Seni Seviyorum (ILY Sign)
    elif hand_shape == "ily_sign":
        content = f"""
        <g stroke="{primary_color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none">
          <!-- Avuç içi gövdesi -->
          <path d="M36 48 Q36 74 52 74 Q64 74 64 48 Z" fill="{primary_color}" fill-opacity="0.2" />
          <!-- Başparmak yana açık -->
          <path d="M36 55 Q20 50 22 40 Q26 36 36 48" stroke="{accent_color}" stroke-width="3.5" />
          <!-- İşaret parmağı dik -->
          <path d="M40 46 L40 16 Q44 12 48 16 L48 46" stroke="{accent_color}" stroke-width="3.5" fill="{accent_color}" fill-opacity="0.2" />
          <!-- Orta ve yüzük parmakları bükülü -->
          <path d="M48 50 Q56 50 56 62" />
          <!-- Serçe parmak dimdik -->
          <path d="M58 46 L64 24 Q67 20 70 24 L68 50" stroke="{accent_color}" stroke-width="3.5" fill="{accent_color}" fill-opacity="0.2" />
          <!-- Bilek -->
          <line x1="44" y1="74" x2="44" y2="92" />
          <line x1="58" y1="74" x2="58" y2="92" />
        </g>
        <!-- Sevgi Kalbi -->
        <path d="M48 64 C48 60 42 56 38 60 C34 64 38 70 48 78 C58 70 62 64 58 60 C54 56 48 60 48 64 Z" fill="{accent_color}" opacity="0.8" />
        """

    # 8. 'L' Harfi Jesti
    elif hand_shape == "l_shape":
        content = f"""
        <g stroke="{primary_color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none">
          <!-- Avuç -->
          <rect x="42" y="46" width="26" height="30" rx="6" fill="{primary_color}" fill-opacity="0.2" />
          <!-- Başparmak yatay açık (L alt kolu) -->
          <path d="M42 58 L18 58 Q14 54 18 50 L42 50" stroke="{accent_color}" stroke-width="3.5" fill="{accent_color}" fill-opacity="0.2" />
          <!-- İşaret parmağı dikey (L dikey kolu) -->
          <path d="M44 46 L44 16 Q48 12 52 16 L52 46" stroke="{accent_color}" stroke-width="3.5" fill="{accent_color}" fill-opacity="0.2" />
          <!-- Diğer 3 parmak kapalı -->
          <line x1="54" y1="56" x2="66" y2="56" />
          <line x1="54" y1="63" x2="66" y2="63" />
          <line x1="54" y1="70" x2="66" y2="70" />
          <!-- Bilek -->
          <line x1="46" y1="76" x2="46" y2="92" />
          <line x1="60" y1="76" x2="60" y2="92" />
        </g>
        """

    # 9. 'C' Harfi / Su İçme (C-shape / Cup)
    elif hand_shape in ("c_shape", "c_shape_shake", "water_cup"):
        content = f"""
        <g stroke="{accent_color}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none">
          <!-- C şeklinde kavisli el profili -->
          <path d="M65 24 Q30 20 28 50 Q30 80 65 76" fill="{primary_color}" fill-opacity="0.15" />
          <!-- Parmak uçları -->
          <path d="M65 24 Q72 26 68 32 Q60 34 50 34" />
          <path d="M65 76 Q72 74 68 68 Q60 66 50 66" />
          <!-- Bilek -->
          <line x1="28" y1="56" x2="14" y2="64" stroke="{primary_color}" stroke-width="3" />
        </g>
        """

    # 10. İki El Çatı / EV
    elif hand_shape == "roof_shape":
        content = f"""
        <g stroke="{accent_color}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none">
          <!-- Sol çatı kanadı (sol el) -->
          <path d="M18 64 L50 28" />
          <!-- Sağ çatı kanadı (sağ el) -->
          <path d="M82 64 L50 28" />
          <!-- Parmak uçlarının zirvede buluşması -->
          <circle cx="50" cy="28" r="5" fill="{accent_color}" />
          <!-- Ev duvarları -->
          <line x1="24" y1="64" x2="24" y2="82" stroke="{primary_color}" stroke-width="2.5" />
          <line x1="76" y1="64" x2="76" y2="82" stroke="{primary_color}" stroke-width="2.5" />
          <line x1="20" y1="82" x2="80" y2="82" stroke="{primary_color}" stroke-width="2.5" />
        </g>
        """

    # 11. Diğer tüm genel jestler için zarif TİD simgesi
    else:
        content = f"""
        <g stroke="{primary_color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none">
          <!-- Avuç İçi -->
          <path d="M35 48 Q35 74 50 74 Q65 74 65 48 Z" fill="{primary_color}" fill-opacity="0.2" />
          <path d="M35 52 Q24 46 28 38 Q32 35 37 44" />
          <path d="M39 44 L39 20 Q42 16 46 20 L46 44" />
          <path d="M48 44 L48 16 Q51 12 55 16 L55 44" />
          <path d="M57 44 L57 20 Q60 16 63 20 L63 46" />
          <path d="M64 47 L64 28 Q67 24 70 28 L70 50" />
          <!-- Bilek -->
          <line x1="42" y1="74" x2="42" y2="90" />
          <line x1="58" y1="74" x2="58" y2="90" />
        </g>
        <circle cx="50" cy="56" r="6" fill="{accent_color}" opacity="0.8" />
        """

    return svg_header + content + svg_footer
