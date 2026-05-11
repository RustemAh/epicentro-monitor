# ============================================================
# feeds.py — Configuración de medios de la red Epicentro Radio
# Para agregar un nuevo medio, añade un dict a esta lista.
# ============================================================

FEEDS = [

    # ── REGIÓN DE COQUIMBO — IV Región ──────────────────────
    {"url": "https://www.elcoquimbano.cl/feed",    "medio": "El Coquimbano",         "zona": "IV Región",         "cobertura": "Toda la red Coquimbo"},
    {"url": "https://www.elserenense.cl/feed",     "medio": "El Serenense",           "zona": "La Serena",         "cobertura": "Cobertura IV Región"},
    {"url": "https://laserenaonline.cl/feed",      "medio": "La Serena Online",       "zona": "La Serena",         "cobertura": "Cobertura IV Región"},
    {"url": "https://serenaycoquimbo.cl/feed",     "medio": "Serena y Coquimbo",      "zona": "IV Región",         "cobertura": "Toda la red Coquimbo"},
    {"url": "https://regiondecoquimbo.cl/feed",    "medio": "Región de Coquimbo",     "zona": "IV Región",         "cobertura": "Toda la red Coquimbo"},
    {"url": "https://ovallehoy.cl/feed",           "medio": "Ovalle Hoy",             "zona": "Ovalle / Limarí",   "cobertura": "Monte Patria 96.3 FM"},
    {"url": "https://www.elmontepatrino.cl/feed",  "medio": "El Montepatrino",        "zona": "Monte Patria",      "cobertura": "Monte Patria 96.3 FM"},
    {"url": "https://www.elcombarbalino.cl/feed",  "medio": "El Combarbalino",        "zona": "Combarbalá",        "cobertura": "Monte Patria 96.3 FM"},
    {"url": "https://illapelchile.cl/feed",        "medio": "El Diario de Illapel",   "zona": "Illapel",           "cobertura": "Illapel 101.1 FM"},
    {"url": "https://www.elillapelino.cl/feed",    "medio": "El Illapelino",          "zona": "Illapel",           "cobertura": "Illapel 101.1 FM"},
    {"url": "https://veetv.cl/feed",               "medio": "VeeTV",                  "zona": "Illapel / Choapa",  "cobertura": "Illapel 101.1 FM / Salamanca 88.3 FM"},
    {"url": "https://www.elsalamanquino.cl/feed",  "medio": "El Salamanquino",        "zona": "Salamanca",         "cobertura": "Salamanca 88.3 FM / Cuncumén 88.3 FM"},
    {"url": "https://losviloschile.cl/feed",       "medio": "Diario de Los Vilos",    "zona": "Los Vilos",         "cobertura": "Los Vilos 98.5 FM"},
    {"url": "https://www.davidnoticias.cl/feed",   "medio": "David Noticias",         "zona": "Los Vilos",         "cobertura": "Los Vilos 98.5 FM"},
    {"url": "https://www.elandacollino.cl/feed",   "medio": "El Andacollino",         "zona": "Andacollo",         "cobertura": "Cobertura IV Región"},
    {"url": "https://www.elpaihuanino.cl/feed",    "medio": "El Paihuanino",          "zona": "Paihuano",          "cobertura": "Cobertura IV Región"},

    # ── REGIÓN DE ATACAMA ────────────────────────────────────
    {"url": "https://www.atacamanoticias.cl/feed", "medio": "Atacama Noticias",       "zona": "Caldera / Vallenar","cobertura": "Caldera 95.5 FM / Vallenar 93.9 FM"},
    {"url": "https://elnoticierodelhuasco.cl/feed","medio": "El Noticiero del Huasco","zona": "Huasco - Freirina", "cobertura": "Huasco - Freirina 97.1 FM"},

    # ── REGIÓN DE VALPARAÍSO ─────────────────────────────────
    {"url": "https://laliguanoticias.cl/feed",     "medio": "La Ligua Noticias",      "zona": "La Ligua",          "cobertura": "La Ligua 88.9 FM"},
    {"url": "https://diariolaquinta.cl/feed",      "medio": "Diario La Quinta",       "zona": "Casablanca",        "cobertura": "Casablanca 96.9 FM / Zapallar-Concón 93.5 FM"},
    {"url": "https://g5noticias.cl/feed/",         "medio": "G5",                     "zona": "Valparaiso",        "cobertura": "Casablanca 96.9 FM / Zapallar-Concón 93.5 FM"},

    # ── REGIÓN DEL BIOBÍO ────────────────────────────────────
    {"url": "https://araucovision.cl/feed",        "medio": "Araucovisión",           "zona": "Arauco",            "cobertura": "Arauco 99.1 FM"},

    # ── REGIÓN DE MAGALLANES ─────────────────────────────────
    {"url": "https://laprensaaustral.cl/feed",     "medio": "La Prensa Austral",      "zona": "Punta Arenas",      "cobertura": "Punta Arenas 88.1 FM / Puerto Natales 100.5 FM"},
    {"url": "https://elmagallanico.com/feed",      "medio": "El Magallánico",         "zona": "Punta Arenas",      "cobertura": "Punta Arenas 88.1 FM"},
    {"url": "https://www.ovejeronoticias.cl/feed", "medio": "Ovejero Noticias",       "zona": "Punta Arenas",      "cobertura": "Punta Arenas 88.1 FM / Puerto Natales 100.5 FM"},

    # ── AGREGAR NUEVOS MEDIOS AQUÍ ───────────────────────────
    # {"url": "https://nuevo-medio.cl/feed", "medio": "Nombre Medio", "zona": "Ciudad", "cobertura": "Frecuencia FM"},
]
