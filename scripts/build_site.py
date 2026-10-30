#!/usr/bin/env python3
"""Build the public bilingual v1.1 site from the canonical manuscripts.

Uses only the Python standard library. Verified PDFs are preserved by default;
--pdf explicitly rebuilds them with an already installed Chrome/Chromium.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / "downloads"
LOCALES = {"zh": ("read", "zh-Hant"), "en": ("read-en", "en")}
SOURCES = {"zh": "handbook.md", "en": "handbook-en.md"}
SITE_URL = "https://farceurliu.github.io/ai-butler-handbook/"


def slugify(title: str, used: set[str]) -> str:
    # Same stable heading algorithm as build_site, without importing its Pillow
    # social-preview dependency into this otherwise standard-library-only build.
    value = re.sub(r"[^\w\u4e00-\u9fff]+", "-", title.strip().lower()).strip("-") or "section"
    base, suffix = value, 2
    while value in used:
        value, suffix = f"{base}-{suffix}", suffix + 1
    used.add(value)
    return value


def safe_url(value: str, *, image: bool = False) -> str:
    """Keep Markdown links inert unless clicked; require local image assets."""
    parsed = urlsplit(value)
    if parsed.scheme and parsed.scheme not in ("https", "http", "mailto"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")
    if image and (parsed.scheme or parsed.netloc):
        raise ValueError("Images must be local; no remote resource fetching")
    if not parsed.scheme:
        target = (ROOT / unquote(parsed.path)).resolve()
        if not target.is_relative_to(ROOT):
            raise ValueError("Local links must stay inside this repository")
    return html.escape(value, quote=True)


def inline(value: str) -> str:
    # Tokenize code first so examples cannot accidentally become markup.
    parts = re.split(r"(`[^`]+`|!?\[[^\]]*\]\([^\s)]+\))", value)
    out = []
    for part in parts:
        if part.startswith("`") and part.endswith("`"):
            out.append(f"<code>{html.escape(part[1:-1])}</code>")
            continue
        link = re.fullmatch(r"(!?)\[([^\]]*)\]\(([^\s)]+)\)", part)
        if link:
            image, label, url = link.groups()
            if image:
                out.append(f'<img src="{safe_url(url, image=True)}" alt="{html.escape(label, quote=True)}" loading="eager">')
            else:
                out.append(f'<a href="{safe_url(url)}">{html.escape(label)}</a>')
        else:
            escaped = html.escape(part)
            escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
            out.append(escaped)
    return "".join(out)


def table_cells(line: str) -> list[str]:
    return [x.strip().replace(r"\|", "|") for x in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


def markdown_to_html(markdown: str, locale: str = "zh") -> tuple[str, list[tuple[str, str]]]:
    out, toc, used = [], [], set()
    lines = markdown.splitlines()
    i, title_count = 0, 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        fence = re.match(r"^(`{3,}|~{3,})(.*)$", line)
        if fence:
            code, i = [], i + 1
            while i < len(lines) and not lines[i].strip().startswith(fence[1]):
                code.append(lines[i])
                i += 1
            if i == len(lines):
                raise ValueError("Unclosed Markdown code fence")
            out.append('<pre tabindex="0"><code>' + html.escape("\n".join(code)) + '</code></pre>')
            i += 1
            continue
        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            level, text = len(heading[1]), heading[2]
            explicit = re.search(r"\s+\{#([\w-]+)\}$", text)
            if explicit:
                text, anchor = text[:explicit.start()], explicit[1]
                if anchor in used:
                    raise ValueError(f"Duplicate heading ID: {anchor}")
                used.add(anchor)
            else:
                anchor = slugify(text, used)
            if level == 1:
                title_count += 1
            if level == 2 and re.match(r"^(?:\d+[.．、 ]|附錄|Appendix\b)", text, re.I):
                toc.append((text, anchor))
            out.append(f'<h{level} id="{anchor}">{inline(text)}</h{level}>')
            i += 1
            continue
        if line.startswith("|") and i + 1 < len(lines):
            separator = table_cells(lines[i + 1])
            if separator and all(re.fullmatch(r":?-{3,}:?", cell) for cell in separator):
                rows = [table_cells(line)]
                i += 2
                while i < len(lines) and lines[i].strip().startswith("|"):
                    rows.append(table_cells(lines[i]))
                    i += 1
                count = len(rows[0])
                if any(len(row) != count for row in rows):
                    raise ValueError("Table rows must have the same number of columns")
                label = "比較表，可左右捲動" if locale == "zh" else "Comparison table; scroll horizontally if needed"
                out.append(f'<div class="table-wrap" tabindex="0" role="region" aria-label="{label}"><table><thead><tr>')
                out.append("".join(f'<th scope="col">{inline(x)}</th>' for x in rows[0]))
                out.append("</tr></thead><tbody>")
                out.extend("<tr>" + "".join(f"<td>{inline(x)}</td>" for x in row) + "</tr>" for row in rows[1:])
                out.append("</tbody></table></div>")
                continue
        image = re.fullmatch(r"!\[([^\]]*)\]\(([^\s)]+)\)", line)
        if image:
            label = "Open the original image (new tab)" if locale == "en" else "開啟原圖（新分頁）"
            url = safe_url(image[2], image=True)
            out.append(f'<figure><a class="figure-link" href="{url}" target="_blank" rel="noopener noreferrer">{inline(line)}</a>'
                       f'<figcaption>{html.escape(image[1])}</figcaption>'
                       f'<a class="figure-zoom" href="{url}" target="_blank" rel="noopener noreferrer">{label}</a></figure>')
            i += 1
            continue
        item = re.match(r"^(?:([-*+])\s+|(\d+)[.)]\s+)(.+)$", line)
        if item:
            ordered = bool(item[2])
            tag = "ol" if ordered else "ul"
            start = f' start="{int(item[2])}"' if ordered else ""
            out.append(f"<{tag}{start}>")
            while i < len(lines):
                item = re.match(r"^(?:([-*+])\s+|(\d+)[.)]\s+)(.+)$", lines[i].strip())
                if not item or bool(item[2]) != ordered:
                    break
                out.append(f"<li>{inline(item[3])}</li>")
                i += 1
            out.append(f"</{tag}>")
            continue
        if line.startswith(">"):
            quotes = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quotes.append(lines[i].strip()[1:].strip())
                i += 1
            out.append("<blockquote>" + "<br>".join(inline(x) for x in quotes) + "</blockquote>")
            continue
        if re.fullmatch(r"(?:-{3,}|\*{3,}|_{3,})", line):
            # Main chapter headings already carry a separator. Keep other
            # thematic breaks, but do not render two rules at chapter joins.
            following = next((x.strip() for x in lines[i + 1:] if x.strip()), "")
            if not re.match(r"^##\s+", following):
                out.append("<hr>")
            i += 1
            continue
        # Give recurring study cues a consistent role without adding headings
        # to the manuscript outline or treating every short paragraph as a label.
        study = re.fullmatch(
            r"(?:\*\*)?(本章學習目標：|本章練習與自我檢查：|"
            r"What you will learn(?: in this chapter)?:|Learning goals for this chapter:|"
            r"(?:Chapter )?practice and self-check:|Practice & self-check:|"
            r"Chapter exercises and self-check:|Chapter review:|Practice checklist:|"
            r"Chapter \d+ exercises:)(?:\*\*)?(.*)", line, re.I)
        if study:
            out.append(f'<p class="study-label"><strong>{html.escape(study[1])}</strong>{inline(study[2].strip())}</p>')
        else:
            # Keep deliberate paragraph boundaries, as build_site does.
            out.append(f"<p>{inline(line)}</p>")
        i += 1
    if title_count != 1:
        raise ValueError(f"Expected one document title, found {title_count}")
    if not toc:
        raise ValueError("No main chapters found (use numbered H2 headings)")
    return "\n".join(out), toc


CSS = r"""
:root{color-scheme:light;--ink:#172b38;--muted:#53646f;--line:#d9e0e4;--accent:#245f8e;--paper:#fff}
*{box-sizing:border-box}html{scroll-padding-top:24px}body{margin:0;background:#f4f6f8;color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"PingFang TC","Microsoft JhengHei",Arial,sans-serif;line-height:1.85}a{color:var(--accent);text-underline-offset:3px;overflow-wrap:anywhere}a:hover{text-decoration-thickness:2px}a:focus-visible,summary:focus-visible,pre:focus-visible,.table-wrap:focus-visible{outline:3px solid #c57815;outline-offset:4px}.skip{position:absolute;left:12px;top:-100px;background:#fff;padding:8px}.skip:focus{top:8px;z-index:10}
.site-header{max-width:1320px;margin:auto;padding:20px;display:flex;align-items:center;justify-content:space-between;gap:20px;border-bottom:1px solid var(--line)}.brand{font-weight:700;text-decoration:none;color:var(--ink)}.header-links{display:flex;gap:18px;flex-wrap:wrap;font-size:14px}.reader-layout{width:min(1320px,calc(100% - 40px));margin:auto;display:grid;grid-template-columns:235px minmax(0,1fr);gap:32px;align-items:start;padding:30px 0 60px}.toc{position:sticky;top:24px;max-height:calc(100vh - 48px);overflow:auto;padding:18px 14px;background:var(--paper);border:1px solid var(--line);border-radius:8px}.toc strong{display:block;margin-bottom:8px}.toc a,.mobile-toc a{display:block;text-decoration:none;font-size:14px;line-height:1.5;padding:7px 0;color:var(--muted)}.toc a:hover,.mobile-toc a:hover{color:var(--accent)}.mobile-toc{display:none}.book{min-width:0;background:var(--paper);border:1px solid var(--line);border-radius:8px;padding:40px clamp(24px,4.5vw,66px);overflow-wrap:anywhere}.edition{color:var(--muted);font-size:13px;margin-top:0}.book h1{font-size:clamp(30px,3.8vw,46px);line-height:1.3;margin:12px 0 28px;letter-spacing:0}.book h2{font-size:26px;line-height:1.5;margin:48px 0 22px;padding-top:24px;border-top:1px solid var(--line)}.book h3{font-size:21px;line-height:1.5;margin:32px 0 14px}.book h4,.book h5,.book h6{font-size:18px;line-height:1.5;margin:24px 0 12px}.book p{margin:0 0 18px}.book li{margin:6px 0}.book ul,.book ol{padding-left:1.65em;margin:14px 0 22px}blockquote{margin:22px 0;padding:14px 18px;border-left:4px solid var(--accent);background:#f1f6fa;color:#344e61}pre{white-space:pre-wrap;overflow-wrap:anywhere;word-break:break-word;background:#f1f4f7;border:1px solid var(--line);border-radius:5px;padding:18px;font-size:14px;line-height:1.75;tab-size:2}code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"PingFang TC",monospace;font-size:.9em}p code,li code,td code{background:#edf3f7;padding:1px 4px;border-radius:3px}.table-wrap{max-width:100%;overflow-x:auto;margin:20px 0 28px}table{border-collapse:collapse;min-width:100%;font-size:14px;line-height:1.65}th,td{border:1px solid var(--line);padding:10px 12px;text-align:left;vertical-align:top;min-width:95px}th{background:#edf3f7}figure{margin:28px 0}img{display:block;max-width:100%;height:auto;margin:auto}figcaption{font-size:13px;color:var(--muted);margin-top:10px;line-height:1.6}hr{border:0;border-top:1px solid var(--line);margin:28px 0}.book-footer{border-top:1px solid var(--line);margin-top:40px;padding-top:20px;font-size:14px;display:flex;gap:20px;flex-wrap:wrap}
/* A book-like display face; the instructions, examples and navigation remain
   system sans. No downloaded fonts or additional asset requests. */
.book{font-size:17px;line-height:1.85}
.book article,.book>.edition,.book-footer{max-width:44rem;margin-left:auto;margin-right:auto}
.book h1,.book h2{font-family:"Iowan Old Style","Songti TC","Noto Serif CJK TC",Georgia,serif;font-weight:600}
.book h1{font-size:44px;line-height:1.45;text-wrap:balance}
.book h2{font-size:29px;line-height:1.55;margin-top:56px}
.book h3{font-size:22px;font-weight:650;margin-top:36px}
.book h4,.book h5,.book h6{font-size:18px;font-weight:650}
.book strong{font-weight:700}
.book .study-label{margin-top:30px;margin-bottom:10px;font-size:16px}
.study-label strong{display:block;margin-bottom:5px;color:var(--ink)}
.study-label+ul,.study-label+ol{margin-top:6px}
pre{font-size:14.5px;line-height:1.75}pre code{font-size:1em}
table{font-size:15px}figcaption{font-size:14px;line-height:1.7}
.edition a{color:inherit;text-decoration:none}.edition a:hover{text-decoration:underline}
.figure-link{display:block}.figure-zoom{display:inline-block;font-size:15px;margin-top:6px;padding:8px 0}
.reader-layout{grid-template-columns:260px minmax(0,1fr)}
/* Keep the last navigation item visible at the initial header/layout offset,
   before the sticky sidebar reaches its 24px top position. Screen-only: PDF
   layout and the separate mobile contents control are unaffected. */
@media screen and (min-width:861px){.toc{max-height:calc(100vh - 130px)}}
.toc-group+.toc-group{margin-top:22px;padding-top:16px;border-top:1px solid var(--line)}
.toc-group-title{font-size:14px;font-weight:700;line-height:1.5;margin:0 0 8px;color:var(--ink)}
.toc-group ul{list-style:none;margin:0;padding:0}.toc-group li{margin:0}
.toc .toc-link,.mobile-toc .toc-link{display:grid;grid-template-columns:28px minmax(0,1fr);align-items:start;gap:9px;padding:9px 4px;line-height:1.6;border-radius:4px}
.toc-link .chapter-number{font-size:12.5px;font-weight:600;line-height:24px;text-align:center;background:#edf3f7;color:#245f8e;border-radius:4px}
.toc .toc-link:hover,.mobile-toc .toc-link:hover{background:#f3f6fa;color:#174d75}
.toc .toc-link:active,.mobile-toc .toc-link:active{background:#e4eef6;color:#153e63}
.toc .toc-link[aria-current="location"],.mobile-toc .toc-link[aria-current="location"]{background:#e4eef6;color:#153e63;font-weight:700;text-decoration:underline;text-underline-offset:4px}
@media(prefers-reduced-motion:no-preference){.toc-link,.header-links a{transition:background-color .12s ease,color .12s ease}}
.mobile-toc[open] summary{margin-bottom:12px}.mobile-toc .toc-link{font-size:15px}
@media screen and (max-width:480px){html[lang="en"] .table-wrap::before{content:"Swipe horizontally to see all columns.";display:block;font-size:14px;line-height:1.6;margin-bottom:8px;color:var(--muted)}html[lang="en"] table{min-width:30rem}html[lang="en"] th,html[lang="en"] td{min-width:10rem;overflow-wrap:normal;word-break:normal;hyphens:none}}
@media(max-width:860px){.site-header{align-items:flex-start}.reader-layout{display:block;width:min(760px,calc(100% - 28px));padding-top:18px}.toc{display:none}.mobile-toc{display:block;background:white;border:1px solid var(--line);border-radius:6px;padding:12px 16px;margin-bottom:16px}.mobile-toc summary{cursor:pointer;font-weight:600}.mobile-toc nav{padding-top:10px}.book{padding:28px 22px}.book h1{font-size:34px}.book h2{font-size:26px}.book h3{font-size:21px}.site-header{padding:16px 14px}.header-links{gap:8px 16px}.brand{font-size:15px}}
@media(max-width:400px){.site-header{display:block}.header-links{margin-top:10px}.book{padding:24px 17px}.book h1{font-size:31px}.book h2{font-size:25px}pre{font-size:14px;padding:13px}}
@page{size:A4;margin:18mm 17mm 20mm;@bottom-left{content:"AI Work Assistant Handbook · v1.1";font:8pt Arial;color:#53646f}@bottom-right{content:counter(page) " / " counter(pages);font:8pt Arial;color:#53646f}}
@media print{html{scroll-padding:0}body{background:white;font-size:10pt;line-height:1.65;-webkit-print-color-adjust:exact;print-color-adjust:exact}.site-header,.toc,.mobile-toc,.skip,.book-footer{display:none!important}.reader-layout{display:block;width:auto;margin:0;padding:0}.book{border:0;border-radius:0;padding:0;overflow-wrap:anywhere}.edition{font-size:8pt;margin-bottom:10pt}.book h1{font-size:25pt;line-height:1.3;margin:0 0 18pt}.book h2{font-size:17pt;line-height:1.4;margin:26pt 0 12pt;padding-top:12pt}.book h3{font-size:13pt;line-height:1.4;margin:18pt 0 9pt}.book h4,.book h5,.book h6{font-size:11pt;margin:14pt 0 7pt}h1,h2,h3,h4,h5,h6{break-after:avoid-page;page-break-after:avoid}p,li{orphans:3;widows:3}.book p{margin:0 0 9pt}.book ul,.book ol{margin:7pt 0 12pt}.book li{margin:3pt 0}pre{font-size:8.4pt;line-height:1.55;padding:9pt;white-space:pre-wrap;overflow:visible;break-inside:auto;box-decoration-break:clone}pre code{font-size:1em}blockquote{padding:8pt 10pt;margin:12pt 0;break-inside:auto}.table-wrap{overflow:visible;margin:12pt 0;break-inside:auto}table{width:100%;table-layout:fixed;min-width:0;font-size:8pt;line-height:1.55}thead{display:table-header-group}th,td{min-width:0;padding:6pt;overflow-wrap:anywhere;word-break:normal}tr{break-inside:avoid-page}figure{break-inside:avoid-page;margin:14pt 0}figure img{max-height:210mm;width:auto;max-width:100%}figcaption{font-size:8pt;margin-top:6pt}a{color:inherit;text-decoration:underline}}
@media print{.book{font-size:10.5pt;line-height:1.7}.book article,.edition{max-width:none}.book .study-label{font-size:10pt;margin:14pt 0 6pt;break-after:avoid-page}.study-label strong{margin-bottom:3pt}.book h1,.book h2{font-weight:600}.book h3,.book h4{font-weight:700}.figure-zoom{display:none}}
"""


def chapter_navigation(chapters: list[tuple[str, str]], en: bool) -> str:
    labels = (["Start here", "Assign, practise and verify", "Everyday methods and safety",
               "Skills, Agents and teams", "Quick reference and closing", "Optional appendices"]
              if en else ["從這裡開始", "交辦、練習與驗收", "常用方法與安全",
                          "Skill、Agent 與團隊", "速查與結語", "附錄選讀"])
    groups: list[list[str]] = [[] for _ in labels]
    for title, anchor in chapters:
        numbered = re.match(r"^(\d+)\.\s*(.+)$", title)
        appendix = re.match(r"^(?:附錄|Appendix)\s+([A-Z])[.:]\s*(.+)$", title)
        if numbered:
            number, text = numbered.groups()
            group = next((i for i, upper in enumerate((4, 11, 17, 20, 22)) if int(number) <= upper), 4)
        elif appendix:
            number, text = appendix.groups()
            group = 5
        else:
            number, text, group = "", title, 5
        groups[group].append(f'<li><a class="toc-link" href="#{anchor}" aria-label="{html.escape(title, quote=True)}">'
                             f'<span class="chapter-number" aria-hidden="true">{number}</span>'
                             f'<span>{html.escape(text)}</span></a></li>')
    return "\n".join(f'<section class="toc-group" aria-label="{label}"><p class="toc-group-title">{label}</p>'
                     f'<ul>{"".join(items)}</ul></section>' for label, items in zip(labels, groups) if items)


def public_metadata(locale: str, name: str) -> str:
    en = locale == "en"
    title = "AI Work Assistant Handbook" if en else "從零開始養成我的 AI 管家"
    description = ("Start with meeting notes. Learn to assign, verify and reuse AI work."
                   if en else "從會議筆記開始，練習交辦、核對，再把好用的方法留下來。")
    image = SITE_URL + f"assets/social-preview-{'en' if en else 'zh'}.png?v=20261029-v11"
    url = SITE_URL + name
    zh_alternate, en_alternate = (("read.html", "read-en.html") if name.startswith("read")
                                  else ("index.html", "english.html"))
    return (f'<meta name="description" content="{description}">'
            f'<meta name="robots" content="index,follow">'
            f'<link rel="canonical" href="{url}">'
            f'<link rel="alternate" hreflang="zh-Hant" href="{SITE_URL}{zh_alternate}">'
            f'<link rel="alternate" hreflang="en" href="{SITE_URL}{en_alternate}">'
            f'<meta property="og:title" content="{title}">'
            f'<meta property="og:description" content="{description}">'
            f'<meta property="og:type" content="website">'
            f'<meta property="og:url" content="{url}">'
            f'<meta property="og:image" content="{image}">'
            f'<meta property="og:image:width" content="1200">'
            f'<meta property="og:image:height" content="630">'
            f'<meta name="twitter:card" content="summary_large_image">'
            f'<meta name="twitter:image" content="{image}">'
            '<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">')


def page(markdown: str, locale: str) -> str:
    stem, lang = LOCALES[locale]
    body, chapters = markdown_to_html(markdown, locale)
    title = re.search(r"^#\s+(.+)$", markdown, re.M)[1]
    en = locale == "en"
    other, language = ("read.html", "繁體中文") if en else ("read-en.html", "English")
    pdf = f"downloads/ai-butler-handbook_v1.1_{locale}.pdf"
    contents, download = ("Contents", "Download PDF") if en else ("章節目錄", "下載 PDF")
    nav = chapter_navigation(chapters, en)
    edition = "Free Public Edition v1.1" if en else "免費公開版 v1.1"
    linkedin = "https://www.linkedin.com/in/farceur-liu-636864b5/"
    home = "english.html" if en else "index.html"
    home_label = "Home" if en else "首頁"
    author_label = "Author on LinkedIn" if en else "作者 LinkedIn"
    contact_label = "Email the author" if en else "Email 聯繫"
    skip, top = ("Skip to content", "Back to top") if en else ("跳到正文", "回到開頭")
    brand = "AI Work Assistant Handbook" if en else "從零開始養成我的 AI 管家"
    return f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
{public_metadata(locale, stem + ".html")}<title>{html.escape(title)}</title><style>{CSS}</style></head>
<body id="top"><a class="skip" href="#main">{skip}</a>
<header class="site-header"><a class="brand" href="{home}">{brand}</a><nav class="header-links" aria-label="{'Reading navigation' if en else '閱讀導覽'}"><a href="{home}">{home_label}</a><a href="{other}" lang="{'zh-Hant' if en else 'en'}">{language}</a><a href="{pdf}" download>{download}</a></nav></header>
<div class="reader-layout"><aside class="toc"><nav aria-label="{contents}"><strong>{contents}</strong>{nav}</nav></aside>
<details class="mobile-toc"><summary>{contents}</summary><nav aria-label="{'Mobile contents' if en else '手機章節目錄'}">{nav}</nav></details>
<main id="main" class="book"><p class="edition">{edition} · <a href="{linkedin}" rel="noopener noreferrer">Farceur Liu</a></p><article>{body}</article>
<footer class="book-footer"><a href="{pdf}" download>{download}</a><a href="{other}">{language}</a><a href="{linkedin}" rel="noopener noreferrer">{author_label}</a><a href="mailto:farceur2021@gmail.com">{contact_label}</a><a href="#top">{top}</a></footer></main></div>
<script src="assets/reader.js" defer></script></body></html>'''


HOME_CSS = r"""
body{background:#fbfcff;color:#101b30;font-size:18px;--accent:#1855ef;--muted:#526079;--line:#cfd9e9;--paper:#fffefc;--ink-blue:#123fb6;--night:#102b6a;--on-night:#d9e5ff;--motion-fast:.16s}
.site-header{max-width:1280px;padding:20px 40px;border:0}.brand{color:var(--accent);font-size:21px}.header-links{align-items:center;font-size:15px;gap:24px}.header-links a{text-decoration:none;font-weight:600}
.home-main{margin:auto}.home-scene{position:relative;background:linear-gradient(115deg,#e8f0ff 0%,#f7faff 55%,#f1f4f5 100%);padding:0 40px 72px;isolation:isolate}.home-scene:before{content:"";position:absolute;inset:0;z-index:-1;background-image:linear-gradient(#1656e908 1px,transparent 1px),linear-gradient(90deg,#1656e908 1px,transparent 1px);background-size:28px 28px;mask-image:linear-gradient(100deg,#000,transparent 70%)}.home-scene:after{content:"";position:absolute;inset:440px 0 0;z-index:-1;background:linear-gradient(177deg,transparent 0 8%,#ece5da55 8.3%,#f2ede68c 65%,#f9f7f2 100%)}
.hero-composition{position:relative;max-width:1140px;margin:auto;display:grid;grid-template-columns:1.2fr .8fr;gap:38px;align-items:center;min-height:575px;padding:22px 0 62px}
.home-hero{position:relative;z-index:2;padding:18px 0 24px}.home-hero h1{margin:0 0 22px;font-weight:800;line-height:1.25;letter-spacing:-.04em;text-wrap:balance}.home-hero h1 span{display:block;font-size:clamp(30px,3.5vw,46px);line-height:1.45}.home-hero h1 strong{display:block;font-size:clamp(65px,7.5vw,96px);line-height:1.22;font-weight:800;color:var(--accent)}.home-hero .lead{font-size:21px;line-height:1.85;margin:0 0 10px;max-width:29em}.home-hero .intro{font-size:18px;line-height:1.85;margin:0 0 28px;max-width:31em;color:var(--muted)}.home-hero .edition{font-size:14px;font-weight:600;margin:17px 0 0;color:var(--muted)}
.home-actions{display:flex;flex-wrap:wrap;gap:14px}.home-button{display:inline-flex;align-items:center;justify-content:center;gap:20px;min-height:52px;padding:12px 25px;border:1px solid #b8cbee;border-radius:6px;text-decoration:none;font-size:18px;font-weight:650;background:var(--paper);color:#12203a}.home-button svg{width:20px;height:20px;flex-shrink:0}.home-button.primary{background:var(--accent);border-color:var(--accent);color:white}.home-button:active{background:#dce7ff}.home-button.primary:active{background:var(--ink-blue)}
.book-showcase{position:relative;z-index:1;margin:0;min-width:0}.book-showcase img{width:100%;height:482px;object-fit:contain;filter:drop-shadow(13px 18px 15px #1d335c20)}.book-link{display:block;position:relative;color:var(--accent);text-decoration:none;border-radius:8px}.book-caption{position:absolute;bottom:-12px;left:50%;transform:translateX(-50%);display:inline-flex;gap:12px;align-items:center;white-space:nowrap;font-size:15px;font-weight:650;background:var(--paper);padding:8px 16px;border:1px solid #c1d2f4;border-radius:999px}.book-caption svg{width:17px;height:17px}.book-link:active .book-caption{background:#dce7ff}
.book-ribbon{position:absolute;left:0;bottom:-2px;width:100%;height:100px;overflow:visible;pointer-events:none;z-index:3}.book-ribbon path{fill:none;stroke:var(--accent);stroke-width:2.6;vector-effect:non-scaling-stroke}
.worksheet{position:relative;max-width:1140px;margin:0 auto;padding:34px 48px 28px;background:var(--paper);box-shadow:0 12px 38px #304b6b14;border:1px solid #e4e7ed;transform:rotate(-.6deg)}.worksheet>*{transform:rotate(.6deg)}.worksheet h2{font-size:clamp(25px,3vw,36px);line-height:1.45;letter-spacing:-.03em;margin:0 0 23px;font-weight:750;scroll-margin-top:30px}.section-kicker{display:block;color:var(--accent);font-size:15px;font-weight:700;letter-spacing:.03em;margin:0 0 10px}.sheet-head,.sheet-row{display:grid;grid-template-columns:1.25fr 1fr .9fr;gap:30px}.sheet-head{color:var(--accent);font-weight:700;font-size:17px;border-bottom:1px solid #aebed6;padding-bottom:13px}.sheet-row{position:relative;isolation:isolate;padding:22px 0;border-bottom:1px solid #dce3ee;font-size:18px;line-height:1.8}.sheet-row p{margin:0}.sheet-row .sheet-cell+.sheet-cell{border-left:1px solid #dce3ee;padding-left:24px}.sheet-mobile-label{display:none}.sheet-check{font-weight:650}.sheet-check mark{background:linear-gradient(transparent 18%,#ffdf9f 18% 85%,transparent 85%);color:#283345;padding:3px 3px;box-decoration-break:clone}.sheet-confirmed{text-decoration:underline;text-decoration-color:var(--accent);text-decoration-thickness:2px;text-underline-offset:7px}.sheet-note{font-size:15px;line-height:1.8;color:var(--muted);margin:18px 0 0}.sheet-note a{white-space:nowrap}
.home-section,.home-route{max-width:1140px;margin:0 auto;padding:80px 0}.home-section h2,.home-route h2{font-size:clamp(30px,3vw,40px);line-height:1.5;letter-spacing:-.025em;margin:0 0 20px;text-wrap:balance}.section-intro{max-width:43em;margin:0 0 36px;color:var(--muted);line-height:1.85}.home-section p{line-height:1.85}
.reader-questions{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:36px;margin:40px 0 0}.reader-questions>div{border-top:2px solid var(--accent);padding:24px 0 0}.reader-questions dt{font-size:23px;font-weight:700;line-height:1.65;margin:0 0 12px}.reader-questions dd{margin:0;color:var(--muted);line-height:1.85}
.home-route{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:80px;padding-top:10px;padding-bottom:88px}.route-intro{padding-top:28px}.route-intro h2{max-width:10em}.route-intro>p{margin:0;color:var(--muted);line-height:1.85}.learning-route{list-style:none;counter-reset:route;margin:0;padding:0}.learning-route li{counter-increment:route;display:grid;grid-template-columns:48px minmax(0,1fr);gap:20px;border-top:1px solid var(--line);padding:26px 0}.learning-route li:before{content:counter(route,decimal-leading-zero);font:500 28px/1.6 ui-monospace,monospace;color:var(--accent)}.learning-route h3{font-size:22px;line-height:1.55;margin:0 0 8px}.learning-route p{margin:0;color:var(--muted);line-height:1.85}.route-start{margin:20px 0 0}.route-start a{display:inline-block;min-height:44px;padding:8px 0;font-size:17px;font-weight:650}
.outcomes-band{background:var(--night);color:white}.outcomes-band .home-section{padding-top:72px;padding-bottom:76px}.outcomes-band h2{max-width:18em;font-size:42px}.outcomes-band .section-intro{color:var(--on-night);max-width:40em}.takeaways{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;margin:42px 0 0}.takeaway-card{position:relative;min-width:0;padding:30px 34px 34px;border-radius:12px;background:var(--paper);color:#101b30;--card-x:clamp(-42px,-3vw,-12px);--card-y:96px;--card-angle:-2.4deg}.takeaway-card:nth-child(even){--card-x:clamp(12px,3vw,42px);--card-angle:2.4deg}.takeaway-card:nth-child(2),.takeaway-card:nth-child(3){background:#e8f0ff}.takeaways dt{font-size:29px;line-height:1.5;color:var(--ink-blue);font-weight:750;margin:0 0 12px}.takeaways dd{margin:0;line-height:1.85;color:#354560;max-width:27em}
.audience-section{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:80px;padding-top:80px;padding-bottom:60px}.audience-main h2{max-width:12em;font-size:34px}.audience-section p{margin:0;line-height:1.85;color:var(--muted)}.optional-reading{padding:4px 0 0 34px;border-left:1px solid var(--line)}.optional-reading h3{font-size:25px;line-height:1.55;margin:0 0 14px}.optional-links{display:flex;flex-direction:column;gap:2px;margin-top:18px}.optional-links a{display:inline-flex;align-items:center;justify-content:space-between;gap:20px;min-height:44px;padding:9px 0;font-size:16px}.optional-links svg{width:18px;height:18px;flex-shrink:0}
.reading-invitation{padding-top:0;padding-bottom:72px;text-align:center}.invitation-inner{padding:64px 28px 0;border-top:1px solid var(--line)}.reading-invitation h2{font-size:42px;max-width:18em;margin:0 auto 18px}.reading-invitation p{text-wrap:pretty;max-width:39em;color:var(--muted);margin:0 auto 28px}.reading-invitation .home-actions{justify-content:center}.home-footer{max-width:1140px;margin:0 auto;padding:28px 0 36px;border-top:1px solid var(--line);display:flex;justify-content:space-between;align-items:flex-start;gap:40px}.home-footer p{font-size:14px;line-height:1.8;max-width:37em;margin:0}.home-footer nav{display:flex;gap:12px 24px;flex-wrap:wrap;font-size:15px;justify-content:flex-end}.home-footer nav a{display:inline-flex;align-items:center;min-height:44px}
.home-button:focus-visible,.home-main a:focus-visible{outline:3px solid var(--accent);outline-offset:5px}.home-button.primary:focus-visible{outline-color:#101b30}
html[lang="en"] .home-hero h1 span{font-size:28px;letter-spacing:-.025em}html[lang="en"] .home-hero h1 strong{font-size:62px;line-height:1.12;max-width:9em}html[lang="en"] .sheet-row{font-size:17px;line-height:1.75}
@media(hover:hover) and (pointer:fine){.home-button:hover{background:#edf3ff;text-decoration:none;border-color:var(--accent)}.home-button.primary:hover{background:var(--ink-blue)}.header-links a:hover{text-decoration:underline}.book-link:hover{text-decoration:none}.book-link:hover .book-caption{background:#edf3ff}}
@media screen and (prefers-reduced-motion:no-preference){.home-button,.book-caption{transition:background-color var(--motion-fast) ease}.scroll-motion .takeaway-card{animation:takeaway-enter 1ms linear backwards,takeaway-exit 1ms linear forwards;animation-timeline:view(block),view(block);animation-range:entry 0% entry 100%,exit 0% exit 100%}@keyframes takeaway-enter{from{transform:translate(var(--card-x),var(--card-y)) rotate(var(--card-angle))}to{transform:none}}@keyframes takeaway-exit{from{transform:none}to{transform:translate(var(--card-x),calc(-1 * var(--card-y))) rotate(calc(-1 * var(--card-angle)))}}}
@media(max-width:1220px){.home-section,.home-route,.home-footer{margin-left:40px;margin-right:40px}}
@media(max-width:1000px) and (min-width:721px){.hero-composition{gap:10px;grid-template-columns:1.2fr .8fr}.home-hero h1 span{font-size:35px}.home-hero h1 strong{font-size:72px}.book-showcase img{height:420px}.worksheet{padding:28px}.sheet-head,.sheet-row{gap:18px}.sheet-row .sheet-cell+.sheet-cell{padding-left:18px}.home-route,.audience-section{gap:40px}.reader-questions{gap:26px}.reader-questions dt{font-size:21px}html[lang="en"] .home-hero h1 strong{font-size:49px}}
@media(max-width:720px){.site-header{display:flex;padding:18px 22px;align-items:center;gap:16px}.brand{font-size:18px}.header-links{font-size:14px;gap:13px;margin-top:0;flex-wrap:nowrap;flex-shrink:0}.header-links a{white-space:nowrap}.header-links .nav-pdf{display:none}.home-scene{padding:0 22px 38px}.home-scene:after{inset:660px 0 0}.hero-composition{display:flex;flex-direction:column;gap:0;min-height:0;padding:0 0 48px}.home-hero{width:100%;padding:30px 0 4px}.home-hero h1{margin-bottom:19px}.home-hero h1 span{font-size:clamp(25px,6.8vw,39px);line-height:1.6}.home-hero h1 strong{font-size:clamp(58px,14vw,80px);line-height:1.25}.home-hero .lead{font-size:18px;line-height:1.8}.home-hero .intro{font-size:16px;margin-bottom:22px}.home-button{font-size:16px;padding:10px 20px;min-height:48px;gap:12px}.home-actions{gap:12px}.home-hero .edition{margin-top:14px}.book-showcase{width:246px;margin-top:15px;align-self:flex-end;margin-right:12px}.book-showcase img{height:305px}.book-caption{font-size:14px;bottom:-9px;padding:7px 13px}.book-ribbon{height:70px;bottom:0;width:200px;left:auto;right:159px}
.worksheet{padding:24px 22px 22px;transform:rotate(-.5deg)}.worksheet>*{transform:none}.worksheet h2{font-size:27px;margin-bottom:14px}.section-kicker{font-size:14px;margin-bottom:8px}.sheet-head{display:none}.sheet-row{display:block;padding:18px 0;font-size:17px}.sheet-row .sheet-cell+.sheet-cell{border:0;padding:13px 0 0 18px;margin:12px 0 0 4px;border-left:2px solid #d8e4fb}.sheet-mobile-label{display:block;color:var(--accent);font-size:14px;font-weight:700;margin-bottom:4px}.sheet-note{font-size:14px;margin-top:17px}
.home-section,.home-route{margin-left:24px;margin-right:24px;padding:44px 0}.home-section h2,.home-route h2{font-size:28px;margin-bottom:16px}.section-intro{font-size:17px;margin-bottom:24px}.reader-questions{display:block;margin-top:28px}.reader-questions>div{padding:20px 0 24px}.reader-questions dt{font-size:21px;margin-bottom:8px}.reader-questions dd{font-size:17px}.home-route{display:block;padding-top:0}.route-intro{padding:0}.route-intro h2{max-width:15em}.route-intro>p{font-size:17px}.learning-route{margin-top:28px}.learning-route li{grid-template-columns:32px minmax(0,1fr);gap:14px;padding:23px 0}.learning-route li:before{font-size:22px}.learning-route h3{font-size:21px}.learning-route p{font-size:17px}.route-start{margin-top:4px}.outcomes-band .home-section{padding-top:44px;padding-bottom:48px}.outcomes-band h2{font-size:30px}.takeaways{grid-template-columns:minmax(0,1fr);gap:18px;margin-top:28px}.takeaway-card,.takeaway-card:nth-child(even){padding:24px;--card-x:0px;--card-y:72px;--card-angle:0deg}.takeaways dt{font-size:26px;margin-bottom:9px}.takeaways dd{font-size:17px}
.audience-section{display:block;padding-bottom:24px}.audience-main h2{max-width:16em}.audience-section p,.reading-invitation p{font-size:17px}.optional-reading{margin-top:30px;padding:26px 0 0;border-left:0;border-top:1px solid var(--line)}.optional-reading h3{font-size:23px}.optional-links{margin-top:14px}.optional-links a{font-size:16px;line-height:1.7;gap:12px}.reading-invitation{padding-top:12px;padding-bottom:44px}.invitation-inner{padding:34px 0 0}.reading-invitation h2{font-size:30px}.home-footer{margin:0 24px;padding:24px 0 30px;display:block}.home-footer p{font-size:14px}.home-footer nav{justify-content:flex-start;gap:0 24px;margin-top:16px}
html[lang="en"] .home-hero h1 span{font-size:23px}html[lang="en"] .home-hero h1 strong{font-size:48px;line-height:1.15;max-width:9em}html[lang="en"] .worksheet h2{font-size:26px}}
@media(max-width:360px){.site-header{padding:16px 18px;gap:12px}html[lang="en"] .brand{max-width:6.5em}.brand{font-size:16px}.header-links{gap:12px;font-size:13px}.home-scene{padding-left:18px;padding-right:18px}.home-hero{padding-top:24px}.home-hero h1 span{font-size:25px}.home-hero h1 strong{font-size:60px}.home-button{padding:10px 16px}.book-showcase{width:218px;margin-right:2px}.book-showcase img{height:278px}.book-ribbon{right:125px}.worksheet{padding:22px 18px}.worksheet h2{font-size:25px}.home-section,.home-route{margin-left:22px;margin-right:22px}html[lang="en"] .home-hero h1 strong{font-size:43px}}
@media print{.home-scene{background:white;padding:0}.hero-composition,.home-route,.audience-section{display:block;min-height:0}.book-showcase,.book-ribbon,.home-actions{display:none}.worksheet{box-shadow:none;transform:none}.outcomes-band{background:white;color:#101b30}.outcomes-band .section-intro,.takeaways dt,.takeaways dd{color:#101b30}.takeaway-card{break-inside:avoid;background:white!important;border:1px solid #cfd9e9}.home-section,.home-route{padding:25px 0}}
"""


def home_page(markdown: str, locale: str) -> str:
    """A reader-facing entrance, bound to the same manuscript and PDFs."""
    stem, lang = LOCALES[locale]
    _, chapters = markdown_to_html(markdown, locale)
    chapter_links = {}
    for title, anchor in chapters:
        match = re.match(r"^(\d+)\.\s", title)
        if match:
            chapter_links[int(match[1])] = f"{stem}.html#{anchor}"
    en = locale == "en"
    title = "AI Work Assistant Handbook" if en else "從零開始養成我的 AI 管家"
    brand = "AI Work Assistant" if en else "AI 管家教學書"
    hero_title = ('<span>From your first task to</span><strong>Your AI work assistant</strong>' if en
                  else '<span>從零開始養成我的</span><strong>AI 管家</strong>')
    edition = "Free Public Edition v1.1" if en else "免費公開版 v1.1"
    reader, other = f"{stem}.html", "index.html" if en else "english.html"
    pdf = f"downloads/ai-butler-handbook_v1.1_{locale}.pdf"
    read, download = ("Start reading", "Download PDF") if en else ("開始閱讀", "下載 PDF")
    lead = ("You do not need every AI tool. Start by assigning one task well." if en
            else "不必追很多工具，先把一件工作交辦好。")
    intro = ("For people bringing AI into everyday work for the first time. Start with meeting notes: assign, check, and refine a task, then save what worked." if en
             else "給第一次把 AI 用進工作與日常的人。從會議筆記練習交辦、核對與修正，再把好用的方法留下來。")
    sheet_title = "Every task traces back to the notes." if en else "每一項待辦，都對得回原文。"
    sheet_labels = ["Original notes", "Organized task", "What to check"] if en else ["原始筆記", "整理後的待辦", "核對重點"]
    sheet_rows = ([
        ("The registration page copy for next week's online workshop has not been finalized. Marketing will provide a revised version by Wednesday.", "Marketing: provide revised registration-page copy. Due: Wednesday.", '<span class="sheet-confirmed">The role and deadline are both in the notes.</span>'),
        ("Customer support and admin have received several questions about the registration flow recently. Someone needs to compile a list of frequently asked questions.", "Compile registration FAQs. Owner and deadline: to confirm.", '<mark>No named owner or deadline. Confirm both.</mark>'),
    ] if en else [
        ("下週線上工作坊報名頁文案還沒確認，行銷週三前提供新版。", "行銷：提供報名頁新版文案。\n期限：週三前。", '<span class="sheet-confirmed">負責角色與期限，原文都有寫明。</span>'),
        ("客服 / 行政近期收到幾件報名流程相關問題，需要整理常見問答。", "整理報名常見問答。\n負責人與期限：待確認。", '<mark>未指派整理人，也沒寫期限，兩項都先確認。</mark>'),
    ])
    sheet_parts = []
    for number, row in enumerate(sheet_rows, 1):
        cells = []
        for i, value in enumerate(row):
            text = value if i == 2 else html.escape(value).replace('\n', '<br>')
            cells.append(f'<div class="sheet-cell" role="group" aria-label="{sheet_labels[i]}"><span class="sheet-mobile-label" aria-hidden="true">{sheet_labels[i]}</span><p class="{"sheet-check" if i == 2 else ""}">{text}</p></div>')
        sheet_parts.append(f'<div class="sheet-row" id="sheet-row-{number}">{"".join(cells)}</div>')
    sheet_body = ''.join(sheet_parts)
    sheet_note = ("An excerpt from the first exercise. Keep what the notes say; confirm what they leave open." if en
                  else "節錄自第 2 章練習。有寫明的留下，沒寫明的先確認。")
    sheet_link = "Try it with the full notes" if en else "拿完整筆記試做"
    cover_alt = "Illustrated cover of the digital AI Work Assistant Handbook" if en else "AI 管家數位手冊的書封示意"
    book_link_label = "Explore the example" if en else "看筆記怎麼變成待辦"
    example_kicker = "See it in practice" if en else "先看一個例子"
    route_kicker = "Practice with the handbook" if en else "照著練一次"
    arrow_icon = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M3 10h13m-5-5 5 5-5 5"/></svg>'
    questions_title = "Want AI to help, but unsure where to start?" if en else "想讓 AI 幫忙，卻不知道從哪開始？"
    questions_intro = ("The missing piece may not be another tool. This handbook uses worked examples, task templates, and checklists to help with three common difficulties."
                       if en else "問題不一定在少了哪個工具。這本書用完整案例、交辦模板與檢查清單，帶你處理三個常見卡點。")
    questions = ([
        ("What can I assign?", "Start with a low-risk task you can check yourself, such as a summary, a task list, or a first draft."),
        ("Why is the result not useful?", "Make the goal, source material, limits, and output format clear. Use the first draft to see what needs correction."),
        ("Can I trust the answer?", "Compare the result with its sources. Separate supported information from assumptions and open questions; keep judgment and responsibility with you."),
    ] if en else [
        ("不知道先交辦什麼？", "從摘要、待辦整理或改寫初稿開始，先選一件風險低、自己能核對的任務。"),
        ("結果和想的不一樣？", "把目標、資料、限制與輸出格式說清楚，先拿到一版能檢查、能修正的結果。"),
        ("這個答案能直接用嗎？", "對照來源，分清楚已有依據、推測與待確認的內容；判斷與責任仍留在自己手上。"),
    ])
    questions_body = ''.join(f'<div><dt>{html.escape(heading)}</dt><dd>{html.escape(description)}</dd></div>'
                             for heading, description in questions)
    route_title = "Try the example. Then use your own material." if en else "先照案例做，再換成你的工作"
    route_intro = ("Return to the relevant chapter when you need help; you do not have to finish the whole book before you begin."
                   if en else "遇到問題時回到對應章節查做法，不必一次讀完整本。")
    steps = ([
        ("Explain the task", "Choose a low-risk task whose result you can check. Provide the goal, source material, limits, and output format."),
        ("Check and refine the result", "Compare it with the source. Look for omissions, misunderstandings, and invented details. Correct problems and confirm missing information."),
        ("Save what worked", "After checking the result, keep useful instructions and checks as a template you can adapt for similar tasks."),
    ] if en else [
        ("先把任務交辦清楚", "選一件低風險、自己能核對的工作，說明目標、資料、限制與希望的輸出格式。"),
        ("對照資料，核對與修正", "逐項查看有沒有遺漏、誤解或擅自補上的內容。有問題就補充或修改，缺少的資訊先確認。"),
        ("把有效的方法留下來", "任務做過、結果也核對過，再把好用的交辦方式與檢查項目存成模板，留待下次調整使用。"),
    ])
    items = "".join(f'<li><div><h3>{html.escape(heading)}</h3><p>{html.escape(description)}</p>'
                    '</div></li>' for heading, description in steps)
    route_start = "Try the first task in Chapter 2" if en else "到第 2 章試做第一件任務"
    outcomes_title = "Take four practical skills into your next task" if en else "讀完，帶走四種實用能力"
    outcomes_intro = ("The meeting notes are a starting point. Use the same habits when you summarize material, draft a reply, or organize a new task."
                      if en else "會議筆記只是起點。整理資料、草擬回覆或面對一件新任務時，也能沿用同一套交辦與核對方法。")
    outcomes = ([
        ("Assign clearly", "Give AI the material and instructions it needs to begin, rather than a vague request to handle everything."),
        ("Judge the result", "Distinguish supported information from open questions. Know what needs checking and when to stop and ask a person."),
        ("Keep useful methods", "Build your own task templates and checklists, so similar work starts with a method you can adapt."),
        ("Choose tools", "Recognize when your current tool is enough, and when you need file handling, reusable instructions, or an assistant that can carry a task forward."),
    ] if en else [
        ("會交辦", "面對一件新任務，能整理出 AI 開始工作所需的資料與說明，不再只丟一句「幫我處理」。"),
        ("會驗收", "分得清已有依據與還要確認的內容，知道哪些地方需要核對，什麼時候應該停下來問人。"),
        ("會保存", "累積自己的交辦模板與檢查清單，下次遇到類似工作，有方法可以沿用，不必每次從頭試。"),
        ("會選工具", "判斷手上的工具是否夠用，何時才需要檔案處理、可重複使用的說明，或能接續執行的助理。"),
    ])
    outcomes_body = ''.join(f'<div class="takeaway-card"><dt>{html.escape(heading)}</dt><dd>{html.escape(description)}</dd></div>'
                            for heading, description in outcomes)
    audience_title = "For people bringing AI into everyday work for the first time" if en else "給第一次把 AI 用進工作與日常的人"
    audience_intro = ("No programming background is needed. Start with a familiar task whose result you can check. If you already use AI but struggle to assign or review work, use the relevant chapters."
                      if en else "不需要先懂程式，也不必先研究一長串工具。只要有一件自己熟悉、能核對結果的小任務，就可以開始練習。已經用過 AI，卻卡在交辦、修改或判斷答案的人，也能從對應章節找做法。")
    optional_title = "Go further when your work needs it" if en else "有需要，再往下讀"
    optional_intro = ("Explore tools for files and longer tasks, Skills for reusable instructions, and Agents for carrying a complete task forward. Chapter 19 follows the same notes through collaboration, limited revision cycles, and controls for data, permissions, and progress. Team leads can also explore team adoption in Chapter 20."
                      if en else "需要處理檔案或更多步驟時，再看工具怎麼選；想重用已驗證的工作說明，可以讀 Skill；想交給助理接續處理，可以讀 Agent。第 19 章沿用同一份筆記，說明分工核對、有限修正，以及資料、權限與進度的管理；團隊主管也可選讀第 20 章的導入與成果保存。")
    optional_links = [(4, "Explore tools and ways to use them" if en else "認識工具與用法"),
                      (18, "Save a method as a Skill" if en else "把方法存成 Skill"),
                      (19, "Explore Agents and collaboration" if en else "認識 Agent 與分工核對")]
    optional_body = ''.join(f'<a href="{chapter_links[number]}">{html.escape(label)}{arrow_icon}</a>' for number, label in optional_links)
    invitation_title = "Start with one small task." if en else "從一件小任務，開始練習。"
    invitation_intro = ("Start with the reading route in Chapter 0 and the exercise in Chapter 2. Download the PDF to keep the examples, templates, and checklists nearby."
                        if en else "第一次閱讀，可以先看第 0 章的使用路線，再到第 2 章試做。也可以下載 PDF，保留範例、模板與檢查清單，遇到類似工作時回來查。")
    disclaimer = "Public Disclaimer and Permissions" if en else "公開版聲明"
    legal_anchor = slugify(disclaimer, set())
    sharing = ("Free to read and share via the original link. See the handbook for permissions and safety guidance."
               if en else "免費閱讀與分享原始連結。引用、使用方式與安全提醒，請見書內聲明。")
    skip = "Skip to content" if en else "跳到正文"
    return f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
{public_metadata(locale, "english.html" if en else "index.html")}<title>{title}</title><style>{CSS}{HOME_CSS}</style></head>
<body><a class="skip" href="#main">{skip}</a><header class="site-header"><a class="brand" href="{'english.html' if en else 'index.html'}">{brand}</a><nav class="header-links" aria-label="{'Main navigation' if en else '主要導覽'}"><a href="{reader}">{read}</a><a href="{other}" lang="{'zh-Hant' if en else 'en'}">{'繁體中文' if en else 'English'}</a><a class="nav-pdf" href="{pdf}" download>PDF</a></nav></header>
<main id="main" class="home-main"><div class="home-scene"><div class="hero-composition"><section class="home-hero"><h1>{hero_title}</h1><p class="lead">{lead}</p><p class="intro">{intro}</p><div class="home-actions"><a class="home-button primary" href="{reader}">{read}{arrow_icon}</a><a class="home-button" href="{pdf}" download>{download}</a></div><p class="edition">{edition}</p></section>
<figure class="book-showcase"><a class="book-link" href="#worksheet-title"><img src="assets/handbook-book-{locale}.png" alt="{cover_alt}" width="1145" height="1374" fetchpriority="high"><span class="book-caption">{book_link_label}<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M10 3v13m-5-5 5 5 5-5"/></svg></span></a></figure>
<svg class="book-ribbon" viewBox="0 0 1140 100" preserveAspectRatio="none" aria-hidden="true"><path pathLength="1" d="M 760 0 C 755 48 510 23 510 100"/></svg></div>
<section class="worksheet" aria-labelledby="worksheet-title"><span class="section-kicker">{example_kicker}</span><h2 id="worksheet-title">{sheet_title}</h2><div class="sheet-head" aria-hidden="true">{''.join('<span>'+x+'</span>' for x in sheet_labels)}</div>{sheet_body}<p class="sheet-note">{sheet_note} <a href="{chapter_links[2]}">{sheet_link}</a></p></section></div>
<section class="home-section" aria-labelledby="questions-title"><h2 id="questions-title">{questions_title}</h2><p class="section-intro">{questions_intro}</p><dl class="reader-questions">{questions_body}</dl></section>
<section class="home-route" aria-labelledby="route-title"><div class="route-intro"><span class="section-kicker">{route_kicker}</span><h2 id="route-title">{route_title}</h2><p>{route_intro}</p><p class="route-start"><a href="{chapter_links[2]}">{route_start}</a></p></div><ol class="learning-route">{items}</ol></section>
<section class="outcomes-band" aria-labelledby="outcomes-title"><div class="home-section"><h2 id="outcomes-title">{outcomes_title}</h2><p class="section-intro">{outcomes_intro}</p><dl class="takeaways">{outcomes_body}</dl></div></section>
<section class="home-section audience-section" aria-labelledby="audience-title"><div class="audience-main"><h2 id="audience-title">{audience_title}</h2><p>{audience_intro}</p></div><div class="optional-reading"><h3>{optional_title}</h3><p>{optional_intro}</p><nav class="optional-links" aria-label="{'Optional chapters' if en else '進階選讀章節'}">{optional_body}</nav></div></section>
<section class="home-section reading-invitation" aria-labelledby="invitation-title"><div class="invitation-inner"><h2 id="invitation-title">{invitation_title}</h2><p>{invitation_intro}</p><div class="home-actions"><a class="home-button primary" href="{reader}">{read}{arrow_icon}</a><a class="home-button" href="{pdf}" download>{download}</a></div></div></section>
<footer class="home-footer"><p>{sharing}</p><nav aria-label="{'Author and permissions' if en else '作者與使用說明'}"><a href="{reader}#{legal_anchor}">{disclaimer}</a><a href="https://www.linkedin.com/in/farceur-liu-636864b5/" rel="noopener noreferrer">Farceur Liu</a><a href="mailto:farceur2021@gmail.com">Email</a></nav></footer></main><script src="assets/home.js" defer></script></body></html>'''



def chrome_path(explicit: str | None = None) -> str:
    candidates = [explicit, os.environ.get("CHROME_BIN"),
                  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                  shutil.which("chromium"), shutil.which("google-chrome"), shutil.which("chromium-browser")]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return str(Path(candidate).resolve())
    raise RuntimeError("PDF generation needs an existing Chrome/Chromium. Set CHROME_BIN; do not install automatically.")


def print_pdf(browser: str, source: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    # A disposable browser profile never opens, modifies or signs into a real profile.
    # All required resources are file:// URLs; DNS and background services are disabled.
    with tempfile.TemporaryDirectory(prefix="ai-handbook-print-") as profile:
        command = [browser, "--headless", f"--user-data-dir={profile}", "--no-first-run",
                   "--no-default-browser-check", "--disable-background-networking",
                   "--disable-component-update", "--disable-sync", "--disable-extensions",
                   "--disable-default-apps", "--disable-domain-reliability", "--metrics-recording-only",
                   "--disable-features=OptimizationHints,MediaRouter,AutofillServerCommunication",
                   "--host-resolver-rules=MAP * ~NOTFOUND", "--no-pdf-header-footer",
                   f"--print-to-pdf={output}", source.as_uri()]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=180)
        if result.returncode or not output.exists() or output.stat().st_size < 1000:
            raise RuntimeError(f"Chrome PDF generation failed for {source.name}: {result.stderr[-1500:]}")


def public_pdf_links(target: Path) -> int:
    """Replace Chrome's local image URI without shifting PDF object offsets.

    Only the known diagram annotation is supported. Its public URI must fit
    inside the original literal; padding goes OUTSIDE the PDF string. Content
    streams, object offsets, text, page geometry and document length stay intact.
    """
    data = target.read_bytes()
    changed = 0

    def replace(match: re.Match[bytes]) -> bytes:
        nonlocal changed
        name = unquote(urlsplit(match[1].decode("utf-8")).path).rsplit("/", 1)[-1]
        if name not in ("meeting-loop-zh.svg", "meeting-loop-en.svg"):
            raise ValueError("Unexpected local PDF annotation; inspect without publishing")
        replacement = b"/URI (" + (SITE_URL + "assets/" + name).encode("ascii") + b")"
        if len(replacement) > len(match[0]):
            raise ValueError("Public PDF annotation does not fit; explicit PDF rebuild required")
        changed += 1
        return replacement.ljust(len(match[0]), b" ")

    public = re.sub(rb"/URI\s+\((file:[^)]*)\)", replace, data)
    if b"file:" in public or b"/Users/" in public:
        raise ValueError("PDF still contains a local URI or private path")
    if changed:
        target.write_bytes(public)
    return changed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", action="store_true", help="Explicitly regenerate PDFs; default preserves the verified release")
    parser.add_argument("--chrome", help="Existing Chrome/Chromium executable for --pdf")
    args = parser.parse_args()
    manuscripts = {locale: (ROOT / name).read_text(encoding="utf-8") for locale, name in SOURCES.items()}
    pages = {}
    for locale, manuscript in manuscripts.items():
        stem = LOCALES[locale][0]
        pages[stem + ".html"] = page(manuscript, locale)
        pages["english.html" if locale == "en" else "index.html"] = home_page(manuscript, locale)
    # Keep the existing LinkedIn entry URL on the same English edition.
    pages["linkedin.html"] = pages["english.html"]
    for name, content in pages.items():
        (ROOT / name).write_text(content, encoding="utf-8")
        print(name)
    if args.pdf:
        browser = chrome_path(args.chrome)
        for locale, (stem, _) in LOCALES.items():
            print_pdf(browser, ROOT / (stem + ".html"), PDF_DIR / f"ai-butler-handbook_v1.1_{locale}.pdf")
    for locale in LOCALES:
        target = PDF_DIR / f"ai-butler-handbook_v1.1_{locale}.pdf"
        if not target.is_file():
            raise RuntimeError("Missing release PDF; restore the verified artifact or explicitly use --pdf")
        public_pdf_links(target)
    print("PASS: public bilingual v1.1 built; historical v1.0 downloads preserved.")


if __name__ == "__main__":
    main()
