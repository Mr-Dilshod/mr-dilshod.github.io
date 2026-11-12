# Ⓓ English lessons site (mr-dilshod.github.io)

- Lessons are `lesson-N.html` (audio in `lesson-N/`). Each file starts itself with `EWD.start({number, title: "Unit: Lesson", meta: "Own It! 1 · Unit · Student's Book p. X", chips: [...]})`.
- `lessons.json` is generated, never edited by hand: `.github/workflows/lessons.yml` runs `tools/build_lessons.py` on every push that touches a lesson file or `worksheets.json`.
- The blog page https://sajqaliruizamin.blogspot.com/p/english.html reads `lessons.json`, so a pushed lesson appears there automatically.
- Worksheet links (Bilimlink) go in `worksheets.json` as `"N": "https://bilimlink.uz/share/..."`. When a new lesson or worksheet arrives, add its entry there in the same push.
- Worksheets are gated: the link is NOT put in `lessons.json` or on the blog. The lesson's end screen (engine `worksheetBox`) fetches `worksheets.json` and shows "Open the worksheet" only after the homework photo is sent. Never publish worksheet links anywhere else.
- The unit name is the part of `title` before the colon, so keep titles as `"Unit 1: Vocabulary"`-style.
