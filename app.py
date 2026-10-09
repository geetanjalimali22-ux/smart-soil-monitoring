import streamlit as st
import os
import hashlib
import pandas as pd
import serial
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
# Crop scan history
HISTORY_FILE = os.path.join(
    os.path.dirname(__file__),
    "scan_history.csv"
)

if "scan_history" not in st.session_state:

    if os.path.exists(HISTORY_FILE):

        history_df = pd.read_csv(HISTORY_FILE)

        st.session_state.scan_history = (
            history_df.to_dict("records")
        )

    else:

        st.session_state.scan_history = []


def create_pdf_report(report, recommendation):

    from io import BytesIO
    from datetime import datetime
    from zoneinfo import ZoneInfo
    from xml.sax.saxutils import escape

    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle,
        KeepTogether
    )

    # ---------------------------------------------------------
    # BASIC INFORMATION
    # ---------------------------------------------------------

    generated_at = datetime.now(
        ZoneInfo("Asia/Kolkata")
    )

    date_text = generated_at.strftime("%d %B %Y")
    time_text = generated_at.strftime("%I:%M %p")

    report_id = generated_at.strftime(
        "SSM-%Y%m%d-%H%M%S"
    )

    college_name = (
        "K. E. Society's Rajarambapu Institute of Technology"
    )

    department = (
        "Electronics & Telecommunication Engineering"
    )

    academic_year = "Environmental Science Project - AY 2026-27"

    # ---------------------------------------------------------
    # PDF BUFFER
    # ---------------------------------------------------------

    pdf_buffer = BytesIO()

    doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm
    )

    # ---------------------------------------------------------
    # COLORS
    # ---------------------------------------------------------

    dark_green = colors.HexColor("#166534")
    medium_green = colors.HexColor("#22C55E")
    light_green = colors.HexColor("#DCFCE7")
    very_light_green = colors.HexColor("#F0FDF4")

    dark_blue = colors.HexColor("#1E3A8A")
    light_blue = colors.HexColor("#EFF6FF")

    dark_text = colors.HexColor("#1F2937")
    medium_gray = colors.HexColor("#6B7280")
    light_gray = colors.HexColor("#F3F4F6")
    border_gray = colors.HexColor("#D1D5DB")

    warning_bg = colors.HexColor("#FEF3C7")
    warning_border = colors.HexColor("#F59E0B")

    white = colors.white

    # ---------------------------------------------------------
    # STYLES
    # ---------------------------------------------------------

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "PDFTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=23,
        leading=27,
        alignment=TA_CENTER,
        textColor=dark_green,
        spaceAfter=5
    )

    subtitle_style = ParagraphStyle(
        "PDFSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        alignment=TA_CENTER,
        textColor=medium_gray,
        spaceAfter=5
    )

    college_style = ParagraphStyle(
        "PDFCollege",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        alignment=TA_CENTER,
        textColor=dark_blue,
        spaceAfter=2
    )

    center_small = ParagraphStyle(
        "CenterSmall",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        alignment=TA_CENTER,
        textColor=medium_gray
    )

    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        alignment=TA_LEFT,
        textColor=dark_green,
        spaceBefore=8,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.2,
        leading=13.5,
        alignment=TA_LEFT,
        textColor=dark_text
    )

    small_style = ParagraphStyle(
        "Small",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        alignment=TA_LEFT,
        textColor=medium_gray
    )

    metric_value_style = ParagraphStyle(
        "MetricValue",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=19,
        alignment=TA_CENTER,
        textColor=dark_green
    )

    metric_label_style = ParagraphStyle(
        "MetricLabel",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        alignment=TA_CENTER,
        textColor=medium_gray
    )

    recommendation_style = ParagraphStyle(
        "Recommendation",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        alignment=TA_LEFT,
        textColor=dark_text
    )

    # ---------------------------------------------------------
    # FOOTER
    # ---------------------------------------------------------

    def add_footer(canvas, document):

        canvas.saveState()

        width, height = A4

        canvas.setStrokeColor(border_gray)
        canvas.setLineWidth(0.6)

        canvas.line(
            18 * mm,
            12 * mm,
            width - 18 * mm,
            12 * mm
        )

        canvas.setFont(
            "Helvetica",
            7.5
        )

        canvas.setFillColor(
            medium_gray
        )

        canvas.drawString(
            18 * mm,
            7 * mm,
            "Smart Soil Monitoring"
        )

        canvas.drawRightString(
            width - 18 * mm,
            7 * mm,
            f"Page {document.page}"
        )

        canvas.restoreState()

    # ---------------------------------------------------------
    # STORY
    # ---------------------------------------------------------

    story = []

    # ---------------------------------------------------------
    # HEADER
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "SMART SOIL MONITORING",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Crop Health & Soil Salinity Assessment Report",
            subtitle_style
        )
    )

    story.append(
        Paragraph(
            escape(college_name),
            college_style
        )
    )

    story.append(
        Paragraph(
            escape(department),
            center_small
        )
    )

    story.append(
        Paragraph(
            escape(academic_year),
            center_small
        )
    )

    story.append(
        Spacer(1, 10)
    )

    # ---------------------------------------------------------
    # REPORT INFORMATION
    # ---------------------------------------------------------

    information_data = [
        [
            Paragraph(
                "<b>Report ID</b>",
                small_style
            ),
            Paragraph(
                escape(report_id),
                small_style
            ),
            Paragraph(
                "<b>Generated</b>",
                small_style
            ),
            Paragraph(
                escape(
                    f"{date_text}, {time_text} IST"
                ),
                small_style
            )
        ]
    ]

    information_table = Table(
        information_data,
        colWidths=[
            27 * mm,
            43 * mm,
            25 * mm,
            65 * mm
        ]
    )

    information_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                light_blue
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.8,
                border_gray
            ),
            (
                "INNERGRID",
                (0, 0),
                (-1, -1),
                0.3,
                border_gray
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                6
            )
        ])
    )

    story.append(
        information_table
    )

    story.append(
        Spacer(1, 13)
    )

    # ---------------------------------------------------------
    # EXECUTIVE SUMMARY
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "1. Assessment Summary",
            section_style
        )
    )

    summary_data = [
        [
            Paragraph(
                "<b>Crop</b>",
                metric_label_style
            ),
            Paragraph(
                "<b>Growth Stage</b>",
                metric_label_style
            ),
            Paragraph(
                "<b>Soil EC</b>",
                metric_label_style
            ),
            Paragraph(
                "<b>Stress Score</b>",
                metric_label_style
            )
        ],
        [
            Paragraph(
                escape(
                    str(report.get("Crop", "-"))
                ),
                metric_value_style
            ),
            Paragraph(
                escape(
                    str(report.get("Growth Stage", "-"))
                ),
                metric_value_style
            ),
            Paragraph(
                escape(
                    str(report.get("Soil EC", "-"))
                ),
                metric_value_style
            ),
            Paragraph(
                escape(
                    str(
                        report.get(
                            "Visible Plant Stress Score",
                            "-"
                        )
                    )
                ),
                metric_value_style
            )
        ]
    ]

    summary_table = Table(
        summary_data,
        colWidths=[
            40 * mm,
            45 * mm,
            35 * mm,
            40 * mm
        ]
    )

    summary_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                very_light_green
            ),
            (
                "BACKGROUND",
                (0, 1),
                (-1, 1),
                white
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.8,
                medium_green
            ),
            (
                "INNERGRID",
                (0, 0),
                (-1, -1),
                0.4,
                border_gray
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7
            )
        ])
    )

    story.append(
        summary_table
    )

    story.append(
        Spacer(1, 14)
    )

    # ---------------------------------------------------------
    # IMAGE ANALYSIS RESULTS
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "2. Plant Image Analysis",
            section_style
        )
    )

    image_data = [
    [
        "Parameter",
        "Measured Result",
        "Interpretation"
    ],
    [
        "Green Coverage",
        str(report.get("Green Coverage", "-")),
        "Percentage of image pixels detected as green"
    ],
    [
        "Average Leaf Hue",
        str(report.get("Average Leaf Hue", "-")),
        "Image-based color indicator"
    ],
    [
        "Visible Plant Stress",
        str(report.get("Visible Plant Stress Score", "-")),
        "Screening indicator from image features"
    ],
    [
        "Temperature",
        str(report.get("Temperature", "-")),
        "Environmental sensor value"
    ],
    [
        "Humidity",
        str(report.get("Humidity", "-")),
        "Environmental sensor value"
    ],
    [
        "Soil Moisture",
        str(report.get("Soil Moisture", "-")),
        "Environmental sensor value"
    ]
]

  

    image_table_data = []

    for row_index, row in enumerate(image_data):

        formatted_row = []

        for value in row:

            if row_index == 0:
                formatted_row.append(
                    Paragraph(
                        str(value),
                        body_style
                    )
                )
            else:
                formatted_row.append(
                    Paragraph(
                        escape(str(value)),
                        body_style
                    )
                )

        image_table_data.append(
            formatted_row
        )

    image_table = Table(
        image_table_data,
        colWidths=[
            43 * mm,
            42 * mm,
            75 * mm
        ],
        repeatRows=1
    )

    image_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                dark_green
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                white
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.8,
                border_gray
            ),
            (
                "INNERGRID",
                (0, 0),
                (-1, -1),
                0.35,
                border_gray
            ),
            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [white, very_light_green]
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                6
            )
        ])
    )

    story.append(
        image_table
    )

    story.append(
        Spacer(1, 14)
    )

    # ---------------------------------------------------------
    # ASSESSMENT RESULT
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "3. Assessment Result",
            section_style
        )
    )

    result_data = [
        [
            Paragraph(
                "<b>Assessment</b>",
                body_style
            ),
            Paragraph(
                "<b>Result</b>",
                body_style
            )
        ],
        [
            "Crop Health",
            str(
                report.get(
                    "Crop Health",
                    "-"
                )
            )
        ],
        [
            "Salinity Risk",
            str(
                report.get(
                    "Risk Level",
                    "-"
                )
            )
        ],
        [
            "Growth Status",
            str(
                report.get(
                    "Growth Status",
                    "-"
                )
            )
        ],
        [
    "Overall Crop Condition",
    str(
        report.get(
            "Overall Crop Condition Score",
            "-"
        )
    )
]
    ]

    result_table_data = []

    for row_index, row in enumerate(result_data):

        if row_index == 0:
            # Header cells are already Paragraph objects
            result_table_data.append(row)

        else:
            result_table_data.append([
                Paragraph(
                    escape(str(row[0])),
                    body_style
                ),
                Paragraph(
                    escape(str(row[1])),
                    body_style
                )
            ])

    result_table = Table(
        result_table_data,
        colWidths=[
            60 * mm,
            100 * mm
        ],
        repeatRows=1
    )

    result_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                dark_blue
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                white
            ),
            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [white, light_gray]
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.8,
                border_gray
            ),
            (
                "INNERGRID",
                (0, 0),
                (-1, -1),
                0.35,
                border_gray
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7
            )
        ])
    )

    story.append(
        result_table
    )

    story.append(
        Spacer(1, 14)
    )

    # ---------------------------------------------------------
    # MANAGEMENT RECOMMENDATION
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "4. Management Recommendation",
            section_style
        )
    )

    recommendation_box = Table(
        [[
            Paragraph(
                escape(
                    str(recommendation)
                ),
                recommendation_style
            )
        ]],
        colWidths=[160 * mm]
    )

    recommendation_box.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                light_green
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                1.0,
                medium_green
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                12
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                12
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                11
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                11
            )
        ])
    )

    story.append(
        recommendation_box
    )

    story.append(
        Spacer(1, 14)
    )

    # ---------------------------------------------------------
    # IMPORTANT SCIENTIFIC NOTE
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "5. Important Interpretation Note",
            section_style
        )
    )

    note_text = (
        "<b>Screening / advisory assessment:</b><br/>"
        "This system uses plant-image features and the entered soil EC "
        "to provide a preliminary crop-condition assessment. "
        "A photograph alone cannot directly measure soil salinity. "
        "Actual soil salinity should be verified using an appropriate "
        "electrical-conductivity test and suitable soil sampling method. "
        "Crop appearance can also be affected by irrigation, drainage, "
        "nutrient availability, drought, disease and other environmental factors."
    )

    note_box = Table(
        [[
            Paragraph(
                note_text,
                small_style
            )
        ]],
        colWidths=[160 * mm]
    )

    note_box.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                warning_bg
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.8,
                warning_border
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                12
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                12
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                10
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                10
            )
        ])
    )

    story.append(
        note_box
    )

    story.append(
        Spacer(1, 12)
    )

    # ---------------------------------------------------------
    # PROJECT DESCRIPTION
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "6. About the Project",
            section_style
        )
    )

    project_description = (
        "Smart Soil Monitoring is an AI-assisted Environmental Science "
        "project that combines plant image analysis, crop growth-stage "
        "information and soil EC input to study visible crop responses "
        "associated with soil salinity. The system generates a crop-health "
        "screening report and basic management guidance."
    )

    story.append(
        Paragraph(
            project_description,
            body_style
        )
    )

    story.append(
        Spacer(1, 12)
    )

    # ---------------------------------------------------------
    # FINAL FOOTER BOX
    # ---------------------------------------------------------

    final_box = Table(
        [[
            Paragraph(
                "<b>Smart Soil Monitoring Application</b><br/>"
                "Environmental Science Project | AY 2026-27",
                center_small
            )
        ]],
        colWidths=[160 * mm]
    )

    final_box.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                very_light_green
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.7,
                border_gray
            ),
            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                8
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                8
            )
        ])
    )

    story.append(
        final_box
    )

    # ---------------------------------------------------------
    # BUILD PDF
    # ---------------------------------------------------------

    doc.build(
        story,
        onFirstPage=add_footer,
        onLaterPages=add_footer
    )

    pdf_buffer.seek(0)

    return pdf_buffer.getvalue()

from image_analysis import analyze_plant_image


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Smart Soil Salinity Monitoring",
    page_icon="🌱",
    layout="centered"
)
# --------------------------------------------------
# SENSOR DATA LAYER
# --------------------------------------------------

st.sidebar.subheader("📡 Sensor Data")

sensor_mode = st.sidebar.selectbox(
    "Sensor Mode",
    [
        "Software Demo Mode",
        "Arduino Mode (USB)"
    ]
)

# Store the last successful Arduino reading between reruns.
if "arduino_readings" not in st.session_state:
    st.session_state["arduino_readings"] = None

if sensor_mode == "Software Demo Mode":

    sensor_temperature = st.sidebar.number_input(
        "🌡️ Temperature (°C)",
        min_value=-10.0,
        max_value=60.0,
        value=32.8,
        step=0.1,
        key="sensor_temperature_demo"
    )

    sensor_humidity = st.sidebar.number_input(
        "💧 Air Humidity (%)",
        min_value=0.0,
        max_value=100.0,
        value=50.0,
        step=1.0,
        key="sensor_humidity_demo"
    )

    sensor_soil_moisture = st.sidebar.number_input(
        "🌱 Soil Moisture (%)",
        min_value=0.0,
        max_value=100.0,
        value=51.0,
        step=1.0,
        key="sensor_soil_moisture_demo"
    )

    sensor_source = "Software demo values"

else:

    # Arduino Uno commonly appears as /dev/ttyACM0 on Ubuntu.
    # Some boards or adapters may use /dev/ttyUSB0 instead.

    serial_port = st.sidebar.text_input(
        "Arduino USB Port",
        value="/dev/ttyACM0",
        help="Example: /dev/ttyACM0 or /dev/ttyUSB0"
    )

    st.sidebar.caption(
        "Baud rate: 9600. The Arduino sketch must send "
        "temperature,humidity,soil_raw,soil_moisture_percent."
    )

    if st.sidebar.button("🔄 Read Arduino Values"):

        try:
            reading = None

            # Open the port, wait for the board to restart,
            # and look for a valid comma-separated reading.
            with serial.Serial(
                serial_port.strip(),
                9600,
                timeout=1
            ) as arduino:

                time.sleep(2)

                for _ in range(8):

                    line = arduino.readline().decode(
                        "utf-8",
                        errors="ignore"
                    ).strip()

                    parts = line.split(",")

                    if len(parts) != 4:
                        continue

                    try:
                        temperature = float(parts[0])
                        humidity = float(parts[1])
                        soil_raw = int(parts[2])
                        soil_moisture = float(parts[3])

                    except ValueError:
                        continue

                    # Reject obviously invalid sensor values.
                    if not (
                        -10 <= temperature <= 60
                        and 0 <= humidity <= 100
                        and 0 <= soil_raw <= 1023
                        and 0 <= soil_moisture <= 100
                    ):
                        continue

                    reading = {
                        "Temperature": temperature,
                        "Humidity": humidity,
                        "Soil Raw": soil_raw,
                        "Soil Moisture": soil_moisture
                    }

                    break

            if reading is not None:
                st.session_state["arduino_readings"] = reading
                st.sidebar.success(
                    "Arduino reading received successfully."
                )

            else:
                st.sidebar.error(
                    "No valid sensor reading received. "
                    "Check the Arduino sketch, baud rate and wiring."
                )

        except (serial.SerialException, OSError) as error:
            st.sidebar.error(
                f"Could not read Arduino USB port: {error}"
            )

    arduino_readings = st.session_state["arduino_readings"]

    if arduino_readings is not None:

        sensor_temperature = arduino_readings["Temperature"]
        sensor_humidity = arduino_readings["Humidity"]
        sensor_soil_moisture = arduino_readings["Soil Moisture"]

        sensor_source = "Arduino USB — last successful reading"

        st.sidebar.write(
            f"Soil sensor raw value: "
            f"{arduino_readings['Soil Raw']}"
        )

    else:

        # Fallback values keep the rest of the app operational.
        # They are NOT real Arduino readings.

        sensor_temperature = 32.8
        sensor_humidity = 50.0
        sensor_soil_moisture = 51.0

        sensor_source = "Demo fallback — no Arduino reading"

        st.sidebar.warning(
            "No Arduino reading is saved yet. "
            "Displayed values are simulated, not live."
        )

# Keep the existing assessment and report inputs consistent.
sensor_data = {
    "Temperature": sensor_temperature,
    "Humidity": sensor_humidity,
    "Soil Moisture": sensor_soil_moisture
}

st.info(
    f"📡 **Sensor source:** {sensor_source} | "
    f"🌡️ {sensor_temperature:.1f} °C | "
    f"💧 {sensor_humidity:.0f}% | "
    f"🌱 {sensor_soil_moisture:.0f}%"
)
# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🌱 Smart Soil Monitoring")

st.sidebar.subheader("Project")

st.sidebar.write(
    "AI-based plant image analysis for "
    "visual salinity-stress assessment."
)

st.sidebar.subheader("Analyzed Parameters")

st.sidebar.write(
    "🌿 Green Area\n"
    "🍃 Green Coverage\n"
    "🎨 Leaf Color\n"
    "🧂 Stress Score\n"
    "🌱 Growth Status"
)

st.sidebar.subheader("Important Note")

st.sidebar.info(
    "Plant images provide visual indicators only. "
    "Actual soil salinity should be verified using "
    "a soil electrical-conductivity (EC) test."
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

# --------------------------------------------------
# PROJECT HEADER
# --------------------------------------------------

st.title("🌱 Smart Soil Salinity Monitoring")

st.subheader(
    "AI-Based Soil Salinity Stress and Crop Growth "
    "Assessment System"
)

st.write(
    "A software-based system that analyzes plant images "
    "to estimate visible salinity-stress risk and assess "
    "crop growth indicators."
)

st.divider()

st.info(
    "📌 Upload a clear plant photograph. "
    "The system analyzes plant greenness and leaf color "
    "to estimate visible salinity-stress risk."
)


# --------------------------------------------------
# LIVE SENSOR DASHBOARD
# --------------------------------------------------

st.header("📡 Environmental Sensor Dashboard")

sensor_col1, sensor_col2, sensor_col3 = st.columns(3)

with sensor_col1:
    st.metric(
        "🌡️ Temperature",
        f"{sensor_temperature:.1f} °C"
    )

with sensor_col2:
    st.metric(
        "💧 Humidity",
        f"{sensor_humidity:.0f} %"
    )

with sensor_col3:
    st.metric(
        "🌱 Soil Moisture",
        f"{sensor_soil_moisture:.0f} %"
    )

st.caption(
    "Current values are software-demo inputs. "
    "Arduino integration will replace these values later."
)

st.divider()

# --------------------------------------------------
# CROP SELECTION
# --------------------------------------------------

st.header("🌾 Select Crop")

crop = st.selectbox(
    "Choose the crop",
    [
        "Rice",
        "Wheat",
        "Maize",
        "Cotton",
        "Sugarcane"
    ]
)
growth_stage = st.selectbox(
    "🌱 Select Crop Growth Stage",
    [
        "Seedling",
        "Tillering / Vegetative",
        "Flowering / Panicle Formation",
        "Grain Filling",
        "Maturity / Harvest"
    ]
)

st.info(f"Selected Growth Stage: {growth_stage}")
soil_ec = st.number_input(
    "🧪 Enter Soil EC (dS/m)",
    min_value=0.0,
    max_value=20.0,
    value=1.0,
    step=0.1
)

st.info(f"Current Soil EC: {soil_ec:.2f} dS/m")

st.success(f"Selected Crop: {crop}")


# --------------------------------------------------
# PLANT IMAGE UPLOAD
# --------------------------------------------------

st.header("📷 Upload Plant Image")

uploaded_file = st.file_uploader(
    "Upload a clear plant photograph",
    type=["jpg", "jpeg", "png"]
)
# --------------------------------------------------
# IMAGE ANALYSIS AND CROP ASSESSMENT
# --------------------------------------------------

if uploaded_file is not None:

    # Read and display uploaded image
    image_bytes = uploaded_file.getvalue()

    st.image(
        image_bytes,
        caption="Uploaded Plant Image",
        width="stretch"
    )

    # Analyze uploaded image
    green_percentage, average_hue, leaf_area_percentage = (
        analyze_plant_image(image_bytes)
    )

    # --------------------------------------------------
    # IMAGE FEATURES
    # --------------------------------------------------

    st.header("🔍 Plant Image Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🌿 Green Area",
            f"{green_percentage:.2f}%"
        )

    with col2:
        st.metric(
            "🌿 Green Coverage",
            f"{leaf_area_percentage:.2f}%"
        )

    with col3:
        st.metric(
            "🎨 Average Leaf Hue",
            f"{average_hue:.2f}"
        )

    # --------------------------------------------------
    # STRESS ESTIMATION
    # --------------------------------------------------

    st.header("🧂 Salinity-Stress Estimation")

    crop_thresholds = {
        "Rice": {"green": 70, "hue": 35},
        "Wheat": {"green": 65, "hue": 35},
        "Maize": {"green": 70, "hue": 35},
        "Cotton": {"green": 65, "hue": 35},
        "Sugarcane": {"green": 70, "hue": 35}
    }

    green_threshold = crop_thresholds[crop]["green"]
    hue_threshold = crop_thresholds[crop]["hue"]

    # Adjust the green threshold for the selected growth stage.
    stage_thresholds = {
        "Seedling": 60,
        "Tillering / Vegetative": 60,
        "Flowering / Panicle Formation": 55,
        "Grain Filling": 45,
        "Maturity / Harvest": 35
    }

    green_threshold = stage_thresholds[growth_stage]

    green_stress = max(
        0,
        min(
            100,
            (green_threshold - green_percentage) * 2
        )
    )

    hue_stress = max(
        0,
        min(
            100,
            (hue_threshold - average_hue) * 3
        )
    )

    stress_score = (
        0.50 * green_stress
        + 0.20 * hue_stress
    )

    stress_score = round(
        max(0, min(100, stress_score)),
        1
    )

    # --------------------------------------------------
    # SALINITY RISK
    # --------------------------------------------------

    if soil_ec <= 2.0:
        stress_level = "Low Salinity Risk"

    elif soil_ec <= 4.0:
        stress_level = "Moderate Salinity Risk"

    else:
        stress_level = "High Salinity Risk"

    st.subheader("🧪 Soil Salinity Risk")

    st.write(
        f"**Entered Soil EC:** {soil_ec:.2f} dS/m"
    )

    if soil_ec <= 2.0:
        st.success(f"🟢 {stress_level}")

    elif soil_ec <= 4.0:
        st.warning(f"🟡 {stress_level}")

    else:
        st.error(f"🔴 {stress_level}")

    # --------------------------------------------------
    # CROP HEALTH ASSESSMENT
    # --------------------------------------------------

    st.header("🌱 Crop Health Assessment")

    if soil_ec > 4.0:
        health_status = "High Salinity Concern"

        st.error(
            "🔴 The entered soil EC indicates high salinity "
            "concern. Verify it with a proper soil test."
        )

    elif soil_ec > 2.0:
        health_status = "Monitor Crop Health"

        st.warning(
            "🟡 Monitor crop development and verify soil EC, "
            "irrigation and drainage conditions."
        )

    elif (
        growth_stage == "Maturity / Harvest"
        and stress_score <= 30
    ):
        health_status = "Healthy / Normal Maturity"

        st.success(
            "🟢 The crop has low estimated visible stress. "
            "Yellowing may be normal during crop maturity."
        )

    elif stress_score <= 30:
        health_status = "Healthy / Low Salinity Concern"

        st.success(
            "🟢 The image shows low estimated visible stress, "
            "and the entered soil EC indicates low concern."
        )

    else:
        health_status = "Monitor Crop Health"

        st.warning(
            "🟡 Visible stress may be present. Other causes "
            "such as drought, disease or nutrient deficiency "
            "should also be investigated."
        )

    st.write(
        f"**Crop Health Status:** {health_status}"
    )

    # --------------------------------------------------
    # PLANT GROWTH ASSESSMENT
    # --------------------------------------------------

    st.header("🌱 Plant Growth Assessment")

    if growth_stage == "Maturity / Harvest":

        if leaf_area_percentage >= 15:
            growth_status = "Normal Maturity / Harvest Stage"

            st.success(
                "🌾 The crop is at maturity/harvest stage. "
                "Reduced green coverage may occur naturally "
                "during maturity."
            )

        else:
            growth_status = "Low Visible Green Coverage"

            st.warning(
                "⚠️ Very low green coverage was detected. "
                "Check the crop image and field conditions."
            )

    elif growth_stage == "Grain Filling":

        if leaf_area_percentage >= 45:
            growth_status = "Good Grain-Filling Appearance"

            st.success(
                "🌾 The image shows relatively high green coverage "
                "for the selected grain-filling stage."
            )

        else:
            growth_status = "Reduced Green Coverage"

            st.warning(
                "⚠️ Reduced green coverage was detected. "
                "Monitor crop development and verify soil EC."
            )

    elif growth_stage == "Flowering / Panicle Formation":

        if leaf_area_percentage >= 55:
            growth_status = "Good Flowering-Stage Appearance"

            st.success(
                "🌱 The image shows relatively high green coverage "
                "for the selected flowering stage."
            )

        else:
            growth_status = "Reduced Green Coverage"

            st.warning(
                "⚠️ Reduced green coverage was detected. "
                "Check soil EC and other crop conditions."
            )

    else:

        if leaf_area_percentage >= 60:
            growth_status = "Good Visible Green Coverage"

            st.success(
                "🌱 The image shows relatively high green coverage."
            )

        elif leaf_area_percentage >= 45:
            growth_status = "Moderate Visible Green Coverage"

            st.warning(
                "🟡 The image shows moderate green coverage."
            )

        else:
            growth_status = "Low Visible Green Coverage"

            st.warning(
                "⚠️ Low green coverage was detected. "
                "Check the image and other crop conditions."
            )

    st.write(
        f"**Visual Growth Status:** {growth_status}"
    )

    st.caption(
        "This assessment uses image features. Actual plant height, "
        "biomass and growth rate require additional measurements."
    )

    # --------------------------------------------------
    # MANAGEMENT RECOMMENDATION
    # --------------------------------------------------

    st.header("💡 Management Recommendation")

    if soil_ec > 4.0:

        recommendation = (
            "The entered soil EC indicates high salinity concern. "
            "Verify the reading using an appropriate soil EC test, "
            "and review irrigation, drainage and crop conditions."
        )

    elif soil_ec > 2.0:

        recommendation = (
            "Monitor crop development and verify the soil EC "
            "reading. Review irrigation and drainage, and check "
            "for other possible causes of visible crop stress."
        )

    elif growth_stage == "Maturity / Harvest":

        recommendation = (
            "The crop is at maturity/harvest stage. Some yellowing "
            "can be natural. Continue normal harvest planning and "
            "monitor field conditions."
        )

    elif stress_score <= 30:

        recommendation = (
            "The crop shows low estimated visible stress. Continue "
            "normal monitoring and suitable irrigation and "
            "soil-management practices."
        )

    elif stress_score <= 60:

        recommendation = (
            "The crop shows possible visible stress. Monitor it "
            "more frequently and check soil EC, irrigation, drainage, "
            "nutrient availability and disease symptoms."
        )

    else:

        recommendation = (
            "The crop shows elevated estimated visible stress. "
            "Verify soil EC and investigate irrigation, drainage, "
            "drought, nutrient deficiency, disease and other "
            "possible causes before deciding on corrective action."
        )

    # Add environmental sensor advice.
    sensor_advice = []

    if sensor_soil_moisture < 30:
        sensor_advice.append(
            "Demo soil-moisture value is low; check irrigation needs."
        )

    elif sensor_soil_moisture > 70:
        sensor_advice.append(
            "Demo soil-moisture value is high; check drainage."
        )

    if sensor_temperature > 35:
        sensor_advice.append(
            "Demo temperature is high; monitor for heat stress."
        )

    elif sensor_temperature < 15:
        sensor_advice.append(
            "Demo temperature is low; monitor crop development."
        )

    if sensor_humidity > 80:
        sensor_advice.append(
            "Demo humidity is high; monitor for disease-favorable conditions."
        )

    elif sensor_humidity < 40:
        sensor_advice.append(
            "Demo humidity is low; monitor crop water requirements."
        )

    if sensor_advice:
        recommendation += (
            " Environmental conditions: "
            + " ".join(sensor_advice)
        )

    st.info(recommendation)

    # --------------------------------------------------
    # STRESS DASHBOARD
    # --------------------------------------------------

    st.header("📊 Stress & Crop Condition Dashboard")

    dash1, dash2, dash3 = st.columns(3)

    with dash1:
        st.metric(
            "🌿 Green Area",
            f"{green_percentage:.1f}%"
        )

    with dash2:
        st.metric(
            "🎨 Leaf Hue",
            f"{average_hue:.1f}"
        )

    with dash3:
        st.metric(
            "🧂 Stress Score",
            f"{stress_score:.1f}/100"
        )

    st.progress(int(stress_score))

    chart_data = pd.DataFrame({
        "Parameter": [
            "Green Area",
            "Leaf Hue",
            "Stress Score"
        ],
        "Value": [
            green_percentage,
            average_hue,
            stress_score
        ]
    })

    st.bar_chart(
        chart_data.set_index("Parameter")
    )

    if stress_score <= 30:
        st.success(
            "🟢 Low estimated visible plant stress."
        )

    elif stress_score <= 60:
        st.warning(
            "🟡 Moderate estimated visible plant stress."
        )

    else:
        st.error(
            "🔴 High estimated visible plant stress."
        )

    st.caption(
        "The stress score is a prototype image-based screening "
        "estimate, not a direct measurement of soil salinity."
    )

    # --------------------------------------------------
    # OVERALL CROP CONDITION SCORE
    # --------------------------------------------------

    st.header("🧠 Overall Crop Condition")

    sensor_score = 0

    if 30 <= sensor_soil_moisture <= 70:
        sensor_score += 10
    else:
        sensor_score += 5

    if 15 <= sensor_temperature <= 35:
        sensor_score += 10
    else:
        sensor_score += 5

    if 40 <= sensor_humidity <= 80:
        sensor_score += 10
    else:
        sensor_score += 5

    overall_score = (
        (100 - stress_score) * 0.6
        + sensor_score
        + max(0, 20 - soil_ec * 5)
    )

    overall_score = round(
        max(0, min(100, overall_score)),
        1
    )

    st.metric(
        "🌱 Overall Crop Condition Score",
        f"{overall_score:.1f}/100"
    )

    st.progress(int(overall_score))

    if overall_score >= 75:
        st.success(
            "🟢 The prototype score indicates a favorable condition."
        )

    elif overall_score >= 50:
        st.warning(
            "🟡 The prototype score indicates a need for monitoring."
        )

    else:
        st.error(
            "🔴 The prototype score indicates increased concern."
        )

    st.caption(
        "This is a prototype score combining image-based stress, "
        "entered soil EC and environmental demo values. It is not "
        "a validated agronomic index."
    )

    # --------------------------------------------------
    # SAVE SCAN HISTORY
    # --------------------------------------------------

    scan_id = hashlib.md5(image_bytes).hexdigest()

    if (
        not st.session_state.scan_history
        or st.session_state.scan_history[-1].get("ID") != scan_id
    ):

        scan_record = {
            "ID": scan_id,
            "Time": datetime.now(
                ZoneInfo("Asia/Kolkata")
            ).strftime("%d-%m-%Y %H:%M"),
            "Crop": crop,
            "Growth Stage": growth_stage,
            "Green Coverage": leaf_area_percentage,
            "Stress Score": stress_score,
            "Overall Score": overall_score,
            "Health": health_status
        }

        st.session_state.scan_history.append(scan_record)

        pd.DataFrame(
            st.session_state.scan_history
        ).to_csv(
            HISTORY_FILE,
            index=False
        )

    # --------------------------------------------------
    # CREATE PDF REPORT
    # --------------------------------------------------

    report = {
        "Crop": crop,
        "Growth Stage": growth_stage,
        "Crop Health": health_status,
        "Soil EC": f"{soil_ec:.2f} dS/m",
        "Green Coverage": f"{leaf_area_percentage:.2f}%",
        "Average Leaf Hue": f"{average_hue:.2f}",
        "Visible Plant Stress Score": f"{stress_score}/100",
        "Overall Crop Condition Score": f"{overall_score:.1f}/100",
        "Risk Level": stress_level,
        "Health Status": health_status,
        "Growth Status": growth_status,
        "Temperature": f"{sensor_temperature:.1f} °C",
        "Humidity": f"{sensor_humidity:.0f}%",
        "Soil Moisture": f"{sensor_soil_moisture:.0f}%"
    }

    pdf_data = create_pdf_report(
        report,
        recommendation
    )

    st.download_button(
        label="📄 Download Crop Health Report (PDF)",
        data=pdf_data,
        file_name="Smart_Soil_Crop_Health_Report.pdf",
        mime="application/pdf"
    )

    st.warning(
        "⚠️ A plant photograph cannot directly measure soil "
        "salinity. Use an appropriate soil electrical-conductivity "
        "(EC) test to verify actual salinity."
    )

else:
    st.info(
        "Upload a plant image to display the image analysis, "
        "crop assessment and downloadable PDF report."
    )


# --------------------------------------------------
# SCAN COMPARISON
# --------------------------------------------------

st.header("📊 Compare Recent Scans")

history = st.session_state.scan_history

if len(history) >= 2:

    previous_scan = history[-2]
    current_scan = history[-1]

    st.subheader("Latest vs Previous Scan")

    previous_green = pd.to_numeric(
        previous_scan.get("Green Coverage"),
        errors="coerce"
    )

    current_green = pd.to_numeric(
        current_scan.get("Green Coverage"),
        errors="coerce"
    )

    previous_stress = pd.to_numeric(
        previous_scan.get("Stress Score"),
        errors="coerce"
    )

    current_stress = pd.to_numeric(
        current_scan.get("Stress Score"),
        errors="coerce"
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        if pd.notna(previous_green) and pd.notna(current_green):
            green_change = float(current_green - previous_green)

            st.metric(
                "🌿 Green Coverage Change",
                f"{green_change:+.2f} percentage points"
            )
        else:
            st.metric(
                "🌿 Green Coverage Change",
                "Unavailable"
            )

    with c2:
        if pd.notna(previous_stress) and pd.notna(current_stress):
            stress_change = float(current_stress - previous_stress)

            st.metric(
                "🧂 Stress Score Change",
                f"{stress_change:+.1f}"
            )
        else:
            st.metric(
                "🧂 Stress Score Change",
                "Unavailable"
            )

    with c3:
        st.metric(
            "🌱 Current Health",
            str(current_scan.get("Health", "Not assessed"))
        )

    previous_overall = pd.to_numeric(
        previous_scan.get("Overall Score"),
        errors="coerce"
    )

    current_overall = pd.to_numeric(
        current_scan.get("Overall Score"),
        errors="coerce"
    )

    if pd.notna(previous_overall) and pd.notna(current_overall):

        overall_change = float(current_overall - previous_overall)

        st.metric(
            "🧠 Overall Score Change",
            f"{overall_change:+.1f} points"
        )

    else:
        st.info(
            "Overall-score comparison will appear after two scans "
            "with saved overall scores."
        )

    st.write(
        f"**Previous Scan:** {previous_scan.get('Time', '-')}"
    )

    st.write(
        f"**Current Scan:** {current_scan.get('Time', '-')}"
    )

else:
    st.info(
        "Upload at least two different plant images to compare scans."
    )


# --------------------------------------------------
# SCAN HISTORY
# --------------------------------------------------

st.header("📜 Scan History")

if st.session_state.scan_history:

    history_df = pd.DataFrame(
        st.session_state.scan_history
    )

    history_df = history_df.drop(
        columns=["ID"],
        errors="ignore"
    )

    st.dataframe(
        history_df,
        hide_index=True
    )

else:
    st.info("No previous scans available yet.")