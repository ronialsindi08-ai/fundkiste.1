import os
import uuid
from datetime import date

import pandas as pd
import streamlit as st


# ---------------------------------------------------------
# Einstellungen
# ---------------------------------------------------------

APP_NAME = "Fundkiste" 912544

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "fundstuecke.csv")
PHOTO_DIR = os.path.join(DATA_DIR, "fotos")

# HIER SPÄTER DEIN TEACHABLE-MACHINE-MODELL EINTRAGEN
MODEL_URL = "HIER_DEIN_TEACHABLE_MACHINE_MODELL_EINTRAGEN"

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
# Daten
# ---------------------------------------------------------

def load_data():
    """Lädt die Fundstücke aus der CSV-Datei."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(PHOTO_DIR, exist_ok=True)

    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=COLUMNS)

    try:
        data = pd.read_csv(DATA_FILE, dtype=str).fillna("")
    except (pd.errors.EmptyDataError, pd.errors.ParserError):
        return pd.DataFrame(columns=COLUMNS)

    for column in COLUMNS:
        if column not in data.columns:
            data[column] = ""

    return data[COLUMNS]


def save_data(data):
    """Speichert alle Fundstücke."""
    os.makedirs(DATA_DIR, exist_ok=True)
    data.to_csv(DATA_FILE, index=False)


def search_items(data, item, category, color, location):
    """Sucht nach passenden Fundstücken."""
    result = data.copy()

    if item:
        result = result[
            result["Gegenstand"].str.contains(item, case=False, na=False)
        ]

    if category != "Alle":
        result = result[result["Kategorie"] == category]

    if color:
        result = result[
            result["Farbe"].str.contains(color, case=False, na=False)
        ]

    if location:
        result = result[
            result["Fundort"].str.contains(location, case=False, na=False)
        ]

    return result


# ---------------------------------------------------------
# Teachable Machine
# ---------------------------------------------------------

def recognize_with_teachable_machine(image):
    """
    Schnittstelle für das spätere Teachable-Machine-Modell.

    Hier kann später die Bilderkennung eingebaut werden.

    MODEL_URL enthält absichtlich noch keine echte Modell-URL.
    """
    if not image:
        return None

    if MODEL_URL.startswith("HIER_"):
        return None

    # Die eigentliche Teachable-Machine-Integration kann hier
    # ergänzt werden, sobald die konkrete Modell-URL bekannt ist.
    return None


# ---------------------------------------------------------
# CSS
# ---------------------------------------------------------

def load_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

        :root {
            --cream: #ddd5b9;
            --cream-light: #e4dcc2;
            --green: #d1d95b;
            --black: #000000;
        }

        .stApp {
            background-color: var(--cream);
            color: var(--black);
            font-family: 'Inter', sans-serif;
        }

        /* Dezentes Muster im Hintergrund */
        .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            opacity: 0.16;
            background-image:
                radial-gradient(circle at 20% 20%, white 0 5px, transparent 6px),
                radial-gradient(circle at 70% 70%, white 0 5px, transparent 6px);
            background-size: 55px 55px;
        }

        .block-container {
            max-width: 900px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        h1, h2, h3, p, label {
            color: var(--black) !important;
        }

        .home-title {
            text-align: center;
            font-size: clamp(3.5rem, 10vw, 7rem);
            line-height: 1;
            font-weight: 400;
            margin-top: 1rem;
            margin-bottom: 1.5rem;
            color: black;
        }

        .school-name {
            text-align: center;
            font-size: clamp(1.2rem, 3vw, 2rem);
            font-weight: 400;
            margin-top: 0.5rem;
            margin-bottom: 0.1rem;
            color: black;
        }

        .school-year {
            text-align: center;
            font-size: 1.1rem;
            margin-bottom: 2.5rem;
            color: black;
        }

        .logo-placeholder {
            text-align: center;
            font-size: 3rem;
            line-height: 1;
            margin-bottom: 0.5rem;
            color: black;
        }

        /* Große Startseiten-Buttons */
        .stButton > button {
            width: 100%;
            min-height: 100px;
            border: none;
            border-radius: 22px;
            background-color: var(--green);
            color: black;
            font-size: clamp(2rem, 5vw, 3.5rem);
            font-weight: 400;
            margin: 0.7rem 0;
            transition: transform 0.1s ease;
        }

        .stButton > button:hover {
            background-color: var(--green);
            color: black;
            transform: scale(1.01);
        }

        .stButton > button:focus {
            color: black;
            border: 2px solid black;
        }

        /* Eingabefelder */
        input, textarea, [data-baseweb="select"] > div {
            border-radius: 12px !important;
        }

        .item-card {
            background: rgba(255, 255, 255, 0.35);
            border: 1px solid rgba(0, 0, 0, 0.12);
            border-radius: 16px;
            padding: 1rem 1.2rem;
            margin-bottom: 1rem;
        }

        .item-title {
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }

        .item-info {
            line-height: 1.7;
        }

        .success-box {
            background: rgba(209, 217, 91, 0.8);
            padding: 1rem;
            border-radius: 14px;
            text-align: center;
            color: black;
            font-weight: 500;
            margin: 1rem 0;
        }

        @media (max-width: 600px) {
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .stButton > button {
                min-height: 85px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# Startseite
# ---------------------------------------------------------

def show_home():
    st.markdown('<div class="home-title">Fundkiste</div>', unsafe_allow_html=True)

    # Wenn später assets/logo.png vorhanden ist, wird es angezeigt.
    logo_path = os.path.join("assets", "logo.png")

    if os.path.exists(logo_path):
        st.image(logo_path, width=75)
    else:
        st.markdown(
            '<div class="logo-placeholder">✦</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="school-name">KATHARINEUM ZU LÜBECK</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="school-year">seit 1531</div>',
        unsafe_allow_html=True,
    )

    left, center, right = st.columns([1, 2, 1])

    with center:
        if st.button("Suchen", key="home_search"):
            st.session_state.page = "search"
            st.rerun()

        if st.button("Eingeben", key="home_add"):
            st.session_state.page = "add"
            st.rerun()

    # Die Illustration ist optional.
    illustration = os.path.join("assets", "fundkiste.png")

    if os.path.exists(illustration):
        st.image(illustration, use_container_width=True)


# ---------------------------------------------------------
# Suchseite
# ---------------------------------------------------------

def show_search(data):
    st.title("Fundstück suchen")

    if st.button("← Zurück", key="back_search"):
        st.session_state.page = "home"
        st.rerun()

    st.write("Suche nach einem verlorenen Gegenstand.")

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

    if st.button("Suchen", key="search_button"):
        results = search_items(
            data,
            item,
            category,
            color,
            location,
        )

        st.session_state.search_results = results

    if "search_results" not in st.session_state:
        return

    results = st.session_state.search_results

    if results.empty:
        st.info("Leider wurde kein passender Gegenstand gefunden.")
        return

    st.subheader(f"{len(results)} Fundstück(e) gefunden")

    for _, row in results.iterrows():
        st.markdown(
            f"""
            <div class="item-card">
                <div class="item-title">
                    {row["Gegenstand"]}
                </div>

                <div class="item-info">
                    <b>Kategorie:</b> {row["Kategorie"]}<br>
                    <b>Farbe:</b> {row["Farbe"]}<br>
                    <b>Fundort:</b> {row["Fundort"]}<br>
                    <b>Gefunden am:</b> {row["Datum"]}<br>
                    <b>Beschreibung:</b> {row["Beschreibung"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------
# Eingabeseite
# ---------------------------------------------------------

def show_add_item(data):
    st.title("Fundstück eingeben")

    if st.button("← Zurück", key="back_add"):
        st.session_state.page = "home"
        st.rerun()

    st.write("Trage hier einen gefundenen Gegenstand ein.")

    with st.form("add_item_form"):
        item = st.text_input(
            "Gegenstand",
            placeholder="z. B. Jacke",
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
            "Kurze Beschreibung",
            placeholder="z. B. Schwarze Winterjacke mit Kapuze.",
        )

        photo = st.file_uploader(
            "Foto (optional)",
            type=["jpg", "jpeg", "png"],
        )

        submitted = st.form_submit_button("Fundstück speichern")

    if not submitted:
        return

    if not item.strip():
        st.warning("Bitte gib einen Gegenstand ein.")
        return

    photo_path = ""

    if photo is not None:
        filename = f"{uuid.uuid4().hex}_{photo.name}"
        photo_path = os.path.join(PHOTO_DIR, filename)

        try:
            with open(photo_path, "wb") as file:
                file.write(photo.getbuffer())
        except OSError:
            photo_path = ""

    # Hier wird später die Bilderkennung aufgerufen.
    predicted_category = recognize_with_teachable_machine(photo)

    if photo is not None and MODEL_URL.startswith("HIER_"):
        st.info(
            "Das Foto wurde gespeichert. "
            "Die Bilderkennung ist noch nicht verbunden."
        )

    new_item = pd.DataFrame(
        [
            {
                "Gegenstand": item.strip(),
                "Kategorie": category,
                "Farbe": color.strip(),
                "Fundort": location.strip(),
                "Datum": found_date.strftime("%d.%m.%Y"),
                "Beschreibung": description.strip(),
                "Foto": photo_path,
            }
        ]
    )

    data = pd.concat([data, new_item], ignore_index=True)
    save_data(data)

    st.markdown(
        """
        <div class="success-box">
            Das Fundstück wurde erfolgreich gespeichert.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# Hauptprogramm
# ---------------------------------------------------------

st.set_page_config(
    page_title="Fundkiste",
    page_icon="🧥",
    layout="centered",
)

load_css()

if "page" not in st.session_state:
    st.session_state.page = "home"

data = load_data()

if st.session_state.page == "home":
    show_home()

elif st.session_state.page == "search":
    show_search(data)

elif st.session_state.page == "add":
    show_add_item(data)
