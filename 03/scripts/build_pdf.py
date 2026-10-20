#!/usr/bin/env python3
"""Формує PDF-версію звіту з тієї самої структури, що й DOCX."""
import os
import html as H

from build_report import CONTENT, TITLE, BASE, SHOTS, LOGS, FIG_W_PER_CHAR, FIG_W_MAX, FIG_W_MIN

OUT_PDF = os.path.join(os.path.dirname(BASE), "src", "ouput", "Звіт_ПР3.pdf")

CSS = """
@page { size: A4; margin: 2cm 1.5cm 2cm 3cm;
        @bottom-center { content: counter(page); font: 11pt "Times New Roman"; } }
@page :first { @bottom-center { content: ""; } }
body { font-family: "Times New Roman", serif; font-size: 14pt; line-height: 1.5;
       text-align: justify; hyphens: auto; }
p { margin: 0; text-indent: 1.25cm; }
h1 { font-size: 14pt; text-align: center; text-indent: 0; margin: 12pt 0 8pt;
     page-break-after: avoid; }
h2 { font-size: 14pt; text-indent: 1.25cm; text-align: left; margin: 10pt 0 4pt;
     page-break-after: avoid; }
.title { text-align: center; text-indent: 0; line-height: 1.15; }
.title.big { font-size: 16pt; font-weight: bold; }
.title.b { font-weight: bold; }
.right { text-align: right; text-indent: 0; line-height: 1.15; }
.sp { height: 1.1cm; }
.sp2 { height: 2.4cm; }
.titlepage { page-break-after: always; height: 100%; }
figure { margin: 6pt 0 10pt; text-align: center; page-break-inside: avoid; }
figure img { display: block; margin: 0 auto; }
figcaption { font-size: 12pt; text-align: center; line-height: 1.15; margin-top: 4pt; }
figcaption b { font-weight: bold; }
"""


def esc(s):
    return H.escape(s, quote=False)


def fig_width_cm(key):
    with open(os.path.join(LOGS, key + ".txt")) as f:
        chars = max(len(l) for l in f.read().split("\n"))
    return min(FIG_W_MAX, max(FIG_W_MIN, chars * FIG_W_PER_CHAR))


def build_html():
    t = TITLE
    out = ['<!doctype html><html lang="uk"><head><meta charset="utf-8">',
           '<title>Звіт до практичної роботи 3</title>',
           '<style>%s</style></head><body>' % CSS]

    out.append('<div class="titlepage">')
    out.append('<p class="title">МІНІСТЕРСТВО ОСВІТИ І НАУКИ УКРАЇНИ</p>')
    out.append('<p class="title b">%s</p>' % esc(t["zvo"].upper()))
    out.append('<p class="title">%s</p>' % esc(t["faculty"]))
    out.append('<p class="title">%s</p>' % esc(t["chair"]))
    out.append('<div class="sp2"></div>')
    out.append('<p class="title big">ЗВІТ</p>')
    out.append('<p class="title">до практичної роботи № 3</p>')
    out.append('<p class="title">з дисципліни «%s»</p>' % esc(t["course"]))
    out.append('<p class="title">на тему: «Робота зі СКБД SQLite. Виконання запитів на вибірку даних»</p>')
    out.append('<div class="sp2"></div>')
    out.append('<p class="right">Виконав(ла): студент(ка) групи %s</p>' % esc(t["group"]))
    out.append('<p class="right">спеціальності %s</p>' % esc(t["specialty"]))
    out.append('<p class="right">%s</p>' % esc(t["student"]))
    out.append('<div class="sp"></div>')
    out.append('<p class="right">Перевірив(ла): %s</p>' % esc(t["teacher"]))
    out.append('<div class="sp"></div>')
    out.append('<p class="right">Оцінка: ______________</p>')
    out.append('<div class="sp2"></div>')
    out.append('<p class="title">%s – %s</p>' % (esc(t["city"]), esc(t["year"])))
    out.append('</div>')

    fig_no = 0
    li_no = 0
    for item in CONTENT:
        kind = item[0]
        if kind == "h1":
            out.append("<h1>%s</h1>" % esc(item[1]))
        elif kind == "h2":
            out.append("<h2>%s</h2>" % esc(item[1]))
        elif kind == "p":
            out.append("<p>%s</p>" % esc(item[1]))
        elif kind == "li":
            out.append("<p>— %s</p>" % esc(item[1]))
        elif kind == "num":
            li_no += 1
            out.append("<p>%d.&nbsp;%s</p>" % (li_no, esc(item[1])))
        elif kind == "fig":
            fig_no += 1
            key, cap = item[1], item[2]
            out.append('<figure><img src="%s" style="width:%.2fcm">'
                       '<figcaption><b>Рис. %d.</b> %s</figcaption></figure>'
                       % (os.path.join(SHOTS, key + ".png"), fig_width_cm(key),
                          fig_no, esc(cap)))
    out.append("</body></html>")
    return "\n".join(out), fig_no


def main():
    import subprocess
    import shutil
    doc, n = build_html()
    tmp = os.path.join(os.environ.get('TMPDIR', '/tmp'), 'report_pr3.html')
    with open(tmp, "w") as f:
        f.write(doc)
    exe = shutil.which("weasyprint")
    if not exe:
        raise SystemExit("weasyprint не знайдено; HTML збережено: " + tmp)
    subprocess.run([exe, tmp, OUT_PDF], check=True)
    print("PDF збережено: %s (рисунків: %d)" % (OUT_PDF, n))


if __name__ == "__main__":
    main()
