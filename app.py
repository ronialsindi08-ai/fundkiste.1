<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fundkiste - Katharineum zu Lübeck</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        brandBg: '#ded6bb',
                        brandBtn: '#d1d95b',
                        brandBtnHover: '#c5cd50',
                        brandText: '#111111',
                        brandCard: '#f5f0e1'
                    },
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                        mono: ['JetBrains Mono', 'monospace']
                    }
                }
            }
        }
    </script>
    
    <style>
        /* Custom CSS matching Streamlit styling specifications */
        body {
            background-color: #ded6bb;
            color: #111111;
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
        }

        /* Large pupil-friendly button override */
        .st-btn {
            background-color: #d1d95b !important;
            color: #111111 !important;
            font-weight: 700 !important;
            font-size: 1.25rem !important;
            border-radius: 12px !important;
            width: 100% !important;
            padding: 1rem 1.5rem !important;
            transition: all 0.2s ease-in-out !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.75rem;
            border: 2px solid rgba(17, 17, 17, 0.1);
        }

        .st-btn:hover {
            background-color: #c5cd50 !important;
            transform: translateY(-2px);
            box-shadow: 0 6px 12px -2px rgba(0, 0, 0, 0.15);
        }

        .st-btn:active {
            transform: translateY(0);
        }

        .st-btn-secondary {
            background-color: #eae5d8 !important;
            border: 2px solid #111111 !important;
        }

        .st-btn-secondary:hover {
            background-color: #dfd8c7 !important;
        }

        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #ded6bb;
        }
        ::-webkit-scrollbar-thumb {
            background: #b8af93;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #9e957a;
        }
    </style>
</head>
<body class="flex flex-col min-h-screen">

    <!-- Top Bar Navigation with Code View Switcher -->
    <header class="bg-[#383329] text-white py-2 px-4 shadow-md sticky top-0 z-50">
        <div class="max-w-[900px] mx-auto flex justify-between items-center text-sm">
            <div class="flex items-center gap-2">
                <i class="fa-solid fa-graduation-cap text-[#d1d95b]"></i>
                <span class="font-semibold tracking-wide">Katharineum zu Lübeck</span>
            </div>
            <div class="flex items-center gap-1 bg-[#25221b] p-1 rounded-lg">
                <button id="tabAppBtn" onclick="switchView('app')" class="px-3 py-1 rounded-md text-xs font-semibold bg-[#d1d95b] text-[#111111] transition-all">
                    <i class="fa-solid fa-mobile-screen mr-1"></i> Web-App Simulation
                </button>
                <button id="tabCodeBtn" onclick="switchView('code')" class="px-3 py-1 rounded-md text-xs font-semibold text-gray-300 hover:text-white transition-all">
                    <i class="fa-solid fa-code mr-1"></i> Python Code (app.py)
                </button>
            </div>
        </div>
    </header>

    <!-- Main Content Container (Max width 900px as requested) -->
    <main class="flex-grow max-w-[900px] w-full mx-auto p-4 md:p-6">

        <!-- Header Section -->
        <div id="headerTitleBlock" class="text-center my-6">
            <h1 class="text-4xl md:text-5xl font-extrabold tracking-tight text-[#111111] mb-2 flex items-center justify-center gap-3">
                <span>Fundkiste</span>
                <span class="text-3xl text-[#635d47]">🔎</span>
            </h1>
            <div class="flex items-center justify-center gap-3 text-sm md:text-base font-semibold text-[#403b2e] tracking-wider uppercase">
                <span>●</span>
                <span>Katharineum zu Lübeck</span>
                <span>●</span>
                <span>seit 1531</span>
            </div>
            <hr class="border-t-2 border-[#111111]/15 mt-6 mb-2">
        </div>

        <!-- ========================================== -->
        <!-- VIEW 1: INTERACTIVE WEB-APP SIMULATION    -->
        <!-- ========================================== -->
        <div id="viewApp" class="space-y-6">

            <!-- PAGE: START -->
            <div id="pageStart" class="space-y-6 py-6">
                <div class="bg-white/40 backdrop-blur-sm p-6 rounded-2xl border border-black/10 text-center mb-8 shadow-sm">
                    <p class="text-lg font-medium text-[#222222]">
                        Willkommen beim digitalen Fundbüro des Katharineums! Hast du etwas verloren oder einen herrenlosen Gegenstand gefunden?
                    </p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-2xl mx-auto">
                    <button onclick="navigateTo('suchen')" class="st-btn py-8 text-xl">
                        <i class="fa-solid fa-magnifying-glass text-2xl"></i>
                        <span>🔎 Suchen</span>
                    </button>

                    <button onclick="navigateTo('eingeben')" class="st-btn py-8 text-xl">
                        <i class="fa-solid fa-camera text-2xl"></i>
                        <span>📷 Fundstück hinzufügen</span>
                    </button>
                </div>

                <!-- Live Statistics Badge -->
                <div class="mt-12 text-center text-sm font-semibold text-[#403b2e] bg-[#d5ccb0] py-2 px-4 rounded-full w-fit mx-auto shadow-inner">
                    <i class="fa-solid fa-box-archive mr-1"></i>
                    Aktuell registrierte Fundstücke: <span id="itemCountBadge">0</span>
                </div>
            </div>

            <!-- PAGE: EINGEBEN (ADD ITEM) -->
            <div id="pageEingeben" class="hidden space-y-6">
                <div class="flex items-center justify-between mb-4">
                    <button onclick="navigateTo('start')" class="px-4 py-2 rounded-xl bg-[#c0b699] hover:bg-[#b0a689] font-bold text-[#111111] transition-all flex items-center gap-2">
                        <i class="fa-solid fa-arrow-left"></i> ← Zurück
                    </button>
                    <h2 class="text-2xl font-bold">Fundstück eingeben</h2>
                </div>

                <div class="bg-[#f5f0e1] p-6 rounded-2xl shadow-sm border border-black/10 space-y-6">
                    <!-- Photo Upload / Capture Section -->
                    <div>
                        <label class="block text-base font-bold text-[#111111] mb-2">
                            📷 Foto des Fundstücks hochladen
                        </label>
                        <div class="flex flex-col items-center justify-center border-2 border-dashed border-[#8c8266] rounded-xl p-6 bg-[#ded6bb]/50 hover:bg-[#ded6bb] transition-all cursor-pointer relative" id="dropArea" onclick="document.getElementById('fileInput').click()">
                            <input type="file" id="fileInput" accept="image/png, image/jpeg, image/jpg" class="hidden" onchange="handleFileSelect(event)">
                            <div id="uploadPlaceholder" class="text-center">
                                <i class="fa-solid fa-cloud-arrow-up text-4xl text-[#524a35] mb-2"></i>
                                <p class="font-semibold text-sm">Klicke hier oder ziehe ein Bild hinein</p>
                                <p class="text-xs text-[#665e47] mt-1">Unterstützte Formate: JPG, JPEG, PNG</p>
                            </div>
                            <!-- Image Preview Container -->
                            <div id="previewContainer" class="hidden w-full flex flex-col items-center">
                                <img id="imagePreview" src="" alt="Vorschau" class="max-h-64 rounded-xl object-contain border border-black/20 shadow-md">
                                <button type="button" onclick="event.stopPropagation(); resetImage();" class="mt-3 text-xs bg-red-600 hover:bg-red-700 text-white font-bold py-1 px-3 rounded-lg">
                                    <i class="fa-solid fa-trash mr-1"></i> Foto entfernen
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- AI Spinner & Recognition Output -->
                    <div id="aiSpinner" class="hidden bg-[#ded6bb] p-4 rounded-xl flex items-center justify-center gap-3 border border-black/10">
                        <i class="fa-solid fa-circle-notch fa-spin text-xl text-[#383329]"></i>
                        <span class="font-semibold text-sm">Die KI erkennt das Fundstück ...</span>
                    </div>

                    <div id="aiResultSuccess" class="hidden space-y-2">
                        <div class="bg-green-100 border-l-4 border-green-600 p-4 rounded-r-xl text-green-900">
                            <p class="font-bold text-lg" id="aiKategorieText">Erkannt: **Mütze**</p>
                            <p class="text-sm font-semibold text-green-800" id="aiConfidenceText">KI-Sicherheit: **98.4%**</p>
                        </div>
                    </div>

                    <div id="aiResultError" class="hidden bg-red-100 border-l-4 border-red-600 p-4 rounded-r-xl text-red-900">
                        <p class="font-bold">Fehler bei der KI-Erkennung</p>
                        <p class="text-xs font-mono mt-1" id="aiErrorMessage">Model context failed</p>
                    </div>

                    <!-- Location Input -->
                    <div>
                        <label for="fundortInput" class="block text-base font-bold text-[#111111] mb-2">
                            📍 Wo wurde es gefunden? <span class="text-red-600">*</span>
                        </label>
                        <input type="text" id="fundortInput" placeholder="z. B. Sporthalle, Pausenhof, Flur OG2, Mensa..." class="w-full p-3 rounded-xl border border-black/20 bg-white font-medium focus:ring-2 focus:ring-[#d1d95b] focus:outline-none">
                    </div>

                    <!-- Warning Message -->
                    <div id="validationWarning" class="hidden bg-amber-100 border-l-4 border-amber-500 p-3 rounded-r-xl text-amber-900 text-sm font-semibold">
                        <i class="fa-solid fa-triangle-exclamation mr-1"></i> Bitte gib einen Fundort an, bevor du das Fundstück speicherst!
                    </div>

                    <!-- Save Button -->
                    <button onclick="saveFundstueck()" class="st-btn text-lg py-4">
                        <i class="fa-solid fa-floppy-disk"></i> Fundstück speichern
                    </button>
                </div>
            </div>

            <!-- PAGE: SUCHEN (SEARCH & FILTER) -->
            <div id="pageSuchen" class="hidden space-y-6">
                <div class="flex items-center justify-between mb-2">
                    <button onclick="navigateTo('start')" class="px-4 py-2 rounded-xl bg-[#c0b699] hover:bg-[#b0a689] font-bold text-[#111111] transition-all flex items-center gap-2">
                        <i class="fa-solid fa-arrow-left"></i> ← Zurück
                    </button>
                    <h2 class="text-2xl font-bold">Fundstücke suchen</h2>
                </div>

                <!-- Filter Controls -->
                <div class="bg-[#f5f0e1] p-5 rounded-2xl border border-black/10 shadow-sm space-y-4">
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <!-- Search term -->
                        <div>
                            <label class="block text-xs font-bold uppercase text-[#403b2e] mb-1">Was suchst du?</label>
                            <input type="text" id="searchFreitext" placeholder="Suchbegriff..." oninput="filterFundstuecke()" class="w-full p-2.5 rounded-xl border border-black/20 bg-white text-sm font-medium focus:ring-2 focus:ring-[#d1d95b] focus:outline-none">
                        </div>

                        <!-- Category Select -->
                        <div>
                            <label class="block text-xs font-bold uppercase text-[#403b2e] mb-1">Kategorie</label>
                            <select id="searchKategorie" onchange="filterFundstuecke()" class="w-full p-2.5 rounded-xl border border-black/20 bg-white text-sm font-medium focus:ring-2 focus:ring-[#d1d95b] focus:outline-none">
                                <option value="Alle">Alle Kategorien</option>
                            </select>
                        </div>

                        <!-- Location Search -->
                        <div>
                            <label class="block text-xs font-bold uppercase text-[#403b2e] mb-1">Fundort</label>
                            <input type="text" id="searchOrt" placeholder="z. B. Sporthalle" oninput="filterFundstuecke()" class="w-full p-2.5 rounded-xl border border-black/20 bg-white text-sm font-medium focus:ring-2 focus:ring-[#d1d95b] focus:outline-none">
                        </div>
                    </div>
                </div>

                <!-- Results Section -->
                <div id="resultsContainer" class="space-y-4">
                    <!-- Dynamic Items injected via JS -->
                </div>

                <div id="noResults" class="hidden text-center py-12 bg-white/30 rounded-2xl border border-dashed border-black/20">
                    <i class="fa-solid fa-ghost text-4xl text-[#776e55] mb-2"></i>
                    <p class="text-lg font-bold text-[#332f24]">Kein passendes Fundstück gefunden.</p>
                    <p class="text-sm text-[#554d39]">Versuche die Filtereinstellungen anzupassen.</p>
                </div>
            </div>

        </div>

        <!-- ========================================== -->
        <!-- VIEW 2: FULL PYTHON STREAMLIT CODE (app.py)-->
        <!-- ========================================== -->
        <div id="viewCode" class="hidden space-y-4">
            <div class="bg-[#2d2a24] p-4 rounded-xl text-white flex justify-between items-center">
                <div>
                    <h3 class="font-bold text-lg text-[#d1d95b]"><i class="fa-brands fa-python mr-2"></i>Vollständige Streamlit Python-App (`app.py`)</h3>
                    <p class="text-xs text-gray-300">Lauffähiger Code mit Keras MobileNetV2 HDF5 Fallback, CSV Storage & st.cache_resource.</p>
                </div>
                <button onclick="copyCodeToClipboard()" class="px-4 py-2 bg-[#d1d95b] text-[#111111] font-bold rounded-lg hover:bg-[#c5cd50] transition-all flex items-center gap-2 text-sm">
                    <i class="fa-regular fa-copy"></i> <span id="copyBtnText">Code kopieren</span>
                </button>
            </div>

            <div class="relative rounded-2xl overflow-hidden border border-black/30 shadow-2xl bg-[#1e1e1e]">
                <pre class="p-4 text-xs font-mono text-gray-200 overflow-x-auto max-h-[70vh] leading-relaxed" id="pythonCodeDisplay"><code># ==============================================================================
# FUNDKISTE - KATHARINEUM ZU LÜBECK (SEIT 1531)
# Vollständige Streamlit Web-Anwendung
# ==============================================================================

import os
import io
import time
import pandas as pd
import numpy as np
from PIL import Image
import streamlit as st
import tensorflow as tf
import h5py

# ------------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & DESIGN
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Fundkiste",
    page_icon="🔎",
    layout="centered"
)

# Custom CSS matching design rules
st.markdown("""
<style>
    /* Content width maximum 900px */
    .block-container {
        max-width: 900px !important;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Background color #ded6bb */
    .stApp {
        background-color: #ded6bb;
        color: #111111;
    }
    
    /* Global Text Color */
    html, body, [class*="css"] {
        color: #111111;
        font-family: 'Inter', sans-serif;
    }
    
    /* Big Pupils Buttons for both old and new Streamlit versions */
    div.stButton > button, div[data-testid="stButton"] > button {
        background-color: #d1d95b !important;
        color: #111111 !important;
        font-weight: bold !important;
        font-size: 20px !important;
        border-radius: 12px !important;
        width: 100% !important;
        border: 1px solid rgba(0,0,0,0.1) !important;
        padding: 0.75rem 1rem !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease-in-out;
    }
    
    div.stButton > button:hover, div[data-testid="stButton"] > button:hover {
        background-color: #c5cd50 !important;
        transform: translateY(-2px);
    }
    
    /* Input fields styling */
    div[data-baseweb="input"] {
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# 2. DATA STORAGE INITIALIZATION (CSV & FOLDERS)
# ------------------------------------------------------------------------------
DATA_DIR = "data"
FOTOS_DIR = os.path.join(DATA_DIR, "fotos")
CSV_PATH = os.path.join(DATA_DIR, "fundstuecke.csv")

os.makedirs(FOTOS_DIR, exist_ok=True)

def lade_datenbank():
    """Lädt die CSV-Datenbank sicher und ergänzt fehlende Spalten."""
    spalten = ["Gegenstand", "Kategorie", "Fundort", "Datum", "Foto"]
    if not os.path.exists(CSV_PATH):
        df = pd.DataFrame(columns=spalten)
        df.to_csv(CSV_PATH, index=False)
        return df
    
    try:
        df = pd.read_csv(CSV_PATH)
        for col in spalten:
            if col not in df.columns:
                df[col] = ""
        return df.fillna("")
    except Exception:
        df = pd.DataFrame(columns=spalten)
        return df


# ------------------------------------------------------------------------------
# 3. KI MODEL LOADING & INFERENCE (TEACHABLE MACHINE / MOBILENET V2)
# ------------------------------------------------------------------------------
MODEL_FILE = "keras_model.h5"
LABELS_FILE = "labels.txt"

@st.cache_resource
def lade_ki():
    """
    Lädt das Keras-Modell mit zweistufigem Fallback:
    1) Direktes keras.models.load_model
    2) Manuelles HDF5-Gewichte-Parsing aus Sequential-Gruppen
    """
    # Labels laden
    labels = []
    if os.path.exists(LABELS_FILE):
        with open(LABELS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(" ", 1)
                labels.append(parts[1] if len(parts) > 1 else parts[0])
    else:
        labels = ["Helm", "Trinkflasche", "Mütze", "Turnbeutel", "Jacke", "Sonstiges"]

    # VERSUCH 1: Standard Keras Load
    try:
        model = tf.keras.models.load_model(MODEL_FILE, compile=False)
        return model, labels, None
    except Exception as err1:
        err_msg1 = str(err1)

    # VERSUCH 2: Manueller Fallback per MobileNetV2 + h5py
    try:
        base_model = tf.keras.applications.MobileNetV2(
            input_shape=(224, 224, 3),
            include_top=False,
            weights=None
        )
        
        with h5py.File(MODEL_FILE, "r") as f:
            weights_grp = f["model_weights"]
            
            # Basis-Gewichte übertragen
            for layer in base_model.layers:
                lname = layer.name
                if lname in weights_grp:
                    lgrp = weights_grp[lname]
                    param_names = [k for k in lgrp.keys()]
                    params = []
                    for p in param_names:
                        # Lookup mit und ohne :0
                        key = p if p in lgrp else p.replace(":0", "")
                        params.append(np.array(lgrp[key]))
                    if params:
                        layer.set_weights(params)

            # Sequential Classifier Gewichte auslesen
            seq3 = weights_grp["sequential_3"]
            dense1_grp = seq3["dense_Dense1"]
            dense2_grp = seq3["dense_Dense2"]

            # Keys auflösen
            k1 = "kernel:0" if "kernel:0" in dense1_grp else "kernel"
            b1 = "bias:0" if "bias:0" in dense1_grp else "bias"
            w_dense1 = np.array(dense1_grp[k1])
            b_dense1 = np.array(dense1_grp[b1])

            k2 = "kernel:0" if "kernel:0" in dense2_grp else "kernel"
            w_dense2 = np.array(dense2_grp[k2])

        # Modell neu zusammenbauen
        x = tf.keras.layers.GlobalAveragePooling2D()(base_model.output)
        x = tf.keras.layers.Dense(w_dense1.shape[1], activation="relu")(x)
        outputs = tf.keras.layers.Dense(len(labels), activation="softmax", use_bias=False)(x)
        
        custom_model = tf.keras.Model(inputs=base_model.input, outputs=outputs)
        
        # Classifier Gewichte setzen
        dense_layers = [l for l in custom_model.layers if isinstance(l, tf.keras.layers.Dense)]
        dense_layers[0].set_weights([w_dense1, b_dense1])
        dense_layers[1].set_weights([w_dense2])

        return custom_model, labels, None

    except Exception as err2:
        return None, labels, f"Model-Load Error:\n1) {err_msg1}\n2) {str(err2)}"


@st.cache_data
def vorhersage_ki(image_bytes):
    """Führt KI-Vorhersage auf Bilddaten durch."""
    model, labels, err = lade_ki()
    if err or model is None:
        return None, 0.0, err
    
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image = image.resize((224, 224))
        img_array = np.asarray(image, dtype=np.float32)
        # Normalisierung: (pixel / 127.5) - 1.0
        normalized_image = (img_array / 127.5) - 1.0
        data = np.expand_dims(normalized_image, axis=0)
        
        prediction = model.predict(data, verbose=0)
        index = np.argmax(prediction[0])
        confidence = float(prediction[0][index]) * 100.0
        kategorie = labels[index] if index < len(labels) else "Unbekannt"
        
        return kategorie, confidence, None
    except Exception as e:
        return None, 0.0, str(e)


# ------------------------------------------------------------------------------
# 4. SESSION STATE & NAVIGATION
# ------------------------------------------------------------------------------
if "seite" not in st.session_state:
    st.session_state.seite = "start"

def set_seite(ziel):
    st.session_state.seite = ziel
    st.rerun()


# Header Banner
st.markdown("<h1 style='text-align: center; margin-bottom: 0px;'>Fundkiste</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold; margin-top: 0px;'>● KATHARINEUM ZU LÜBECK ● seit 1531</p>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #111111; opacity: 0.15;'>", unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# SEITE 1: STARTSEITE
# ------------------------------------------------------------------------------
if st.session_state.seite == "start":
    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔎 Suchen"):
            set_seite("suchen")
    with col2:
        if st.button("📷 Fundstück hinzufügen"):
            set_seite("eingeben")


# ------------------------------------------------------------------------------
# SEITE 2: FUNDSTÜCK HINZUFÜGEN
# ------------------------------------------------------------------------------
elif st.session_state.seite == "eingeben":
    if st.button("← Zurück"):
        set_seite("start")
        
    st.subheader("Fundstück hinzufügen")
    
    uploaded_file = st.file_uploader("Foto des Fundstücks hochladen", type=["jpg", "jpeg", "png"])
    fundort = st.text_input("Wo wurde es gefunden?")
    
    kategorie_erkannt = None
    
    if uploaded_file is not None:
        image_bytes = uploaded_file.getvalue()
        # Bild anzeigen mit moderner Streamlit Syntax width="stretch"
        st.image(image_bytes, width="stretch")
        
        with st.spinner("Die KI erkennt das Fundstück ..."):
            kat, conf, err = vorhersage_ki(image_bytes)
            
        if err:
            st.error("Fehler bei der KI-Erkennung:")
            st.code(err)
            kategorie_erkannt = "Unbekannt"
        else:
            kategorie_erkannt = kat
            st.success(f"Erkannt: **{kat}**")
            st.info(f"KI-Sicherheit: **{conf:.1f}%**")
            
    if st.button("Speichern"):
        if not fundort.strip():
            st.warning("Bitte gib einen Fundort an!")
        elif uploaded_file is None:
            st.warning("Bitte lade zuerst ein Foto des Fundstücks hoch!")
        else:
            # Foto mit EINDEUTIGEM Zeitstempel speichern
            timestamp = int(time.time() * 1000)
            date_str = time.strftime("%d.%m.%Y")
            file_ext = os.path.splitext(uploaded_file.name)[1].lower() or ".jpg"
            dateiname = f"fund_{timestamp}{file_ext}"
            foto_pfad = os.path.join(FOTOS_DIR, dateiname)
            
            # Speicher-Bild konvertieren nach RGB (für JPEG Transparenz-Sicherheit)
            img = Image.open(uploaded_file).convert("RGB")
            img.save(foto_pfad)
            
            # CSV Eintrag vornehmen
            df = lade_datenbank()
            neuer_eintrag = pd.DataFrame([{
                "Gegenstand": kategorie_erkannt or "Gegenstand",
                "Kategorie": kategorie_erkannt or "Unbekannt",
                "Fundort": fundort.strip(),
                "Datum": date_str,
                "Foto": foto_pfad
            }])
            
            df = pd.concat([df, neuer_eintrag], ignore_index=True)
            df.to_csv(CSV_PATH, index=False)
            
            st.success("Fundstück erfolgreich gespeichert!")
            time.sleep(1)
            set_seite("start")


# ------------------------------------------------------------------------------
# SEITE 3: FUNDSTÜCKE SUCHEN
# ------------------------------------------------------------------------------
elif st.session_state.seite == "suchen":
    if st.button("← Zurück"):
        set_seite("start")
        
    st.subheader("Fundstücke suchen")
    
    df = lade_datenbank()
    
    if df.empty:
        st.info("Es wurden noch keine Fundstücke eingetragen.")
    else:
        # Filter
        c1, c2, c3 = st.columns(3)
        with c1:
            query_text = st.text_input("Was suchst du?")
        with c2:
            kategorien = ["Alle"] + sorted(list(set(df["Kategorie"].astype(str).tolist())))
            selected_kat = st.selectbox("Kategorie", kategorien)
        with c3:
            query_ort = st.text_input("Fundort")

        # Gefilterter DataFrame (case-insensitive & regex=False)
        gefiltert = df.copy()
        
        if query_text.strip():
            gefiltert = gefiltert[gefiltert["Gegenstand"].str.contains(query_text, case=False, regex=False) |
                                 gefiltert["Kategorie"].str.contains(query_text, case=False, regex=False)]
            
        if selected_kat != "Alle":
            gefiltert = gefiltert[gefiltert["Kategorie"] == selected_kat]
            
        if query_ort.strip():
            gefiltert = gefiltert[gefiltert["Fundort"].str.contains(query_ort, case=False, regex=False)]

        # Anzeige der Ergebnisse
        if gefiltert.empty:
            st.warning("Kein passendes Fundstück gefunden.")
        else:
            for idx, row in gefiltert.iterrows():
                st.divider()
                col_img, col_info = st.columns([1, 2])
                
                with col_img:
                    if os.path.exists(str(row["Foto"])):
                        st.image(row["Foto"], width="stretch")
                    else:
                        st.text("Kein Bild")
                        
                with col_info:
                    st.subheader(str(row["Gegenstand"]))
                    st.write(f"Kategorie: **{row['Kategorie']}**")
                    st.write(f"Fundort: **{row['Fundort']}**")
                    st.write(f"Datum: **{row['Datum']}**")
</code></pre>
            </div>
        </div>

    </main>

    <!-- Footer -->
    <footer class="text-center py-4 text-xs font-semibold text-[#554e3a] border-t border-black/10">
        Katharineum zu Lübeck &bull; Digitales Fundbüro &bull; Seit 1531
    </footer>

    <script>
        // Sample Initial Data (Demo Items for Katharineum zu Lübeck)
        const DEFAULT_ITEMS = [
            {
                id: '1695000000001',
                gegenstand: 'Fahrradhelm (ABUS)',
                kategorie: 'Helm',
                fundort: 'Sporthalle A (Umkleide)',
                datum: '20.09.2026',
                foto: 'https://images.unsplash.com/photo-1557804506-669a67965ba0?w=500&auto=format&fit=crop&q=80',
                confidence: 99.1
            },
            {
                id: '1695000000002',
                gegenstand: 'Trinkflasche (Rot)',
                kategorie: 'Trinkflasche',
                fundort: 'Großer Pausenhof',
                datum: '21.09.2026',
                foto: 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500&auto=format&fit=crop&q=80',
                confidence: 96.5
            },
            {
                id: '1695000000003',
                gegenstand: 'Wollmütze (Dunkelblau)',
                kategorie: 'Mütze',
                fundort: 'Flur OG 2 (nahe R204)',
                datum: '22.09.2026',
                foto: 'https://images.unsplash.com/photo-1576871337632-b9aef4c17ab9?w=500&auto=format&fit=crop&q=80',
                confidence: 94.8
            }
        ];

        // State Management
        let items = [];
        let uploadedImageBase64 = null;
        let simulatedCategory = null;

        // Initialize App
        window.onload = function() {
            loadItemsFromStorage();
            updateItemCountBadge();
            populateCategorySelect();
            renderSearchResults();
        };

        // Switch Top Header View (App vs Python Code)
        function switchView(view) {
            const appView = document.getElementById('viewApp');
            const codeView = document.getElementById('viewCode');
            const appBtn = document.getElementById('tabAppBtn');
            const codeBtn = document.getElementById('tabCodeBtn');

            if (view === 'app') {
                appView.classList.remove('hidden');
                codeView.classList.add('hidden');
                appBtn.className = 'px-3 py-1 rounded-md text-xs font-semibold bg-[#d1d95b] text-[#111111] transition-all';
                codeBtn.className = 'px-3 py-1 rounded-md text-xs font-semibold text-gray-300 hover:text-white transition-all';
            } else {
                appView.classList.add('hidden');
                codeView.classList.remove('hidden');
                codeBtn.className = 'px-3 py-1 rounded-md text-xs font-semibold bg-[#d1d95b] text-[#111111] transition-all';
                appBtn.className = 'px-3 py-1 rounded-md text-xs font-semibold text-gray-300 hover:text-white transition-all';
            }
        }

        // Navigation between pages
        function navigateTo(page) {
            document.getElementById('pageStart').classList.add('hidden');
            document.getElementById('pageEingeben').classList.add('hidden');
            document.getElementById('pageSuchen').classList.add('hidden');

            if (page === 'start') {
                document.getElementById('pageStart').classList.remove('hidden');
                resetForm();
            } else if (page === 'eingeben') {
                document.getElementById('pageEingeben').classList.remove('hidden');
            } else if (page === 'suchen') {
                document.getElementById('pageSuchen').classList.remove('hidden');
                filterFundstuecke();
            }
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        // Storage operations
        function loadItemsFromStorage() {
            const stored = localStorage.getItem('fundkiste_items');
            if (stored) {
                try {
                    items = JSON.parse(stored);
                } catch(e) {
                    items = DEFAULT_ITEMS;
                }
            } else {
                items = DEFAULT_ITEMS;
                localStorage.setItem('fundkiste_items', JSON.stringify(items));
            }
        }

        function saveItemsToStorage() {
            localStorage.setItem('fundkiste_items', JSON.stringify(items));
            updateItemCountBadge();
            populateCategorySelect();
        }

        function updateItemCountBadge() {
            document.getElementById('itemCountBadge').textContent = items.length;
        }

        // File Selection & AI Classifier Simulation
        function handleFileSelect(event) {
            const file = event.target.files[0];
            if (!file) return;

            if (!file.type.match('image.*')) {
                alert('Bitte wähle eine gültige Bilddatei (JPG, PNG) aus.');
                return;
            }

            const reader = new FileReader();
            reader.onload = function(e) {
                uploadedImageBase64 = e.target.result;
                document.getElementById('imagePreview').src = uploadedImageBase64;
                document.getElementById('uploadPlaceholder').classList.add('hidden');
                document.getElementById('previewContainer').classList.remove('hidden');

                // Trigger AI Recognition Simulation
                runSimulatedAI(file.name);
            };
            reader.readAsDataURL(file);
        }

        function resetImage() {
            uploadedImageBase64 = null;
            simulatedCategory = null;
            document.getElementById('fileInput').value = '';
            document.getElementById('imagePreview').src = '';
            document.getElementById('uploadPlaceholder').classList.remove('hidden');
            document.getElementById('previewContainer').classList.add('hidden');
            document.getElementById('aiSpinner').classList.add('hidden');
            document.getElementById('aiResultSuccess').classList.add('hidden');
            document.getElementById('aiResultError').classList.add('hidden');
        }

        function resetForm() {
            resetImage();
            document.getElementById('fundortInput').value = '';
            document.getElementById('validationWarning').classList.add('hidden');
        }

        function runSimulatedAI(fileName) {
            const spinner = document.getElementById('aiSpinner');
            const successBox = document.getElementById('aiResultSuccess');
            const errorBox = document.getElementById('aiResultError');

            spinner.classList.remove('hidden');
            successBox.classList.add('hidden');
            errorBox.classList.add('hidden');

            // Simulate Teachable Machine delay
            setTimeout(() => {
                spinner.classList.add('hidden');

                // AI Categories matching model labels
                const categories = ['Helm', 'Trinkflasche', 'Mütze', 'Turnbeutel', 'Jacke', 'Mappe/Buch'];
                const lowerName = fileName.toLowerCase();

                let detected = categories[Math.floor(Math.random() * categories.length)];
                if (lowerName.includes('helm')) detected = 'Helm';
                else if (lowerName.includes('flasche') || lowerName.includes('bottle')) detected = 'Trinkflasche';
                else if (lowerName.includes('mütze') || lowerName.includes('hat')) detected = 'Mütze';
                else if (lowerName.includes('beutel') || lowerName.includes('bag')) detected = 'Turnbeutel';

                const confidence = (89 + Math.random() * 10).toFixed(1);
                simulatedCategory = detected;

                document.getElementById('aiKategorieText').innerHTML = `Erkannt: <strong>${detected}</strong>`;
                document.getElementById('aiConfidenceText').innerHTML = `KI-Sicherheit: <strong>${confidence}%</strong>`;
                successBox.classList.remove('hidden');
            }, 1200);
        }

        // Save new item
        function saveFundstueck() {
            const fundort = document.getElementById('fundortInput').value.trim();
            const warning = document.getElementById('validationWarning');

            if (!fundort) {
                warning.classList.remove('hidden');
                return;
            }
            warning.classList.add('hidden');

            if (!uploadedImageBase64) {
                alert('Bitte lade ein Foto des Fundstücks hoch.');
                return;
            }

            const now = new Date();
            const day = String(now.getDate()).padStart(2, '0');
            const month = String(now.getMonth() + 1).padStart(2, '0');
            const year = now.getFullYear();
            const formattedDate = `${day}.${month}.${year}`;

            const newItem = {
                id: String(Date.now()),
                gegenstand: simulatedCategory || 'Fundstück',
                kategorie: simulatedCategory || 'Sonstiges',
                fundort: fundort,
                datum: formattedDate,
                foto: uploadedImageBase64,
                confidence: 95.0
            };

            items.unshift(newItem);
            saveItemsToStorage();

            alert('✅ Fundstück erfolgreich in der Fundkiste registriert!');
            navigateTo('start');
        }

        // Search & Filter Logic
        function populateCategorySelect() {
            const select = document.getElementById('searchKategorie');
            const categories = new Set(items.map(item => item.kategorie));
            
            select.innerHTML = '<option value="Alle">Alle Kategorien</option>';
            categories.forEach(cat => {
                const opt = document.createElement('option');
                opt.value = cat;
                opt.textContent = cat;
                select.appendChild(opt);
            });
        }

        function filterFundstuecke() {
            const freitext = document.getElementById('searchFreitext').value.toLowerCase().trim();
            const kategorie = document.getElementById('searchKategorie').value;
            const ort = document.getElementById('searchOrt').value.toLowerCase().trim();

            const filtered = items.filter(item => {
                const matchFreitext = !freitext || 
                    item.gegenstand.toLowerCase().includes(freitext) || 
                    item.kategorie.toLowerCase().includes(freitext);

                const matchKategorie = (kategorie === 'Alle') || (item.kategorie === kategorie);

                const matchOrt = !ort || item.fundort.toLowerCase().includes(ort);

                return matchFreitext && matchKategorie && matchOrt;
            });

            renderSearchResults(filtered);
        }

        function renderSearchResults(resultsList = items) {
            const container = document.getElementById('resultsContainer');
            const noResults = document.getElementById('noResults');

            container.innerHTML = '';

            if (resultsList.length === 0) {
                noResults.classList.remove('hidden');
                return;
            }
            noResults.classList.add('hidden');

            resultsList.forEach(item => {
                const card = document.createElement('div');
                card.className = 'bg-[#f5f0e1] rounded-2xl p-4 border border-black/10 shadow-sm flex flex-col md:flex-row gap-4 items-center transition-all hover:shadow-md';

                card.innerHTML = `
                    <div class="w-full md:w-1/3 h-48 rounded-xl overflow-hidden bg-[#ded6bb] flex items-center justify-center border border-black/10 flex-shrink-0">
                        <img src="${item.foto}" alt="${item.gegenstand}" class="w-full h-full object-cover" onerror="this.src='https://placehold.co/400x300/ded6bb/111111?text=Kein+Foto'">
                    </div>
                    <div class="w-full md:w-2/3 space-y-2">
                        <div class="flex justify-between items-start">
                            <h3 class="text-xl font-extrabold text-[#111111]">${escapeHtml(item.gegenstand)}</h3>
                            <span class="text-xs font-bold bg-[#d1d95b] px-3 py-1 rounded-full border border-black/10">
                                ${escapeHtml(item.kategorie)}
                            </span>
                        </div>
                        <div class="text-sm space-y-1 text-[#222222]">
                            <p>📍 Fundort: <strong class="font-bold">${escapeHtml(item.fundort)}</strong></p>
                            <p>📅 Datum: <strong class="font-bold">${escapeHtml(item.datum)}</strong></p>
                        </div>
                    </div>
                `;
                container.appendChild(card);
            });
        }

        function escapeHtml(str) {
            if (!str) return '';
            return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
        }

        // Copy Python code helper
        function copyCodeToClipboard() {
            const codeText = document.getElementById('pythonCodeDisplay').innerText;
            const textarea = document.createElement('textarea');
            textarea.value = codeText;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);

            const btnText = document.getElementById('copyBtnText');
            btnText.textContent = 'Kopiert! ✓';
            setTimeout(() => {
                btnText.textContent = 'Code kopieren';
            }, 2000);
        }
    </script>
</body>
</html>
