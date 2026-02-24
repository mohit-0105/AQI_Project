from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame
from reportlab.lib.colors import HexColor
import os

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "AQI_Project_Report.pdf")

# ── COLOUR PALETTE ────────────────────────────────────────────────────────────
C_DARK_BLUE   = HexColor("#1a2b4a")
C_MID_BLUE    = HexColor("#2c5282")
C_LIGHT_BLUE  = HexColor("#ebf4ff")
C_ACCENT      = HexColor("#3182ce")
C_GREEN       = HexColor("#276749")
C_GREEN_BG    = HexColor("#f0fff4")
C_ORANGE      = HexColor("#c05621")
C_ORANGE_BG   = HexColor("#fffaf0")
C_RED         = HexColor("#9b2335")
C_GREY_LIGHT  = HexColor("#f7fafc")
C_GREY_MID    = HexColor("#e2e8f0")
C_GREY_DARK   = HexColor("#4a5568")
C_WHITE       = colors.white
C_BLACK       = colors.black

# ── STYLES ────────────────────────────────────────────────────────────────────
base_styles = getSampleStyleSheet()

def make_style(name, parent="Normal", **kw):
    return ParagraphStyle(name, parent=base_styles[parent], **kw)

styles = {
    "cover_title": make_style("cover_title", "Title",
        fontSize=28, textColor=C_WHITE, alignment=TA_CENTER,
        spaceAfter=6, leading=34),
    "cover_sub": make_style("cover_sub", "Normal",
        fontSize=13, textColor=HexColor("#bee3f8"), alignment=TA_CENTER,
        spaceAfter=4),
    "cover_meta": make_style("cover_meta", "Normal",
        fontSize=10, textColor=HexColor("#90cdf4"), alignment=TA_CENTER,
        spaceAfter=3),

    "h1": make_style("h1", "Heading1",
        fontSize=16, textColor=C_WHITE, spaceAfter=2, spaceBefore=0,
        backColor=C_MID_BLUE, leftIndent=-10, rightIndent=-10,
        borderPadding=(6, 10, 6, 10), leading=20),
    "h2": make_style("h2", "Heading2",
        fontSize=13, textColor=C_DARK_BLUE, spaceAfter=4, spaceBefore=10,
        borderPadding=(0, 0, 2, 0)),
    "h3": make_style("h3", "Heading3",
        fontSize=11, textColor=C_ACCENT, spaceAfter=3, spaceBefore=6,
        fontName="Helvetica-Bold"),

    "body": make_style("body", "Normal",
        fontSize=10, textColor=C_GREY_DARK, leading=15,
        spaceAfter=5, alignment=TA_JUSTIFY),
    "body_bold": make_style("body_bold", "Normal",
        fontSize=10, textColor=C_DARK_BLUE, leading=15,
        spaceAfter=4, fontName="Helvetica-Bold"),
    "bullet": make_style("bullet", "Normal",
        fontSize=10, textColor=C_GREY_DARK, leading=14,
        spaceAfter=3, leftIndent=18, bulletIndent=8),
    "code": make_style("code", "Code",
        fontSize=8.5, textColor=HexColor("#2d3748"),
        backColor=HexColor("#edf2f7"), leading=13,
        leftIndent=12, rightIndent=12, spaceAfter=6,
        borderPadding=(6, 8, 6, 8)),
    "caption": make_style("caption", "Normal",
        fontSize=8.5, textColor=C_GREY_DARK, alignment=TA_CENTER,
        spaceAfter=8, fontName="Helvetica-Oblique"),
    "toc_entry": make_style("toc_entry", "Normal",
        fontSize=10, textColor=C_MID_BLUE, leading=18),
    "footer_text": make_style("footer_text", "Normal",
        fontSize=8, textColor=HexColor("#a0aec0"), alignment=TA_CENTER),
    "highlight_kv": make_style("highlight_kv", "Normal",
        fontSize=10, textColor=C_DARK_BLUE, leading=14,
        spaceAfter=2, fontName="Helvetica-Bold"),
}

# ── TABLE HELPERS ─────────────────────────────────────────────────────────────
def header_row_style(row=0, cols=None):
    end_col = cols - 1 if cols else -1
    return [
        ("BACKGROUND",  (0, row), (end_col, row), C_MID_BLUE),
        ("TEXTCOLOR",   (0, row), (end_col, row), C_WHITE),
        ("FONTNAME",    (0, row), (end_col, row), "Helvetica-Bold"),
        ("FONTSIZE",    (0, row), (end_col, row), 9),
        ("ALIGN",       (0, row), (end_col, row), "CENTER"),
        ("TOPPADDING",  (0, row), (end_col, row), 6),
        ("BOTTOMPADDING",(0, row),(end_col, row), 6),
    ]

def data_rows_style(num_rows, start=1, col_end=-1):
    styles_list = [
        ("FONTNAME",    (0, start), (col_end, num_rows), "Helvetica"),
        ("FONTSIZE",    (0, start), (col_end, num_rows), 9),
        ("ALIGN",       (0, start), (col_end, num_rows), "CENTER"),
        ("VALIGN",      (0, 0),     (col_end, num_rows), "MIDDLE"),
        ("TOPPADDING",  (0, start), (col_end, num_rows), 5),
        ("BOTTOMPADDING",(0, start),(col_end, num_rows), 5),
        ("GRID",        (0, 0),     (col_end, num_rows), 0.5, C_GREY_MID),
        ("ROWBACKGROUNDS",(0, start),(col_end, num_rows),
         [C_WHITE, C_GREY_LIGHT]),
    ]
    return styles_list

def make_table(data, col_widths, left_align_col=None):
    ts = TableStyle(
        header_row_style(0, len(data[0])) +
        data_rows_style(len(data) - 1)
    )
    if left_align_col is not None:
        ts.add("ALIGN", (left_align_col, 1), (left_align_col, -1), "LEFT")
    t = Table(data, colWidths=col_widths)
    t.setStyle(ts)
    return t

def info_box(label, value, bg=C_LIGHT_BLUE):
    data = [[Paragraph(f"<b>{label}</b>", styles["body_bold"]),
             Paragraph(str(value), styles["body"])]]
    t = Table(data, colWidths=[4.5*cm, 11*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,0), bg),
        ("BACKGROUND", (1,0), (1,0), C_WHITE),
        ("BOX",        (0,0), (-1,-1), 0.5, C_GREY_MID),
        ("INNERGRID",  (0,0), (-1,-1), 0.5, C_GREY_MID),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING",(0,0), (-1,-1), 8),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
    ]))
    return t

def section_header(text):
    return [
        Spacer(1, 0.35*cm),
        Table([[Paragraph(f"  {text}", styles["h1"])]],
              colWidths=[17.2*cm],
              style=TableStyle([
                  ("BACKGROUND", (0,0), (-1,-1), C_MID_BLUE),
                  ("TOPPADDING", (0,0), (-1,-1), 0),
                  ("BOTTOMPADDING",(0,0),(-1,-1), 0),
                  ("LEFTPADDING",(0,0),(-1,-1), 0),
              ])),
        Spacer(1, 0.2*cm),
    ]

def subsection(text):
    return [
        Spacer(1, 0.15*cm),
        Paragraph(text, styles["h2"]),
        HRFlowable(width="100%", thickness=1, color=C_ACCENT, spaceAfter=4),
    ]

def body(text):
    return Paragraph(text, styles["body"])

def bullet_item(text):
    return Paragraph(f"• {text}", styles["bullet"])

def code_block(text):
    return Paragraph(text.replace("\n", "<br/>").replace(" ", "&nbsp;"), styles["code"])

# ── PAGE TEMPLATE ─────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = A4
MARGIN = 1.9*cm

def add_page_decorations(canvas, doc):
    canvas.saveState()
    # Header bar
    canvas.setFillColor(C_DARK_BLUE)
    canvas.rect(0, PAGE_H - 1.1*cm, PAGE_W, 1.1*cm, fill=1, stroke=0)
    canvas.setFillColor(C_WHITE)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(MARGIN, PAGE_H - 0.7*cm, "AQI Prediction Using Machine Learning")
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 0.7*cm, "College AI Project Report")
    # Footer bar
    canvas.setFillColor(C_GREY_MID)
    canvas.rect(0, 0, PAGE_W, 0.85*cm, fill=1, stroke=0)
    canvas.setFillColor(C_GREY_DARK)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(MARGIN, 0.3*cm, "Confidential — For Examination Purposes Only")
    canvas.drawRightString(PAGE_W - MARGIN, 0.3*cm, f"Page {doc.page}")
    # Left accent stripe
    canvas.setFillColor(C_ACCENT)
    canvas.rect(0, 0.85*cm, 3, PAGE_H - 1.1*cm - 0.85*cm, fill=1, stroke=0)
    canvas.restoreState()

def cover_page_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(C_DARK_BLUE)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFillColor(C_MID_BLUE)
    canvas.rect(0, PAGE_H * 0.38, PAGE_W, PAGE_H * 0.62, fill=1, stroke=0)
    canvas.setFillColor(C_ACCENT)
    canvas.rect(0, PAGE_H * 0.36, PAGE_W, 4, fill=1, stroke=0)
    canvas.setFillColor(HexColor("#1a365d"))
    canvas.rect(0, 0, PAGE_W, PAGE_H * 0.38, fill=1, stroke=0)
    canvas.restoreState()

# ── BUILD DOCUMENT ────────────────────────────────────────────────────────────
def build_pdf():
    doc = BaseDocTemplate(
        OUTPUT_PATH, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=1.5*cm, bottomMargin=1.2*cm,
    )

    content_frame = Frame(
        MARGIN, 1.1*cm,
        PAGE_W - 2*MARGIN, PAGE_H - 2.5*cm,
        id="content"
    )
    cover_frame = Frame(
        0, 0, PAGE_W, PAGE_H, id="cover"
    )

    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame],
                     onPage=cover_page_bg),
        PageTemplate(id="main",  frames=[content_frame],
                     onPage=add_page_decorations),
    ])

    story = []

    # ── COVER PAGE ────────────────────────────────────────────────────────────
    story.append(Spacer(1, 3.8*cm))
    story.append(Paragraph("AIR QUALITY INDEX", styles["cover_title"]))
    story.append(Paragraph("PREDICTION USING MACHINE LEARNING", styles["cover_title"]))
    story.append(Spacer(1, 0.4*cm))

    cover_divider = Table([[""]],
        colWidths=[10*cm],
        style=TableStyle([
            ("LINEABOVE", (0,0), (-1,-1), 2, HexColor("#63b3ed")),
            ("TOPPADDING",(0,0),(-1,-1), 0),
            ("BOTTOMPADDING",(0,0),(-1,-1), 0),
        ]))
    story.append(Table([[cover_divider]], colWidths=[PAGE_W],
        style=TableStyle([("ALIGN",(0,0),(-1,-1),"CENTER")])))
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph("A Comprehensive Technical Project Report", styles["cover_sub"]))
    story.append(Spacer(1, 2.5*cm))
    story.append(Paragraph("Bachelor of Engineering — Artificial Intelligence", styles["cover_meta"]))
    story.append(Paragraph("Academic Year: 2025–2026", styles["cover_meta"]))
    story.append(Spacer(1, 2.2*cm))

    meta_data = [
        ["Dataset",        "India City Daily AQI (2015–2020)"],
        ["Total Records",  "24,850 rows × 16 columns"],
        ["Best Model",     "Random Forest Regressor"],
        ["Best R² Score",  "0.9105  (91.05% variance explained)"],
        ["Best MAE",       "20.60 AQI units"],
        ["Cities Covered", "26 Indian cities"],
    ]
    meta_style = ParagraphStyle("ms", fontSize=9.5, textColor=C_WHITE, leading=14)
    meta_label_style = ParagraphStyle("ml", fontSize=9.5,
        textColor=HexColor("#bee3f8"), leading=14, fontName="Helvetica-Bold")
    meta_table_data = [[
        Paragraph(r[0], meta_label_style),
        Paragraph(r[1], meta_style)
    ] for r in meta_data]
    mt = Table(meta_table_data, colWidths=[5*cm, 10*cm])
    mt.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), HexColor("#1e3a5f")),
        ("TOPPADDING",   (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING",  (0,0),(-1,-1), 10),
        ("BOX",          (0,0),(-1,-1), 0.5, HexColor("#4a90c4")),
        ("INNERGRID",    (0,0),(-1,-1), 0.3, HexColor("#2c5282")),
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[HexColor("#1e3a5f"), HexColor("#1a3356")]),
    ]))
    story.append(mt)
    story.append(Spacer(1, 1.5*cm))
    story.append(Paragraph("Submitted for Examination · February 2026", styles["cover_meta"]))

    # Switch to main template
    story.append(PageBreak())
    story.append(NextPageTemplate("main"))  # noqa — defined inline below

    # ── TABLE OF CONTENTS ─────────────────────────────────────────────────────
    story.append(NextPageTemplate_real("main"))

    toc_items = [
        ("1.", "Project Overview & Objectives"),
        ("2.", "Problem Statement"),
        ("3.", "Dataset Description"),
        ("4.", "Data Preprocessing"),
        ("5.", "Exploratory Data Analysis (EDA)"),
        ("6.", "Machine Learning Pipeline"),
        ("7.", "Model Architecture & Theory"),
        ("8.", "Evaluation Metrics"),
        ("9.", "Results & Model Comparison"),
        ("10.", "Feature Importance Analysis"),
        ("11.", "Custom Test Scenarios"),
        ("12.", "Early Warning System"),
        ("13.", "Interactive AQI Map"),
        ("14.", "Project File Structure"),
        ("15.", "Limitations & Future Work"),
        ("16.", "Conclusion"),
    ]
    story += section_header("Table of Contents")
    for num, title in toc_items:
        story.append(Paragraph(
            f'<font color="#2c5282"><b>{num}</b></font>&nbsp;&nbsp;{title}',
            styles["toc_entry"]
        ))
    story.append(PageBreak())

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 1 — PROJECT OVERVIEW
    # ─────────────────────────────────────────────────────────────────────────
    story += section_header("1. Project Overview & Objectives")
    story.append(body(
        "This project applies supervised machine learning to predict the Air Quality Index (AQI) of "
        "Indian cities based on real-time atmospheric pollutant concentration data. Three regression "
        "algorithms — Linear Regression, Random Forest, and Gradient Boosting — were trained, "
        "evaluated, and compared on a publicly available dataset spanning 2015 to 2020."
    ))
    story.append(Spacer(1, 0.3*cm))

    story += subsection("Primary Objectives")
    for obj in [
        "Build and train ML regression models to predict AQI from pollutant sensor readings.",
        "Compare three different algorithms and identify the best performing model.",
        "Identify which pollutants contribute most significantly to AQI (feature importance).",
        "Create an early warning system that translates a predicted AQI into an actionable alert.",
        "Develop an interactive HTML map to visualise historical AQI across Indian cities.",
        "Produce reusable test scripts for validating model predictions across diverse scenarios.",
    ]:
        story.append(bullet_item(obj))

    story += subsection("Technology Stack")
    tech = [
        ["Component", "Technology", "Purpose"],
        ["Programming Language", "Python 3.x", "Core development language"],
        ["Data Manipulation", "pandas, NumPy", "DataFrame operations, numerical computing"],
        ["Machine Learning", "scikit-learn", "Model training, evaluation, preprocessing"],
        ["Visualisation", "matplotlib, seaborn", "Charts, heatmaps, scatter plots"],
        ["Interactive Map", "Leaflet.js (HTML/JS)", "Browser-based AQI map of India"],
        ["Development Env.", "Jupyter Notebook", "Interactive code + output environment"],
    ]
    story.append(make_table(tech, [4.5*cm, 4*cm, 8.2*cm], left_align_col=2))

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 2 — PROBLEM STATEMENT
    # ─────────────────────────────────────────────────────────────────────────
    story.append(PageBreak())
    story += section_header("2. Problem Statement")
    story.append(body(
        "Air pollution is one of the most critical environmental challenges in India, with cities "
        "like Delhi, Patna, and Lucknow consistently recording some of the worst air quality "
        "globally. The official AQI computation formula (CPCB, India) requires manual calculation "
        "of sub-indices for individual pollutants and is not easily adaptable to automated, "
        "real-time alerting systems."
    ))
    story.append(Spacer(1, 0.2*cm))
    story.append(body(
        "This project poses the question: <i>Can a machine learning model learn the mapping between "
        "atmospheric pollutant concentration readings and the resulting AQI, with sufficient accuracy "
        "to power a real-time early warning system?</i>"
    ))
    story.append(Spacer(1, 0.3*cm))

    story += subsection("AQI Scale (India — CPCB Standard)")
    aqi_table = [
        ["AQI Range", "Category", "Health Impact"],
        ["0 – 50",   "Good",           "Minimal impact on general population"],
        ["51 – 100", "Satisfactory",   "Minor discomfort for sensitive individuals"],
        ["101 – 200","Moderate",        "Breathing discomfort for lung/heart patients"],
        ["201 – 300","Poor",            "Discomfort for everyone on prolonged exposure"],
        ["301 – 400","Very Poor",       "Respiratory illness on prolonged exposure"],
        ["401 – 500","Severe",          "Serious effects even on brief exposure"],
        ["500+",     "Hazardous",       "Health emergency — affects healthy people"],
    ]
    ts_aqi = TableStyle(
        header_row_style(0, 3) + data_rows_style(7)
    )
    row_colors = [
        HexColor("#e6ffe6"), HexColor("#f5fff0"),
        HexColor("#ffffe0"), HexColor("#fff3e0"),
        HexColor("#ffe0e0"), HexColor("#ffd0d0"), HexColor("#ffc0c0"),
    ]
    for i, c in enumerate(row_colors, start=1):
        ts_aqi.add("BACKGROUND", (0, i), (-1, i), c)
    t_aqi = Table(aqi_table, colWidths=[2.5*cm, 3.5*cm, 10.7*cm])
    t_aqi.setStyle(ts_aqi)
    story.append(t_aqi)

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 3 — DATASET
    # ─────────────────────────────────────────────────────────────────────────
    story.append(PageBreak())
    story += section_header("3. Dataset Description")
    story.append(body(
        "The dataset used is <b>India City Daily AQI (2015–2020)</b>, a real-world collection of "
        "daily pollutant measurements and computed AQI values across 26 major Indian cities, "
        "sourced from CPCB monitoring stations."
    ))
    story.append(Spacer(1, 0.25*cm))
    kv = [
        ("Source",         "CPCB — Central Pollution Control Board, India"),
        ("File",           "city_day-Copy1.csv"),
        ("Total Rows",     "29,533 (raw) → 24,850 (after dropping missing AQI rows)"),
        ("Total Columns",  "16"),
        ("Date Range",     "January 2015 – July 2020"),
        ("Cities",         "26 major Indian cities"),
        ("Target Column",  "AQI (continuous numeric value)"),
    ]
    for k, v in kv:
        story.append(info_box(k, v))
    story.append(Spacer(1, 0.3*cm))

    story += subsection("Column Reference")
    cols_data = [
        ["Column", "Description", "Unit", "Type"],
        ["City",      "Name of the Indian city",                          "Text",   "Categorical"],
        ["Date",      "Date of measurement",                              "YYYY-MM-DD","Temporal"],
        ["PM2.5",     "Particulate matter ≤ 2.5 microns (fine dust/smoke)","µg/m³", "Feature"],
        ["PM10",      "Particulate matter ≤ 10 microns (coarser dust)",   "µg/m³",  "Feature"],
        ["NO",        "Nitric Oxide — vehicle exhaust, combustion",       "µg/m³",  "Feature"],
        ["NO2",       "Nitrogen Dioxide — NO oxidised by O2",             "µg/m³",  "Feature"],
        ["NOx",       "Nitrogen Oxides — sum of NO + NO2",                "µg/m³",  "Feature"],
        ["NH3",       "Ammonia — agriculture, fertilizers, livestock",    "µg/m³",  "Feature"],
        ["CO",        "Carbon Monoxide — incomplete combustion",          "mg/m³",  "Feature"],
        ["SO2",       "Sulphur Dioxide — coal/diesel burning",            "µg/m³",  "Feature"],
        ["O3",        "Ozone — sunlight + NO2 + VOC reaction",            "µg/m³",  "Feature"],
        ["Benzene",   "VOC — petrol, paint, tobacco smoke",               "µg/m³",  "Feature"],
        ["Toluene",   "VOC — paint, adhesives, solvents",                 "µg/m³",  "Feature"],
        ["Xylene",    "VOC — printing, rubber manufacturing",             "µg/m³",  "Feature"],
        ["AQI",       "Air Quality Index (computed value)",               "Number", "TARGET"],
        ["AQI_Bucket","AQI category label (Good/Moderate/Poor…)",         "Text",   "Label"],
    ]
    ts_col = TableStyle(
        header_row_style(0, 4) + data_rows_style(len(cols_data) - 1)
    )
    ts_col.add("BACKGROUND", (0, 15), (-1, 15), HexColor("#fff3cd"))
    ts_col.add("FONTNAME",   (0, 15), (-1, 15), "Helvetica-Bold")
    t_col = Table(cols_data, colWidths=[2.3*cm, 5.8*cm, 2.3*cm, 2.5*cm])
    t_col.setStyle(ts_col)
    story.append(t_col)
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        "<i>Note: City and Date were NOT used as ML features. Only the 12 pollutant columns "
        "were used as model inputs (X). AQI was the target output (y).</i>",
        styles["caption"]
    ))

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 4 — DATA PREPROCESSING
    # ─────────────────────────────────────────────────────────────────────────
    story.append(PageBreak())
    story += section_header("4. Data Preprocessing")
    story.append(body(
        "Raw sensor data is rarely clean. Missing values, sensor failures, and data gaps are "
        "common in environmental datasets. Two preprocessing strategies were applied."
    ))

    story += subsection("Step 1 — Drop Rows with Missing AQI (Target)")
    story.append(body(
        "AQI is the output variable. Any row without an AQI value is useless for supervised "
        "learning because the model has no ground truth to learn from. These rows were removed."
    ))
    story.append(code_block(
        "# Drop rows where AQI is missing — cannot train without a target\n"
        "df = df.dropna(subset=['AQI'])\n"
        "# Raw: 29,533 rows → After drop: 24,850 rows"
    ))

    story += subsection("Step 2 — Mean Imputation for Missing Pollutant Values")
    story.append(body(
        "For the 12 input pollutant features, missing values were replaced with the column mean. "
        "This strategy retains all rows while providing a statistically neutral estimate for "
        "missing sensor readings."
    ))
    story.append(code_block(
        "pollutant_cols = ['PM2.5','PM10','NO','NO2','NOx','NH3',\n"
        "                  'CO','SO2','O3','Benzene','Toluene','Xylene']\n"
        "df[pollutant_cols] = df[pollutant_cols].fillna(df[pollutant_cols].mean())"
    ))

    story += subsection("Preprocessing Results Summary")
    pre_data = [
        ["Metric", "Before Cleaning", "After Cleaning"],
        ["Total Rows",               "29,533",    "24,850"],
        ["Missing AQI values",       "~4,683",    "0"],
        ["Missing pollutant values", "Thousands", "0 (mean-imputed)"],
        ["Ready for ML",             "No",        "Yes ✓"],
    ]
    story.append(make_table(pre_data, [5.5*cm, 5*cm, 5.7*cm]))

    story += subsection("Why Mean Imputation?")
    for pt in [
        "<b>Preserves data volume:</b> Dropping rows with any missing pollutant value would lose significant data.",
        "<b>No data leakage:</b> Mean is computed on the entire column, not from test data separately.",
        "<b>Works well when:</b> Missing data is random (MCAR/MAR) and the feature is not the dominant predictor.",
        "<b>Limitation:</b> Injects bias if missing data is systematic (e.g., a sensor always fails on high-pollution days).",
    ]:
        story.append(bullet_item(pt))

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 5 — EDA
    # ─────────────────────────────────────────────────────────────────────────
    story.append(PageBreak())
    story += section_header("5. Exploratory Data Analysis (EDA)")
    story.append(body(
        "Before model training, the dataset was explored visually and statistically to understand "
        "its structure, distributions, and relationships between variables."
    ))

    eda_items = [
        ("AQI Distribution Histogram",
         "eda_visualizations.png — top left",
         "Shows the frequency distribution of AQI values across all city-days. "
         "A right-skewed distribution indicates most days have moderate AQI with "
         "a long tail of extreme pollution events."),
        ("Top 10 Most Polluted Cities",
         "eda_visualizations.png — top right",
         "Horizontal bar chart of average AQI per city. Northern Indian cities "
         "(Delhi, Patna, Lucknow) typically dominate due to traffic density, "
         "geography, and winter temperature inversions that trap pollutants."),
        ("Pollutant Correlation with AQI (Heatmap)",
         "eda_visualizations.png — bottom left",
         "Pearson correlation coefficient between each pollutant and AQI. "
         "PM2.5 and CO show the highest correlation (≈0.8–0.9) since they "
         "are primary components of India's AQI formula. O3 may show weak or "
         "negative correlation in some contexts."),
        ("AQI Category Distribution",
         "eda_visualizations.png — bottom right",
         "Count of records in each AQI bucket. Reveals class imbalance — "
         "'Moderate' and 'Poor' days far outnumber 'Good' or 'Hazardous' days "
         "in the Indian urban dataset."),
        ("Regression Scatter Plots",
         "regplots.png",
         "AQI vs each of the top 6 pollutants with fitted regression lines. "
         "Reveals linearity vs non-linearity in individual relationships."),
        ("Box Plots — Pollutant Distribution",
         "boxplots.png",
         "Spread, median, quartiles, and outliers for PM2.5, CO, NO2, "
         "SO2, PM10, and O3. Extreme outliers are visible especially for PM2.5 "
         "and CO, indicating industrial incidents or severe pollution episodes."),
        ("Residual Analysis",
         "residual_analysis.png",
         "Post-model: histogram of residuals (Actual - Predicted) should be "
         "centred at zero for a well-fitted model. Residuals vs Predicted plot "
         "checks for heteroscedasticity (error variance increasing with AQI)."),
    ]

    for title, file_ref, description in eda_items:
        story.append(KeepTogether([
            Paragraph(title, styles["h3"]),
            info_box("Output File", file_ref, C_GREEN_BG),
            body(description),
            Spacer(1, 0.2*cm),
        ]))

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 6 — ML PIPELINE
    # ─────────────────────────────────────────────────────────────────────────
    story.append(PageBreak())
    story += section_header("6. Machine Learning Pipeline")

    story += subsection("Feature and Target Definition")
    story.append(code_block(
        "features = ['PM2.5','PM10','NO','NO2','NOx','NH3',\n"
        "            'CO','SO2','O3','Benzene','Toluene','Xylene']\n\n"
        "X = df[features]   # Input matrix  — shape: (24850, 12)\n"
        "y = df['AQI']      # Target vector — shape: (24850,)"
    ))
    story.append(body(
        "X and y are the two fundamental objects in supervised learning. X contains all the "
        "information the model sees as inputs; y contains the correct answers it is trained to predict."
    ))

    story += subsection("Train-Test Split")
    story.append(code_block(
        "X_train, X_test, y_train, y_test = train_test_split(\n"
        "    X, y, test_size=0.2, random_state=42\n"
        ")\n"
        "# Training set: 19,880 rows (80%)\n"
        "# Testing set:   4,970 rows (20%)"
    ))

    split_data = [
        ["Split", "Rows", "Percentage", "Purpose"],
        ["Training Set", "~19,880", "80%", "Model sees and learns from this data"],
        ["Testing Set",   "~4,970", "20%", "Model NEVER sees this during training — used only for final evaluation"],
    ]
    story.append(make_table(split_data, [3*cm, 2.5*cm, 3*cm, 8.2*cm], left_align_col=3))
    story.append(Spacer(1, 0.2*cm))
    story.append(body(
        "<b>Why random_state=42?</b> This seeds the random number generator so the split is "
        "identical every time the code runs, making results reproducible. Without it, every "
        "execution would split differently and produce slightly different scores."
    ))

    story += subsection("Training All Three Models")
    story.append(code_block(
        "models = {\n"
        "    'Linear Regression': LinearRegression(),\n"
        "    'Random Forest':     RandomForestRegressor(n_estimators=100, random_state=42),\n"
        "    'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42)\n"
        "}\n\n"
        "for name, model in models.items():\n"
        "    model.fit(X_train, y_train)      # Train\n"
        "    y_pred = model.predict(X_test)   # Predict on unseen test set\n"
        "    # Compute MAE, RMSE, R²"
    ))

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 7 — MODEL THEORY
    # ─────────────────────────────────────────────────────────────────────────
    story.append(PageBreak())
    story += section_header("7. Model Architecture & Theory")

    story += subsection("7.1 Linear Regression")
    story.append(body(
        "Linear Regression models the target as a weighted linear combination of all input features:"
    ))
    story.append(code_block(
        "AQI = β₀ + β₁·PM2.5 + β₂·CO + β₃·NO + … + β₁₂·Xylene + ε\n\n"
        "Where β₁ … β₁₂ are learned coefficients (weights) and ε is the error term.\n"
        "Training minimises the Sum of Squared Residuals (SSR) using the Normal Equation or gradient descent."
    ))
    lr_pros = [
        ("Strengths", "Fast to train; fully interpretable coefficients; no hyperparameter tuning needed"),
        ("Weaknesses", "Assumes linearity — real AQI relationships are non-linear; sensitive to outliers; "
                       "cannot model feature interactions"),
        ("Result",     "R² = 0.8092 — reasonable baseline but misses complex pollution dynamics"),
    ]
    for k, v in lr_pros:
        story.append(info_box(k, v, C_LIGHT_BLUE))
    story.append(Spacer(1, 0.15*cm))

    story += subsection("7.2 Random Forest Regressor")
    story.append(body(
        "Random Forest is an ensemble learning method that builds multiple independent Decision Trees "
        "using the <b>Bagging (Bootstrap Aggregating)</b> technique:"
    ))
    for step in [
        "<b>Step 1 — Bootstrap:</b> Draw a random sample (with replacement) from the training data for each tree.",
        "<b>Step 2 — Random Feature Subspace:</b> At each split point, only a random subset of features is "
        "considered (not all 12). This decorrelates the trees.",
        "<b>Step 3 — Grow Trees:</b> Each tree is grown deep (low bias, high variance individually).",
        "<b>Step 4 — Aggregate:</b> Final prediction = average of all 100 tree predictions. "
        "Averaging reduces variance without increasing bias.",
    ]:
        story.append(bullet_item(step))
    story.append(Spacer(1, 0.1*cm))
    rf_info = [
        ("n_estimators=100", "100 trees are built and averaged. More trees = more stable but slower."),
        ("random_state=42",  "Seeds the randomness for reproducibility"),
        ("Feature Importance","After training, each feature's contribution to error reduction is tracked"),
        ("Result",           "R² = 0.9105 — Best model in this project ✓"),
    ]
    for k, v in rf_info:
        story.append(info_box(k, v, C_LIGHT_BLUE))
    story.append(Spacer(1, 0.15*cm))

    story += subsection("7.3 Gradient Boosting Regressor")
    story.append(body(
        "Gradient Boosting builds trees <b>sequentially</b>, where each new tree corrects the errors "
        "of all previous trees combined. It uses the <b>Boosting</b> strategy:"
    ))
    for step in [
        "<b>Iteration 1:</b> Fit a shallow decision tree to the data. Compute residuals (actual - predicted).",
        "<b>Iteration 2:</b> Fit a new tree to the residuals. Add it to the ensemble with a small weight (learning rate).",
        "<b>Iteration 3–100:</b> Repeat — each tree targets the remaining unexplained residuals.",
        "<b>Final prediction:</b> Sum of all 100 trees' weighted predictions.",
    ]:
        story.append(bullet_item(step))
    story.append(Spacer(1, 0.1*cm))
    gb_info = [
        ("Learning Rate",    "Default 0.1 — controls how aggressively each tree corrects errors"),
        ("n_estimators=100", "100 boosting iterations (trees)"),
        ("Loss Function",    "Mean Squared Error (MSE) by default"),
        ("Result",           "R² = 0.8952 — strong performance, close second to Random Forest"),
    ]
    for k, v in gb_info:
        story.append(info_box(k, v, C_LIGHT_BLUE))

    story += subsection("Comparison: Bagging vs Boosting")
    cmp_data = [
        ["Aspect", "Random Forest (Bagging)", "Gradient Boosting (Boosting)"],
        ["Tree Building",   "Parallel (independent trees)",  "Sequential (each fixes previous)"],
        ["Data Sampling",   "Random bootstrap subsets",      "Full dataset, weighted residuals"],
        ["Error Reduction", "Reduces variance",              "Reduces bias"],
        ["Overfitting Risk","Lower",                         "Higher (needs careful tuning)"],
        ["Training Speed",  "Faster",                        "Slower"],
        ["This Project R²", "0.9105 ✓ Best",                 "0.8952"],
    ]
    story.append(make_table(cmp_data, [4*cm, 6.1*cm, 6.6*cm]))

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 8 — EVALUATION METRICS
    # ─────────────────────────────────────────────────────────────────────────
    story.append(PageBreak())
    story += section_header("8. Evaluation Metrics")

    metrics_detail = [
        ("MAE — Mean Absolute Error",
         "MAE = (1/n) × Σ|yᵢ - ŷᵢ|",
         "Average absolute difference between actual and predicted AQI. "
         "Treats all errors equally regardless of size. Expressed in same units as AQI. "
         "<b>Lower is better.</b> Random Forest MAE = 20.60 means the model is wrong "
         "by an average of 20.6 AQI units per prediction."),
        ("RMSE — Root Mean Square Error",
         "RMSE = √[ (1/n) × Σ(yᵢ - ŷᵢ)² ]",
         "Like MAE but squares individual errors first, then takes the root. "
         "This makes RMSE more sensitive to large errors — a prediction off by 100 "
         "contributes 10,000 to the sum before root, vs only 100 for MAE. "
         "RMSE > MAE always. A large RMSE/MAE gap indicates the presence of large "
         "outlier predictions. <b>Lower is better.</b>"),
        ("R² — Coefficient of Determination",
         "R² = 1 - [Σ(yᵢ - ŷᵢ)² / Σ(yᵢ - ȳ)²]",
         "Proportion of variance in AQI that the model explains. R²=1.0 means "
         "perfect predictions. R²=0 means the model is no better than always "
         "predicting the mean AQI. R² can be negative (model worse than baseline). "
         "Random Forest R²=0.9105 means the model explains 91.05% of all AQI "
         "variation in the test set. <b>Higher is better. Maximum is 1.0.</b>"),
    ]

    for metric_name, formula, explanation in metrics_detail:
        story.append(KeepTogether([
            Paragraph(metric_name, styles["h3"]),
            code_block(formula),
            body(explanation),
            Spacer(1, 0.2*cm),
        ]))

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 9 — RESULTS
    # ─────────────────────────────────────────────────────────────────────────
    story.append(PageBreak())
    story += section_header("9. Results & Model Comparison")

    story += subsection("Model Performance Table")
    results_data = [
        ["Model", "MAE ↓", "RMSE ↓", "R² ↑", "Verdict"],
        ["Linear Regression",  "31.20", "59.11", "0.8092", "Baseline — acceptable"],
        ["Random Forest",      "20.60", "40.49", "0.9105", "★ Best Model"],
        ["Gradient Boosting",  "23.71", "43.80", "0.8952", "Strong — close second"],
    ]
    ts_res = TableStyle(
        header_row_style(0, 5) + data_rows_style(3)
    )
    ts_res.add("BACKGROUND", (0, 2), (-1, 2), HexColor("#f0fff4"))
    ts_res.add("FONTNAME",   (0, 2), (-1, 2), "Helvetica-Bold")
    ts_res.add("TEXTCOLOR",  (0, 2), (-1, 2), C_GREEN)
    t_res = Table(results_data, colWidths=[4.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 4.7*cm])
    t_res.setStyle(ts_res)
    story.append(t_res)
    story.append(Spacer(1, 0.2*cm))

    story += subsection("Output Files Generated")
    output_data = [
        ["File", "Content"],
        ["eda_visualizations.png",  "4-panel EDA: histogram, top cities, correlation heatmap, category distribution"],
        ["model_comparison.png",    "Side-by-side bar charts: MAE, RMSE, R² for all 3 models"],
        ["feature_importance.png",  "Horizontal bar chart of Random Forest feature importances"],
        ["best_model_analysis.png", "Scatter plot: Actual AQI vs Random Forest Predicted AQI"],
        ["regplots.png",            "AQI vs top 6 pollutants with regression lines (2×3 grid)"],
        ["boxplots.png",            "Box plots for PM2.5, CO, NO2, SO2, PM10, O3 distributions"],
        ["residual_analysis.png",   "Residual histogram + residuals vs predicted scatter plot"],
        ["full_output.txt",         "Text summary of dataset shape, model metrics, and test case results"],
    ]
    story.append(make_table(output_data, [5.5*cm, 11.2*cm], left_align_col=1))

    story += subsection("Key Observations")
    for obs in [
        "Random Forest achieves the best performance across all three metrics, reducing MAE by 34% "
        "compared to Linear Regression.",
        "The gap between RMSE and MAE (≈2× for all models) indicates the presence of difficult "
        "outlier predictions — likely extreme industrial pollution events.",
        "Linear Regression's R²=0.8092 confirms that while the dominant relationships (PM2.5, CO) "
        "are approximately linear, the full AQI response is non-linear and requires ensemble methods.",
        "Gradient Boosting slightly underperforms Random Forest here, potentially because the "
        "default learning rate and tree depth are not optimal for this dataset size.",
    ]:
        story.append(bullet_item(obs))

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 10 — FEATURE IMPORTANCE
    # ─────────────────────────────────────────────────────────────────────────
    story.append(PageBreak())
    story += section_header("10. Feature Importance Analysis")
    story.append(body(
        "After training, Random Forest exposes a `feature_importances_` array that quantifies "
        "how much each input feature contributed to reducing prediction error across all 100 trees. "
        "Scores sum to 1.0."
    ))
    story.append(Spacer(1, 0.2*cm))

    fi_data = [
        ["Rank", "Feature", "Importance Score", "Cumulative", "Interpretation"],
        ["1",  "PM2.5",   "0.491", "49.1%",  "Primary driver — fine particulate matter"],
        ["2",  "CO",      "0.368", "85.9%",  "Carbon monoxide — traffic & combustion"],
        ["3",  "NO",      "0.037", "89.6%",  "Nitric oxide — minor contributor"],
        ["4",  "PM10",    "0.037", "93.3%",  "Coarse particulates — correlated with PM2.5"],
        ["5",  "O3",      "0.015", "94.8%",  "Ozone — seasonal, photochemical"],
        ["6",  "NOx",     "0.012", "96.0%",  "Total nitrogen oxides"],
        ["7",  "SO2",     "0.010", "97.0%",  "Sulphur dioxide"],
        ["8",  "NO2",     "0.008", "97.8%",  "Nitrogen dioxide"],
        ["9",  "Toluene", "0.007", "98.5%",  "Volatile organic compound"],
        ["10", "Xylene",  "0.006", "99.1%",  "Volatile organic compound"],
        ["11", "Benzene", "0.005", "99.6%",  "Volatile organic compound"],
        ["12", "NH3",     "0.003", "99.9%",  "Ammonia — agricultural sources"],
    ]
    ts_fi = TableStyle(
        header_row_style(0, 5) + data_rows_style(12)
    )
    for row in [1, 2]:
        ts_fi.add("BACKGROUND", (0, row), (-1, row), HexColor("#e6f7ff"))
        ts_fi.add("FONTNAME",   (0, row), (-1, row), "Helvetica-Bold")
    t_fi = Table(fi_data, colWidths=[1.2*cm, 2.5*cm, 3*cm, 2.8*cm, 7.2*cm])
    t_fi.setStyle(ts_fi)
    story.append(t_fi)
    story.append(Spacer(1, 0.15*cm))

    story += subsection("Analysis")
    for pt in [
        "<b>PM2.5 dominates (49%)</b> because India's official AQI formula assigns PM2.5 the highest "
        "sub-index weight. The ML model learned this from the data without being explicitly programmed.",
        "<b>PM2.5 + CO together account for 85.9%</b> of predictive power. This means if only two sensors "
        "were available, most of the AQI signal is captured.",
        "<b>VOCs (Benzene, Toluene, Xylene) collectively contribute &lt;2%</b> — likely because their "
        "concentrations in this dataset are generally low and their CPCB sub-index breakpoints rarely "
        "dominate.",
        "<b>NH3 at 0.3%</b> is the least important feature — ammonia primarily affects odour and is "
        "not a dominant AQI component under CPCB guidelines.",
        "<b>Multicollinearity note:</b> NOx = NO + NO2 by definition. Having all three as features "
        "introduces redundancy. Tree-based models handle this by splitting importance across correlated "
        "features, which may understate the true importance of NO and NO2 individually.",
    ]:
        story.append(bullet_item(pt))

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 11 — TEST SCENARIOS
    # ─────────────────────────────────────────────────────────────────────────
    story.append(PageBreak())
    story += section_header("11. Custom Test Scenarios")
    story.append(body(
        "Five realistic pollution scenarios were constructed manually and passed to the trained "
        "Random Forest model to validate that predictions are sensible across the full AQI spectrum."
    ))
    story.append(Spacer(1, 0.2*cm))

    scenario_data = [
        ["Scenario", "PM2.5", "PM10", "CO", "Predicted AQI", "Category", "Real-World Context"],
        ["Delhi Winter Smog",  "250", "300", "5.0",  "~393", "Very Poor",  "Winter temperature inversion"],
        ["Moderate Urban Day", "80",  "100", "1.5",  "~172", "Moderate",   "Typical weekday in metro"],
        ["Hill Station",       "12",  "25",  "0.3",  "~36",  "Good",       "Shimla/Ooty clear day"],
        ["Extreme Industrial", "400", "500", "10.0", "~508", "Hazardous",  "Factory complex / major fire"],
        ["Near-Clean Rural",   "5",   "10",  "0.1",  "~31",  "Good",       "Remote village, minimal traffic"],
    ]
    ts_sc = TableStyle(
        header_row_style(0, 7) + data_rows_style(5)
    )
    ts_sc.add("BACKGROUND", (0, 4), (-1, 4), HexColor("#fff3cd"))
    ts_sc.add("BACKGROUND", (0, 3), (-1, 3), HexColor("#f0fff4"))
    ts_sc.add("BACKGROUND", (0, 5), (-1, 5), HexColor("#f0fff4"))
    ts_sc.add("BACKGROUND", (0, 2), (-1, 2), HexColor("#fff3cd"))
    ts_sc.add("BACKGROUND", (0, 1), (-1, 1), HexColor("#ffe0e0"))
    ts_sc.add("BACKGROUND", (0, 6), (-1, 6), HexColor("#ffd0d0"))
    t_sc = Table(scenario_data, colWidths=[3.5*cm, 1.5*cm, 1.5*cm, 1.2*cm, 2.8*cm, 2.5*cm, 3.7*cm])
    t_sc.setStyle(ts_sc)
    story.append(t_sc)
    story.append(Spacer(1, 0.2*cm))

    story += subsection("How Categories Are Assigned in Code")
    story.append(code_block(
        "test_cases['Category'] = pd.cut(\n"
        "    predictions,\n"
        "    bins=[0, 50, 100, 200, 300, 400, 500, 9999],\n"
        "    labels=['Good','Satisfactory','Moderate',\n"
        "            'Poor','Very Poor','Severe','Hazardous']\n"
        ")"
    ))
    story.append(body(
        "pd.cut() maps each continuous predicted AQI number into the corresponding "
        "CPCB category bucket, matching the official AQI classification standard."
    ))

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 12 — EARLY WARNING SYSTEM
    # ─────────────────────────────────────────────────────────────────────────
    story.append(PageBreak())
    story += section_header("12. Early Warning System")
    story.append(body(
        "The Early Warning System (EWS) is the practical deployment interface of the trained model. "
        "It wraps the Random Forest predictions with an alert classification and a human-readable "
        "recommended action, simulating what a government monitoring system would display."
    ))

    story += subsection("Function Signature")
    story.append(code_block(
        "def aqi_early_warning(\n"
        "    pm25=200, pm10=250, no2=50, co=4.0, o3=30,\n"
        "    # Less critical — defaults are dataset column means:\n"
        "    no=17.6, nox=32.3, nh3=23.5, so2=14.5,\n"
        "    benzene=3.3, toluene=8.7, xylene=3.1\n"
        "):"
    ))
    story.append(body(
        "Only the five primary pollutants need to be supplied by the user: "
        "<b>PM2.5, PM10, NO2, CO, O3</b>. The remaining seven are pre-filled "
        "with dataset means, reducing data entry burden in operational use."
    ))

    story += subsection("Alert Level Logic")
    alert_data = [
        ["Predicted AQI", "Alert Level", "Recommended Action"],
        ["≤ 50",    "GOOD",             "No action needed. Air quality is satisfactory."],
        ["51–100",  "SATISFACTORY",     "Sensitive individuals should limit prolonged outdoor exertion."],
        ["101–200", "MODERATE",         "People with respiratory issues should avoid outdoor activity."],
        ["201–300", "POOR",             "ALERT: General public may experience health effects."],
        ["301–400", "VERY POOR",        "HIGH ALERT: Stay indoors. Wear masks if going outside."],
        ["400+",    "SEVERE/HAZARDOUS", "EMERGENCY: Authorities should restrict traffic and industry."],
    ]
    story.append(make_table(alert_data, [2.8*cm, 3.5*cm, 10.4*cm], left_align_col=2))

    story += subsection("Demo Output — Three Scenarios")
    demo_data = [
        ["Scenario", "Key Inputs", "Predicted AQI", "Alert Level"],
        ["Delhi Winter Morning", "PM2.5=180, CO=3.0, NO2=45", "~320", "VERY POOR"],
        ["Hill Station Clear Day","PM2.5=15,  CO=0.3, NO2=8",  "~40",  "GOOD"],
        ["Industrial Zone",      "PM2.5=350, CO=8.0, NO2=90", "~490", "SEVERE/HAZARDOUS"],
    ]
    story.append(make_table(demo_data, [4.5*cm, 5*cm, 3*cm, 4.2*cm]))

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 13 — INTERACTIVE MAP
    # ─────────────────────────────────────────────────────────────────────────
    story.append(PageBreak())
    story += section_header("13. Interactive AQI Map")
    story.append(body(
        "A fully interactive HTML/JavaScript map of India was generated programmatically using Python, "
        "powered by the open-source Leaflet.js mapping library. The map visualises the historical "
        "average AQI for each city as a colour-coded, size-scaled circular marker."
    ))

    story += subsection("Technical Architecture")
    for step in [
        "<b>Step 1 — Aggregate data:</b> groupby('City')['AQI'].mean() computes average AQI per city.",
        "<b>Step 2 — Coordinates:</b> A hardcoded dictionary maps city names to (latitude, longitude) — "
        "26 cities included.",
        "<b>Step 3 — Colour + radius function:</b> get_color(aqi) returns a hex colour and category label. "
        "Circle radius = max(8, min(30, aqi/15)) — proportional to AQI but capped at 30px.",
        "<b>Step 4 — JavaScript generation:</b> Python f-strings inject city data into JavaScript "
        "L.circleMarker() calls, generating a Leaflet map with interactive popups.",
        "<b>Step 5 — Save as HTML:</b> The entire map (HTML + embedded JS) is written to "
        "interactive_aqi_map.html — open in any browser, no server needed.",
    ]:
        story.append(bullet_item(step))

    story += subsection("Map Colour Legend")
    legend_data = [
        ["Colour",  "AQI Range", "Category"],
        ["Green (#00e400)",    "0–50",   "Good"],
        ["Lime (#92d14f)",     "51–100", "Satisfactory"],
        ["Yellow (#ffff00)",   "101–200","Moderate"],
        ["Orange (#ff7e00)",   "201–300","Poor"],
        ["Red (#ff0000)",      "301–400","Very Poor"],
        ["Dark Red (#8b0000)", "400+",   "Severe / Hazardous"],
    ]
    story.append(make_table(legend_data, [4.5*cm, 3*cm, 9.2*cm]))
    story.append(Spacer(1, 0.2*cm))
    story.append(body(
        "Each city marker is clickable and displays a popup showing the city name, "
        "average AQI value, and category. The map uses OpenStreetMap tiles for the base layer."
    ))

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 14 — FILE STRUCTURE
    # ─────────────────────────────────────────────────────────────────────────
    story.append(PageBreak())
    story += section_header("14. Project File Structure")

    files_data = [
        ["File / Folder", "Type", "Description"],
        ["city_day-Copy1.csv",       "Input Data",  "Raw dataset — 29,533 rows of city AQI readings"],
        ["Untitled.ipynb",           "Notebook",    "Main project notebook — all code, outputs, and charts"],
        ["quick_test.py",            "Script",      "Minimal script showing single-prediction structure"],
        ["test_aqi_model.py",        "Script",      "5 named test scenarios with expected AQI categories"],
        ["full_output.txt",          "Output",      "Text summary: model metrics + test case predictions"],
        ["interactive_aqi_map.html", "Output",      "Browser-openable interactive Leaflet.js map of India"],
        ["eda_visualizations.png",   "Output Chart","4-panel EDA visualisation"],
        ["model_comparison.png",     "Output Chart","MAE/RMSE/R² comparison bar charts"],
        ["feature_importance.png",   "Output Chart","Random Forest feature importance bar chart"],
        ["best_model_analysis.png",  "Output Chart","Actual vs Predicted AQI scatter plot"],
        ["regplots.png",             "Output Chart","AQI vs top-6 pollutants regression plots"],
        ["boxplots.png",             "Output Chart","Pollutant distribution box plots"],
        ["residual_analysis.png",    "Output Chart","Residual histogram + residuals vs predicted"],
        ["PROJECT_EXPLAINED.md",     "Documentation","Full beginner guide to the project"],
        ["VIVA_QUESTIONS.md",        "Documentation","80 examiner-style viva questions"],
        ["AQI_Project_Report.pdf",   "Documentation","This project report"],
    ]
    story.append(make_table(files_data, [5*cm, 3*cm, 8.7*cm], left_align_col=2))

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 15 — LIMITATIONS & FUTURE WORK
    # ─────────────────────────────────────────────────────────────────────────
    story.append(PageBreak())
    story += section_header("15. Limitations & Future Work")

    story += subsection("Current Limitations")
    limitations = [
        ("No Temporal Features",
         "The Date column was dropped. Seasonal patterns (winter smog, monsoon clearing) and "
         "long-term trends are not captured by the model."),
        ("Random Split on Time-Series Data",
         "A random 80/20 split allows future data to appear in training. A proper time-based split "
         "(train on 2015–2018, test on 2019–2020) would give a more realistic performance estimate."),
        ("No Weather Data",
         "Temperature, humidity, wind speed, and direction strongly affect pollutant dispersion "
         "and AQI. Absence of these features is a significant gap."),
        ("Mean Imputation Bias",
         "If missing sensor readings are systematically correlated with pollution levels, "
         "mean imputation introduces bias."),
        ("Model Not Persisted",
         "The trained model is not saved to disk (pickle/joblib). Every notebook run retrains from scratch, "
         "making deployment impractical."),
        ("No Uncertainty Quantification",
         "The model predicts a point estimate (e.g., AQI=280) with no confidence interval. "
         "A prediction range (e.g., 280±35) would be far more useful for decision-making."),
        ("Nowcasting, Not Forecasting",
         "The model predicts current AQI from current pollutant readings. Predicting future AQI "
         "(e.g., 6 hours ahead) requires time-series architectures like LSTM."),
        ("Geographic Generalisation",
         "Trained exclusively on 26 Indian cities (2015–2020). Cannot reliably predict AQI for "
         "cities not in the training distribution, or for periods beyond 2020."),
    ]
    for title, desc in limitations:
        story.append(KeepTogether([
            Paragraph(title, styles["h3"]),
            body(desc),
            Spacer(1, 0.1*cm),
        ]))

    story += subsection("Proposed Improvements")
    improvements = [
        "Add temporal features: month, season, day-of-week, year trend.",
        "Use time-based train/test split (e.g., train 2015–2018, test 2019–2020).",
        "Integrate weather data (temperature, humidity, wind) from open APIs.",
        "Apply cross-validation (5-fold) for more robust model evaluation.",
        "Hyperparameter tuning via GridSearchCV or RandomizedSearchCV.",
        "Perform feature selection using LASSO or Recursive Feature Elimination (RFE).",
        "Serialize the trained model with joblib for deployment as a REST API (Flask/FastAPI).",
        "Add prediction intervals using quantile regression forests.",
        "Build an LSTM or Transformer model for actual future AQI forecasting.",
        "Scale the system to all 700+ CPCB stations across India.",
    ]
    for imp in improvements:
        story.append(bullet_item(imp))

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 16 — CONCLUSION
    # ─────────────────────────────────────────────────────────────────────────
    story.append(PageBreak())
    story += section_header("16. Conclusion")
    story.append(body(
        "This project successfully demonstrates the application of supervised machine learning "
        "to the environmental domain of air quality prediction. Three regression models were "
        "trained and evaluated on a real-world dataset of 24,850 daily pollutant readings "
        "across 26 Indian cities."
    ))
    story.append(Spacer(1, 0.2*cm))
    story.append(body(
        "The <b>Random Forest Regressor</b> emerged as the best-performing model with an "
        "<b>R² of 0.9105</b>, meaning it explains over 91% of all AQI variation in unseen test "
        "data — a strong result for a real-world, noisy environmental dataset."
    ))
    story.append(Spacer(1, 0.2*cm))
    story.append(body(
        "Feature importance analysis revealed that <b>PM2.5 (49.1%) and CO (36.8%)</b> together "
        "account for nearly 86% of predictive power, consistent with their dominant role in "
        "India's official AQI formula. The project extended beyond model training to deliver "
        "three practical outputs: an early warning system, an interactive geographic map, "
        "and reusable test scripts."
    ))
    story.append(Spacer(1, 0.3*cm))

    final_data = [
        ["Metric", "Value"],
        ["Best Model",              "Random Forest Regressor"],
        ["R² Score",                "0.9105 (91.05% variance explained)"],
        ["MAE",                     "20.60 AQI units"],
        ["RMSE",                    "40.49 AQI units"],
        ["Training Set Size",       "19,880 samples"],
        ["Testing Set Size",        "4,970 samples"],
        ["Number of Features",      "12 pollutant readings"],
        ["Number of Models Compared","3 (Linear, RF, GB)"],
        ["Cities in Dataset",       "26 Indian cities"],
        ["Date Range",              "January 2015 – July 2020"],
    ]
    story.append(make_table(final_data, [7*cm, 9.7*cm]))
    story.append(Spacer(1, 0.3*cm))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_ACCENT))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        "AQI Prediction Project — Technical Report | February 2026 | AI Course Examination Submission",
        styles["caption"]
    ))

    # ── PATCH: resolve forward-reference for NextPageTemplate ─────────────────
    for i, elem in enumerate(story):
        if isinstance(elem, _NPT_Placeholder):
            story[i] = elem.resolve()

    doc.build(story)
    print(f"✓ PDF saved: {OUTPUT_PATH}")


# Helper to switch template mid-document
from reportlab.platypus import ActionFlowable

class _NPT_Placeholder:
    def __init__(self, name):
        self.name = name
    def resolve(self):
        return NextPageTemplate_real(self.name)

def NextPageTemplate(name):          # used before class defined
    return _NPT_Placeholder(name)

class NextPageTemplate_real(ActionFlowable):
    def __init__(self, pt):
        ActionFlowable.__init__(self)
        self.pt = pt
    def apply(self, doc):
        doc._nextPageTemplateCycle = None
        try:
            doc.handle_nextPageTemplate(self.pt)
        except Exception:
            pass


if __name__ == "__main__":
    build_pdf()
