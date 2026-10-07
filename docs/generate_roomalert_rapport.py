#!/usr/bin/env python3
"""Genereer RoomAlert concurrentie-onderzoek PDF."""

from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUT = Path("/opt/cursor/artifacts/RoomAlert_Concurrentieonderzoek.pdf")
OUT_REPO = Path("/workspace/docs/RoomAlert_Concurrentieonderzoek.pdf")

PAGE_W, PAGE_H = A4
MARGIN = 1.8 * cm

# Calm professional palette (not purple/cream AI defaults)
INK = colors.HexColor("#1A1F2E")
MUTED = colors.HexColor("#5C6578")
ACCENT = colors.HexColor("#0E7C6B")
ACCENT_LIGHT = colors.HexColor("#E6F5F2")
LINE = colors.HexColor("#D8DEE9")
HEADER_BG = colors.HexColor("#1A1F2E")
ROW_ALT = colors.HexColor("#F7F8FA")
WARN = colors.HexColor("#8B4513")
WHITE = colors.white


def styles():
    base = getSampleStyleSheet()
    s = {}
    s["cover_brand"] = ParagraphStyle(
        "cover_brand",
        parent=base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=ACCENT,
        alignment=TA_CENTER,
        spaceAfter=8,
        tracking=1,
    )
    s["cover_title"] = ParagraphStyle(
        "cover_title",
        parent=base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=26,
        leading=32,
        textColor=INK,
        alignment=TA_CENTER,
        spaceAfter=12,
    )
    s["cover_sub"] = ParagraphStyle(
        "cover_sub",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=17,
        textColor=MUTED,
        alignment=TA_CENTER,
        spaceAfter=6,
    )
    s["h1"] = ParagraphStyle(
        "h1",
        parent=base["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        textColor=INK,
        spaceBefore=18,
        spaceAfter=10,
        borderPadding=0,
    )
    s["h2"] = ParagraphStyle(
        "h2",
        parent=base["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=ACCENT,
        spaceBefore=14,
        spaceAfter=6,
    )
    s["body"] = ParagraphStyle(
        "body",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=INK,
        alignment=TA_JUSTIFY,
        spaceAfter=7,
    )
    s["bullet"] = ParagraphStyle(
        "bullet",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13,
        textColor=INK,
        leftIndent=2,
        spaceAfter=3,
    )
    s["cell"] = ParagraphStyle(
        "cell",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10.5,
        textColor=INK,
    )
    s["cell_h"] = ParagraphStyle(
        "cell_h",
        parent=base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10.5,
        textColor=WHITE,
    )
    s["callout"] = ParagraphStyle(
        "callout",
        parent=base["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=10,
        leading=14,
        textColor=INK,
        alignment=TA_CENTER,
    )
    s["footer"] = ParagraphStyle(
        "footer",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=8,
        textColor=MUTED,
        alignment=TA_CENTER,
    )
    s["meta"] = ParagraphStyle(
        "meta",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=9,
        textColor=MUTED,
        alignment=TA_CENTER,
        spaceAfter=4,
    )
    s["verdict"] = ParagraphStyle(
        "verdict",
        parent=base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        textColor=INK,
        spaceAfter=6,
    )
    return s


def p(text, style):
    return Paragraph(text, style)


def bullets(items, style):
    return ListFlowable(
        [ListItem(Paragraph(i, style), leftIndent=8, bulletColor=ACCENT) for i in items],
        bulletType="bullet",
        start="•",
        leftIndent=12,
        bulletFontSize=9,
        spaceBefore=2,
        spaceAfter=8,
    )


def table(data, col_widths, header=True):
    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    style_cmds = [
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("TEXTCOLOR", (0, 0), (-1, -1), INK),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, ROW_ALT]),
    ]
    if header:
        style_cmds += [
            ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("TOPPADDING", (0, 0), (-1, 0), 6),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ]
    t.setStyle(TableStyle(style_cmds))
    return t


def callout_box(text, s):
    inner = Paragraph(text, s["callout"])
    t = Table([[inner]], colWidths=[PAGE_W - 2 * MARGIN - 4 * mm])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), ACCENT_LIGHT),
                ("BOX", (0, 0), (-1, -1), 1.2, ACCENT),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    return t


def add_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 1.2 * cm, PAGE_W - MARGIN, 1.2 * cm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(MARGIN, 0.7 * cm, "RoomAlert — Concurrentieonderzoek (vertrouwelijk)")
    canvas.drawRightString(PAGE_W - MARGIN, 0.7 * cm, f"Pagina {doc.page}")
    canvas.restoreState()


def build():
    s = styles()
    story = []

    # —— Cover ——
    story.append(Spacer(1, 3.2 * cm))
    story.append(p("ROOMALERT.NL", s["cover_brand"]))
    story.append(p("Concurrentieonderzoek &amp; productadvies", s["cover_title"]))
    story.append(
        p(
            "Diepe analyse van de Nederlandse huur-alertmarkt,<br/>positionering en wat te bouwen om uniek én winstgevend te worden.",
            s["cover_sub"],
        )
    )
    story.append(Spacer(1, 1.2 * cm))
    story.append(callout_box("Abonnement: €1 proef · na 7 dagen €14,99 / maand", s))
    story.append(Spacer(1, 1.5 * cm))
    story.append(p(f"Datum: {date.today().strftime('%d %B %Y')}", s["meta"]))
    story.append(p("Bronnen: roomalert.nl, stekkies.com, rentslam.com, kamernet.nl, woonbusters.nl e.a.", s["meta"]))
    story.append(p("Opgesteld als intern strategierapport", s["meta"]))
    story.append(PageBreak())

    # —— 1. Samenvatting ——
    story.append(p("1. Samenvatting", s["h1"]))
    story.append(
        p(
            "RoomAlert is een Telegram-gebaseerde alertdienst voor kamers en studio’s in Amsterdam en Utrecht. "
            "Gebruikers stellen filters in, krijgen een melding bij passend aanbod, en kunnen reageren via de bot "
            "zonder telefoonnummer te delen. Aanbod komt uit eigen plaatsingen plus Roofz en Woongroep.net. "
            "Grote platforms (Facebook, Kamernet, Pararius, Funda) worden bewust niet gelezen.",
            s["body"],
        )
    )
    story.append(
        p(
            "De Nederlandse alertmarkt is druk: meer dan twintig betaalde diensten claimen “eerste zijn”. "
            "Concurrenten als Stekkies en RentSlam mikken op breed huuraanbod (1000+ sites) tegen €16,65–€29,95. "
            "RoomAlert wint niet op volume-scraping. De kans zit in een smalle, geloofwaardige niche: "
            "<b>privacy-first kamerreacties + gecureerd aanbod + snelle Telegram-melding</b>.",
            s["body"],
        )
    )
    story.append(
        p(
            "Met het gekozen model (€1 proef, daarna €14,99/maand) is circa €5.000 omzet per maand haalbaar "
            "met ongeveer 335 actieve betalende zoekers — zonder Stekkies te imiteren.",
            s["body"],
        )
    )

    # —— 2. Product ——
    story.append(p("2. Wat RoomAlert nu is", s["h1"]))
    story.append(p("Kernproduct", s["h2"]))
    story.append(
        bullets(
            [
                "Kanaal: Telegram-bot (geen aparte app vereist)",
                "Doelgroep: studenten en starters in krappe studentensteden",
                "Steden live: Amsterdam en Utrecht (Rotterdam, Den Haag, Eindhoven, Groningen gepland)",
                "Filters: stad, max. huur, min. oppervlakte, vaste/langere huur, inschrijven",
                "USP’s: snelle melding, privacy bij reageren, eerlijk over bronnen, vetted eigen plaatsingen",
            ],
            s["bullet"],
        )
    )
    story.append(p("Sterktes", s["h2"]))
    story.append(
        bullets(
            [
                "Heldere, rustige positionering en transparante communicatie",
                "Privacy: verhuurder ziet voornaam + korte tekst, geen nummer/mail/Telegram-naam",
                "Lage drempel via Telegram",
                "Eigen aanbod wordt nagekeken vóór publicatie",
                "Eerlijk over wat wél en niet wordt gelezen — bouwt vertrouwen",
            ],
            s["bullet"],
        )
    )
    story.append(p("Zwaktes / risico’s", s["h2"]))
    story.append(
        bullets(
            [
                "Beperkt aanbod (weinig bronnen) → risico op lege of stille bot",
                "Alleen twee steden live",
                "Afhankelijkheid van Telegram (deel NL-zoekers mist WhatsApp)",
                "Nog geen webzoekervaring naast de bot",
                "Concurrentie scoort op “1000+ websites” — marketingpressure",
            ],
            s["bullet"],
        )
    )

    # —— 3. Concurrentie ——
    story.append(p("3. Concurrentielandschap", s["h1"]))
    story.append(
        p(
            "Er zijn grofweg drie categorieën: (A) brede huuralerts, (B) kamermarktplaatsen, "
            "(C) matching/swipe-apps. RoomAlert zit tussen A en B: alert + eigen reactieflow, "
            "maar kamer-first in plaats van alle huurwoningen.",
            s["body"],
        )
    )

    cell = s["cell"]
    cell_h = s["cell_h"]

    def C(t):
        return Paragraph(str(t), cell)

    def H(t):
        return Paragraph(str(t), cell_h)

    story.append(p("Vergelijkingstabel (prijzen peildatum juli 2026 / eigen sites)", s["h2"]))
    data = [
        [H("Speler"), H("Type"), H("Prijs"), H("Sterkte"), H("Zwakte t.o.v. RoomAlert")],
        [
            C("Stekkies"),
            C("Breed alert"),
            C("€16,65–29,95"),
            C("1000+ sites, speed, search buddy"),
            C("Duur, noise, niet kamer-first"),
        ],
        [
            C("RentSlam"),
            C("Breed alert + Telegram"),
            C("€16,65–29,95"),
            C("App + mail + Telegram, NL-breed"),
            C("Generiek; zelfde race als Stekkies"),
        ],
        [
            C("Kamernet"),
            C("Marktplaats"),
            C("€38 / 4 wkn"),
            C("Grootste kamervoorraad"),
            C("Paywall om te reageren; traag gevoel"),
        ],
        [
            C("Pararius+"),
            C("Eigen alert"),
            C("€29,95"),
            C("Professioneel aanbod"),
            C("Minder kamer-niche"),
        ],
        [
            C("WoonBusters"),
            C("Low-cost alert"),
            C("€3,99–5,99"),
            C("Prijsleider"),
            C("Minder privacy/kamer-USP"),
        ],
        [
            C("Dingdong e.a."),
            C("Match/swipe"),
            C("Vaak gratis"),
            C("Social matching"),
            C("Geen pure speed-alert"),
        ],
        [
            C("<b>RoomAlert</b>"),
            C("Kamer-alert + bot"),
            C("<b>€1 → €14,99</b>"),
            C("Privacy, eerlijkheid, Telegram"),
            C("Volume & steden nog beperkt"),
        ],
    ]
    story.append(table(data, [2.4 * cm, 2.8 * cm, 2.6 * cm, 4.2 * cm, 4.2 * cm]))
    story.append(Spacer(1, 0.4 * cm))
    story.append(
        p(
            "Conclusie concurrentie: <b>niet winnen op “meer scrapers”</b>. "
            "Winnen op vertrouwen, privacy, kamerkwaliteit en snelle, nette reacties.",
            s["body"],
        )
    )

    story.append(PageBreak())

    # —— 4. Monetisatie ——
    story.append(p("4. Monetisatie: €1 proef → €14,99", s["h1"]))
    story.append(
        p(
            "Gekozen model: <b>€1 proefperiode van 7 dagen</b>, daarna automatisch <b>€14,99 per maand</b>. "
            "Dit zit onder Stekkies/RentSlam (vaak €17–30) en onder Kamernet Premium, "
            "maar boven pure low-cost alerts. Dat past bij een premium-niche (privacy + kamer) zonder student-onvriendelijk te zijn.",
            s["body"],
        )
    )
    story.append(p("Pad naar €5.000 / maand", s["h2"]))
    monet = [
        [H("Metric"), H("Berekening"), H("Uitkomst")],
        [C("Doelomzet"), C("€5.000 / maand"), C("—")],
        [C("Prijs na proef"), C("€14,99"), C("—")],
        [C("Benodigde betalende zoekers"), C("5.000 ÷ 14,99"), C("~334 actieve abonnees")],
        [C("Met 60% proef→betaald"), C("334 ÷ 0,60"), C("~557 proefstarts / maand (steady state)")],
        [C("Met 40% proef→betaald"), C("334 ÷ 0,40"), C("~835 proefstarts / maand")],
    ]
    story.append(table(monet, [4.5 * cm, 5.5 * cm, 6.2 * cm]))
    story.append(Spacer(1, 0.35 * cm))
    story.append(
        p(
            "Let op: zoekers zoeken tijdelijk (vaak 4–12 weken). Churn is structureel. "
            "Daarom zijn <b>constante instroom</b> (campussen, content, partnerships) en "
            "<b>voldoende aanbod</b> belangrijker dan een eenmalige spike in trials.",
            s["body"],
        )
    )
    story.append(p("Aanbevolen gratis vs. betaald", s["h2"]))
    freemium = [
        [H("Gratis / €1-proef"), H("Betaald (€14,99)")],
        [
            C("Profiel aanmaken, filters, beperkte of delayed alerts, verkennen van de bot"),
            C("Instant meldingen, onbeperkt reageren via bot, scherpere filters, prioriteit bij piekuren"),
        ],
        [
            C("Kamer plaatsen (blijft gratis voor supply)"),
            C("Optioneel later: boost / spotlight voor verhuurders (tweede inkomstenlijn)"),
        ],
    ]
    story.append(table(freemium, [8.1 * cm, 8.1 * cm]))

    # —— 5. Wat bouwen ——
    story.append(p("5. Wat nog bouwen: uniek + winstgevend", s["h1"]))
    story.append(
        p(
            "Onderstaande prioriteit is bewust smal. Eerst bewijs dat zoekers betalen en verhuurders blijven, "
            "daarna steden uitbreiden.",
            s["body"],
        )
    )
    story.append(p("Fix now (hoogste impact)", s["h2"]))
    build_now = [
        [H("#"), H("Bouw"), H("Waarom"), H("Prioriteit")],
        [
            C("1"),
            C("Supply-engine"),
            C("Meer vetted eigen kamers + 3–5 legale kamerbronnen. Zonder volume geen retentie."),
            C("Kritiek"),
        ],
        [
            C("2"),
            C("Abonnement live (€1 → €14,99)"),
            C("Duidelijke paywall na 7 dagen; transparante prijs op site."),
            C("Kritiek"),
        ],
        [
            C("3"),
            C("Reactiekwaliteit"),
            C("Profiel + 1-tap reactie + anti-spam. Privacy blijft USP; verhuurders krijgen betere leads."),
            C("Hoog"),
        ],
        [
            C("4"),
            C("Verhuurder-inbox in Telegram"),
            C("Shortlist, interesseren/afwijzen, blokkeren. Houdt exclusief aanbod vast."),
            C("Hoog"),
        ],
    ]
    story.append(table(build_now, [1.0 * cm, 3.6 * cm, 8.5 * cm, 2.0 * cm]))

    story.append(p("Optimize later", s["h2"]))
    later = [
        [H("Bouw"), H("Wanneer")],
        [C("Stad 3 (bijv. Rotterdam of Groningen)"), C("Na bewezen conversie in AMS + Utrecht")],
        [C("WhatsApp naast Telegram"), C("Als Telegram-bereik de groei remt")],
        [C("Kamer-buddy (2 zoekers, 1 profiel)"), C("Na stabiele betaalde base")],
        [C("Scam-score / light verificatie"), C("Als differentiator t.o.v. Facebook-chaos")],
        [C("Uni / HBO partnerships"), C("Voor voorspelbare student-instroom")],
    ]
    story.append(table(later, [8.5 * cm, 7.7 * cm]))

    story.append(p("Niet bouwen (voorlopig)", s["h2"]))
    story.append(
        bullets(
            [
                "Race naar 1000+ scrapers tegen Stekkies/RentSlam",
                "Native iOS/Android app vóór product-market fit",
                "Volledige vrije-sector appartementen (verwatert de niche)",
                "“Wij reageren voor jou”-dienst (€80+/mnd) — te operationeel zwaar",
            ],
            s["bullet"],
        )
    )

    # —— 6. Positionering ——
    story.append(p("6. Aanbevolen positionering", s["h1"]))
    story.append(
        callout_box(
            "“De snelle, privacy-first kamerbot voor studentensteden — "
            "niet alle huurwoningen van Nederland.”",
            s,
        )
    )
    story.append(Spacer(1, 0.35 * cm))
    story.append(
        p(
            "Herhaal dit in site, bot-onboarding en ads. Vermijd generieke claims als "
            "“wij vinden alles” of “1000 websites” tenzij dat waar én houdbaar is.",
            s["body"],
        )
    )

    # —— 7. Risico’s ——
    story.append(p("7. Risico’s en aandachtspunten", s["h1"]))
    risks = [
        [H("Risico"), H("Impact"), H("Mitigatie")],
        [
            C("Te weinig aanbod"),
            C("Hoog — churn"),
            C("Supply eerst; partnerships; vetted plaatsingen stimuleren"),
        ],
        [
            C("Juridisch scrapen / ToS"),
            C("Hoog"),
            C("Alleen toegestane bronnen; blijf eerlijk over limieten"),
        ],
        [
            C("Proef misbruik (€1 zonder intentie)"),
            C("Middel"),
            C("Limits in proef; fraud-checks; duidelijke auto-verlenging"),
        ],
        [
            C("Hoge churn na vinden kamer"),
            C("Structureel"),
            C("Accepteer; focus op maandelijkse instroom + referrals"),
        ],
        [
            C("Prijsdruk van low-cost alerts"),
            C("Middel"),
            C("Differentiëren op privacy + kamerkwaliteit, niet op laagste prijs"),
        ],
    ]
    story.append(table(risks, [4.0 * cm, 2.8 * cm, 9.4 * cm]))

    # —— 8. Next steps ——
    story.append(p("8. Beste volgende stappen", s["h1"]))
    story.append(
        bullets(
            [
                "Meet baseline: actieve zoekers, meldingen/week, reacties, geplaatste kamers, proefstarts.",
                "Zet abonnement live: €1 / 7 dagen → €14,99, met heldere copy op roomalert.nl.",
                "Verbeter verhuurder-inbox + reactiekwaliteit (retention aan beide kanten).",
                "Verhoog vetted supply vóór een derde stad.",
                "Pas daarna Rotterdam of Groningen toevoegen — één stad tegelijk.",
            ],
            s["bullet"],
        )
    )

    story.append(Spacer(1, 0.6 * cm))
    story.append(p("Eindoordeel", s["h2"]))
    story.append(
        p(
            "RoomAlert kan uniek en winstgevend worden als niche-product, niet als generic huuralert. "
            "Het abonnement (€1 → €14,99) is marktconform en past bij een pad naar circa €5k/maand. "
            "Succes hangt af van aanbodkwaliteit, trust en consistente instroom van zoekers — "
            "niet van de breedste scraper.",
            s["verdict"],
        )
    )

    story.append(Spacer(1, 0.4 * cm))
    story.append(p("— Einde rapport —", s["meta"]))

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=1.5 * cm,
        bottomMargin=1.8 * cm,
        title="RoomAlert Concurrentieonderzoek",
        author="Strategisch productadvies",
        subject="Concurrentieanalyse en monetisatie RoomAlert.nl",
    )
    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)

    # Copy into repo docs as well
    OUT_REPO.write_bytes(OUT.read_bytes())
    print(f"Wrote {OUT}")
    print(f"Wrote {OUT_REPO}")
    print(f"Size: {OUT.stat().st_size} bytes")


if __name__ == "__main__":
    build()
