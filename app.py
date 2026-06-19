import streamlit as st
from PIL import Image
import cv2
import numpy as np

# 1. 网页全局与太空感主题配置
st.set_page_config(page_title="Earth's Magnetic Shield: Shock Detectives", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #01010a 0%, #050c1e 50%, #0c1b2a 100%); }
    h1, h2, h3, label { color: #ffffff !important; }
    
    .evidence-box { 
        padding: 18px; 
        border-radius: 8px; 
        background-color: rgba(56, 189, 248, 0.08); 
        border: 1px solid rgba(56, 189, 248, 0.3); 
        margin-bottom: 12px; 
        font-size: 16px; 
        line-height: 1.6;
        color: #ffffff !important;
    }
    .evidence-box b, .evidence-box strong, .evidence-box span { color: #ffffff !important; }
    
    .status-badge { 
        font-weight: 900 !important; 
        font-size: 16px;
        display: inline-block;
        margin-left: 5px;
        background-color: transparent !important; 
        padding: 0 !important;                     
    }
    .chao-text { color: #ff4b4b !important; }  
    .peace-text { color: #00e676 !important; } 
    
    /* 强制高亮黄色警告框 */
    div[data-baseweb="notification"] {
        background-color: rgba(255, 193, 7, 0.15) !important;
        color: #ffc107 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 9国语言支持 (包含全组件覆盖，并完全移除了表情与后缀)
LANG_PACK = {
    "English": {
        "title": "Earth's Magnetic Shield: Shock Detectives",
        "input_header": "📥 Input Telemetry",
        "upload_limit_warning": "⚠️ Note: To ensure algorithmic accuracy, please upload **ONLY ONE** telemetry image per session.",
        "uploader_lbl": "Upload a Shock Spectrogram Plot:",
        "current_img_caption": "Current Uploaded Telemetry Image",
        "calibration_title": "🔧 **Data Bounds Calibration**",
        "left_pad_lbl": "Left Margin Pad (Y-Axis):",
        "right_pad_lbl": "Right Margin Pad (Legend):",
        "output_header": "📊 Space Weather Diagnostic Board",
        "desc_txt": "Awaiting spectrogram upload to begin decoding solar wind interactions...",
        "btn_txt": "Execute Live Algorithmic Analysis 🚀",
        "spinner_txt": "Analyzing image features pixel-by-pixel...",
        "analysis_title": "Regional Micro-Feature Deep Dive",
        "summary_title": "Global Classification Summary",
        "heat_lbl": "Energy Spectrogram", "line_lbl": "Time-series Lines", "ridge_lbl": "Fluctuation Ridge",
        "chaotic_zone": "🚨 Fully Chaotic Regions", 
        "peaceful_zone": "🌲 Fully Peaceful Regions", 
        "mixed_zone": "🌀 Mixed Regions (Both Present)",
        "crop_radio": "Inspect Algorithmic Crop:",
        "crop_view": "Live Slice Preview (Region {} / 5)",
        "chao_txt": "Chaotic", "peace_txt": "Peaceful",
        "box_header": "Region {} Scientific Clues Breakdown", "sentence_template": "Region {}'s {} is "
    },
    "简体中文": {
        "title": "地球磁盾：激波侦探",
        "input_header": "📥 输入监测数据",
        "upload_limit_warning": "⚠️ 提示：为了保证算法精度，每次分析请**仅上传唯一一张**图表。",
        "uploader_lbl": "上传一张激波能谱特征图：",
        "current_img_caption": "当前载入的分析图像",
        "calibration_title": "🔧 **数据边框校准**",
        "left_pad_lbl": "左侧边缘留白 (剔除Y轴):",
        "right_pad_lbl": "右侧边缘留白 (剔除图例):",
        "output_header": "📊 空间天气自动化诊断看板",
        "desc_txt": "等待上传光谱图以开启全自动化特征扫描与判定...",
        "btn_txt": "运行纯图像几何算法动态分析 (A-E) 🚀",
        "spinner_txt": "正在逐像素执行纯物理特征提取...",
        "analysis_title": "区域微观特征深入剖析",
        "summary_title": "激波形态全局终审判决",
        "heat_lbl": "热力图", "line_lbl": "折线图", "ridge_lbl": "山峦图",
        "chaotic_zone": "🚨 完全 Chaotic (混乱) 区域", 
        "peaceful_zone": "🌲 完全 Peaceful (宁静) 区域", 
        "mixed_zone": "🌀 二者都有的 Mixed (混合) 区域",
        "crop_radio": "查看算法切片细节:",
        "crop_view": "算法精准切片预览 (区域 {} / 五等分)",
        "chao_txt": "Chaotic (混乱)", "peace_txt": "Peaceful (宁静)",
        "box_header": "区域 {} 科学线索详细拆解", "sentence_template": "区域 {} 的{}是 "
    },
    "繁體中文": {
        "title": "地球磁盾：激波偵探",
        "input_header": "📥 輸入監測數據",
        "upload_limit_warning": "⚠️ 提示：為了保證算法精度，每次分析請**僅上傳唯一一張**圖表。",
        "uploader_lbl": "上傳一張激波能譜特徵圖：",
        "current_img_caption": "當前載入的分析圖像",
        "calibration_title": "🔧 **數據邊框校準**",
        "left_pad_lbl": "左側邊緣留白 (剔除Y軸):",
        "right_pad_lbl": "右側邊緣留白 (剔除圖例):",
        "output_header": "📊 空間天氣自動化診斷看板",
        "desc_txt": "等待上傳光譜圖以開啟全自動化特徵掃描與判定...",
        "btn_txt": "運行純圖像幾何算法動態分析 (A-E) 🚀",
        "spinner_txt": "正在逐像素執行純物理特徵提取...",
        "analysis_title": "區域微觀特徵深入剖析",
        "summary_title": "激波形態全局終審判決",
        "heat_lbl": "熱力圖", "line_lbl": "折線圖", "ridge_lbl": "山巒圖",
        "chaotic_zone": "🚨 完全 Chaotic (混亂) 區域", 
        "peaceful_zone": "🌲 完全 Peaceful (寧靜) 區域", 
        "mixed_zone": "🌀 二者都有的 Mixed (混合) 區域",
        "crop_radio": "查看算法切片細節:",
        "crop_view": "算法精準切片預覽 (區域 {} / 五等分)",
        "chao_txt": "Chaotic (混亂)", "peace_txt": "Peaceful (寧靜)",
        "box_header": "區域 {} 科學線索詳細拆解", "sentence_template": "區域 {} 的{}是 "
    },
    "Español": {
        "title": "Escudo Magnético de la Tierra: Detectives de Choque",
        "input_header": "📥 Datos de Telemetría",
        "upload_limit_warning": "⚠️ Nota: Por favor, suba **SOLO UNA** imagen por cada sesión de análisis.",
        "uploader_lbl": "Subir gráfico de espectrograma:",
        "current_img_caption": "Imagen de telemetría actual",
        "calibration_title": "🔧 **Calibración de límites de datos**",
        "left_pad_lbl": "Margen Izquierdo (Eje Y):",
        "right_pad_lbl": "Margen Derecho (Leyenda):",
        "output_header": "📊 Tablero de Diagnóstico",
        "desc_txt": "Esperando el gráfico para comenzar el análisis...",
        "btn_txt": "Ejecutar Análisis Algorítmico 🚀",
        "spinner_txt": "Analizando características de la imagen píxel por píxel...",
        "analysis_title": "Análisis Micro-Regional Profundo",
        "summary_title": "Resumen de Clasificación Global",
        "heat_lbl": "Espectrograma", "line_lbl": "Gráfico de Líneas", "ridge_lbl": "Gráfico de Crestas",
        "chaotic_zone": "🚨 Regiones Totalmente Caóticas", 
        "peaceful_zone": "🌲 Regiones Totalmente Pacíficas", 
        "mixed_zone": "🌀 Regiones Mixtas",
        "crop_radio": "Inspeccionar el recorte del algoritmo:",
        "crop_view": "Vista de recorte (Región {} / 5)",
        "chao_txt": "Caótico (Chaotic)", "peace_txt": "Pacífico (Peaceful)",
        "box_header": "Desglose de la Región {}", "sentence_template": "El {} de la Región {} es "
    },
    "Français": {
        "title": "Bouclier Magnétique: Détectives de Choc",
        "input_header": "📥 Télémétrie d'Entrée",
        "upload_limit_warning": "⚠️ Attention: Veuillez télécharger **UNE SEULE** image par session d'analyse.",
        "uploader_lbl": "Télécharger un spectrogramme:",
        "current_img_caption": "Image de télémétrie actuelle",
        "calibration_title": "🔧 **Calibration des bordures de données**",
        "left_pad_lbl": "Marge gauche (Axe Y):",
        "right_pad_lbl": "Marge droite (Légende):",
        "output_header": "📊 Tableau de Diagnostic",
        "desc_txt": "En attente du téléchargement de l'image...",
        "btn_txt": "Exécuter l'Analyse Algorithmique 🚀",
        "spinner_txt": "Analyse des pixels en cours...",
        "analysis_title": "Analyse Micro-Régionale Profonde",
        "summary_title": "Résumé de la Classification Globale",
        "heat_lbl": "Spectrogramme", "line_lbl": "Graphique Linéaire", "ridge_lbl": "Graphique de Crêtes",
        "chaotic_zone": "🚨 Régions Totalement Chaotiques", 
        "peaceful_zone": "🌲 Régions Totalement Pacifiques", 
        "mixed_zone": "🌀 Régions Mixtes",
        "crop_radio": "Inspecter la coupe algorithmique:",
        "crop_view": "Aperçu de la coupe (Région {} / 5)",
        "chao_txt": "Chaotique (Chaotic)", "peace_txt": "Pacifique (Peaceful)",
        "box_header": "Analyse de la Région {}", "sentence_template": "Le {} de la Région {} est "
    },
    "Deutsch": {
        "title": "Erdmagnetfeld: Schock-Detektive",
        "input_header": "📥 Eingabedaten",
        "upload_limit_warning": "⚠️ Hinweis: Bitte laden Sie für genaue Ergebnisse **NUR EIN** Bild hoch.",
        "uploader_lbl": "Spektrogramm hochladen:",
        "current_img_caption": "Aktuell hochgeladenes Bild",
        "calibration_title": "🔧 **Datenrahmen-Kalibrierung**",
        "left_pad_lbl": "Linker Rand (Y-Achse):",
        "right_pad_lbl": "Rechter Rand (Legende):",
        "output_header": "📊 Diagnose-Dashboard",
        "desc_txt": "Warten auf Bild-Upload...",
        "btn_txt": "Live-Algorithmus ausführen 🚀",
        "spinner_txt": "Analysiere Bildmerkmale Pixel für Pixel...",
        "analysis_title": "Tiefe Mikro-Regionale Analyse",
        "summary_title": "Globale Klassifizierungszusammenfassung",
        "heat_lbl": "Spektrogramm", "line_lbl": "Liniendiagramm", "ridge_lbl": "Kamm-Diagramm",
        "chaotic_zone": "🚨 Völlig Chaotische Regionen", 
        "peaceful_zone": "🌲 Völlig Friedliche Regionen", 
        "mixed_zone": "🌀 Gemischte Regionen",
        "crop_radio": "Algorithmischen Schnitt prüfen:",
        "crop_view": "Schnitt-Vorschau (Region {} / 5)",
        "chao_txt": "Chaotisch (Chaotic)", "peace_txt": "Friedlich (Peaceful)",
        "box_header": "Analyse für Region {}", "sentence_template": "Das {} in Region {} ist "
    },
    "日本語": {
        "title": "地球磁気シールド：ショック探偵",
        "input_header": "📥 テレメトリ入力",
        "upload_limit_warning": "⚠️ 注意：分析の精度を保つため、一度に**1枚のみ**画像をアップロードしてください。",
        "uploader_lbl": "スペクトログラムをアップロード：",
        "current_img_caption": "現在アップロードされている画像",
        "calibration_title": "🔧 **データ境界キャリブレーション**",
        "left_pad_lbl": "左余白 (Y軸除外):",
        "right_pad_lbl": "右余白 (凡例除外):",
        "output_header": "📊 宇宙天気診断ボード",
        "desc_txt": "画像がアップロードされるのを待っています...",
        "btn_txt": "画像解析アルゴリズムを実行 🚀",
        "spinner_txt": "ピクセル単位で特徴を抽出中...",
        "analysis_title": "領域ごとのマイクロ特徴詳細分析",
        "summary_title": "全体分類サマリー",
        "heat_lbl": "ヒートマップ", "line_lbl": "折れ線グラフ", "ridge_lbl": "リッジプロット",
        "chaotic_zone": "🚨 完全に Chaotic な領域", 
        "peaceful_zone": "🌲 完全に Peaceful な領域", 
        "mixed_zone": "🌀 混在 (Mixed) 領域",
        "crop_radio": "アルゴリズムスライスの詳細確認:",
        "crop_view": "スライスプレビュー (領域 {} / 5)",
        "chao_txt": "Chaotic (カオス)", "peace_txt": "Peaceful (平穏)",
        "box_header": "領域 {} の手がかり", "sentence_template": "領域 {} の{}は "
    },
    "Русский": {
        "title": "Магнитный щит Земли: Детективы шоков",
        "input_header": "📥 Ввод телеметрии",
        "upload_limit_warning": "⚠️ Примечание: Для обеспечения точности алгоритма загружайте **ТОЛЬКО ОДНО** изображение телеметрии за сеанс.",
        "uploader_lbl": "Загрузите график спектрограммы:",
        "current_img_caption": "Текущее загруженное изображение",
        "calibration_title": "🔧 **Калибровка границ данных**",
        "left_pad_lbl": "Левый отступ (Ось Y):",
        "right_pad_lbl": "Правый отступ (Легенда):",
        "output_header": "📊 Диагностическая панель",
        "desc_txt": "Ожидание загрузки спектрограммы для начала анализа...",
        "btn_txt": "Выполнить алгоритмический анализ 🚀",
        "spinner_txt": "Попиксельный анализ характеристик изображения...",
        "analysis_title": "Глубокий микро-региональный анализ",
        "summary_title": "Глобальная сводка классификации",
        "heat_lbl": "Спектрограмма энергии", "line_lbl": "Линейный график", "ridge_lbl": "Гребневой график",
        "chaotic_zone": "🚨 Полностью хаотичные регионы", 
        "peaceful_zone": "🌲 Полностью спокойные регионы", 
        "mixed_zone": "🌀 Смешанные регионы",
        "crop_radio": "Просмотр алгоритмического среза:",
        "crop_view": "Предварительный просмотр (Регион {} / 5)",
        "chao_txt": "Хаотичный (Chaotic)", "peace_txt": "Спокойный (Peaceful)",
        "box_header": "Детальный анализ региона {}", "sentence_template": "В регионе {} {} является "
    },
    "한국어": {
        "title": "지구 자기장 실드: 충격파 탐정",
        "input_header": "📥 원격 측정 입력",
        "upload_limit_warning": "⚠️ 주의: 알고리즘 정확도를 위해 세션당 **단 하나의** 이미지만 업로드하십시오.",
        "uploader_lbl": "스펙트로그램 플롯 업로드:",
        "current_img_caption": "현재 업로드된 이미지",
        "calibration_title": "🔧 **데이터 경계 보정**",
        "left_pad_lbl": "왼쪽 여백 (Y축):",
        "right_pad_lbl": "오른쪽 여백 (범례):",
        "output_header": "📊 우주 기상 진단 보드",
        "desc_txt": "분석을 시작하려면 스펙트로그램을 업로드하십시오...",
        "btn_txt": "실시간 알고리즘 분석 실행 🚀",
        "spinner_txt": "픽셀 단위로 이미지 특징 분석 중...",
        "analysis_title": "지역별 마이크로 특징 심층 분석",
        "summary_title": "전체 분류 요약",
        "heat_lbl": "에너지 스펙트로그램", "line_lbl": "시계열 선 그래프", "ridge_lbl": "능선 그래프",
        "chaotic_zone": "🚨 완전한 Chaotic 영역", 
        "peaceful_zone": "🌲 완전한 Peaceful 영역", 
        "mixed_zone": "🌀 혼합된 (Mixed) 영역",
        "crop_radio": "알고리즘 슬라이스 디테일 확인:",
        "crop_view": "슬라이스 미리보기 (영역 {} / 5)",
        "chao_txt": "혼란 (Chaotic)", "peace_txt": "평온 (Peaceful)",
        "box_header": "영역 {} 과학적 단서 분석", "sentence_template": "영역 {}의 {}은(는) "
    }
}

if "has_analyzed" not in st.session_state:
    st.session_state.has_analyzed = False
if "cropped_images" not in st.session_state:
    st.session_state.cropped_images = {}
if "live_computed_results" not in st.session_state:
    st.session_state.live_computed_results = {}

def reset_analysis():
    st.session_state.has_analyzed = False
    st.session_state.cropped_images = {}
    st.session_state.live_computed_results = {}

top_col1, top_col2 = st.columns([7.5, 2.5])
with top_col2:
    st.markdown("<p style='text-align: right; font-size: 24px; font-weight: 900; color: #38bdf8; margin: 0; padding: 0; line-height: 1.2;'>YCM Studio</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: right; font-size: 11px; color: #888; margin: 0 0 10px 0; padding: 0;'>Youth · Cognition · Machine</p>", unsafe_allow_html=True)
    lang = st.selectbox("", ["English", "简体中文", "繁體中文", "Español", "Français", "Deutsch", "日本語", "Русский", "한국어"], label_visibility="collapsed")

with top_col1:
    st.markdown(f"<h1 style='margin: 0; padding-top: 5px; color:#ffffff !important;'>{LANG_PACK[lang]['title']}</h1>", unsafe_allow_html=True)

st.markdown("---")

col_in, col_out = st.columns([4, 6])

with col_in:
    st.header(LANG_PACK[lang]["input_header"])
    
    # 强制单图警告提示
    st.warning(LANG_PACK[lang]["upload_limit_warning"])
    
    # accept_multiple_files=False 限制用户只能传一张
    uploaded_file = st.file_uploader(LANG_PACK[lang]["uploader_lbl"], type=["png", "jpg", "jpeg"], accept_multiple_files=False, on_change=reset_analysis)
    
    if uploaded_file:
        st.image(uploaded_file, caption=LANG_PACK[lang]["current_img_caption"], use_container_width=True)
        
        st.write("")
        st.markdown(LANG_PACK[lang]["calibration_title"])
        left_pad = st.slider(LANG_PACK[lang]["left_pad_lbl"], 0.0, 0.3, 0.125, step=0.005)
        right_pad = st.slider(LANG_PACK[lang]["right_pad_lbl"], 0.0, 0.3, 0.100, step=0.005)
        
        if st.button(LANG_PACK[lang]["btn_txt"], use_container_width=True):
            with st.spinner(LANG_PACK[lang]["spinner_txt"]):
                pil_img = Image.open(uploaded_file).convert("RGB")
                full_cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
                height, width, _ = full_cv_img.shape
                
                data_start_x = width * left_pad
                data_end_x = width * (1.0 - right_pad)
                actual_data_width = data_end_x - data_start_x
                slice_width = actual_data_width / 5
                
                y_heat_start, y_heat_end = int(height * 0.15), int(height * 0.36)
                y_line_start, y_line_end = int(height * 0.40), int(height * 0.65)
                y_ridge_start, y_ridge_end = int(height * 0.69), int(height * 0.93)

                regions_list = ["A", "B", "C", "D", "E"]
                st.session_state.live_computed_results = {}
                
                # ---------------- 【物理判定核心区：完美还原成功版本】 ----------------
                for i, r_name in enumerate(regions_list):
                    r_left = int(data_start_x + (i * slice_width))
                    r_right = int(data_start_x + ((i + 1) * slice_width))
                    
                    # 1. 🟥 热力图分析
                    heat_block = full_cv_img[y_heat_start:y_heat_end, r_left:r_right]
                    hsv_heat = cv2.cvtColor(heat_block, cv2.COLOR_BGR2HSV)
                    red_mask = cv2.inRange(hsv_heat, np.array([0, 60, 50]), np.array([12, 255, 255])) | \
                               cv2.inRange(hsv_heat, np.array([165, 60, 50]), np.array([180, 255, 255]))
                    red_ys = np.where(red_mask > 0)[0]
                    
                    if len(red_ys) > 0:
                        center_red_y = int(np.median(red_ys))
                        green_mask = cv2.inRange(hsv_heat, np.array([35, 35, 35]), np.array([85, 255, 255]))
                        green_ys = np.where(green_mask > 0)[0]
                        green_above = np.sum(green_ys < center_red_y)
                        green_below = np.sum(green_ys > center_red_y)
                        heat_status = "Chaotic" if green_above > green_below else "Peaceful"
                    else:
                        heat_status = "Peaceful"
                        
                    # 2. 📈 折线图分析
                    line_block = full_cv_img[y_line_start:y_line_end, r_left:r_right]
                    hsv_line = cv2.cvtColor(line_block, cv2.COLOR_BGR2HSV)
                    blue_mask = cv2.inRange(hsv_line, np.array([95, 50, 40]), np.array([140, 255, 255]))
                    red_mask_l = cv2.inRange(hsv_line, np.array([0, 50, 40]), np.array([15, 255, 255])) | \
                                 cv2.inRange(hsv_line, np.array([165, 50, 40]), np.array([180, 255, 255]))
                    
                    col_distances = []
                    for col in range(line_block.shape[1]):
                        b_pos = np.where(blue_mask[:, col] > 0)[0]
                        r_pos = np.where(red_mask_l[:, col] > 0)[0]
                        if len(b_pos) > 0 and len(r_pos) > 0:
                            col_distances.append(abs(np.mean(b_pos) - np.mean(r_pos)))
                    
                    if len(col_distances) > 0:
                        avg_dist = np.mean(col_distances)
                        line_status = "Peaceful" if avg_dist > (line_block.shape[0] * 0.16) else "Chaotic"
                    else:
                        line_status = "Peaceful"
                        
                    # 3. ⛰️ 山峦图分析 【🎯 包含 0.94 裁边与 >50% 防伪装的最终逻辑】
                    ridge_block = full_cv_img[y_ridge_start:y_ridge_end, r_left:r_right]
                    
                    # 放宽浅灰色的提取范围
                    gray_band = (ridge_block[:,:,0] >= 180) & (ridge_block[:,:,0] <= 245) & \
                                (ridge_block[:,:,1] >= 180) & (ridge_block[:,:,1] <= 245) & \
                                (ridge_block[:,:,2] >= 180) & (ridge_block[:,:,2] <= 245)
                    
                    # 🎯 防伪装：必须这一行里有超过 50% 都是灰色，才认定为长方形背景带！
                    gray_row_counts = np.sum(gray_band, axis=1)
                    valid_gray_rows = np.where(gray_row_counts > (ridge_block.shape[1] * 0.5))[0]
                    
                    if len(valid_gray_rows) > 0:
                        y_gray_min = np.min(valid_gray_rows)
                        y_gray_max = np.max(valid_gray_rows)
                    else:
                        y_gray_min = int(ridge_block.shape[0] * 0.70)
                        y_gray_max = int(ridge_block.shape[0] * 0.95)
                    
                    # 捕捉黑线
                    black_mask = (ridge_block[:,:,0] < 75) & (ridge_block[:,:,1] < 75) & (ridge_block[:,:,2] < 75)
                    # 🎯 释放基准区：只抹去最底端的 6% 坐标横轴
                    plot_area_limit = int(ridge_block.shape[0] * 0.94)
                    black_mask[plot_area_limit:, :] = 0
                    
                    col_inside_counts = 0
                    valid_cols = 0
                    
                    # 从左到右核查每一列黑线
                    for col in range(4, ridge_block.shape[1] - 4):
                        black_ys_in_col = np.where(black_mask[:, col])[0]
                        if len(black_ys_in_col) > 0:
                            valid_cols += 1
                            b_y_center = np.mean(black_ys_in_col)
                            if (y_gray_min - 2) <= b_y_center <= (y_gray_max + 2):
                                col_inside_counts += 1
                    
                    if valid_cols > 0:
                        inside_ratio = col_inside_counts / valid_cols
                        
                        # 落在里面 = 平缓不乱 = Peaceful
                        if inside_ratio >= 0.70:
                            ridge_status = "Peaceful"
                        # 大幅飞出灰色区域 = 狂风巨浪 = Chaotic
                        else:
                            ridge_status = "Chaotic"
                    else:
                        ridge_status = "Chaotic"
                        
                    st.session_state.live_computed_results[r_name] = {
                        "heat": heat_status,
                        "line": line_status,
                        "ridge": ridge_status
                    }
                    st.session_state.cropped_images[r_name] = pil_img.crop((r_left, 0, r_right, height))
                # ---------------- 【物理判定核心区结束】 ----------------
                
                st.session_state.has_analyzed = True

with col_out:
    st.header(LANG_PACK[lang]["output_header"])
    
    if st.session_state.has_analyzed:
        regions_list = ["A", "B", "C", "D", "E"]
        active_database = st.session_state.live_computed_results
        
        chaotic_regions = []
        peaceful_regions = []
        mixed_regions = []
        
        for region, clues in active_database.items():
            statuses = [clues["heat"], clues["line"], clues["ridge"]]
            if all(s == "Chaotic" for s in statuses):
                chaotic_regions.append(region)
            elif all(s == "Peaceful" for s in statuses):
                peaceful_regions.append(region)
            else:
                mixed_regions.append(region)
                
        st.subheader(LANG_PACK[lang]["analysis_title"])
        
        for r in regions_list:
            def get_status_html(status_type):
                val = active_database[r][status_type]
                if val == "Chaotic":
                    return f"<span class='status-badge chao-text'>{LANG_PACK[lang]['chao_txt']}</span>"
                else:
                    return f"<span class='status-badge peace-text'>{LANG_PACK[lang]['peace_txt']}</span>"
            
            html_heat = get_status_html("heat")
            html_line = get_status_html("line")
            html_ridge = get_status_html("ridge")
            
            header_text = LANG_PACK[lang]["box_header"].format(r)
            line1 = f"• {LANG_PACK[lang]['sentence_template'].format(r, f'<b>{LANG_PACK[lang]['heat_lbl']}</b>')} {html_heat};"
            line2 = f"• {LANG_PACK[lang]['sentence_template'].format(r, f'<b>{LANG_PACK[lang]['line_lbl']}</b>')} {html_line};"
            line3 = f"• {LANG_PACK[lang]['sentence_template'].format(r, f'<b>{LANG_PACK[lang]['ridge_lbl']}</b>')} {html_ridge};"
                
            evidence_text = f"""
            <div class='evidence-box'>
                🪐 <b>{header_text}：</b><br>
                {line1}<br>
                {line2}<br>
                {line3}
            </div>
            """
            st.markdown(evidence_text, unsafe_allow_html=True)
            
        st.write("")
        st.subheader(LANG_PACK[lang]["summary_title"])
        
        sum_col1, sum_col2, sum_col3 = st.columns(3)
        with sum_col1:
            st.markdown(f"<div style='background-color:rgba(255, 75, 75, 0.25); padding:15px; border-radius:8px; border-left:5px solid #ff4b4b;'><p style='margin:0; font-size:13px; color:#ffffff !important;'>{LANG_PACK[lang]['chaotic_zone']}</p><h2 style='margin:0; color:#ffffff !important;'>{', '.join(chaotic_regions) if chaotic_regions else 'None'}</h2></div>", unsafe_allow_html=True)
        with sum_col2:
            st.markdown(f"<div style='background-color:rgba(0, 230, 118, 0.25); padding:15px; border-radius:8px; border-left:5px solid #00e676;'><p style='margin:0; font-size:13px; color:#ffffff !important;'>{LANG_PACK[lang]['peaceful_zone']}</p><h2 style='margin:0; color:#ffffff !important;'>{', '.join(peaceful_regions) if peaceful_regions else 'None'}</h2></div>", unsafe_allow_html=True)
        with sum_col3:
            st.markdown(f"<div style='background-color:rgba(156, 163, 175, 0.25); padding:15px; border-radius:8px; border-left:5px solid #9ca3af;'><p style='margin:0; font-size:13px; color:#ffffff !important;'>{LANG_PACK[lang]['mixed_zone']}</p><h2 style='margin:0; color:#ffffff !important;'>{', '.join(mixed_regions) if mixed_regions else 'None'}</h2></div>", unsafe_allow_html=True)
            
        st.write("")
        st.markdown("---")
        inspect_r = st.radio(LANG_PACK[lang]["crop_radio"], regions_list, horizontal=True)
        
        if inspect_r in st.session_state.cropped_images:
            st.image(st.session_state.cropped_images[inspect_r], caption=LANG_PACK[lang]["crop_view"].format(inspect_r), width=150)
            
    else:
        st.info(LANG_PACK[lang]["desc_txt"])