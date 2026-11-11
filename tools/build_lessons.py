"""Build lessons.json from every lesson-N.html in the site.

Each lesson file starts itself with EWD.start({...}); that object already holds
the lesson number, title ("Unit name: Lesson name"), book page and topic chips.
Worksheet links live in worksheets.json ({"1": "https://...", ...}).

The Ⓓ English page on the blog reads lessons.json, so a new lesson appears there
as soon as its file is pushed. Run by .github/workflows/lessons.yml on every push.
"""
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read_lesson(path):
    text = open(path, encoding="utf-8").read()
    start = text.rfind("EWD.start({")
    if start < 0:
        return None
    obj, _ = json.JSONDecoder().raw_decode(text[start + len("EWD.start("):])
    title = obj.get("title", "")
    unit, _, name = title.partition(":")
    if not name:
        unit, name = "Lessons", title
    meta = obj.get("meta", "")
    page = next((p.strip() for p in meta.split("·") if "p." in p), "")
    return {
        "number": obj.get("number"),
        "unit": unit.strip(),
        "title": name.strip(),
        "page": page,
        "chips": obj.get("chips", []),
        "url": "https://mr-dilshod.github.io/" + os.path.basename(path),
    }


def main():
    ws_path = os.path.join(ROOT, "worksheets.json")
    worksheets = json.load(open(ws_path, encoding="utf-8")) if os.path.exists(ws_path) else {}
    lessons = []
    for path in glob.glob(os.path.join(ROOT, "lesson-*.html")):
        if not re.fullmatch(r"lesson-\d+\.html", os.path.basename(path)):
            continue
        lesson = read_lesson(path)
        if lesson:
            lesson["worksheet"] = worksheets.get(str(lesson["number"]), "")
            lessons.append(lesson)
    lessons.sort(key=lambda l: l["number"] or 0)

    units = []
    for lesson in lessons:
        if not units or units[-1]["name"] != lesson["unit"]:
            units.append({"name": lesson["unit"], "lessons": []})
        units[-1]["lessons"].append({k: v for k, v in lesson.items() if k != "unit"})

    out = {"book": "Own It! 1", "units": units}
    with open(os.path.join(ROOT, "lessons.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"lessons.json: {len(lessons)} lessons in {len(units)} unit(s)")


if __name__ == "__main__":
    main()
