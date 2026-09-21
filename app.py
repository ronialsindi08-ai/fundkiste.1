import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image, ImageOps
import tensorflow as tf
import os


# -----------------------------
# Einstellungen
# -----------------------------

st.set_page_config(
    page_title="Fundkiste",
    page_icon="🔎",
    layout="centered"
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #ded6bb;
    }

    h1, h2, h3, p, label {
        color: black !important;
    }

    .stButton > button {
        background-color: #d1d95b;
        color: black;
        border: none;
        border-radius: 12px;
        width: 100%;
        padding: 14px;
        font-size: 18px;
    }

    .stButton > button:hover {
        background-color: #c3cc4c;
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Dateien
# -----------------------------

MODEL_DATEI = "keras_model.h5"
LABEL_DATEI = "labels.txt"

DATA_ORDNER = "data"
FOTO_ORDNER = os.path.join(DATA_ORDNER, "fotos")
CSV_DATEI = os.path.join(DATA_ORDNER, "fundstuecke.csv")

os.makedirs(FOTO_ORDNER, exist_ok=True)


# -----------------------------
# Labels laden
# -----------------------------

def lade_labels():
    labels = []

    with open(LABEL_DATEI, "r", encoding="utf-8") as datei:
        for zeile in datei:
            zeile = zeile.strip()

            if not zeile:
                continue

            teile = zeile.split(" ", 1)

            if len(teile) == 2:
                labels.append(teile[1].strip())
            else:
                labels.append(zeile)

    return labels


labels = lade_labels()


# -----------------------------
# Kompatibilität für altes
# Teachable-Machine-Modell
# -----------------------------

class MeineDepthwiseConv2D(tf.keras.layers.DepthwiseConv2D):

    @classmethod
    def from_config(cls, config):
        config = config.copy()

        # Alte Teachable-Machine-Modelle
        # enthalten manchmal groups=1.
        config.pop("groups", None)

        return super().from_config(config)


class MeineFunctional(tf.keras.Model):

    def call(self, inputs, training=None, mask=None):

        # Alte Keras-Modelle können beim Aufruf
        # zusätzlich einen mask-Parameter bekommen.
        # Für unser Bildmodell wird dieser nicht benötigt.

        return super().call(
            inputs,
            training=training
        )


# -----------------------------
# Modell laden
# -----------------------------

@st.cache_resource
def lade_modell():

    if not os.path.exists(MODEL_DATEI):
        return None, "Die Datei keras_model.h5 wurde nicht gefunden."

    try:

        modell = tf.keras.models.load_model(
            MODEL_DATEI,
            compile=False,
            custom_objects={
                "DepthwiseConv2D": MeineDepthwiseConv2D,
                "Functional": MeineFunctional
            }
        )

        return modell, None

    except Exception as e:

        return None, str(e)


modell, modell_fehler = lade_modell()


# -----------------------------
# KI-Erkennung
# -----------------------------

def erkenne_bild(bild):

    if modell is None:
        return None, 0, modell_fehler

    try:

        bild = bild.convert("RGB")

        bild = ImageOps.fit(
            bild,
            (224, 224),
            Image.Resampling.LANCZOS
        )

        bild_array = np.asarray(
            bild
        ).astype(np.float32)

        # Teachable Machine Normalisierung
        bild_array = (
            bild_array / 127.5
        ) - 1

        bild_array = np.expand_dims(
            bild_array,
            axis=0
        )

        # Modell direkt aufrufen
        # statt model.predict()
        vorhersage = modell(
            bild_array,
            training=False
        )

        vorhersage = np.asarray(
            vorhersage
        ).reshape(-1)

        if len(vorhersage) != len(labels):

            return (
                None,
                0,
                "Das Modell liefert "
                + str(len(vorhersage))
                + " Ergebnisse, aber labels.txt enthält "
                + str(len(labels))
                + " Labels."
            )

        index = int(
            np.argmax(vorhersage)
        )

        erkannte_label = labels[index]

        sicherheit = (
            float(vorhersage[index]) * 100
        )

        return (
            erkannte_label,
            sicherheit,
            None
        )

    except Exception as e:

        return (
            None,
            0,
            str(e)
        )


# -----------------------------
# Kategorie bestimmen
# -----------------------------

def bestimme_kategorie(label):

    label = label.lower().strip()

    if "helm" in label:
        return "Helm"

    if "flasche" in label:
        return "Flasche"

    if "mütze" in label or "muetze" in label:
        return "Mütze"

    if "turnbeutel" in label:
        return "Turnbeutel"

    return "Sonstiges"


# -----------------------------
# Daten laden
# -----------------------------

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

    return pd.read_csv(
        CSV_DATEI
    )


# -----------------------------
# Daten speichern
# -----------------------------

def speichere_daten(daten):

    os.makedirs(
        DATA_ORDNER,
        exist_ok=True
    )

    daten.to_csv(
        CSV_DATEI,
        index=False,
        encoding="utf-8"
    )


# -----------------------------
# Startseite
# -----------------------------

def startseite():

    st.title("Fundkiste")

    st.markdown(
        """
        <div style="text-align:center; margin-top:-10px;">
            <div style="font-size:45px;">⬛</div>
            <h3>KATHARINEUM ZU LÜBECK</h3>
            <p>seit 1531</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    if st.button("🔎 Suchen"):

        st.session_state["seite"] = "suchen"
        st.rerun()

    st.write("")

    if st.button("📦 Fundstück hinzufügen"):

        st.session_state["seite"] = "hinzufügen"
        st.rerun()


# -----------------------------
# Fundstück hinzufügen
# -----------------------------

def fundstueck_hinzufuegen():

    st.title("Fundstück hinzufügen")

    if st.button("← Zurück"):

        st.session_state["seite"] = "start"
        st.rerun()

    st.write("")

    st.write(
        "Lade ein Foto des Fundstücks hoch."
    )

    foto = st.file_uploader(
        "Foto auswählen",
        type=[
            "jpg",
            "jpeg",
            "png"
        ]
    )

    if foto is not None:

        bild = Image.open(foto)

        st.image(
            bild,
            caption="Hochgeladenes Foto",
            use_container_width=True
        )

        if st.button("🤖 KI erkennen lassen"):

            with st.spinner(
                "Die KI analysiert das Foto..."
            ):

                label, sicherheit, fehler = erkenne_bild(
                    bild
                )

            if fehler:

                st.error(
                    "Die KI konnte das Foto nicht analysieren."
                )

                st.code(
                    fehler
                )

            else:

                kategorie = bestimme_kategorie(
                    label
                )

                st.success(
                    "Erkannt: "
                    + kategorie
                )

                st.write(
                    "KI-Erkennung: "
                    + label
                )

                st.write(
                    "Sicherheit: "
                    + f"{sicherheit:.1f}%"
                )

                st.session_state["erkannt"] = True
                st.session_state["label"] = label
                st.session_state["kategorie"] = kategorie
                st.session_state["bild"] = bild

    if st.session_state.get(
        "erkannt",
        False
    ):

        st.write("")

        fundort = st.text_input(
            "Wo wurde der Gegenstand gefunden?"
        )

        if st.button(
            "Fundstück speichern"
        ):

            if not fundort:

                st.warning(
                    "Bitte gib noch den Fundort ein."
                )

            else:

                daten = lade_daten()

                neue_nummer = (
                    len(daten) + 1
                )

                dateiname = (
                    "fundstueck_"
                    + str(neue_nummer)
                    + ".jpg"
                )

                fotopfad = os.path.join(
                    FOTO_ORDNER,
                    dateiname
                )

                st.session_state["bild"].save(
                    fotopfad
                )

                neuer_eintrag = pd.DataFrame(
                    [{
                        "Gegenstand":
                            st.session_state["label"],

                        "Kategorie":
                            st.session_state["kategorie"],

                        "Fundort":
                            fundort,

                        "Datum":
                            pd.Timestamp.now().strftime(
                                "%d.%m.%Y"
                            ),

                        "Foto":
                            fotopfad
                    }]
                )

                daten = pd.concat(
                    [
                        daten,
                        neuer_eintrag
                    ],
                    ignore_index=True
                )

                speichere_daten(
                    daten
                )

                st.success(
                    "Das Fundstück wurde gespeichert!"
                )

                st.session_state["erkannt"] = False


# -----------------------------
# Suche
# -----------------------------

def suchen():

    st.title(
        "Fundstücke suchen"
    )

    if st.button("← Zurück"):

        st.session_state["seite"] = "start"
        st.rerun()

    daten = lade_daten()

    if daten.empty:

        st.info(
            "Es wurden noch keine Fundstücke eingetragen."
        )

        return

    suchtext = st.text_input(
        "Wonach suchst du?"
    )

    kategorie = st.selectbox(
        "Kategorie",
        [
            "Alle",
            "Helm",
            "Flasche",
            "Mütze",
            "Turnbeutel",
            "Sonstiges"
        ]
    )

    ergebnis = daten.copy()

    if suchtext:

        text = suchtext.lower()

        ergebnis = ergebnis[
            ergebnis["Gegenstand"]
            .astype(str)
            .str.lower()
            .str.contains(
                text,
                na=False
            )
            |
            ergebnis["Fundort"]
            .astype(str)
            .str.lower()
            .str.contains(
                text,
                na=False
            )
        ]

    if kategorie != "Alle":

        ergebnis = ergebnis[
            ergebnis["Kategorie"]
            == kategorie
        ]

    if ergebnis.empty:

        st.warning(
            "Kein passendes Fundstück gefunden."
        )

    else:

        for _, eintrag in ergebnis.iterrows():

            st.markdown("---")

            st.subheader(
                str(
                    eintrag["Kategorie"]
                )
            )

            st.write(
                "Fundort:",
                str(
                    eintrag["Fundort"]
                )
            )

            st.write(
                "Datum:",
                str(
                    eintrag["Datum"]
                )
            )

            if (
                "Foto" in eintrag
                and os.path.exists(
                    str(eintrag["Foto"])
                )
            ):

                st.image(
                    str(eintrag["Foto"]),
                    width=300
                )


# -----------------------------
# Navigation
# -----------------------------

if "seite" not in st.session_state:

    st.session_state["seite"] = "start"


if st.session_state["seite"] == "start":

    startseite()


elif st.session_state["seite"] == "hinzufügen":

    fundstueck_hinzufuegen()


elif st.session_state["seite"] == "suchen":

    suchen()
