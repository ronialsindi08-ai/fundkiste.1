# --------------------------------------------------
# KI laden
# --------------------------------------------------

@st.cache_resource
def lade_ki():

    # ------------------------------------------------
    # Weg 1: das komplette Modell direkt laden
    # (der offizielle Teachable-Machine-Weg)
    # ------------------------------------------------

    try:
        modell = tf.keras.models.load_model(
            MODEL_DATEI,
            compile=False
        )

        return {"art": "komplett", "modell": modell}

    except Exception:
        pass  # falls das nicht klappt: Weg 2

    # ------------------------------------------------
    # Weg 2: Gewichte manuell aus der H5-Datei lesen
    # ------------------------------------------------

    def lies_gewicht(gruppe, name):
        """Sucht ein Gewicht in einer HDF5-Gruppe.

        Teachable-Machine-Dateien speichern die Namen mit
        ':0'-Endung ('kernel:0' statt 'kernel'). Manche
        Keras-Dateien legen die Gewichte zusätzlich eine
        Untergruppe tiefer ab. Beides wird hier abgedeckt.
        """

        kandidaten = [name, name + ":0"]

        for kandidat in kandidaten:
            if kandidat in gruppe:
                return np.array(gruppe[kandidat])

        untergruppen = [
            gruppe[schluessel]
            for schluessel in gruppe
            if isinstance(gruppe[schluessel], h5py.Group)
        ]

        for untergruppe in untergruppen:
            for kandidat in kandidaten:
                if kandidat in untergruppe:
                    return np.array(untergruppe[kandidat])

        raise ValueError(
            f"Gewicht fehlt: {name} "
            f"(vorhanden in der Datei: {list(gruppe.keys())})"
        )

    # MobileNetV2 aufbauen
    basis = tf.keras.applications.MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights=None
    )

    # Gewichte aus dem alten Teachable-Machine-Modell
    with h5py.File(MODEL_DATEI, "r") as datei:

        gewicht_gruppe = datei["model_weights"]["sequential_1"]

        fehlende_schichten = []

        for layer in basis.layers:

            if not layer.weights:
                continue

            if layer.name not in gewicht_gruppe:
                fehlende_schichten.append(layer.name)
                continue

            layer_gruppe = gewicht_gruppe[layer.name]

            neue_gewichte = []

            for variable in layer.weights:

                variablen_name = variable.name.split("/")[-1]
                variablen_name = variablen_name.split(":")[0]

                # FIX: sucht jetzt 'kernel' UND 'kernel:0'
                neue_gewichte.append(
                    lies_gewicht(layer_gruppe, variablen_name)
                )

            layer.set_weights(neue_gewichte)

        # FIX: vorher wurden fehlende Schichten stillschweigend
        # übersprungen -> MobileNetV2 hätte zufällige Gewichte
        # behalten und Unsinn vorhergesagt
        if fehlende_schichten:
            raise ValueError(
                "Die Schichtnamen in keras_model.h5 passen nicht zu "
                "MobileNetV2. Fehlende Schichten: "
                + ", ".join(fehlende_schichten[:10])
            )

        # Klassifikator
        klassifikator_gruppe = datei["model_weights"]["sequential_3"]

        dense1_gewicht = lies_gewicht(
            klassifikator_gruppe["dense_Dense1"], "kernel"
        )

        dense1_bias = lies_gewicht(
            klassifikator_gruppe["dense_Dense1"], "bias"
        )

        dense2_gewicht = lies_gewicht(
            klassifikator_gruppe["dense_Dense2"], "kernel"
        )

    # Größen automatisch aus der Datei übernehmen
    eingang, versteckt = dense1_gewicht.shape
    klassen = dense2_gewicht.shape[1]

    if klassen != len(labels):
        raise ValueError(
            f"labels.txt hat {len(labels)} Einträge, "
            f"das Modell erwartet aber {klassen} Klassen."
        )

    if eingang != basis.output_shape[-1]:
        raise ValueError(
            "Die Klassifikator-Eingabe "
            f"({eingang}) passt nicht zur MobileNetV2-Ausgabe "
            f"({basis.output_shape[-1]})."
        )

    klassifikator = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(eingang,)),
        tf.keras.layers.Dense(
            versteckt,
            activation="relu",
            name="dense_eins"
        ),
        tf.keras.layers.Dense(
            klassen,
            activation="softmax",
            use_bias=False,
            name="dense_zwei"
        )
    ])

    klassifikator.get_layer("dense_eins").set_weights([
        dense1_gewicht,
        dense1_bias
    ])

    klassifikator.get_layer("dense_zwei").set_weights([
        dense2_gewicht
    ])

    return {"art": "manuell", "basis": basis, "klassifikator": klassifikator}


# --------------------------------------------------
# Bild erkennen
# --------------------------------------------------

def erkenne_bild(bild, ki):

    bild = bild.convert("RGB")
    bild = bild.resize((224, 224))

    bild_array = np.asarray(bild).astype(np.float32)

    # Genau die übliche Teachable-Machine-Normalisierung
    bild_array = (bild_array / 127.5) - 1.0

    bild_array = np.expand_dims(bild_array, axis=0)

    if ki["art"] == "komplett":

        vorhersage = ki["modell"](
            bild_array,
            training=False
        )

    else:

        # MobileNetV2
        merkmale = ki["basis"](bild_array, training=False)

        # Global Average Pooling
        merkmale = tf.reduce_mean(
            merkmale,
            axis=[1, 2]
        )

        # Klassifikation
        vorhersage = ki["klassifikator"](
            merkmale,
            training=False
        )

    vorhersage = vorhersage.numpy()[0]

    index = int(np.argmax(vorhersage))
    sicherheit = float(vorhersage[index])

    return labels[index], sicherheit


@st.cache_data(show_spinner=False)
def erkenne_bild_bytes(bild_bytes):

    bild = Image.open(io.BytesIO(bild_bytes))

    ki = lade_ki()

    return erkenne_bild(bild, ki)
