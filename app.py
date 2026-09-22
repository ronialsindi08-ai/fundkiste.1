import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import pandas as pd
import os
import io
import h5py


# --------------------------------------------------
# Einstellungen
# --------------------------------------------------

st.set_page_config(
    page_title="Fundkiste",
    page_icon="🔎",
    layout="centered"
)

HINTERGRUND = "#ded6bb"
BUTTON = "#d1d95b"

MODEL_DATEI = "keras_model.h5"
LABEL_DATEI = "labels.txt"

DATEN_ORDNER = "data"
CSV_DATEI = os.path.join(DATEN_ORDNER, "fundstuecke.csv")
FOTO_ORDNER = os.path.join(DATEN_ORDNER, "fotos")

SPALTEN = ["Gegenstand", "Kategorie", "Fundort", "Datum", "Foto"]

# FIX: Session-State direkt am Anfang initialisieren
if "seite" not in st.session_state:
    st.session_state.seite = "start"


# --------------------------------------------------
# Design
# --------------------------------------------------

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {HINTERGRUND};
    }}

    .block-container {{
        max-width: 900px;
        padding-top: 2rem;
    }}

    h1, h2, h3, p, label {{
        color: #111111;
    }}

    /* FIX: zusätzlicher Selektor für neuere Streamlit-Versionen */
    div.stButton > button,
    div[data-testid="stButton"] > button {{
        background-color: {BUTTON};
        color: #111111;
        border: none;
        border-radius: 12px;
        font-size: 20px;
        font-weight: bold;
        padding: 14px 20px;
        width: 100%;
    }}

    div.stButton > button:hover,
    div[data-testid="stButton"] > button:hover {{
        background-color: #c5cd50;
        color: #111111;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Ordner erstellen
# --------------------------------------------------

os.makedirs(DATEN_ORDNER, exist_ok=True)
os.makedirs(FOTO_ORDNER, exist_ok=True)


# --------------------------------------------------
# Labels laden
# --------------------------------------------------

def lade_labels():
    labels = []

    with open(LABEL_DATEI, "r", encoding="utf-8") as datei:
        for zeile in datei:
            zeile = zeile.strip()

            if not zeile:
                continue

            teile = zeile.split(maxsplit=1)

            if len(teile) == 2:
                labels.append(teile[1].strip())

    return labels


# FIX: klare Fehlermeldung statt Absturz, wenn labels.txt fehlt
try:
    labels = lade_labels()
except FileNotFoundError:
    st.error("Die Datei 'labels.txt' wurde nicht gefunden.")
    st.stop()


# --------------------------------------------------
# KI laden
# --------------------------------------------------

@st.cache_resource
def lade_ki():

    # MobileNetV2 aufbauen
    basis = tf.keras.applications.MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights=None
    )

    # Gewichte aus dem alten Teachable-Machine-Modell
    with h5py.File(MODEL_DATEI, "r") as datei:

        gewicht_gruppe = datei["model_weights"]["sequential_1"]

        for layer in basis.layers:

            if not layer.weights:
                continue

            if layer.name not in gewicht_gruppe:
                continue

            layer_gruppe = gewicht_gruppe[layer.name]

            neue_gewichte = []

            for variable in layer.weights:

                variablen_name = variable.name.split("/")[-1]
                variablen_name = variablen_name.split(":")[0]

                if variablen_name not in layer_gruppe:
                    raise ValueError(
                        f"Gewicht fehlt: {layer.name} / {variablen_name}"
                    )

                neue_gewichte.append(
                    np.array(layer_gruppe[variablen_name])
                )

            layer.set_weights(neue_gewichte)

        # Klassifikator
        klassifikator_gruppe = datei["model_weights"]["sequential_3"]

        dense1_gewicht = np.array(
            klassifikator_gruppe["dense_Dense1"]["kernel:0"]
        )

        dense1_bias = np.array(
            klassifikator_gruppe["dense_Dense1"]["bias:0"]
        )

        dense2_gewicht = np.array(
            klassifikator_gruppe["dense_Dense2"]["kernel:0"]
        )

    klassifikator = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(1280,)),
        tf.keras.layers.Dense(
            100,
            activation="relu"
        ),
        tf.keras.layers.Dense(
            len(labels),
            activation="softmax",
            use_bias=False
        )
    ])

    klassifikator.layers[0].set_weights([
        dense1_gewicht,
        dense1_bias
    ])

    klassifikator.layers[1].set_weights([
        dense2_gewicht
    ])

    return basis, klassifikator


# --------------------------------------------------
# Bild erkennen
# --------------------------------------------------

def erkenne_bild(bild, basis, klassifikator):

    bild = bild.convert("RGB")
    bild = bild.resize((224, 224))

    bild_array = np.asarray(bild).astype(np.float32)

    # Genau die übliche Teachable-Machine-Normalisierung
    bild_array = (bild_array / 127.5) - 1.0

    bild_array = np.expand_dims(bild_array, axis=0)

    # MobileNetV2
    merkmale = basis(bild_array, training=False)

    # Global Average Pooling
    merkmale = tf.reduce_mean(
        merkmale,
        axis=[1, 2]
    )

    # Klassifikation
    vorhersage = klassifikator(
        merkmale,
        training=False
    )

    vorhersage = vorhersage.numpy()[0]

    index = int(np.argmax(vorhersage))
    sicherheit = float(vorhersage[index])

    return labels[index], sicherheit


# FIX: Ergebnis cachen – vorher hat die KI bei JEDEM
# Tastendruck (z. B. im Fundort-Feld) alles neu gerechnet
@st.cache_data(show_spinner=False)
def erkenne_bild_bytes(bild_bytes):

    bild = Image.open(io.BytesIO(bild_bytes))

    basis, klassifikator = lade_ki()

    return erkenne_bild(bild, basis, klassifikator)


# --------------------------------------------------
# Daten laden
# --------------------------------------------------

def leere_daten():
    return pd.DataFrame(columns=SPALTEN)


def lade_daten():

    if not os.path.exists(CSV_DATEI):
        return leere_daten()

    # FIX: gezielte Fehler statt blankem except
    try:
        daten = pd.read_csv(CSV_DATEI, encoding="utf-8")
    except (pd.errors.EmptyDataError, pd.errors.ParserError, UnicodeDecodeError):
        return leere_daten()

    # FIX: fehlende Spalten ergänzen, leere Zellen aufräumen
    for spalte in SPALTEN:
        if spalte not in daten.columns:
            daten[spalte] = ""

    daten = daten.fillna("")

    return daten


def speichere_daten(daten):
    daten.to_csv(
        CSV_DATEI,
        index=False,
        encoding="utf-8"
    )


# --------------------------------------------------
# Startseite
# --------------------------------------------------

def startseite():

    st.title("Fundkiste")

    st.markdown(
        """
        <div style="text-align:center; margin-top:-10px;">
            <div style="font-size:45px;">●</div>
            <h3>KATHARINEUM ZU LÜBECK</h3>
            <p>seit 1531</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔎 Suchen"):
            st.session_state.seite = "suchen"
            st.rerun()

    with col2:
        if st.button("📷 Fundstück hinzufügen"):
            st.session_state.seite = "eingeben"
            st.rerun()


# --------------------------------------------------
# Fundstück hinzufügen
# --------------------------------------------------

def fundstueck_hinzufuegen():

    st.header("Fundstück hinzufügen")

    if st.button("← Zurück"):
        st.session_state.seite = "start"
        st.rerun()

    st.write("")

    bild = st.file_uploader(
        "Foto des Fundstücks hochladen",
        type=["jpg", "jpeg", "png"]
    )

    fundort = st.text_input(
        "Wo wurde es gefunden?"
    )

    if bild is None:
        return

    bild_bytes = bild.getvalue()

    # FIX: defekte/unlesbare Datei abfangen
    # (stand vorher außerhalb von try und hat die App crashen lassen)
    try:
        foto = Image.open(io.BytesIO(bild_bytes))
    except Exception:
        st.error("Diese Datei konnte nicht als Bild gelesen werden.")
        return

    # FIX: use_container_width → width
    st.image(
        foto,
        caption="Hochgeladenes Foto",
        width="stretch"
    )

    try:

        with st.spinner("Die KI erkennt das Fundstück ..."):
            kategorie, sicherheit = erkenne_bild_bytes(bild_bytes)

        st.success(
            f"Erkannt: **{kategorie}**"
        )

        st.write(
            f"KI-Sicherheit: **{sicherheit * 100:.1f}%**"
        )

        if not fundort.strip():
            st.info(
                "Bitte noch den Fundort eingeben."
            )
            return

        if st.button("Fundstück speichern"):

            daten = lade_daten()

            # FIX: eindeutiger Dateiname per Zeitstempel.
            # Vorher konnte ein Foto überschrieben werden,
            # wenn Zeilen aus der CSV gelöscht wurden.
            endung = os.path.splitext(bild.name)[1].lower()
            if endung not in (".jpg", ".jpeg", ".png"):
                endung = ".jpg"

            zeitstempel = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S_%f")
            dateiname = zeitstempel + "_fundstueck" + endung

            foto_pfad = os.path.join(
                FOTO_ORDNER,
                dateiname
            )

            # FIX: JPEG kann keine Transparenz speichern
            speicher_foto = foto
            if endung in (".jpg", ".jpeg") and foto.mode != "RGB":
                speicher_foto = foto.convert("RGB")

            speicher_foto.save(foto_pfad)

            neuer_eintrag = pd.DataFrame([{
                "Gegenstand": kategorie,
                "Kategorie": kategorie,
                "Fundort": fundort.strip(),
                "Datum": pd.Timestamp.now().strftime("%d.%m.%Y"),
                "Foto": foto_pfad
            }])

            daten = pd.concat(
                [daten, neuer_eintrag],
                ignore_index=True
            )

            speichere_daten(daten)

            st.success(
                "Das Fundstück wurde gespeichert."
            )

            st.session_state.seite = "start"

            st.rerun()

    except Exception as fehler:

        st.error(
            "Die KI konnte das Bild nicht verarbeiten."
        )

        st.code(str(fehler))


# --------------------------------------------------
# Suche
# --------------------------------------------------

def suchen():

    st.header("Fundstücke suchen")

    if st.button("← Zurück"):
        st.session_state.seite = "start"
        st.rerun()

    st.write("")

    daten = lade_daten()

    if len(daten) == 0:
        st.info(
            "Es wurden noch keine Fundstücke eingetragen."
        )
        return

    suche = st.text_input(
        "Was suchst du?"
    )

    # FIX: Kategorien dynamisch aus den Daten statt fest im Code
    kategorien = ["Alle"] + sorted(
        wert
        for wert in daten["Kategorie"].astype(str).str.strip().unique()
        if wert
    )

    kategorie = st.selectbox(
        "Kategorie",
        kategorien
    )

    fundort = st.text_input(
        "Fundort"
    )

    ergebnis = daten.copy()

    if suche:
        ergebnis = ergebnis[
            ergebnis["Gegenstand"]
            .astype(str)
            .str.contains(
                suche,
                case=False,
                na=False,
                regex=False
            )
        ]

    if kategorie != "Alle":
        ergebnis = ergebnis[
            ergebnis["Kategorie"]
            .astype(str)
            .str.strip()
            .str.lower()
            == kategorie.strip().lower()
        ]

    if fundort:
        ergebnis = ergebnis[
            ergebnis["Fundort"]
            .astype(str)
            .str.contains(
                fundort,
                case=False,
                na=False,
                regex=False
            )
        ]

    st.write("")

    if len(ergebnis) == 0:

        st.warning(
            "Kein passendes Fundstück gefunden."
        )

    else:

        st.write(
            f"**{len(ergebnis)} Fundstück(e) gefunden:**"
        )

        for _, eintrag in ergebnis.iterrows():

            st.markdown("---")

            col1, col2 = st.columns([1, 2])

            with col1:

                foto_pfad = str(
                    eintrag.get("Foto", "")
                ).strip()

                if (
                    foto_pfad
                    and os.path.exists(foto_pfad)
                ):
                    # FIX: use_container_width → width
                    st.image(
                        foto_pfad,
                        width="stretch"
                    )

            with col2:

                st.subheader(
                    str(eintrag["Gegenstand"])
                )

                st.write(
                    f"**Kategorie:** {eintrag['Kategorie']}"
                )

                st.write(
                    f"**Fundort:** {eintrag['Fundort']}"
                )

                st.write(
                    f"**Datum:** {eintrag['Datum']}"
                )


# --------------------------------------------------
# Navigation
# --------------------------------------------------

if st.session_state.seite == "start":
    startseite()

elif st.session_state.seite == "eingeben":
    fundstueck_hinzufuegen()

elif st.session_state.seite == "suchen":
    suchen()
