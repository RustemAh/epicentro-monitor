#!/usr/bin/env python3
"""
scanner.py — Escanea todos los feeds RSS de la red Epicentro
y guarda los resultados en data/noticias.json
"""
import json, re, requests, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from feeds import FEEDS

MAX_ITEMS = 8   # noticias por medio
TIMEOUT   = 12  # segundos por request

def strip_cdata(text):
    if not text: return ""
    return re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', text, flags=re.DOTALL).strip()

def strip_html(text):
    return re.sub(r'<[^>]+>', '', text or '').strip()[:350]

def parse_feed(feed):
    items = []
    try:
        r = requests.get(feed["url"], timeout=TIMEOUT,
                         headers={"User-Agent": "EpicentroBot/1.0 (RSS Reader)"})
        r.raise_for_status()
        xml_text = re.sub(r' xmlns(?::[a-z]+)?="[^"]*"', '', r.text)
        xml_text = re.sub(r'<\?xml[^>]+\?>', '', xml_text)
        root = ET.fromstring(xml_text)
        channel = root.find('.//channel') or root
        entries = channel.findall('.//item') or root.findall('.//{http://www.w3.org/2005/Atom}entry')

        for entry in entries[:MAX_ITEMS]:
            t = entry.find('title')
            l = entry.find('link')
            d = entry.find('description') or entry.find('summary')
            p = entry.find('pubDate') or entry.find('published') or entry.find('updated')

            title = strip_cdata(t.text if t is not None else "").strip()
            link  = strip_cdata(l.text if l is not None else "").strip()
            desc  = strip_html(strip_cdata(d.text if d is not None else ""))
            pub   = p.text.strip() if p is not None and p.text else ""

            if title and len(title) > 5:
                items.append({
                    "titulo":          title,
                    "enlace":          link,
                    "descripcion":     desc,
                    "publicado":       pub,
                    "medio":           feed["medio"],
                    "zona":            feed["zona"],
                    "cobertura_radio": feed["cobertura"],
                })

        print(f"  ✅ {feed['medio']}: {len(items)} noticias")
    except Exception as e:
        print(f"  ❌ {feed['medio']}: {e}")
    return items

def main():
    print(f"\n🔄 Escaneo iniciado — {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"   Feeds configurados: {len(FEEDS)}\n")

    todas = []
    for feed in FEEDS:
        todas.extend(parse_feed(feed))

    Path("data").mkdir(exist_ok=True)
    with open("data/noticias.json", "w", encoding="utf-8") as f:
        json.dump(todas, f, ensure_ascii=False, indent=2)

    with open("data/ultimo_escaneo.txt", "w") as f:
        f.write(datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))

    print(f"\n✅ Total: {len(todas)} noticias guardadas en data/noticias.json")
    print(f"   Medios activos: {len(set(n['medio'] for n in todas))}/{len(FEEDS)}")

if __name__ == "__main__":
    main()
