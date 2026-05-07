#!/usr/bin/env python3
from __future__ import annotations

import html
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MD = ROOT / "downloads" / "從零開始養成我的AI管家_公開版.md"
COVER_PREVIEW = ROOT / "assets" / "cover-preview.png"
SOCIAL_PREVIEW = ROOT / "assets" / "social-preview.png"
SITE_URL = "https://farceurliu.github.io/ai-butler-handbook/"
SOCIAL_PREVIEW_URL = f"{SITE_URL}assets/social-preview.png"
LINKEDIN_URL = "https://www.linkedin.com/in/farceur-liu-636864b5/"
CONTACT_EMAIL = "farceur2021@gmail.com"
CONTACT_MAILTO = f"mailto:{CONTACT_EMAIL}"


def slugify(title: str, used: set[str]) -> str:
    value = re.sub(r"[^\w\u4e00-\u9fff]+", "-", title.strip().lower()).strip("-")
    if not value:
        value = "section"
    base = value
    i = 2
    while value in used:
        value = f"{base}-{i}"
        i += 1
    used.add(value)
    return value


def inline(text: str) -> str:
    value = html.escape(text)
    value = re.sub(r"`([^`]+)`", r"<code>\1</code>", value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", value)
    return value


def markdown_to_html(markdown: str) -> tuple[str, list[tuple[int, str, str]]]:
    lines = markdown.splitlines()
    out: list[str] = []
    toc: list[tuple[int, str, str]] = []
    used: set[str] = set()
    in_code = False
    code_lines: list[str] = []
    list_type: str | None = None
    table_lines: list[str] = []

    def close_list() -> None:
        nonlocal list_type
        if list_type:
            out.append(f"</{list_type}>")
            list_type = None

    def close_table() -> None:
        nonlocal table_lines
        if not table_lines:
            return
        rows = [split_table(row) for row in table_lines if row.strip()]
        table_lines = []
        if len(rows) < 2:
            for row in rows:
                out.append(f"<p>{inline(' | '.join(row))}</p>")
            return
        out.append("<div class=\"table-wrap\"><table>")
        header = rows[0]
        out.append("<thead><tr>" + "".join(f"<th>{inline(cell)}</th>" for cell in header) + "</tr></thead>")
        out.append("<tbody>")
        for row in rows[2:]:
            out.append("<tr>" + "".join(f"<td>{inline(cell)}</td>" for cell in row) + "</tr>")
        out.append("</tbody></table></div>")

    def split_table(row: str) -> list[str]:
        value = row.strip()
        if value.startswith("|"):
            value = value[1:]
        if value.endswith("|"):
            value = value[:-1]
        return [cell.strip() for cell in value.split("|")]

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()

        if stripped.startswith("```"):
            close_table()
            close_list()
            if in_code:
                out.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
                code_lines = []
                in_code = False
            else:
                in_code = True
            continue

        if in_code:
            code_lines.append(line)
            continue

        if "|" in stripped and stripped.startswith("|") and stripped.endswith("|"):
            close_list()
            table_lines.append(stripped)
            continue
        close_table()

        if not stripped:
            close_list()
            continue

        match = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if match:
            close_list()
            level = len(match.group(1))
            title = match.group(2).strip()
            if level == 1 and "從零開始養成我的 AI 管家" in title:
                continue
            anchor = slugify(title, used)
            if level <= 3:
                toc.append((level, title, anchor))
            out.append(f"<h{level} id=\"{anchor}\">{inline(title)}</h{level}>")
            continue

        if stripped.startswith(">"):
            close_list()
            quote = stripped.lstrip(">").strip()
            out.append(f"<blockquote>{inline(quote)}</blockquote>")
            continue

        bullet = re.match(r"^[-*]\s+(.+)$", stripped)
        number = re.match(r"^\d+\.\s+(.+)$", stripped)
        if bullet or number:
            tag = "ul" if bullet else "ol"
            if list_type != tag:
                close_list()
                out.append(f"<{tag}>")
                list_type = tag
            item = bullet.group(1) if bullet else number.group(1)
            out.append(f"<li>{inline(item)}</li>")
            continue

        close_list()
        out.append(f"<p>{inline(stripped)}</p>")

    if in_code:
        out.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
    close_table()
    close_list()
    return "\n".join(out), toc


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def copy_if_different(source: Path, destination: Path) -> None:
    if source.resolve() == destination.resolve():
        return
    shutil.copy2(source, destination)


def html_page(title: str, body: str, description: str, extra_head: str = "", path: str = "") -> str:
    head_extra = f"\n{extra_head}" if extra_head else ""
    canonical_url = f"{SITE_URL}{path}"
    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <link rel="canonical" href="{html.escape(canonical_url)}">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{html.escape(canonical_url)}">
  <meta property="og:site_name" content="從零開始養成我的 AI 管家">
  <meta property="og:locale" content="zh_TW">
  <meta property="og:image" content="{SOCIAL_PREVIEW_URL}">
  <meta property="og:image:secure_url" content="{SOCIAL_PREVIEW_URL}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="從零開始養成我的 AI 管家免費公開手冊預覽圖">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(description)}">
  <meta name="twitter:image" content="{SOCIAL_PREVIEW_URL}">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="assets/styles.css">{head_extra}
</head>
<body>
{body}
</body>
</html>
"""


def html_page_en(title: str, body: str, description: str, path: str = "english.html") -> str:
    canonical_url = f"{SITE_URL}{path}"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <link rel="canonical" href="{html.escape(canonical_url)}">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{html.escape(canonical_url)}">
  <meta property="og:site_name" content="AI Work Assistant Handbook">
  <meta property="og:locale" content="en_US">
  <meta property="og:image" content="{SOCIAL_PREVIEW_URL}">
  <meta property="og:image:secure_url" content="{SOCIAL_PREVIEW_URL}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Free public AI work assistant handbook preview image">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(description)}">
  <meta name="twitter:image" content="{SOCIAL_PREVIEW_URL}">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="assets/styles.css">
</head>
<body>
{body}
</body>
</html>
"""


def nav(active: str, locale: str = "zh") -> str:
    if locale == "en":
        brand = "AI Workflow Handbook"
        home_label = "Home"
        read_label = "Read Chinese Edition"
        aria_label = "Main navigation"
    else:
        brand = "AI 管家教學書"
        home_label = "首頁"
        read_label = "線上閱讀"
        aria_label = "主要導覽"
    return f"""<header class="site-header">
  <a class="brand" href="index.html">{brand}</a>
  <nav aria-label="{aria_label}">
    <a class="{ 'active' if active == 'home' else '' }" href="index.html">{home_label}</a>
    <a class="{ 'active' if active == 'read' else '' }" href="read.html">{read_label}</a>
    <a class="{ 'active' if active == 'english' else '' }" href="english.html">English</a>
    <a href="downloads/從零開始養成我的AI管家_免費公開版_v1.0.pdf">PDF</a>
    <a href="{LINKEDIN_URL}" target="_blank" rel="noopener noreferrer">LinkedIn</a>
    <a href="{CONTACT_MAILTO}">Email</a>
  </nav>
</header>"""


def build_index(toc: list[tuple[int, str, str]]) -> str:
    chapters = "\n".join(
        f'<a href="read.html#{anchor}"><span>{html.escape(title)}</span></a>'
        for level, title, anchor in toc
        if level == 2 and not title.startswith("目錄")
    )
    body = f"""{nav('home')}
<main>
  <section class="hero launch-hero">
    <div class="hero-copy">
      <h1><span>從零開始養成我的</span><span>AI 管家</span></h1>
      <p class="lead"><span>你需要的 AI 工具其實不多。</span><span>真正的差距，是會不會把 AI 調教成能交辦、可驗收、能累積的工作夥伴。</span></p>
      <div class="hero-actions">
        <a class="button primary" href="read.html">線上閱讀</a>
        <a class="button" href="downloads/從零開始養成我的AI管家_免費公開版_v1.0.pdf">下載 PDF</a>
        <a class="button" href="english.html">English Overview</a>
        <a class="button" href="{LINKEDIN_URL}" target="_blank" rel="noopener noreferrer">作者 LinkedIn</a>
      </div>
      <div class="proof-row" aria-label="公開版重點">
        <span><strong>v1.0</strong> 免費公開版</span>
        <span><strong>22</strong> 章養成路線</span>
        <span><strong>4</strong> 個 Skill 案例</span>
      </div>
    </div>
    <div class="hero-showcase launch-showcase" aria-label="AI 管家教學書預覽">
      <figure class="cover launch-cover">
        <img src="assets/cover-preview.png" alt="從零開始養成我的 AI 管家書籍預覽">
      </figure>
    </div>
  </section>

  <section class="thesis-section launch-thesis">
    <h2>這不是工具清單，而是一套把 AI 用進工作的養成方法。</h2>
    <p>多數人卡住，不是因為少用某個冷門 AI 工具，而是不知道怎麼讓 ChatGPT、Codex、Claude Code 或 Gemini CLI 做到自己想要的結果。這本書把「怎麼問、怎麼驗、怎麼修、怎麼留下流程」整理成新手也能照著練的路線。</p>
  </section>

  <section class="problem-section">
    <div class="section-heading">
      <h2>先解決三個常見卡點</h2>
    </div>
    <div class="problem-grid">
      <div>
        <span>01</span>
        <h3>不知道該交辦什麼</h3>
        <p>從摘要、整理、分類、改寫這類低風險任務開始，先建立可驗收的成功經驗。</p>
      </div>
      <div>
        <span>02</span>
        <h3>問了但結果不好</h3>
        <p>把目標、資料、限制、輸出格式和不要做的事講清楚，讓 AI 先產出可修的第一版。</p>
      </div>
      <div>
        <span>03</span>
        <h3>不知道能不能相信</h3>
        <p>用驗收清單分清事實、推測、待確認項目，把人的判斷留在流程裡。</p>
      </div>
    </div>
  </section>

  <section class="workflow-section">
    <div class="section-heading">
      <h2>從第一件低風險任務開始</h2>
    </div>
    <div class="workflow-steps">
      <div><span>01</span><strong>選一件低風險任務</strong><p>從整理、摘要、分類、改寫這類可驗收工作開始。</p></div>
      <div><span>02</span><strong>交辦清楚</strong><p>說明目標、資料來源、限制、輸出格式與不要做的事。</p></div>
      <div><span>03</span><strong>驗收與修正</strong><p>分清事實、推測、待確認項目，不把判斷責任交出去。</p></div>
      <div><span>04</span><strong>保存成流程</strong><p>把反覆成功的方法整理成模板，必要時再升級成 Skill。</p></div>
    </div>
  </section>

  <section class="band outcome-section">
    <div class="section-heading">
      <h2>學完後，你會帶走四種能力</h2>
    </div>
    <div class="outcome-grid">
      <div>
        <h3>會交辦</h3>
        <p>把目標、資料、邊界、輸出格式與驗收方式講清楚，讓 AI 產出可檢查的第一版。</p>
      </div>
      <div>
        <h3>會驗收</h3>
        <p>不照單全收，分清事實、推測與待確認項目，保留人的判斷與責任。</p>
      </div>
      <div>
        <h3>會沉澱</h3>
        <p>把跑通的方法保存成模板，必要時再整理成 Skill，讓經驗可以被重複使用。</p>
      </div>
      <div>
        <h3>會選工具</h3>
        <p>分清 Chat、Codex / Claude Code / Gemini CLI 和 Skill 的使用時機，不再被工具清單牽著走。</p>
      </div>
    </div>
  </section>

  <section class="split audience-section">
    <div>
      <h2>給第一次把 AI 用進工作的人</h2>
      <p>這本書不是工具排行榜，也不是要你追逐每個新產品。它從低風險任務開始，帶你練習 Chat、Codex / Claude Code / Gemini CLI、工作流與 Skill 的使用邊界。</p>
    </div>
    <div class="reader-list">
      <p>第一次接觸 AI 的工作者</p>
      <p>想把 AI 用進日常流程的小團隊</p>
      <p>想理解 Codex / Claude Code / Gemini CLI 的使用者</p>
      <p>想把好用工作流整理成 Skill 的人</p>
    </div>
  </section>

  <section class="reading-section">
    <div>
      <h2>先讀完，再挑一個真實任務練一次。</h2>
      <p>公開版保留線上閱讀與 PDF 兩種入口。建議先快速讀過養成路線，再拿一個低風險工作照著交辦、驗收、調教，最後把跑通的方法保存成自己的模板。</p>
    </div>
    <div class="reading-actions">
      <a class="button primary" href="read.html">開始線上閱讀</a>
      <a class="button" href="downloads/從零開始養成我的AI管家_免費公開版_v1.0.pdf">下載 PDF</a>
    </div>
  </section>

  <section class="contact-section">
    <div class="contact-layout">
      <div class="contact-copy">
        <div class="section-heading">
          <h2>想交流 AI 管家養成、工作流或導入經驗</h2>
        </div>
        <p class="section-copy">歡迎透過 LinkedIn 認識 Farceur Liu；合作、分享邀約或 AI 工作流交流，也可以直接寄信到 <a href="{CONTACT_MAILTO}">{CONTACT_EMAIL}</a>。</p>
        <div class="hero-actions">
          <a class="button" href="{LINKEDIN_URL}" target="_blank" rel="noopener noreferrer">前往 LinkedIn</a>
          <a class="button" href="{CONTACT_MAILTO}">Email 聯繫</a>
        </div>
      </div>
      <div class="linkedin-badge-card" aria-label="Farceur Liu LinkedIn 個人檔案">
        <div class="badge-base LI-profile-badge" data-locale="zh_TW" data-size="medium" data-theme="dark" data-type="VERTICAL" data-vanity="farceur-liu-636864b5" data-version="v1"><a class="badge-base__link LI-simple-link" href="https://tw.linkedin.com/in/farceur-liu-636864b5?trk=profile-badge">Farceur Liu</a></div>
      </div>
    </div>
  </section>

  <section class="band">
    <div class="section-heading">
      <h2>章節索引</h2>
    </div>
    <div class="chapter-grid">{chapters}</div>
  </section>
</main>
<footer>
  <p>© 2026 <a href="{LINKEDIN_URL}" target="_blank" rel="noopener noreferrer">Farceur Liu</a>. 合作與交流可寄信至 <a href="{CONTACT_MAILTO}">{CONTACT_EMAIL}</a>。免費公開版可分享原始連結，商業使用請先取得授權。</p>
</footer>"""
    linkedin_script = '  <script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>'
    return html_page("從零開始養成我的 AI 管家｜免費公開版", body, "AI 管家公開教學書，教你把 AI 從聊天工具養成可交辦、可驗收、可累積的工作助理。", linkedin_script)


def build_read(content_html: str, toc: list[tuple[int, str, str]]) -> str:
    toc_links = "\n".join(
        f'<a class="toc-l{level}" href="#{anchor}">{html.escape(title)}</a>'
        for level, title, anchor in toc
        if level <= 3
    )
    body = f"""{nav('read')}
<main class="reader-layout">
  <aside class="toc">
    <strong>目錄</strong>
    {toc_links}
  </aside>
  <article class="book">
    <p class="eyebrow">免費公開版 v1.0 · Farceur Liu · 2026-05-06</p>
    <h1>從零開始養成我的 AI 管家</h1>
    {content_html}
  </article>
</main>
<footer>
  <p><a href="index.html">回首頁</a> · <a href="downloads/從零開始養成我的AI管家_免費公開版_v1.0.pdf">下載 PDF</a> · <a href="{LINKEDIN_URL}" target="_blank" rel="noopener noreferrer">作者 LinkedIn</a> · <a href="{CONTACT_MAILTO}">Email 聯繫</a></p>
</footer>"""
    return html_page("線上閱讀｜從零開始養成我的 AI 管家", body, "從零開始養成我的 AI 管家免費公開版線上閱讀。", path="read.html")


def build_english() -> str:
    body = f"""{nav('english', 'en')}
<main>
  <section class="hero launch-hero">
    <div class="hero-copy">
      <p class="eyebrow">English Overview</p>
      <h1><span>Build Your AI</span><span>Work Assistant</span></h1>
      <p class="lead"><span>A practical self-study handbook for building repeatable AI workflows.</span><span>The full edition is written in Traditional Chinese.</span></p>
      <div class="hero-actions">
        <a class="button primary" href="read.html">Read Chinese Edition</a>
        <a class="button" href="downloads/從零開始養成我的AI管家_免費公開版_v1.0.pdf">Download Chinese PDF</a>
        <a class="button" href="{LINKEDIN_URL}" target="_blank" rel="noopener noreferrer">Connect on LinkedIn</a>
      </div>
      <div class="proof-row" aria-label="Book highlights">
        <span><strong>v1.0</strong> Free public edition</span>
        <span><strong>22</strong> chapters</span>
        <span><strong>4</strong> Skill examples</span>
      </div>
    </div>
    <div class="hero-showcase launch-showcase" aria-label="AI Work Assistant Handbook preview">
      <figure class="cover launch-cover">
        <img src="assets/cover-preview.png" alt="Chinese AI work assistant handbook preview">
      </figure>
    </div>
  </section>

  <section class="thesis-section launch-thesis">
    <h2>The tool is not the differentiator. Your workflow is.</h2>
    <p>Most people do not need more AI tools. They need a clearer way to assign work, check the output, improve the result, and save the process for next time. The original Chinese title is <strong>從零開始養成我的 AI 管家</strong>; this English page explains the method in terms of an AI work assistant.</p>
  </section>

  <section class="problem-section">
    <div class="section-heading">
      <h2>Who this is for</h2>
    </div>
    <div class="problem-grid">
      <div>
        <span>01</span>
        <h3>First-time AI users</h3>
        <p>Professionals who want to use ChatGPT, Claude, or Gemini for real work &mdash; not just casual chat.</p>
      </div>
      <div>
        <span>02</span>
        <h3>Small teams</h3>
        <p>Teams adopting AI tools and looking for a shared, repeatable method rather than individual workarounds.</p>
      </div>
      <div>
        <span>03</span>
        <h3>Workflow builders</h3>
        <p>People who want to turn one-off prompts into reusable templates, SOPs, or stable AI skills.</p>
      </div>
    </div>
  </section>

  <section class="workflow-section">
    <div class="section-heading">
      <h2>What you will learn</h2>
    </div>
    <div class="workflow-steps">
      <div><span>01</span><strong>Give clear assignments</strong><p>State the goal, source material, constraints, output format, and what the AI must not assume.</p></div>
      <div><span>02</span><strong>Check the output</strong><p>Separate facts from guesses and open questions. Keep human judgment inside the loop.</p></div>
      <div><span>03</span><strong>Improve through feedback</strong><p>Turn a usable first draft into a better second version by naming exactly what missed.</p></div>
      <div><span>04</span><strong>Save what works</strong><p>Preserve repeatable assignments as templates, scripts, SOPs, or skills.</p></div>
    </div>
  </section>

  <section class="band outcome-section">
    <div class="section-heading">
      <h2>7-day starter path</h2>
      <p style="color:var(--muted);margin-top:8px;font-size:17px;">Adapted from Chapter 0. Pick one real, low-risk task from your work and follow this rhythm.</p>
    </div>
    <div class="outcome-grid">
      <div><h3>Day 1</h3><p>Complete one low-risk task end-to-end. The goal is a verified first draft, not perfection. (Ch. 2)</p></div>
      <div><h3>Day 2</h3><p>Turn that first draft into a second version. Write specific corrections, not vague complaints. (Ch. 6, 10, 11)</p></div>
      <div><h3>Day 3</h3><p>Summarize a real customer or user message into a clean internal note. (Ch. 7.2, 8.2)</p></div>
      <div><h3>Day 4</h3><p>Review an outbound reply draft for accuracy and risk before sending it. (Ch. 7.3, 15)</p></div>
      <div><h3>Day 5</h3><p>Pick a scenario from your own job and run a full assign &rarr; verify &rarr; refine cycle. (Ch. 8)</p></div>
      <div><h3>Day 6</h3><p>Save your best assignment as a reusable template. (Ch. 16, 19)</p></div>
      <div><h3>Day 7</h3><p>Reflect: is this workflow stable enough to become a Skill? (Ch. 18)</p></div>
    </div>
  </section>

  <section class="band">
    <div class="section-heading">
      <h2>Safety &amp; disclaimer</h2>
    </div>
    <p class="section-copy">This handbook provides general AI workflow methods for self-study. It is <strong>not</strong> legal, financial, medical, security, or HR advice. AI assistants make mistakes &mdash; always verify outputs before acting on them, especially for external communications, financial figures, or consequential decisions. <strong>Keep a human in the loop for anything that matters.</strong></p>
    <p class="section-copy" style="margin-top:16px;">Do not feed confidential company data, personal information, credentials, or regulated content into AI tools without confirming your organization&rsquo;s data policies first. Tool names, interfaces, and capabilities change; treat this handbook as a method guide, not product documentation.</p>
    <p class="section-copy" style="margin-top:16px;">ChatGPT, Claude, Gemini, Codex, Claude Code, Gemini CLI, Notion, Gmail, and Outlook are trademarks of their respective owners. This handbook is independent and is not affiliated with, endorsed by, or sponsored by any of those products or companies.</p>
    <p class="section-copy" style="margin-top:16px;">Free public edition &mdash; share the original link freely. Commercial reuse (paid courses, training materials, consulting deliverables, or enterprise training resale) requires the author&rsquo;s explicit written permission.</p>
  </section>

  <section class="reading-section">
    <div>
      <h2>Read the full book</h2>
      <p>This is an English overview. The complete handbook is written in Traditional Chinese. The online reader includes a sticky table of contents and is mobile-friendly. A PDF is available for offline reading or printing.</p>
    </div>
    <div class="reading-actions">
      <a class="button primary" href="read.html">Read Chinese Edition</a>
      <a class="button" href="downloads/從零開始養成我的AI管家_免費公開版_v1.0.pdf">Download Chinese PDF</a>
    </div>
  </section>

  <section class="contact-section">
    <div class="contact-copy">
      <div class="section-heading">
        <h2>Get in touch</h2>
      </div>
      <p class="section-copy">Questions about the book, AI workflow adoption, or speaking and collaboration opportunities? Connect on LinkedIn or send an email to <a href="{CONTACT_MAILTO}">{CONTACT_EMAIL}</a>.</p>
      <div class="hero-actions">
        <a class="button" href="{LINKEDIN_URL}" target="_blank" rel="noopener noreferrer">LinkedIn &mdash; Farceur Liu</a>
        <a class="button" href="{CONTACT_MAILTO}">Email</a>
      </div>
    </div>
  </section>
</main>
<footer>
  <p>&copy; 2026 <a href="{LINKEDIN_URL}" target="_blank" rel="noopener noreferrer">Farceur Liu</a>. Free to share with original link. Commercial reuse requires explicit permission. Contact: <a href="{CONTACT_MAILTO}">{CONTACT_EMAIL}</a>.</p>
</footer>"""
    return html_page_en(
        "AI Work Assistant Handbook — English Overview",
        body,
        "An English overview of a Traditional Chinese self-study handbook for building repeatable AI workflows and an AI work assistant.",
        path="english.html",
    )


def build_linkedin_entry() -> str:
    body = f"""<header class="site-header">
  <a class="brand" href="index.html">AI Workflow Handbook</a>
  <nav aria-label="LinkedIn entry navigation">
    <a href="index.html">Public Site</a>
    <a href="read.html">Read Online</a>
    <a href="english.html">English Overview</a>
  </nav>
</header>
<main class="linkedin-entry">
  <section class="hero launch-hero">
    <div class="hero-copy">
      <p class="eyebrow">Free Public Handbook</p>
      <h1><span>AI Work Assistant</span><span>Handbook</span></h1>
      <p class="lead"><span>A practical self-study guide for building repeatable AI workflows.</span><span>Original Chinese title: 從零開始養成我的 AI 管家</span></p>
      <div class="hero-actions">
        <a class="button primary" href="index.html">Open Public Site</a>
        <a class="button" href="read.html">Read Online</a>
        <a class="button" href="english.html">English Overview</a>
      </div>
      <div class="proof-row" aria-label="Handbook highlights">
        <span><strong>v1.0</strong> Free public edition</span>
        <span><strong>22</strong> chapters</span>
        <span><strong>4</strong> Skill cases</span>
      </div>
    </div>
    <div class="hero-showcase launch-showcase" aria-label="Handbook preview">
      <figure class="cover launch-cover">
        <img src="assets/cover-preview.png" alt="AI work assistant handbook cover preview">
      </figure>
    </div>
  </section>

  <section class="thesis-section launch-thesis">
    <h2>Use fewer tools. Build better workflows.</h2>
    <p>This lightweight page is a LinkedIn-safe entry point for the handbook. The full site contains the public landing page, online reader, PDF download, and author contact information.</p>
  </section>
</main>
<footer>
  <p>&copy; 2026 <a href="{LINKEDIN_URL}" target="_blank" rel="noopener noreferrer">Farceur Liu</a>. Contact: <a href="{CONTACT_MAILTO}">{CONTACT_EMAIL}</a>.</p>
</footer>"""
    return html_page_en(
        "AI Work Assistant Handbook | Farceur Liu",
        body,
        "A free public self-study handbook for building repeatable AI workflows and an AI work assistant.",
        path="linkedin.html",
    )


def build_styles() -> str:
    return """
:root {
  color-scheme: light;
  --ink: #101828;
  --muted: #667085;
  --line: #d6dfeb;
  --soft: #f3f7fc;
  --paper: #ffffff;
  --accent: #2563eb;
  --accent-dark: #1d4ed8;
  --accent-ink: #12306f;
  --teal: #0f766e;
  --accent-soft: rgba(37, 99, 235, 0.10);
  --shadow-soft: 0 1px 0 rgba(15, 23, 42, 0.05), 0 24px 60px rgba(30, 64, 175, 0.10);
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  color: var(--ink);
  background:
    linear-gradient(rgba(37, 99, 235, .035) 1px, transparent 1px),
    linear-gradient(90deg, rgba(37, 99, 235, .03) 1px, transparent 1px),
    linear-gradient(180deg, #ffffff 0, #f6f9fd 42rem, #ffffff 78rem);
  background-size: 40px 40px, 40px 40px, auto;
  line-height: 1.7;
  overflow-x: hidden;
}
a { color: inherit; }
.site-header {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 24px;
  padding: 16px 32px;
  background: rgba(255, 255, 255, .92);
  border-bottom: 1px solid var(--line);
  backdrop-filter: blur(12px);
}
.brand {
  font-weight: 800;
  text-decoration: none;
  color: var(--accent-dark);
}
nav {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  color: var(--muted);
  font-size: 14px;
}
nav a {
  text-decoration: none;
}
nav a.active,
nav a:hover {
  color: var(--accent-dark);
}
main {
  width: min(1200px, calc(100% - 40px));
  margin: 0 auto;
}
.hero {
  position: relative;
  min-height: auto;
  display: grid;
  grid-template-columns: minmax(0, 1.08fr) minmax(340px, 460px);
  gap: 72px;
  align-items: center;
  padding: 76px 0 72px;
}
.launch-hero {
  overflow: hidden;
  border-bottom: 1px solid rgba(37, 99, 235, .12);
}
.launch-hero::before,
.launch-hero::after {
  content: "";
  position: absolute;
  pointer-events: none;
  z-index: 0;
}
.launch-hero::before {
  left: clamp(-430px, -30vw, -180px);
  top: -190px;
  width: clamp(520px, 68vw, 900px);
  height: clamp(760px, 76vw, 1040px);
  border-radius: 50%;
  background: rgba(42, 111, 255, .086);
}
.launch-hero::after {
  right: clamp(-520px, -34vw, -220px);
  top: 42px;
  width: clamp(520px, 68vw, 860px);
  height: clamp(640px, 70vw, 880px);
  border-radius: 50%;
  background: rgba(20, 184, 166, .055);
}
.launch-hero > * {
  position: relative;
  z-index: 1;
}
.hero-copy h1 {
  max-width: 760px;
  margin: 0 0 18px;
  font-size: clamp(42px, 7vw, 80px);
  line-height: 1.05;
  letter-spacing: 0;
  overflow-wrap: anywhere;
}
.hero-copy h1 span {
  display: block;
}
.lead {
  max-width: 720px;
  font-size: 22px;
  color: var(--muted);
  overflow-wrap: anywhere;
}
.lead span {
  display: block;
}
.eyebrow {
  margin: 0 0 8px;
  color: var(--accent-dark);
  font-size: 14px;
  font-weight: 800;
  letter-spacing: 0;
}
.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 30px;
}
.proof-row {
  display: flex;
  flex-wrap: wrap;
  gap: 16px 24px;
  margin-top: 30px;
  color: var(--muted);
  font-size: 14px;
}
.proof-row span {
  display: inline-flex;
  align-items: baseline;
  gap: 7px;
}
.proof-row strong {
  color: var(--accent-dark);
  font-size: 20px;
}
.hero-note {
  margin: 22px 0 0;
  color: var(--muted);
  font-size: 14px;
}
.button {
  display: inline-flex;
  align-items: center;
  min-height: 46px;
  padding: 10px 19px;
  border: 1px solid var(--line);
  border-radius: 6px;
  background: var(--paper);
  color: var(--ink);
  font-weight: 750;
  text-decoration: none;
}
.button.primary {
  background: linear-gradient(135deg, var(--accent-dark) 0%, var(--accent) 100%);
  border-color: var(--accent);
  color: white;
}
.button:hover {
  border-color: var(--accent);
  color: var(--accent-dark);
}
.button.primary:hover {
  color: white;
}
.button.ghost {
  background: transparent;
}
.cover {
  margin: 0;
}
.hero-showcase {
  position: relative;
}
.launch-showcase {
  display: grid;
  justify-items: end;
}
.cover img {
  width: 100%;
  display: block;
  border: 1px solid var(--line);
  border-radius: 8px;
  box-shadow: var(--shadow-soft);
  background: white;
}
.launch-cover {
  width: min(390px, 88%);
}
.band,
.split,
.workflow-section,
.contact-section,
.problem-section,
.reading-section {
  padding: 64px 0;
  border-top: 1px solid var(--line);
}
.thesis-section {
  display: grid;
  grid-template-columns: minmax(0, .95fr) minmax(320px, .82fr);
  gap: 48px;
  align-items: end;
  padding: 58px 0;
}
.launch-thesis {
  border-top: 0;
  border-bottom: 1px solid var(--line);
}
.thesis-section p {
  margin: 0;
  color: var(--muted);
  font-size: 18px;
}
.section-heading {
  max-width: 720px;
  margin-bottom: 26px;
}
h2 {
  margin: 0;
  font-size: clamp(28px, 4vw, 44px);
  line-height: 1.15;
  letter-spacing: 0;
  overflow-wrap: anywhere;
}
h3 {
  margin: 0 0 8px;
  font-size: 20px;
  letter-spacing: 0;
}
.problem-section {
  border-top: 0;
}
.problem-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
}
.problem-grid > div {
  padding: 24px 0 0;
  border-top: 2px solid rgba(37, 99, 235, .28);
}
.problem-grid span {
  display: block;
  margin-bottom: 14px;
  color: var(--teal);
  font-weight: 800;
  font-size: 13px;
}
.problem-grid p {
  margin: 0;
  color: var(--muted);
}
.outcome-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 18px;
}
.outcome-grid > div,
.reader-list p,
.chapter-grid a {
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--paper);
  box-shadow: 0 1px 0 rgba(15, 23, 42, 0.04);
}
.outcome-grid > div {
  padding: 22px;
}
.outcome-grid p,
.split p,
.section-copy {
  color: var(--muted);
}
.section-copy {
  max-width: 760px;
  margin: 0;
}
.split {
  display: grid;
  grid-template-columns: minmax(0, .9fr) minmax(280px, .7fr);
  gap: 42px;
  align-items: start;
}
.workflow-section {
  border-top-color: rgba(37, 99, 235, .20);
  border-bottom: 1px solid var(--line);
}
.workflow-steps {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
}
.workflow-steps > div {
  min-height: 190px;
  padding: 20px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
}
.workflow-steps span {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  margin-bottom: 18px;
  border-radius: 999px;
  background: var(--accent-soft);
  color: var(--accent-dark);
  font-weight: 800;
  font-size: 13px;
}
.workflow-steps strong {
  display: block;
  margin-bottom: 8px;
  font-size: 18px;
}
.workflow-steps p {
  margin: 0;
  color: var(--muted);
}
.reading-section {
  display: grid;
  grid-template-columns: minmax(0, .92fr) minmax(260px, .44fr);
  gap: 44px;
  align-items: center;
  padding: 54px min(5vw, 58px);
  border: 1px solid rgba(37, 99, 235, .18);
  border-radius: 8px;
  background: #ffffff;
  box-shadow: 0 1px 0 rgba(15, 23, 42, .04);
}
.reading-section p {
  max-width: 760px;
  color: var(--muted);
}
.reading-actions {
  display: grid;
  gap: 12px;
}
.contact-section {
  position: relative;
  overflow: hidden;
  margin-top: 8px;
  padding: 52px min(5vw, 58px);
  border: 1px solid rgba(37, 99, 235, .18);
  border-radius: 8px;
  background: #ffffff;
}
.contact-section::before {
  content: "";
  position: absolute;
  left: clamp(-300px, -24vw, -150px);
  top: -180px;
  width: clamp(420px, 54vw, 640px);
  height: clamp(520px, 58vw, 720px);
  border-radius: 50%;
  background: rgba(42, 111, 255, .07);
  pointer-events: none;
}
.contact-section::after {
  content: "";
  position: absolute;
  right: clamp(-340px, -28vw, -180px);
  top: 16px;
  width: clamp(420px, 58vw, 680px);
  height: clamp(500px, 56vw, 700px);
  border-radius: 50%;
  background: rgba(20, 184, 166, .052);
  pointer-events: none;
}
.contact-section > * {
  position: relative;
  z-index: 1;
}
.contact-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(260px, 340px);
  gap: 36px;
  align-items: center;
}
.contact-copy {
  min-width: 0;
}
.linkedin-badge-card {
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.linkedin-badge-card > .LI-profile-badge > .LI-simple-link {
  display: none !important;
}
.reader-list {
  display: grid;
  gap: 10px;
}
.reader-list p {
  margin: 0;
  padding: 14px 16px;
  color: var(--ink);
}
.chapter-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}
.chapter-grid a {
  padding: 13px 15px;
  text-decoration: none;
}
.chapter-grid a:hover {
  border-color: var(--accent);
}
footer {
  max-width: 1180px;
  margin: 0 auto;
  padding: 28px 20px 44px;
  color: var(--muted);
  font-size: 14px;
}
.reader-layout {
  width: min(1320px, calc(100% - 40px));
  display: grid;
  grid-template-columns: 260px minmax(0, 1fr);
  gap: 36px;
  align-items: start;
  padding: 34px 0 60px;
}
.toc {
  position: sticky;
  top: 82px;
  max-height: calc(100vh - 110px);
  overflow: auto;
  padding: 16px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--paper);
}
.toc strong {
  display: block;
  margin-bottom: 10px;
}
.toc a {
  display: block;
  padding: 6px 0;
  color: var(--muted);
  font-size: 14px;
  text-decoration: none;
}
.toc .toc-l3 {
  padding-left: 14px;
  font-size: 13px;
}
.toc a:hover {
  color: var(--accent-dark);
}
.book {
  min-width: 0;
  padding: 42px min(7vw, 72px);
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--paper);
}
.book h1 {
  margin: 0 0 28px;
  font-size: clamp(34px, 5vw, 58px);
  line-height: 1.12;
  letter-spacing: 0;
}
.book h2 {
  margin-top: 54px;
  padding-top: 24px;
  border-top: 1px solid var(--line);
}
.book h3 {
  margin-top: 32px;
}
.book h4,
.book h5,
.book h6 {
  margin-top: 24px;
  font-size: 17px;
}
.book p,
.book li {
  color: #26323a;
}
blockquote {
  margin: 20px 0;
  padding: 14px 18px;
  border-left: 4px solid var(--accent);
  background: var(--accent-soft);
  color: #1e3a5f;
}
pre {
  overflow: auto;
  padding: 16px;
  border-radius: 8px;
  background: #0f1724;
  color: #f8fbff;
}
code {
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: .92em;
}
p code,
li code {
  padding: 2px 5px;
  border-radius: 4px;
  background: var(--accent-soft);
  color: var(--accent-dark);
}
.table-wrap {
  overflow-x: auto;
  margin: 20px 0;
}
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}
th,
td {
  padding: 10px 12px;
  border: 1px solid var(--line);
  vertical-align: top;
}
th {
  background: var(--soft);
  text-align: left;
}
@media (max-width: 900px) {
  .site-header,
  .hero,
  .split,
  .thesis-section,
  .reader-layout,
  .problem-grid,
  .outcome-grid,
  .workflow-steps,
  .chapter-grid,
  .reading-section {
    grid-template-columns: 1fr;
  }
  .site-header {
    position: static;
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
    padding: 14px 20px;
  }
  nav {
    width: 100%;
    overflow-x: auto;
    padding-bottom: 2px;
  }
  .hero {
    min-height: auto;
    padding-top: 34px;
    gap: 34px;
  }
  .hero-copy h1 {
    font-size: 38px;
    line-height: 1.12;
  }
  .lead {
    font-size: 19px;
  }
  .hero-actions {
    display: grid;
    grid-template-columns: 1fr;
  }
  .button {
    justify-content: center;
    width: 100%;
  }
  .cover {
    max-width: 280px;
  }
  .launch-showcase {
    justify-items: start;
  }
  .launch-cover {
    width: min(280px, 100%);
  }
  .problem-grid > div {
    padding-top: 18px;
  }
  .reading-section {
    padding: 34px 20px;
  }
  .contact-section {
    padding: 34px 20px;
  }
  .contact-layout {
    grid-template-columns: 1fr;
  }
  .linkedin-badge-card {
    justify-content: flex-start;
  }
  .toc {
    position: static;
    max-height: none;
  }
  .book {
    padding: 28px 20px;
  }
}
"""


def main() -> None:
    markdown = SOURCE_MD.read_text(encoding="utf-8")
    if not SOCIAL_PREVIEW.exists():
        raise FileNotFoundError(f"Missing social preview image: {SOCIAL_PREVIEW}")
    content_html, toc = markdown_to_html(markdown)

    write(ROOT / "index.html", build_index(toc))
    write(ROOT / "read.html", build_read(content_html, toc))
    write(ROOT / "english.html", build_english())
    write(ROOT / "linkedin.html", build_linkedin_entry())
    write(ROOT / "assets" / "styles.css", build_styles())
    write(ROOT / ".nojekyll", "")

    downloads = ROOT / "downloads"
    downloads.mkdir(parents=True, exist_ok=True)
    copy_if_different(SOURCE_MD, downloads / "從零開始養成我的AI管家_公開版.md")

    assets = ROOT / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    if COVER_PREVIEW.exists() and not (assets / "cover-preview.png").exists():
        shutil.copy2(COVER_PREVIEW, assets / "cover-preview.png")


if __name__ == "__main__":
    main()
