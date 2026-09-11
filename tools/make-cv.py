#!/usr/bin/env python3
"""Generate files/Domagoj_Knez_CV.pdf in the same visual language as knez.dev.

    python3 -m venv .venv && .venv/bin/pip install reportlab
    .venv/bin/python tools/make-cv.py
"""
from pathlib import Path
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "files" / "Domagoj_Knez_CV.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

for name, file in [
    ("Disp", "BricolageGrotesque-700.ttf"), ("DispSemi", "BricolageGrotesque-600.ttf"),
    ("Sans", "SpaceGrotesk-400.ttf"), ("SansMed", "SpaceGrotesk-500.ttf"),
    ("SansBold", "SpaceGrotesk-700.ttf"),
    ("Mono", "JetBrainsMono-400.ttf"), ("MonoMed", "JetBrainsMono-500.ttf"),
]:
    pdfmetrics.registerFont(TTFont(name, str(HERE / "fonts" / file)))

# Catppuccin Latte — the site's light theme, and it prints cleanly
INK   = HexColor("#3C3F55")
INK2  = HexColor("#5C6070")
INK3  = HexColor("#8C90A0")
ACC   = HexColor("#3D7D22")
LINE  = HexColor("#DCE0E8")
BAND  = HexColor("#EFF1F5")
WHITE = HexColor("#FFFFFF")

W, H = A4
SIDE_W = 188.0
M = 30.0                      # sidebar inner margin
CX = SIDE_W + 32              # main column x
CW = W - CX - 38              # main column width
TOP = H - 46
BOTTOM = 44

MULTIPAGE = False
c = rl_canvas.Canvas(str(OUT), pagesize=A4)
c.setTitle("Domagoj Knez — Full-Stack Software Engineer")
c.setAuthor("Domagoj Knez")
c.setSubject("Curriculum vitae")
c.setKeywords("full-stack engineer, Python, Django, TypeScript, React, AWS, Zagreb")


def wrap(text, font, size, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if pdfmetrics.stringWidth(trial, font, size) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def band(page_first=True):
    c.setFillColor(BAND)
    c.rect(0, 0, SIDE_W, H, stroke=0, fill=1)


def para(x, y, text, font, size, colour, width, leading, space_after=0):
    c.setFont(font, size)
    c.setFillColor(colour)
    for ln in wrap(text, font, size, width):
        c.drawString(x, y, ln)
        y -= leading
    return y - space_after


def label(x, y, text, width=None, colour=None):
    up = text.upper()
    t = c.beginText(x, y)
    t.setFont("MonoMed", 6.6)
    t.setFillColor(colour or ACC)
    t.setCharSpace(1.5)
    t.textOut(up)
    t.setCharSpace(0)
    c.drawText(t)
    if width:
        c.setStrokeColor(LINE)
        c.setLineWidth(0.6)
        tw = pdfmetrics.stringWidth(up, "MonoMed", 6.6) + 1.5 * len(up) + 10
        c.line(x + tw, y + 2.2, x + width, y + 2.2)
    return y - 14


# ───────────────────────── page 1: sidebar ─────────────────────────
band()
sx, sw = M, SIDE_W - 2 * M
y = TOP

photo = ROOT / "assets" / "portrait.jpg"
if photo.exists():
    ps = 86.0
    c.saveState()
    p = c.beginPath()
    p.roundRect(sx, y - ps, ps, ps, 10)
    c.clipPath(p, stroke=0)
    img = ImageReader(str(photo))
    iw, ih = img.getSize()
    s = max(ps / iw, ps / ih)
    dw, dh = iw * s, ih * s
    c.drawImage(img, sx - (dw - ps) / 2, y - ps - (dh - ps) * 0.82, dw, dh, mask=None)
    c.restoreState()
    y -= ps + 20

c.setFont("Disp", 23)
c.setFillColor(INK)
c.drawString(sx, y, "Domagoj")
y -= 24
c.drawString(sx, y, "Knez")
y -= 17
c.setFont("SansMed", 9)
c.setFillColor(ACC)
c.drawString(sx, y, "Full-Stack Software Engineer")
y -= 26

y = label(sx, y, "Contact")
c.setFont("Mono", 7.1)
for line in ["domagoj@coretech.hr", "+385 98 191 7958", "Zagreb, Croatia",
             "knez.dev", "linkedin.com/in/dknez", "github.com/domknez"]:
    c.setFillColor(INK2)
    c.drawString(sx, y, line)
    y -= 11.4
y -= 12

y = label(sx, y, "Skills")
SKILLS = [
    ("Backend", "Python, Django, DRF, FastAPI, SQLAlchemy, Node.js, Nest.js, Hono, Java, Spring Boot"),
    ("Frontend", "TypeScript, React, Next.js, RTK Query, D3.js"),
    ("Data", "PostgreSQL, MySQL, OracleDB, Redis, Apache Solr"),
    ("Cloud & infra", "AWS, Azure, GCP, Cloudflare, Docker, Kubernetes, Terraform, Ansible"),
    ("Also", "REST, gRPC, SOAP, microservices, SAP Hybris, Camunda BPM"),
]
for head, items in SKILLS:
    c.setFont("SansBold", 7.6)
    c.setFillColor(INK)
    c.drawString(sx, y, head)
    y -= 10.2
    y = para(sx, y, items, "Sans", 7.4, INK2, sw, 9.6, 8)
y -= 4

y = label(sx, y, "Education")
for deg, place, when in [
    ("MSc, Information and Communication Technology", "FER, University of Zagreb", "2012"),
    ("BSc, Computing", "FER, University of Zagreb", "2010"),
]:
    y = para(sx, y, deg, "SansBold", 7.6, INK, sw, 9.6)
    y = para(sx, y, place + " · " + when, "Sans", 7.2, INK3, sw, 9.4, 8)
y -= 4

y = label(sx, y, "Certifications")
for cert in [
    "SAP Certified Development Professional — SAP Hybris Commerce 6.2 Developer, 2018",
    "SAP Certified Product Support Specialist — SAP Hybris Commerce 6.0, 2018",
]:
    y = para(sx, y, cert, "Sans", 7.2, INK2, sw, 9.4, 8)
y -= 4

y = label(sx, y, "Languages")
for lang, level in [("Croatian", "Native"), ("English", "Full professional"), ("German", "Limited working")]:
    c.setFont("SansBold", 7.4)
    c.setFillColor(INK)
    c.drawString(sx, y, lang)
    c.setFont("Sans", 7.2)
    c.setFillColor(INK3)
    c.drawRightString(sx + sw, y, level)
    y -= 11


# ───────────────────────── page flow ─────────────────────────
def sidebar_continued():
    band()
    c.setFont("Disp", 15)
    c.setFillColor(INK)
    c.drawString(M, TOP - 4, "Domagoj")
    c.drawString(M, TOP - 20, "Knez")
    c.setFont("Mono", 6.9)
    c.setFillColor(INK3)
    c.drawString(M, TOP - 40, "domagoj@coretech.hr")
    c.drawString(M, TOP - 51, "knez.dev")


def new_page():
    global MULTIPAGE
    MULTIPAGE = True
    c.setFont("Mono", 6.6)
    c.setFillColor(INK3)
    c.drawString(M, BOTTOM, "Page %d" % c.getPageNumber())
    c.showPage()
    sidebar_continued()
    return label(CX, TOP, "Experience — continued", CW)


def block_height(lines_specs):
    return sum(n * lead for n, lead in lines_specs)

# ───────────────────────── page 1: main column ─────────────────────────
y = TOP
y = label(CX, y, "Profile", CW)
y = para(CX, y,
         "Full-stack engineer, thirteen years across telecom, e-commerce, payments, insurance, accounting "
         "SaaS, eSIM connectivity and industrial AI. Own consultancy since 2020, working end to end: Python "
         "and Django on one side, TypeScript and React on the other, AWS, Azure or GCP underneath.",
         "Sans", 8.1, INK2, CW, 11.0, 13)

y = label(CX, y, "Experience", CW)


def company(y, name, role, dates, blurb=None):
    need = 22 + (len(wrap(blurb, "Sans", 7.9, CW)) * 10.4 if blurb else 0) + 38
    if y - need < BOTTOM:
        y = new_page()
    c.setFont("DispSemi", 11.5)
    c.setFillColor(INK)
    c.drawString(CX, y, name)
    c.setFont("Mono", 7)
    c.setFillColor(INK3)
    c.drawRightString(CX + CW, y + 0.6, dates)
    y -= 11.0
    c.setFont("SansMed", 8.0)
    c.setFillColor(ACC)
    c.drawString(CX, y, role)
    y -= 11
    if blurb:
        y = para(CX, y, blurb, "Sans", 7.9, INK2, CW, 10.4, 2)
    return y


def project(y, name, role, desc, tech):
    need = 11 + len(wrap(desc, "Sans", 7.9, CW - 11)) * 10.1 + len(wrap(tech, "Mono", 6.6, CW - 11)) * 8.6 + 10
    if y - need < BOTTOM:
        y = new_page()
    c.setFillColor(ACC)
    c.rect(CX + 1.5, y + 2.2, 3, 3, stroke=0, fill=1)
    c.setFont("SansBold", 8.6)
    c.setFillColor(INK)
    c.drawString(CX + 11, y, name)
    off = pdfmetrics.stringWidth(name, "SansBold", 8.6) + 17
    if role:
        c.setFont("Mono", 6.8)
        c.setFillColor(INK3)
        c.drawString(CX + off, y + 0.4, role)
    y -= 10.2
    y = para(CX + 11, y, desc, "Sans", 7.9, INK2, CW - 11, 10.1, 1)
    y = para(CX + 11, y, tech, "Mono", 6.6, INK3, CW - 11, 8.6, 6)
    return y


y = company(y, "CoreTech d.o.o.", "Owner & Consultant", "2020 — present",
            "Independent consultancy — long engagements, owning a slice of the product end to end. "
            "Projects listed alphabetically.")
y -= 2

y = project(y, "Bondio", "Senior engineer",
            "eSIM connectivity API for travel businesses, IoT platforms and resellers — 1000+ networks across 200+ "
            "countries. Backend services and the customer-facing dashboard.",
            "Nest.js · React · AWS · Terraform · Docker")
y = project(y, "Fondion", "",
            "ERP for the construction industry. Python backend, React frontend optimisation, and the team's migration "
            "from hand-written SQL to the SQLAlchemy ORM.",
            "Python · FastAPI · SQLAlchemy · Alembic · React · PostgreSQL · AWS · Docker")
y = project(y, "MontBlancAI", "Lead engineer",
            "Industrial AI platform helping machine manufacturers cut downtime and optimise maintenance. Full product "
            "stack: the interface, the backend services, and the Alpinist AI core that turns machine data into insight.",
            "Django · DRF · React · TypeScript · RTK Query · D3.js · PostgreSQL · Azure · Docker")
y = project(y, "Takeaway", "",
            "Mobile food and drink ordering system taken from MVP to production. Backend refactoring, streamlined "
            "build and test pipelines, new features.",
            "Node.js · Hapi · JavaScript · Vue.js · PostgreSQL · Redis · Docker")
y = project(y, "Tiketti", "Team lead",
            "Event ticketing platform, plus a block builder vendors use to assemble their own pages. Rebuilt the legacy "
            "translation tool into the monorepo, folded it into the Next.js app and reworked S3 and R2 handling.",
            "Node.js · Next.js · TypeScript · Hono · Cloudflare · AWS · Terraform · Docker")

y = company(y, "FreshBooks", "Senior Software Engineer & Team Lead", "Jun 2021 — Nov 2024",
            "Django microservice with DRF fronting core services, serving REST APIs to two React applications. Moved "
            "into a lead role for two engineers while staying hands-on.")
y = para(CX, y, "Python · Django · DRF · React · Tailwind · MySQL · GCP · Docker",
         "Mono", 6.6, INK3, CW, 8.6, 12)

y = company(y, "Adcubum", "Senior Software Engineer", "Dec 2019 — Jun 2021",
            "Microservice for communication with German and Swiss insurance associations, supporting vehicle "
            "registration inside a move to microservice architecture.")
y = para(CX, y, "Java · Spring Boot · OracleDB · Kubernetes · gRPC · Camunda BPM · Docker",
         "Mono", 6.6, INK3, CW, 8.6, 12)

y = company(y, "Verso Altima Group", "Java Developer Expert", "May 2017 — Dec 2019",
            "Lead developer on the Payment Gateway: a proxy integrating the new SAP Hybris webshop with a range of "
            "payment providers.")
y = para(CX, y, "Java · Spring · SAP Hybris · Apache Solr · Nginx · REST · SOAP · Ansible",
         "Mono", 6.6, INK3, CW, 8.6, 12)

y = company(y, "mStart d.o.o.", "E-Commerce Specialist", "Feb 2016 — May 2017",
            "Developed Abrakadabra, a new e-commerce platform.")
y = para(CX, y, "Spring · Maven · Apache Solr · Nginx · REST", "Mono", 6.6, INK3, CW, 8.6, 12)

y = company(y, "Ericsson Nikola Tesla d.d.", "Software Developer", "Sep 2013 — Feb 2016",
            "Requirements analysis and automated test cases; new test environments and automated test flows.")
y = para(CX, y, "C · Erlang · Java · JUnit · Spring · Git · Bash", "Mono", 6.6, INK3, CW, 8.6, 12)

if y - 26 < BOTTOM:
    y = new_page()
c.setStrokeColor(LINE)
c.setLineWidth(0.6)
c.line(CX, y + 4, CX + CW, y + 4)
y -= 10
c.setFont("Mono", 6.8)
c.setFillColor(INK3)
c.drawString(CX, y, "References available on request.")

if MULTIPAGE:
    c.setFont("Mono", 6.6)
    c.setFillColor(INK3)
    c.drawString(M, BOTTOM, "Page %d" % c.getPageNumber())
c.save()
print("wrote", OUT, OUT.stat().st_size, "bytes")
