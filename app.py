```python
import os
import uuid
from datetime import date

import pandas as pd
import streamlit as st


# =========================================================
# FUNDKISTE – KATHARINEUM ZU LÜBECK
# =========================================================

APP_NAME = "Fundkiste"
SCHOOL_NAME = "KATHARINEUM ZU LÜBECK"
SCHOOL_YEAR = "seit 1531"


# =========================================================
# DATEIEN UND ORDNER
# =========================================================

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "fundstuecke.csv")
PHOTO_DIR = os.path.join(DATA_DIR, "fotos")


# =========================================================
# KATEGORIEN
# =========================================================

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


# Spalten der CSV-Datei
COLUMNS = [
    "Gegenstand",
    "Kategorie",
    "Farbe",
    "Fundort",
    "Datum",
    "Beschreibung",
    "Foto",
]


# =========================================================
# SEITEN-EINSTELLUNGEN
# =========================================================

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🧥",
    layout="centered",
)


# =========================================================
# ORDNER ERSTELLEN
# =========================================================

def create_directories():
    """Erstellt die benötigten Ordner."""

    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(PHOTO_DIR, exist_ok=True)


create_directories()


# =========================================================
# CSS / DESIGN
# =========================================================

def load_css():
    """Lädt das Design der Fundkiste."""

    st.markdown(
        """
        <style>

        /* -----------------------------------------
           HINTERGRUND
        ----------------------------------------- */

        .stApp {
            background-color: #ded6bb;
            color: #000000;
        }

        .block-container {
            max-width: 900px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }


        /* -----------------------------------------
           TEXT
        ----------------------------------------- */

        h1,
        h2,
        h3,
        p,
        label {
            color: #000000 !important;
        }


        /* -----------------------------------------
           STARTSEITE
        ----------------------------------------- */

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
            margin-top: 0.5rem;
        }

        .school-year {
            text-align: center;
            font-size: 1.1rem;
            color: #000000;
            margin-bottom: 2.5rem;
        }


        /* -----------------------------------------
           HAUPTBUTTONS
        ----------------------------------------- */

        .stButton > button {
            width: 100%;
            min-height: 85px;

            border: none;
            border-radius: 22px;

            background-color: #d1d95b;
            color: #000000;

            font-size: clamp(1.7rem, 5vw, 2.8rem);
            font-weight: 400;

            margin: 0.7rem 0;
        }

        .stButton > button:hover {
            background-color: #c7cf50;
            color: #000000;
        }

        .stButton > button:focus {
            color: #000000;
            border: 2px solid #000000;
        }


        /* -----------------------------------------
           EINGABEFELDER
        ----------------------------------------- */

        input,
        textarea {
            border-radius: 12px !important;
        }


        /* -----------------------------------------
           FUNDSTÜCK-KARTE
        ----------------------------------------- */

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


        /* -----------------------------------------
           ERFOLG
        ----------------------------------------- */

        .success-box {
            background-color: rgba(209, 217, 91, 0.90);

            padding: 1rem;

            border-radius: 14px;

            text-align: center;

            color: #000000;

            font-weight: 600;

            margin-top: 1rem;
        }


        /* -----------------------------------------
           MOBIL
        ----------------------------------------- */

        @media (max-width: 600px) {

            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .stButton > button {
                min-height: 75px;
            }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


load_css()


# =========================================================
# DATEN LADEN
# =========================================================

def load_data():
    """Lädt die Fundstücke aus der CSV-Datei."""

    create_directories()

    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=COLUMNS)

    try:
        data = pd.read_csv(
            DATA_FILE,
            dtype=str,
        ).fillna("")

    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=COLUMNS)

    except pd.errors.ParserError:
        st.error(
            "Die gespeicherte Fundstück-Datei konnte "
            "nicht gelesen werden."
        )

        return pd.DataFrame(columns=COLUMNS)

    # Fehlende Spalten automatisch ergänzen.
    for column in COLUMNS:

        if column not in data.columns:
            data[column] = ""

    return data[COLUMNS]


# =========================================================
# DATEN SPEICHERN
# =========================================================

def save_data(data):
    """Speichert alle Fundstücke."""

    create_directories()

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


# =========================================================
# SUCHFUNKTION
# =========================================================

def search_items(
    data,
    item,
    category,
    color,
    location,
):
    """Sucht nach passenden Fundstücken."""

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


# =========================================================
# HTML SICHER MACHEN
# =========================================================

def safe_text(value):
    """Verhindert Probleme durch Sonderzeichen in HTML."""

    if pd.isna(value):
        return ""

    text = str(value)

    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace('"', "&quot;")
    text = text.replace("'", "&#39;")

    return text


# =========================================================
# STARTSEITE
# =========================================================

def show_home():

    st.markdown(
        '<div class="home-title">Fundkiste</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="school-name">'
        "KATHARINEUM ZU LÜBECK"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="school-year">seit 1531</div>',
        unsafe_allow_html=True,
    )

    st.write("")


    # -----------------------------------------
    # BUTTONS
    # -----------------------------------------

    left, center, right = st.columns(
        [1, 2, 1]
    )

    with center:

        if st.button(
            "Suchen",
            key="home_search",
        ):

            st.session_state.page = "search"

            # Alte Suchergebnisse löschen.
            if "search_results" in st.session_state:
                del st.session_state.search_results

            st.rerun()


        if st.button(
            "Eingeben",
            key="home_add",
        ):

            st.session_state.page = "add"

            st.rerun()


# =========================================================
# SUCHSEITE
# =========================================================

def show_search(data):

    st.title("Fundstück suchen")

    # -----------------------------------------
    # ZURÜCK
    # -----------------------------------------

    if st.button(
        "← Zurück",
        key="back_search",
    ):

        st.session_state.page = "home"

        if "search_results" in st.session_state:
            del st.session_state.search_results

        st.rerun()


    st.write(
        "Suche nach einem verlorenen Gegenstand."
    )


    # -----------------------------------------
    # SUCHFELDER
    # -----------------------------------------

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


[     UTC     ] Logs for kathfind.streamlit.app/

────────────────────────────────────────────────────────────────────────────────────────

[11:34:00] 🚀 Starting up repository: 'fundkiste.1', branch: 'main', main module: 'app.py'

[11:34:00] 🐙 Cloning repository...

[11:34:02] 🐙 Cloning into '/mount/src/fundkiste.1'...

[11:34:02] 🐙 Cloned repository!

[11:34:02] 🐙 Pulling code changes from Github...

[11:34:02] 📦 Processing dependencies...

──────────────────────────────────────── uv ───────────────────────────────────────────

Using uv pip install.

Using Python 3.10.21 environment at /home/adminuser/venv

Resolved 39 packages in 652ms

Prepared 39 packages in 1.95s

Installed 39 packages in 109ms

 + altair==6.2.2

 + anyio==4.15.1

 + attrs==26.1.0

 + certifi==2026.7.22

 + charset-normalizer==3.5.1

 + click==8.5.0

 + exceptiongroup==1.3.1

 + h11==0.16.0

 + httptools==0.8.0

 + idna==3.19[2026-09-08 11:34:05.848143] 

 + itsdangerous==2.2.0

 + jinja2==3.1.6

 + jsonschema==4.26.0

 + jsonschema-specifications==2025.9.1

 + markupsafe==3.0.3

 + narwhals==2.25.0

 + numpy==2.2.6

 [2026-09-08 11:34:05.848522] + packaging==26.3

 + pandas==2.3.3

 + pillow==12.3.0

 + protobuf==7.36.1

 + pyarrow==25.0.1

 [2026-09-08 11:34:05.848918] + pydeck==0.9.3

 + python-dateutil==2.9.0.post0

 + python-multipart==0.0.32

 + pytz==2026.3.post1

 + referencing==0.37.0

 + requests==2.34.2

 [2026-09-08 11:34:05.849197] + rpds-py==0.30.0

 + six==1.17.0

 + starlette==1.6.0

 + streamlit==1.63.0

 [2026-09-08 11:34:05.849423] + toml==0.10.2

 + typing-extensions==4.16.0

 + tzdata==2026.3

 + urllib3==2.7.0

 + uvicorn==0.52.4

 +[2026-09-08 11:34:05.849572]  watchdog==6.0.0

 + websockets==16.1.1

Checking if Streamlit is installed

Found Streamlit version 1.63.0 in the environment

Detected pyarrow 25.0.1 (known segfault, apache/arrow#50471). Replacing with pyarrow<25.

Using uv pip install.

Using Python 3.10.21 environment at /home/adminuser/venv

Resolved 1 package in 31ms

Prepared 1 package in 1.09s

Uninstalled 1 package in 101ms

Installed 1 package in 80ms

 - pyarrow==25.0.1

 + pyarrow==24.0.0

Installing rich for an improved exception logging

Using uv pip install.

Using Python 3.10.21 environment at /home/adminuser/venv

Resolved 4 packages in 127ms

Prepared 4 packages in 123ms

Installed 4 packages in 12ms

 + markdown-it-py==4.2.0

 + mdurl==0.1.2

 + pygments[2026-09-08 11:34:10.495392] ==2.21.0

 + rich==15.0.0

────────────────────────────────────────────────────────────────────────────────────────

[11:34:11] 🐍 Python dependencies were installed from /mount/src/fundkiste.1/requirements.txt using uv.

Check if streamlit is installed

Streamlit is already installed

[11:34:13] 📦 Processed dependencies!

2026-09-08 11:34:14.537 Uvicorn server started on :::8501

2026-09-08 11:34:19.750 Script compilation error

Traceback (most recent call last):

  File "/home/adminuser/venv/lib/python3.10/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 651, in _run_script

    code = self._script_cache.get_bytecode(script_path)

  File "/home/adminuser/venv/lib/python3.10/site-packages/streamlit/runtime/scriptrunner/script_cache.py", line 72, in get_bytecode

    filebody = magic.add_magic(filebody, script_path)

  File "/home/adminuser/venv/lib/python3.10/site-packages/streamlit/runtime/scriptrunner/magic.py", line 45, in add_magic

    tree = ast.parse(code, script_path, "exec")

  File "/usr/local/lib/python3.10/ast.py", line 50, in parse

    return compile(source, filename, mode, flags,

  File "/mount/src/fundkiste.1/app.py", line 13

    APP_NAME = "Fundkiste" 912544

                           ^^^^^^

SyntaxError: invalid syntax

2026-09-08 11:34:19.766 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.

2026-09-08 11:34:20.168 Script compilation error

Traceback (most recent call last):

  File "/home/adminuser/venv/lib/python3.10/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 651, in _run_script

    code = self._script_cache.get_bytecode(script_path)

  File "/home/adminuser/venv/lib/python3.10/site-packages/streamlit/runtime/scriptrunner/script_cache.py", line 72, in get_bytecode

    filebody = magic.add_magic(filebody, script_path)

  File "/home/adminuser/venv/lib/python3.10/site-packages/streamlit/runtime/scriptrunner/magic.py", line 45, in add_magic

    tree = ast.parse(code, script_path, "exec")

  File "/usr/local/lib/python3.10/ast.py", line 50, in parse

    return compile(source, filename, mode, flags,

  File "/mount/src/fundkiste.1/app.py", line 13

    APP_NAME = "Fundkiste" 912544

                           ^^^^^^

SyntaxError: invalid syntax

2026-09-08 11:34:20.171 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.

2026-09-08 11:34:22.586 Script compilation error

Traceback (most recent call last):

  File "/home/adminuser/venv/lib/python3.10/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 651, in _run_script

    code = self._script_cache.get_bytecode(script_path)

  File "/home/adminuser/venv/lib/python3.10/site-packages/streamlit/runtime/scriptrunner/script_cache.py", line 72, in get_bytecode

    filebody = magic.add_magic(filebody, script_path)

  File "/home/adminuser/venv/lib/python3.10/site-packages/streamlit/runtime/scriptrunner/magic.py", line 45, in add_magic

    tree = ast.parse(code, script_path, "exec")

  File "/usr/local/lib/python3.10/ast.py", line 50, in parse

    return compile(source, filename, mode, flags,

  File "/mount/src/fundkiste.1/app.py", line 13

    APP_NAME = "Fundkiste" 912544

                           ^^^^^^

SyntaxError: invalid syntax

2026-09-08 11:34:22.587 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.

2026-09-08 11:35:11.425 Script compilation error

Traceback (most recent call last):

  File "/home/adminuser/venv/lib/python3.10/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 651, in _run_script

    code = self._script_cache.get_bytecode(script_path)

  File "/home/adminuser/venv/lib/python3.10/site-packages/streamlit/runtime/scriptrunner/script_cache.py", line 72, in get_bytecode

    filebody = magic.add_magic(filebody, script_path)

  File "/home/adminuser/venv/lib/python3.10/site-packages/streamlit/runtime/scriptrunner/magic.py", line 45, in add_magic

    tree = ast.parse(code, script_path, "exec")

  File "/usr/local/lib/python3.10/ast.py", line 50, in parse

    return compile(source, filename, mode, flags,

  File "/mount/src/fundkiste.1/app.py", line 13

    APP_NAME = "Fundkiste" 912544

                           ^^^^^^

SyntaxError: invalid syntax

2026-09-08 11:35:11.427 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.

main
ronialsindi08-ai/fundkiste.1/main/app.py

    location = st.text_input(
        "Fundort",
        placeholder="z. B. Sporthalle",
    )


    # -----------------------------------------
    # SUCHEN
    # -----------------------------------------

    if st.button(
        "Suchen",
        key="perform_search",
    ):

        results = search_items(
            data=data,
            item=item,
            category=category,
            color=color,
            location=location,
        )

        st.session_state.search_results = results


    # -----------------------------------------
    # NOCH NICHT GESUCHT
    # -----------------------------------------

    if "search_results" not in st.session_state:
        return


    results = st.session_state.search_results


    # -----------------------------------------
    # KEINE ERGEBNISSE
    # -----------------------------------------

    if results.empty:

        if data.empty:

            st.info(
                "Es wurden noch keine Fundstücke "
                "eingetragen."
            )

        else:

            st.info(
                "Leider wurde kein passendes "
                "Fundstück gefunden."
            )

        return


    # -----------------------------------------
    # ERGEBNISSE
    # -----------------------------------------

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
                    {item_category}
                    <br>

                    <b>Farbe:</b>
                    {item_color}
                    <br>

                    <b>Fundort:</b>
                    {item_location}
                    <br>

                    <b>Gefunden am:</b>
                    {item_date}
                    <br>

                    <b>Beschreibung:</b>
                    {item_description}

                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# FUNDSTÜCK EINGEBEN
# =========================================================

def show_add_item(data):

    st.title("Fundstück eingeben")


    # -----------------------------------------
    # ZURÜCK
    # -----------------------------------------

    if st.button(
        "← Zurück",
        key="back_add",
    ):

        st.session_state.page = "home"

        st.rerun()


    st.write(
        "Trage hier einen gefundenen "
        "Gegenstand ein."
    )


    # -----------------------------------------
    # FORMULAR
    # -----------------------------------------

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
            type=[
                "jpg",
                "jpeg",
                "png",
            ],
        )

        submitted = st.form_submit_button(
            "Fundstück speichern"
        )


    # -----------------------------------------
    # FORMULAR NOCH NICHT ABGESCHICKT
    # -----------------------------------------

    if not submitted:
        return


    # -----------------------------------------
    # VALIDIERUNG
    # -----------------------------------------

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


    # -----------------------------------------
    # FOTO SPEICHERN
    # -----------------------------------------

    photo_path = ""


    if photo is not None:

        # Sicheren Dateinamen erzeugen.
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
            f"{uuid.uuid4().hex}"
            f"{extension}"
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


    # -----------------------------------------
    # NEUES FUNDSTÜCK
    # -----------------------------------------

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


    # -----------------------------------------
    # DATEN HINZUFÜGEN
    # -----------------------------------------

    updated_data = pd.concat(
        [
            data,
            new_item,
        ],
        ignore_index=True,
    )


    # -----------------------------------------
    # SPEICHERN
    # -----------------------------------------

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


# =========================================================
# APP-START
# =========================================================

if "page" not in st.session_state:

    st.session_state.page = "home"


# Daten laden.
data = load_data()


# -----------------------------------------
# SEITE AUSWÄHLEN
# -----------------------------------------

if st.session_state.page == "home":

    show_home()


elif st.session_state.page == "search":

    show_search(data)


elif st.session_state.page == "add":

    show_add_item(data)


else:

    # Falls ein unbekannter Seitenname
    # vorhanden ist, zurück zur Startseite.

    st.session_state.page = "home"

    st.rerun()
```
