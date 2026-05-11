# 📻 Epicentro Radio — Monitor de Noticias

Monitor automático de noticias para la red de coberturas de Epicentro Radio.
Se actualiza automáticamente cada 4 horas mediante GitHub Actions y se publica en GitHub Pages.

## 🗺️ Coberturas de la red

| Zona | Frecuencia |
|------|-----------|
| Casablanca | 96.9 FM |
| La Ligua | 88.9 FM |
| Zapallar-Concón | 93.5 FM |
| Salamanca | 88.3 FM |
| Caldera | 95.5 FM |
| Vallenar | 93.9 FM |
| Los Vilos | 98.5 FM |
| Huasco - Freirina | 97.1 FM |
| Illapel | 101.1 FM |
| Monte Patria | 96.3 FM |
| Punta Arenas | 88.1 FM |
| Cuncumén | 88.3 FM |
| Arauco | 99.1 FM |
| Puerto Natales | 100.5 FM |

## 🚀 Configuración en GitHub (paso a paso)

### 1. Crear el repositorio
1. Ve a [github.com/new](https://github.com/new)
2. Nombre: `epicentro-monitor` (o el que prefieras)
3. Privado o público (ambos funcionan)
4. Haz clic en **Create repository**

### 2. Subir los archivos
```bash
git init
git add .
git commit -m "🚀 Primer commit — Monitor Epicentro"
git remote add origin https://github.com/TU_USUARIO/epicentro-monitor.git
git push -u origin main
```

### 3. Activar GitHub Pages
1. Ve a **Settings → Pages**
2. Source: **GitHub Actions**
3. Guarda

### 4. Ejecutar el primer escaneo
1. Ve a **Actions → Escanear medios y publicar**
2. Haz clic en **Run workflow**
3. En ~1 minuto tu monitor estará en:
   `https://TU_USUARIO.github.io/epicentro-monitor`

## ➕ Agregar nuevos medios

Edita el archivo `src/feeds.py` y añade un dict al final de la lista `FEEDS`:

```python
{"url": "https://nuevo-medio.cl/feed", "medio": "Nombre del Medio", "zona": "Ciudad", "cobertura": "Frecuencia FM"},
```

Haz commit y push → el próximo escaneo incluirá el nuevo medio automáticamente.

## ⚙️ Cambiar la frecuencia de escaneo

Edita `.github/workflows/scan.yml`, línea `cron`:

```yaml
- cron: '0 */4 * * *'   # cada 4 horas (actual)
- cron: '0 */2 * * *'   # cada 2 horas
- cron: '0 8,14,20 * * *' # a las 8:00, 14:00 y 20:00
```

## 📁 Estructura del proyecto

```
epicentro-monitor/
├── .github/
│   └── workflows/
│       └── scan.yml          ← automatización
├── src/
│   ├── feeds.py              ← lista de medios (editar aquí)
│   ├── scanner.py            ← escanea los RSS
│   └── build.py              ← genera el HTML final
├── data/
│   ├── noticias.json         ← noticias escaneadas
│   └── ultimo_escaneo.txt    ← timestamp del último escaneo
├── public/
│   └── index.html            ← panel web (generado automáticamente)
└── README.md
```
