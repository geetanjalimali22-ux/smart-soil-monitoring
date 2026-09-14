import streamlit as st
import pandas as pd

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
    "🍃 Leaf Area\n"
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
# IMAGE ANALYSIS
# --------------------------------------------------

if uploaded_file is not None:

    # Display uploaded image
    st.image(
        uploaded_file,
        caption="Uploaded Plant Image",
        use_container_width=True
    )

    # Read image
    image_bytes = uploaded_file.getvalue()

    # Analyze image
    green_percentage, average_hue, leaf_area_percentage = analyze_plant_image(
    image_bytes
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
            "🍃 Leaf Area",
            f"{leaf_area_percentage:.2f}%"
        )

    with col3:
        st.metric(
            "🎨 Average Leaf Hue",
            f"{average_hue:.2f}"
        )


    # --------------------------------------------------
    # VISUAL SALINITY-STRESS ESTIMATION
    # --------------------------------------------------

    st.header("🧂 Salinity-Stress Estimation")

    # Calculate stress from plant image features.
    # Higher stress is associated with lower greenness
    # and lower leaf-color values.

    # --------------------------------------------------
    # CROP-SPECIFIC THRESHOLDS
    # --------------------------------------------------

    crop_thresholds = {

        "Rice": {
            "green": 70,
            "hue": 35
        },

        "Wheat": {
            "green": 65,
            "hue": 35
        },

        "Maize": {
            "green": 70,
            "hue": 35
        },

        "Cotton": {
            "green": 65,
            "hue": 35
        },

        "Sugarcane": {
            "green": 70,
            "hue": 35
        }
    }


    green_threshold = crop_thresholds[crop]["green"]
    hue_threshold = crop_thresholds[crop]["hue"]


    # --------------------------------------------------
    # CALCULATE IMAGE-BASED STRESS
    # --------------------------------------------------
    if growth_stage == "Maturity / Harvest":
        green_threshold = 35
    elif growth_stage == "Grain Filling":
        green_threshold = 45
    elif growth_stage == "Flowering / Panicle Formation":
        green_threshold = 55
    elif growth_stage == "Tillering / Vegetative":
        green_threshold = 60
    else:
        green_threshold = 60

    green_stress = max(
        0,
        min(100, (green_threshold - green_percentage) * 2)
    )
    hue_stress = max(0, min(100, (hue_threshold - average_hue) * 3))


    # Combined salinity-stress score
    stress_score = (
        0.50 * green_stress +
        0.20 * hue_stress 
    )
    stress_score = max(
        0,
        min(
            100,
            stress_score
        )
    )

    stress_score = round(
        stress_score,
        1
    )

    # --------------------------------------------------
    # RISK LEVEL
    # --------------------------------------------------

    if soil_ec <= 2.0:

        stress_level = "Low Salinity Risk"
        status = "Low Salinity Concern"

        st.success(
            f"🟢 {stress_level}"
        )

        if growth_stage == "Maturity / Harvest":
            suggestion = (
                "The crop is at maturity/harvest stage. "
                "Yellowing can be normal. Plan harvesting at "
                "the appropriate maturity and continue checking soil EC."
            )
        else:
            suggestion = (
                "The crop shows low visible stress. "
                "Continue normal crop monitoring and maintain "
                "appropriate irrigation and soil management."
            )
    elif soil_ec <= 4.0:
        suggestion = (
    "Monitor the crop closely. "
    "Verify soil EC with a proper soil test and "
    "check irrigation, drainage, and crop development."
    )


    else:
        suggestion = (
    "High salinity concern requires verification. "
    "Repeat the soil EC measurement, check irrigation "
    "and drainage, and assess the crop for other possible causes of stress."
    )

    # --------------------------------------------------
    # STRESS SCORE
    # --------------------------------------------------

    st.subheader("📊 Visible Plant Stress Score")

    st.metric(
        "Estimated Stress Score",
        f"{stress_score}/100"
    )

    st.progress(
        int(stress_score)
    )
    # --------------------------------------------------
    # STRESS VISUALIZATION
    # --------------------------------------------------

    st.subheader("📈 Stress Level Visualization")

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

    st.caption(
        "0 = very low visible stress | "
        "100 = very high visible stress"
    )

    # --------------------------------------------------
    # RESULT
    # --------------------------------------------------
    
    st.header("🌱 Crop Health Assessment")
    # CROP HEALTH ASSESSMENT

    if growth_stage == "Maturity / Harvest" and soil_ec <= 2.0:

        health_status = "Healthy / Normal Maturity"

        st.success(
            "🟢 The crop appears healthy for the selected "
            "maturity stage. Yellowing can be normal during "
            "rice maturity."
        )

    elif soil_ec <= 2.0 and stress_score <= 30:

        health_status = "Healthy / Low Salinity Concern"

        st.success(
            "🟢 The crop shows low visible stress and "
            "low salinity concern based on the entered soil EC."
        )

    elif soil_ec <= 4.0:

        health_status = "Monitor Crop Health"

        st.warning(
            "🟡 The crop should be monitored. "
            "Salinity risk may be present, so verify soil EC "
            "and observe crop development."
        )

    else:

        health_status = "High Salinity Concern"

        st.error(
            "🔴 High salinity concern detected from the "
            "entered soil EC. Verify the EC measurement "
            "and investigate crop conditions."
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
                "Yellowing and reduced green coverage can be normal "
                "during rice maturity."
            )

        else:
            growth_status = "Low Visible Green Coverage"

            st.warning(
                "⚠️ Very low green coverage was detected. "
                "At maturity this may be natural senescence, but "
                "soil EC and field conditions should be checked."
            )

    elif growth_stage == "Grain Filling":

        if leaf_area_percentage >= 45:
            growth_status = "Good Grain-Filling Appearance"

            st.success(
                "🌾 The crop shows good visible green coverage "
                "for the grain-filling stage."
            )

        else:
            growth_status = "Reduced Green Coverage"

            st.warning(
                "⚠️ Reduced green coverage detected during grain filling. "
                "Monitor crop condition and verify soil EC."
            )

    elif growth_stage == "Flowering / Panicle Formation":

        if leaf_area_percentage >= 55:
            growth_status = "Good Flowering-Stage Appearance"

            st.success(
                "🌱 The crop shows good visible green coverage "
                "during flowering/panicle formation."
            )

        else:
            growth_status = "Reduced Green Coverage"

            st.warning(
                "⚠️ Reduced green coverage detected during flowering. "
                "Check soil EC and other crop conditions."
            )

    else:

        if leaf_area_percentage >= 60:
            growth_status = "Good Vegetative Growth"

            st.success(
                "🌱 The plant shows good visible green coverage."
            )

        elif leaf_area_percentage >= 45:
            growth_status = "Moderate Vegetative Growth"

            st.warning(
                "🟡 The plant shows moderate visible green coverage."
            )

        else:
            growth_status = "Low Visible Green Coverage"

            st.error(
                "🔴 The plant shows low visible green coverage."
            )

  

    st.write(
        f"**Visual Growth Status:** {growth_status}"
    )

    st.caption(
        "This is an image-based visual growth assessment. "
        "Actual plant height, biomass, and growth rate require "
        "additional measurements."
    )
    # -----------------------------------------------
    # CROP HEALTH REPORT
    # -----------------------------------------------

    st.header("📋 Crop Health Report")

    if soil_ec <= 2.0:
        stress_level = "Low Salinity Risk"
    elif soil_ec <= 4.0:
        stress_level = "Moderate Salinity Risk"
    else:
        stress_level = "High Salinity Risk"

    report = {
        "Crop": crop,
        "Growth Stage": growth_stage,
        "Crop Health": health_status,
        "Soil EC": f"{soil_ec:.2f} dS/m",
        "Green Area": f"{green_percentage:.2f}%",
        "Leaf Area": f"{leaf_area_percentage:.2f}%",
        "Average Leaf Hue": f"{average_hue:.2f}",
        "Visible Plant Stress Score": f"{stress_score}/100",
        "Risk Level": stress_level,
        "Health Status": health_status,
        "Growth Status": growth_status
    }

    report_df = pd.DataFrame(
        list(report.items()),
        columns=["Parameter", "Result"]
    )

    st.table(report_df)

    # --------------------------------------------------
    # MANAGEMENT RECOMMENDATION
    # --------------------------------------------------

    st.header("💡 Management Recommendation")
    if soil_ec <= 2.0:
        st.success(
            f"🟢 Soil EC is {soil_ec:.2f} dS/m. "
            "The entered EC indicates relatively low salinity."
        )
    elif soil_ec <= 4.0:
        st.warning(
            f"🟡 Soil EC is {soil_ec:.2f} dS/m. "
            "The entered EC indicates increased salinity risk. "
            "Monitor the crop and soil conditions."
        )
    else:
        st.error(
            f"🔴 Soil EC is {soil_ec:.2f} dS/m. "
            "The entered EC indicates high salinity risk. "
            "Verify the measurement and consider appropriate soil "
            "and irrigation management."
        )
    # --------------------------------------------------
    # CROP MANAGEMENT ADVISORY
    # --------------------------------------------------

    if growth_stage == "Maturity / Harvest":
        if soil_ec <= 2.0:
            recommendation = (
                "The crop appears to be at the maturity/harvest stage. "
                "Yellowing can be a normal part of rice maturity. "
                "Continue normal harvest planning and monitor soil conditions."
            )
        elif soil_ec <= 4.0:
            recommendation = (
                "The crop is at maturity/harvest stage. "
                "Some yellowing may be natural, but the entered soil EC "
                "indicates increased salinity concern. "
                "Verify soil EC and maintain suitable irrigation and drainage."
            )
        else:
            recommendation = (
                "The crop is at maturity/harvest stage and the entered soil EC "
                "indicates high salinity concern. "
                "Verify the EC measurement and check irrigation and drainage "
                "conditions before making management decisions."
            )

    elif stress_score <= 30:
        recommendation = (
            "The crop shows low visible stress for the selected growth stage. "
            "Continue normal crop monitoring, irrigation and soil management."
        )

    elif stress_score <= 60:
        recommendation = (
            "The crop shows some possible visible stress. "
            "Monitor the crop more frequently and verify soil EC, irrigation "
            "and drainage conditions. Check for other causes such as nutrient "
            "deficiency, drought or disease."
        )

    else:
        recommendation = (
            "The crop shows significant visible stress. "
            "Verify soil EC using a proper electrical-conductivity test and "
            "check irrigation, drainage, drought, nutrient deficiency, disease "
            "and other possible causes before taking corrective action."
        )

    st.write(recommendation)

    # --------------------------------------------------
    # DOWNLOAD REPORT
    # --------------------------------------------------

    report_text = f"""
    SMART SOIL SALINITY MONITORING REPORT
    =====================================

    Crop: {crop}

    Green Area: {green_percentage:.2f}%
    Leaf Area: {leaf_area_percentage:.2f}%
    Average Leaf Hue: {average_hue:.2f}

    Stress Score: {stress_score}/100
    Risk Level: {stress_level}
    Health Status: {status}
    Growth Status: {growth_status}

    Management Recommendation:
    {recommendation}

    NOTE:
    This is an image-based visual assessment.
    Actual soil salinity should be verified using
    a soil electrical-conductivity (EC) test.
    """

    st.download_button(
        label="📥 Download Crop Health Report",
        data=report_text,
        file_name="crop_health_report.txt",
        mime="text/plain"
    )
    # --------------------------------------------------
    # IMPORTANT NOTE
    # --------------------------------------------------

    st.warning(
        "⚠️ This is an image-based visual stress estimate. "
        "A plant photograph alone cannot directly measure "
        "soil salinity. For actual salinity measurement, "
        "use a soil electrical-conductivity (EC) test."
    )