import os
import uuid
from datetime import date

import numpy as np
import pandas as pd
import streamlit as st
import tensorflow as tf

from PIL import Image, ImageOps


# ---------------------------------------------------------
# EINSTELLUNGEN
# ---------------------------------------------------------

APP_NAME = "Fundkiste"
SCHOOL_NAME = "KATHARINEUM ZU LÜBECK"
SCHOOL_YEAR = "seit 1531"

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "fundstuecke.csv")
PHOTO_DIR = os.path.join(DATA_DIR, "fotos")

MODEL_FILE = "keras_model.h5"
LABEL_FILE = "labels.txt"

CATEGORIES = [
    "Helm",
    "Flasche",
    "Mütze",
    "Turnbeutel",
    "Sonstiges",
]

COLUMNS = [
    "Gegenstand",
    "Kategorie",
    "Farbe",
    "Fundort",
    "Datum",
    "Beschreibung",
    "Foto",
]


# ---------------------------------------------------------
# STREAMLIT
# ---------------------------------------------------------

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🧥",
    layout="centered",
)


# ---------------------------------------------------------
# ORDNER
# ---------------------------------------------------------

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PHOTO_DIR, exist_ok=True)


# ---------------------------------------------------------
# DESIGN
# ---------------------------------------------------------

st.markdown(
    """
    <style>
    .stApp {
        background-color: #ded6bb;
        color: #000000;
    }

    .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, p, label {
        color: #000000 !important;
    }

    .home-title {
        text-align: center;
        font-size: clamp(4rem, 11vw, 8rem);
        line-height: 1;
        font-weight: 400;
        color: #000000;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
    }

    .school-name {
        text-align: center;
        font-size: clamp(1.2rem, 3vw, 2rem);
        font-weight: 400;
        color: #000000;
    }

    .school-year {
        text-align: center;
        font-size: 1.1rem;
        color: #000000;
        margin-bottom: 2.5rem;
    }

    .stButton > button {
        width: 100%;
        min-height: 80px;
        border: none;
        border-radius: 22px;
        background-color: #d1d95b;
        color: #000000;
        font-size: 2rem;
        font-weight: 400;
        margin: 0.6rem 0;
    }

    .stButton > button:hover {
        background-color: #c7cf50;
        color: #000000;
    }

    .item-card {
        background-color: rgba(255, 255, 255, 0.40);
        border: 1px solid rgba(0, 0, 0, 0.12);
        border-radius: 18px;
        padding: 1.3rem;
        margin-bottom: 1rem;
    }

    .item-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #000000;
        margin-bottom: 0.7rem;
    }

    .item-info {
        color: #000000;
        line-height: 1.8;
    }

    .success-box {
        background-color: #d1d95b;
        padding: 1rem;
        border-radius: 14px;
        text-align: center;
        color: #000000;
        font-weight: 600;
        margin-top: 1rem;
    }

    input, textarea {
        border-radius: 12px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# KI LADEN
# ---------------------------------------------------------

@st.cache_resource
def load_model():

    if not os.path.exists(MODEL_FILE):
        return None, "keras_model.h5 wurde nicht gefunden."

    try:
        model = tf.keras.models.load_model(
            MODEL_FILE,
            compile=False
        )

        return model, None

    except Exception as e:
        return None, str(e)


@st.cache_data
def load_labels():

    if not os.path.exists(LABEL_FILE):
        return [], "labels.txt wurde nicht gefunden."

    try:

        with open(
            LABEL_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            labels = [
                line.strip()
                for line in file
                if line.strip()
            ]

        cleaned_labels = []

        for label in labels:

            parts = label.split(" ", 1)

            if (
                len(parts) == 2
                and parts[0].isdigit()
            ):
                label = parts[1]

            cleaned_labels.append(label)

        return cleaned_labels, None

    except Exception as e:
        return [], str(e)


model, model_error = load_model()
labels, labels_error = load_labels()


# ---------------------------------------------------------
# KI-ERKENNUNG
# ---------------------------------------------------------

def predict_image(image):

    if model is None:
        return None, 0.0, model_error

    if not labels:
        return None, 0.0, labels_error

    try:

        # -------------------------------------------------
        # TEACHABLE MACHINE:
        # 224 x 224 Pixel
        # -------------------------------------------------

        image = image.convert("RGB")

        # Bild proportional zuschneiden
        image = ImageOps.fit(
            image,
            (224, 224),
            Image.Resampling.LANCZOS
        )

        # Bild in numpy umwandeln
        image_array = np.asarray(
            image,
            dtype=np.float32
        )

        # -------------------------------------------------
        # TEACHABLE MACHINE NORMALISIERUNG
        #
        # Werte:
        # 0...255
        #
        # werden zu:
        # -1...1
        # -------------------------------------------------

        image_array = (
            image_array / 127.5
        ) - 1.0

        # Batch-Dimension hinzufügen
        image_array = np.expand_dims(
            image_array,
            axis=0
        )

        # -------------------------------------------------
        # KI
        # -------------------------------------------------

        prediction = model.predict(
            image_array,
            verbose=0
        )

        prediction = np.asarray(
            prediction
        ).reshape(-1)

        # -------------------------------------------------
        # PRÜFEN
        # -------------------------------------------------

        if len(prediction) != len(labels):

            return (
                None,
                0.0,
                (
                    "Das Modell liefert "
                    f"{len(prediction)} Klassen, "
                    f"aber labels.txt enthält "
                    f"{len(labels)} Klassen."
                )
            )

        # -------------------------------------------------
        # BESTE KLASSE
        # -------------------------------------------------

        index = int(
            np.argmax(prediction)
        )

        confidence = float(
            prediction[index]
        )

        label = labels[index]

        return (
            label,
            confidence,
            None
        )

    except Exception as e:

        return (
            None,
            0.0,
            str(e)
        )


# ---------------------------------------------------------
# KATEGORIE
# ---------------------------------------------------------

def get_category(label):

    text = label.lower()

    if "helm" in text:
        return "Helm"

    if "flasche" in text:
        return "Flasche"

    if "mütze" in text or "muetze" in text:
        return "Mütze"

    if "turnbeutel" in text:
        return "Turnbeutel"

    return "Sonstiges"


# ---------------------------------------------------------
# DATEN LADEN
# ---------------------------------------------------------

def load_data():

    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(
            columns=COLUMNS
        )

    try:

        data = pd.read_csv(
            DATA_FILE,
            dtype=str,
            encoding="utf-8-sig",
        ).fillna("")

    except pd.errors.EmptyDataError:

        return pd.DataFrame(
            columns=COLUMNS
        )

    except (
        OSError,
        pd.errors.ParserError
    ):

        st.error(
            "Die gespeicherten Fundstücke konnten nicht gelesen werden."
        )

        return pd.DataFrame(
            columns=COLUMNS
        )

    for column in COLUMNS:

        if column not in data.columns:
            data[column] = ""

    return data[COLUMNS]


# ---------------------------------------------------------
# DATEN SPEICHERN
# ---------------------------------------------------------

def save_data(data):

    try:

        data.to_csv(
            DATA_FILE,
            index=False,
            encoding="utf-8-sig",
        )

        return True

    except OSError:

        st.error(
            "Die Fundstücke konnten nicht gespeichert werden."
        )

        return False


# ---------------------------------------------------------
# SUCHEN
# ---------------------------------------------------------

def search_items(
    data,
    item,
    category,
    color,
    location,
):

    result = data.copy()

    if item.strip():

        result = result[
            result["Gegenstand"].str.contains(
                item.strip(),
                case=False,
                na=False,
                regex=False,
            )
        ]

    if category != "Alle":

        result = result[
            result["Kategorie"] == category
        ]

    if color.strip():

        result = result[
            result["Farbe"].str.contains(
                color.strip(),
                case=False,
                na=False,
                regex=False,
            )
        ]

    if location.strip():

        result = result[
            result["Fundort"].str.contains(
                location.strip(),
                case=False,
                na=False,
                regex=False,
            )
        ]

    return result


# ---------------------------------------------------------
# HTML SICHER MACHEN
# ---------------------------------------------------------

def safe_text(value):

    if pd.isna(value):
        return ""

    text = str(value)

    replacements = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;",
    }

    for old, new in replacements.items():

        text = text.replace(
            old,
            new
        )

    return text


# ---------------------------------------------------------
# STARTSEITE
# ---------------------------------------------------------

def show_home():

    st.markdown(
        '<div class="home-title">Fundkiste</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="school-name">{SCHOOL_NAME}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="school-year">{SCHOOL_YEAR}</div>',
        unsafe_allow_html=True,
    )

    left, center, right = st.columns(
        [1, 2, 1]
    )

    with center:

        if st.button(
            "Suchen",
            key="home_search",
        ):

            st.session_state.page = "search"

            st.session_state.pop(
                "search_results",
                None
            )

            st.rerun()

        if st.button(
            "Fundstück hinzufügen",
            key="home_add",
        ):

            st.session_state.page = "add"

            st.rerun()


# ---------------------------------------------------------
# SUCHSEITE
# ---------------------------------------------------------

def show_search(data):

    st.title(
        "Fundstück suchen"
    )

    if st.button(
        "← Zurück",
        key="back_search",
    ):

        st.session_state.page = "home"

        st.session_state.pop(
            "search_results",
            None
        )

        st.rerun()

    st.write(
        "Suche nach einem verlorenen Gegenstand."
    )

    item = st.text_input(
        "Gegenstand",
        placeholder="z. B. Helm",
    )

    category = st.selectbox(
        "Kategorie",
        ["Alle"] + CATEGORIES,
    )

    color = st.text_input(
        "Farbe",
        placeholder="z. B. Schwarz",
    )

    location = st.text_input(
        "Fundort",
        placeholder="z. B. Sporthalle",
    )

    if st.button(
        "Suchen",
        key="perform_search",
    ):

        st.session_state.search_results = (
            search_items(
                data,
                item,
                category,
                color,
                location,
            )
        )

    if "search_results" not in st.session_state:
        return

    results = st.session_state.search_results

    if results.empty:

        if data.empty:

            st.info(
                "Es wurden noch keine Fundstücke eingetragen."
            )

        else:

            st.info(
                "Leider wurde kein passendes Fundstück gefunden."
            )

        return

    st.subheader(
        f"{len(results)} Fundstück(e) gefunden"
    )

    for _, row in results.iterrows():

        item_name = safe_text(
            row["Gegenstand"]
        )

        item_category = safe_text(
            row["Kategorie"]
        )

        item_color = safe_text(
            row["Farbe"]
        )

        item_location = safe_text(
            row["Fundort"]
        )

        item_date = safe_text(
            row["Datum"]
        )

        item_description = safe_text(
            row["Beschreibung"]
        )

        if not item_description:

            item_description = (
                "Keine Beschreibung vorhanden."
            )

        st.markdown(
            f"""
            <div class="item-card">

                <div class="item-title">
                    {item_name}
                </div>

                <div class="item-info">

                    <b>Kategorie:</b>
                    {item_category}<br>

                    <b>Fundort:</b>
                    {item_location}<br>

                    <b>Gefunden am:</b>
                    {item_date}<br>

                    <b>Beschreibung:</b>
                    {item_description}

                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        photo_path = row["Foto"]

        if (
            photo_path
            and os.path.exists(photo_path)
        ):

            st.image(
                photo_path,
                caption="Foto des Fundstücks",
            )


# ---------------------------------------------------------
# FUNDSTÜCK HINZUFÜGEN
# ---------------------------------------------------------

def show_add_item(data):

    st.title(
        "Fundstück hinzufügen"
    )

    if st.button(
        "← Zurück",
        key="back_add",
    ):

        st.session_state.page = "home"

        st.rerun()

    st.write(
        "Lade einfach ein Foto hoch. "
        "Die KI erkennt den Gegenstand automatisch."
    )

    photo = st.file_uploader(
        "Foto hochladen",
        type=[
            "jpg",
            "jpeg",
            "png"
        ],
    )

    if photo is None:

        st.info(
            "Lade ein Foto hoch."
        )

        return

    image = Image.open(photo)

    st.image(
        image,
        caption="Hochgeladenes Foto",
        use_container_width=True,
    )

    if st.button(
        "KI erkennen lassen",
        key="recognize_photo",
    ):

        with st.spinner(
            "Die KI analysiert das Foto..."
        ):

            label, confidence, error = (
                predict_image(image)
            )

        if error is not None:

            st.error(
                "Die KI konnte das Foto nicht analysieren."
            )

            st.code(error)

            return

        st.session_state.predicted_label = label
        st.session_state.predicted_confidence = confidence
        st.session_state.predicted_category = (
            get_category(label)
        )

    if "predicted_label" not in st.session_state:
        return

    label = st.session_state.predicted_label

    confidence = (
        st.session_state.predicted_confidence
    )

    category = (
        st.session_state.predicted_category
    )

    st.success(
        f"Erkannt: {label}"
    )

    st.write(
        f"**Kategorie:** {category}"
    )

    st.write(
        f"**Sicherheit:** {confidence * 100:.1f} %"
    )

    location = st.text_input(
        "Fundort",
        placeholder="z. B. Sporthalle oder Schulhof",
    )

    if st.button(
        "Fundstück speichern",
        key="save_ai_item",
    ):

        if not location.strip():

            location = "Nicht angegeben"

        extension = os.path.splitext(
            photo.name
        )[1].lower()

        filename = (
            uuid.uuid4().hex
            + extension
        )

        photo_path = os.path.join(
            PHOTO_DIR,
            filename,
        )

        try:

            with open(
                photo_path,
                "wb"
            ) as file:

                file.write(
                    photo.getbuffer()
                )

        except OSError:

            st.error(
                "Das Foto konnte nicht gespeichert werden."
            )

            return

        new_item = pd.DataFrame(
            [
                {
                    "Gegenstand": label,
                    "Kategorie": category,
                    "Farbe": "",
                    "Fundort": location.strip(),
                    "Datum": date.today().strftime(
                        "%d.%m.%Y"
                    ),
                    "Beschreibung": (
                        "Automatisch durch die KI erkannt."
                    ),
                    "Foto": photo_path,
                }
            ]
        )

        updated_data = pd.concat(
            [
                data,
                new_item,
            ],
            ignore_index=True,
        )

        if save_data(updated_data):

            st.markdown(
                """
                <div class="success-box">
                    ✓ Fundstück erfolgreich gespeichert!
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.info(
                "Das Fundstück ist jetzt bei der Suche verfügbar."
            )

            st.session_state.pop(
                "predicted_label",
                None
            )

            st.session_state.pop(
                "predicted_confidence",
                None
            )

            st.session_state.pop(
                "predicted_category",
                None
            )


# ---------------------------------------------------------
# APP START
# ---------------------------------------------------------

if "page" not in st.session_state:

    st.session_state.page = "home"


data = load_data()


if st.session_state.page == "home":

    show_home()

elif st.session_state.page == "search":

    show_search(data)

elif st.session_state.page == "add":

    show_add_item(data)

else:

    st.session_state.page = "home"

    st.rerun()
