
import os
import uuid
from datetime import date

import pandas as pd
import streamlit as st


APP_NAME = "Fundkiste"
SCHOOL_NAME = "KATHARINEUM ZU LÜBECK"
SCHOOL_YEAR = "seit 1531"

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "fundstuecke.csv")
PHOTO_DIR = os.path.join(DATA_DIR, "fotos")

CATEGORIES = [
    "Kleidung",
    "Schlüssel",
    "Trinkflasche",
    "Tasche",
    "Handy",
    "Schmuck",
    "Schulmaterial",
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
# DATEN LADEN
# ---------------------------------------------------------

def load_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=COLUMNS)

    try:
        data = pd.read_csv(
            DATA_FILE,
            dtype=str,
            encoding="utf-8-sig",
        ).fillna("")

    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=COLUMNS)

    except (OSError, pd.errors.ParserError):
        st.error(
            "Die gespeicherten Fundstücke konnten nicht "
            "gelesen werden."
        )
        return pd.DataFrame(columns=COLUMNS)

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
        text = text.replace(old, new)

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

    left, center, right = st.columns([1, 2, 1])

    with center:

        if st.button(
            "Suchen",
            key="home_search",
        ):
            st.session_state.page = "search"
            st.session_state.pop(
                "search_results",
                None,
            )
            st.rerun()

        if st.button(
            "Eingeben",
            key="home_add",
        ):
            st.session_state.page = "add"
            st.rerun()


# ---------------------------------------------------------
# SUCHSEITE
# ---------------------------------------------------------

def show_search(data):

    st.title("Fundstück suchen")

    if st.button(
        "← Zurück",
        key="back_search",
    ):
        st.session_state.page = "home"
        st.session_state.pop(
            "search_results",
            None,
        )
        st.rerun()

    st.write(
        "Suche nach einem verlorenen Gegenstand."
    )

    item = st.text_input(
        "Gegenstand",
        placeholder="z. B. Jacke",
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
        st.session_state.search_results = search_items(
            data,
            item,
            category,
            color,
            location,
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

        item_name = safe_text(row["Gegenstand"])
        item_category = safe_text(row["Kategorie"])
        item_color = safe_text(row["Farbe"])
        item_location = safe_text(row["Fundort"])
        item_date = safe_text(row["Datum"])
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
                    <b>Kategorie:</b> {item_category}<br>
                    <b>Farbe:</b> {item_color}<br>
                    <b>Fundort:</b> {item_location}<br>
                    <b>Gefunden am:</b> {item_date}<br>
                    <b>Beschreibung:</b> {item_description}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        photo_path = row["Foto"]

        if photo_path and os.path.exists(photo_path):
            st.image(
                photo_path,
                caption="Foto des Fundstücks",
            )


# ---------------------------------------------------------
# FUNDSTÜCK EINGEBEN
# ---------------------------------------------------------

def show_add_item(data):

    st.title("Fundstück eingeben")

    if st.button(
        "← Zurück",
        key="back_add",
    ):
        st.session_state.page = "home"
        st.rerun()

    st.write(
        "Trage hier einen gefundenen Gegenstand ein."
    )

    with st.form(
        "add_item_form",
        clear_on_submit=True,
    ):

        item = st.text_input(
            "Gegenstand",
            placeholder="z. B. Schwarze Jacke",
        )

        category = st.selectbox(
            "Kategorie",
            CATEGORIES,
        )

        color = st.text_input(
            "Farbe",
            placeholder="z. B. Schwarz",
        )

        location = st.text_input(
            "Fundort",
            placeholder="z. B. Sporthalle",
        )

        found_date = st.date_input(
            "Datum",
            value=date.today(),
        )

        description = st.text_area(
            "Beschreibung",
            placeholder=(
                "z. B. Schwarze Winterjacke "
                "mit Kapuze."
            ),
        )

        photo = st.file_uploader(
            "Foto (optional)",
            type=["jpg", "jpeg", "png"],
        )

        submitted = st.form_submit_button(
            "Fundstück speichern"
        )

    if not submitted:
        return

    if not item.strip():
        st.warning(
            "Bitte gib einen Gegenstand ein."
        )
        return

    if not location.strip():
        st.warning(
            "Bitte gib einen Fundort ein."
        )
        return

    photo_path = ""

    if photo is not None:

        extension = os.path.splitext(
            photo.name
        )[1].lower()

        if extension not in [
            ".jpg",
            ".jpeg",
            ".png",
        ]:
            st.warning(
                "Dieses Fotoformat wird nicht unterstützt."
            )
            return

        filename = (
            uuid.uuid4().hex + extension
        )

        photo_path = os.path.join(
            PHOTO_DIR,
            filename,
        )

        try:
            with open(
                photo_path,
                "wb",
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
                "Gegenstand": item.strip(),
                "Kategorie": category,
                "Farbe": color.strip(),
                "Fundort": location.strip(),
                "Datum": found_date.strftime(
                    "%d.%m.%Y"
                ),
                "Beschreibung": description.strip(),
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
