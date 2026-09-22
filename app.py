import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import pandas as pd
import os
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

    div.stButton > button {{
        background-color: {BUTTON};
        color: #111111;
        border: none;
        border-radius: 12px;
        font-size: 20px;
        font-weight: bold;
        padding: 14px 20px;
        width: 100%;
    }}

    div.stButton > button:hover {{
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


labels = lade_labels()


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


# --------------------------------------------------
# Daten laden
# --------------------------------------------------

def lade_daten():

    if not os.path.exists(CSV_DATEI):
        return pd.DataFrame(
            columns=[
                "Gegenstand",
                "Kategorie",
                "Fundort",
                "Datum",
                "Foto"
            ]
        )

    try:
        return pd.read_csv(CSV_DATEI)
    except:
        return pd.DataFrame(
            columns=[
                "Gegenstand",
                "Kategorie",
                "Fundort",
                "Datum",
                "Foto"
            ]
        )


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

    if bild is not None:

        foto = Image.open(bild)

        st.image(
            foto,
            caption="Hochgeladenes Foto",
            use_container_width=True
        )

        try:

            basis, klassifikator = lade_ki()

            with st.spinner("Die KI erkennt das Fundstück ..."):

                kategorie, sicherheit = erkenne_bild(
                    foto,
                    basis,
                    klassifikator
                )

            st.success(
                f"Erkannt: **{kategorie}**"
            )

            st.write(
                f"KI-Sicherheit: **{sicherheit * 100:.1f}%**"
            )

            if fundort:

                if st.button("Fundstück speichern"):

                    daten = lade_daten()

                    dateiname = (
                        str(len(daten) + 1)
                        + "_fundstueck."
                        + bild.name.split(".")[-1]
                    )

                    foto_pfad = os.path.join(
                        FOTO_ORDNER,
                        dateiname
                    )

                    foto.save(foto_pfad)

                    neuer_eintrag = pd.DataFrame([{
                        "Gegenstand": kategorie,
                        "Kategorie": kategorie,
                        "Fundort": fundort,
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

            else:
                st.info(
                    "Bitte noch den Fundort eingeben."
                )

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

    kategorie = st.selectbox(
        "Kategorie",
        [
            "Alle",
            "helm",
            "flasche",
            "mütze",
            "turnbeutel",
            "sonstiges"
        ]
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
                na=False
            )
        ]

    if kategorie != "Alle":
        ergebnis = ergebnis[
            ergebnis["Kategorie"]
            .astype(str)
            .str.lower()
            == kategorie.lower()
        ]

    if fundort:
        ergebnis = ergebnis[
            ergebnis["Fundort"]
            .astype(str)
            .str.contains(
                fundort,
                case=False,
                na=False
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
                )

                if (
                    foto_pfad
                    and os.path.exists(foto_pfad)
                ):
                    st.image(
                        foto_pfad,
                        use_container_width=True
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

if "seite" not in st.session_state:
    st.session_state.seite = "start"


if st.session_state.seite == "start":
    startseite()

elif st.session_state.seite == "eingeben":
    fundstueck_hinzufuegen()

elif st.session_state.seite == "suchen":
    suchen()
