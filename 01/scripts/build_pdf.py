#!/usr/bin/env python3
"""Формує PDF-версію звіту з тієї самої структури, що й DOCX (через weasyprint)."""
import os
import html as H
import shutil
import subprocess

from build_report import CONTENT, TITLE, THEME, BASE, SHOTS, OUT_DIR, fig_width_cm

OUT_PDF = os.path.join(OUT_DIR, "Звіт_ПР1.pdf")
CSS = """
@page { size: A4; margin: 2cm 1.5cm 2cm 3cm;
        @bottom-center { content: counter(page); font: 11pt "Times New Roman"; } }
@page :first { @bottom-center { content: ""; } }
body { font-family: "Times New Roman", serif; font-size: 14pt; line-height: 1.5; text-align: justify; }
p { margin: 0; text-indent: 1.25cm; }
h1 { font-size: 14pt; text-align: center; margin: 12pt 0 8pt; page-break-after: avoid; }
h2 { font-size: 14pt; text-indent: 1.25cm; margin: 10pt 0 4pt; page-break-after: avoid; }
.title { text-align: center; text-indent: 0; line-height: 1.15; }
.title.big { font-size: 16pt; font-weight: bold; }
.title.b { font-weight: bold; }
.right { text-align: right; text-indent: 0; line-height: 1.15; }
.sp { height: 1.1cm; } .sp2 { height: 2.4cm; }
.titlepage { page-break-after: always; height: 100%; }
figure { margin: 6pt 0 10pt; text-align: center; page-break-inside: avoid; }
figure img { display: block; margin: 0 auto; }
figcaption { font-size: 12pt; text-align: center; line-height: 1.15; margin-top: 4pt; }
"""


def esc(s):
    return H.escape(s, quote=False)


def build_html():
    t = TITLE
    o = ['<!doctype html><html lang="uk"><head><meta charset="utf-8"><title>Звіт ПР1</title>',
         '<style>%s</style></head><body><div class="titlepage">' % CSS,
         '<p class="title">МІНІСТЕРСТВО ОСВІТИ І НАУКИ УКРАЇНИ</p>',
         '<p class="title b">%s</p>' % esc(t["zvo"].upper()),
         '<p class="title">%s</p>' % esc(t["faculty"]),
         '<p class="title">%s</p>' % esc(t["chair"]),
         '<div class="sp2"></div><p class="title big">ЗВІТ</p>',
         '<p class="title">до практичної роботи № 1</p>',
         '<p class="title">з дисципліни «%s»</p>' % esc(t["course"]),
         '<p class="title">на тему: «%s»</p>' % esc(THEME),
         '<div class="sp2"></div>',
         '<p class="right">Виконав(ла): студент(ка) групи %s</p>' % esc(t["group"]),
         '<p class="right">спеціальності %s</p>' % esc(t["specialty"]),
         '<p class="right">%s</p>' % esc(t["student"]),
         '<div class="sp"></div><p class="right">Перевірив(ла): %s</p>' % esc(t["teacher"]),
         '<div class="sp"></div><p class="right">Оцінка: ______________</p>',
         '<div class="sp2"></div><p class="title">%s – %s</p></div>' % (esc(t["city"]), esc(t["year"]))]
    fig_no = li_no = 0
    for item in CONTENT:
        k = item[0]
        if k == "h1":
            o.append("<h1>%s</h1>" % esc(item[1]))
        elif k == "h2":
            o.append("<h2>%s</h2>" % esc(item[1]))
        elif k == "p":
            o.append("<p>%s</p>" % esc(item[1]))
        elif k == "num":
            li_no += 1
            o.append("<p>%d.&nbsp;%s</p>" % (li_no, esc(item[1])))
        elif k == "fig":
            fig_no += 1
            o.append('<figure><img src="%s" style="width:%.2fcm"><figcaption><b>Рис. %d.</b> %s'
                     '</figcaption></figure>' % (os.path.join(SHOTS, item[1] + ".png"),
                                                 fig_width_cm(item[1]), fig_no, esc(item[2])))
    o.append("</body></html>")
    return "\n".join(o), fig_no


def main():
    doc, n = build_html()
    tmp = os.path.join(BASE, "scripts", "report.html")
    with open(tmp, "w") as f:
        f.write(doc)
    subprocess.run([shutil.which("weasyprint"), tmp, OUT_PDF], check=True)
    os.remove(tmp)
    print("PDF збережено: %s (рисунків: %d)" % (OUT_PDF, n))


if __name__ == "__main__":
    main()
