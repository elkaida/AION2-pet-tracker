"""Обновляет data/names.json именами питомцев с metabot.gg (база из клиента игры).

Запускается вручную, когда в игре появляются новые питомцы; оверлей сам на сайт
не ходит. Русских имён на сайте нет - они остаются те, что выучены из чата.

  python tools/fetch_pet_names.py
"""
import html as htmllib
import json
import os
import re
import sys
import time
import urllib.request

LANGS = ["en", "de", "es", "fr", "ko", "pt"]
URL = "https://metabot.gg/{lang}/aion-2/mounts"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "names.json")
# <span data-a2-k="own:m:1097"><a ... href="/en/aion-2/mounts/karnif">...Karnif...</a>
ROW = re.compile(r'data-a2-k="own:m:(\d+)"[^>]*>\s*<a\b[^>]*>(.*?)</a>', re.S)


def download(url, attempts=4):
    req = urllib.request.Request(url, headers={"User-Agent": "AION2-pet-tracker (github.com/elkaida/AION2-pet-tracker)"})
    for i in range(attempts):
        try:
            return urllib.request.urlopen(req, timeout=120).read().decode("utf-8")
        except OSError as e:  # сайт иногда долго рендерит страницу
            if i == attempts - 1:
                raise
            print(f"  повтор ({e})")
            time.sleep(5 * (i + 1))


def fetch(lang):
    page = download(URL.format(lang=lang))
    names = {}
    for pid, inner in ROW.findall(page):
        name = htmllib.unescape(re.sub(r"<[^>]+>", "", inner)).strip()
        if name:
            names[int(pid)] = name
    return names


def main():
    try:
        data = json.load(open(OUT, encoding="utf-8"))
    except FileNotFoundError:
        data = {}
    for lang in LANGS:
        names = fetch(lang)
        if len(names) < 150:  # разметка сайта поменялась - не затираем базу
            sys.exit(f"{lang}: найдено только {len(names)} имён, проверьте разбор страницы")
        data[lang] = {str(k): v for k, v in sorted(names.items())}
        print(f"{lang}: {len(names)}")
    order = ["en", "ru"] + [l for l in LANGS if l != "en"]
    data = {l: data[l] for l in order + sorted(set(data) - set(order)) if l in data}
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("->", os.path.normpath(OUT))


if __name__ == "__main__":
    main()
