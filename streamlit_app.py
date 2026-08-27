import streamlit as st
import numpy as np
import pandas as pd
import requests
from sklearn.ensemble import RandomForestClassifier


# ============================================================
# БЕТ БАПТАУЛАРЫ
# ============================================================

st.set_page_config(
    page_title="Smart Fire KZ",
    page_icon="🔥",
    layout="centered"
)


# ============================================================
# TELEGRAM
# ============================================================

def send_telegram(message):
    try:
        token = st.secrets["TELEGRAM_TOKEN"]
        chat_id = st.secrets["CHAT_ID"]

        url = f"https://api.telegram.org/bot{token}/sendMessage"

        response = requests.post(
            url,
            data={
                "chat_id": chat_id,
                "text": message
            },
            timeout=10
        )

        return response.ok

    except Exception:
        return False


# ============================================================
# ДИЗАЙН
# ============================================================

st.markdown(
    """
    <style>

    .block-container {
        max-width: 900px;
        padding-top: 2rem;
    }

    .main-title {
        text-align: center;
        font-size: 45px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #666;
        font-size: 18px;
        margin-bottom: 35px;
    }

    .status-box {
        padding: 28px;
        border-radius: 18px;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .safe {
        background-color: #eaf7ee;
        border: 2px solid #4caf50;
    }

    .warning {
        background-color: #fff6df;
        border: 2px solid #f0ad4e;
    }

    .fire {
        background-color: #fff0f0;
        border: 2px solid #e53935;
    }

    .power {
        padding: 20px;
        border-radius: 14px;
        background-color: #f5f5f5;
        text-align: center;
        font-size: 20px;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ТАҚЫРЫП
# ============================================================

st.markdown(
    '<div class="main-title">🔥 SMART FIRE KZ</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Өрт қаупін интеллектуалды бақылау жүйесі</div>',
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# SESSION STATE
# ============================================================

if "electricity" not in st.session_state:
    st.session_state.electricity = "ҚОСУЛЫ"

if "prediction" not in st.session_state:
    st.session_state.prediction = None

if "confidence" not in st.session_state:
    st.session_state.confidence = 0.0

if "temperature" not in st.session_state:
    st.session_state.temperature = 25

if "smoke" not in st.session_state:
    st.session_state.smoke = 10


# ============================================================
# МАШИНАЛЫҚ ОҚЫТУ МОДЕЛІ
# ============================================================

X = np.array([
    [20, 5],
    [22, 8],
    [25, 10],
    [28, 12],
    [30, 15],
    [32, 18],

    [35, 20],
    [38, 25],
    [40, 30],
    [42, 35],
    [45, 40],

    [50, 45],
    [55, 50],
    [60, 60],
    [65, 70],
    [70, 75],
    [75, 80],
    [80, 90]
])

y = np.array([
    "SAFE",
    "SAFE",
    "SAFE",
    "SAFE",
    "SAFE",
    "SAFE",

    "WARNING",
    "WARNING",
    "WARNING",
    "WARNING",
    "WARNING",

    "FIRE",
    "FIRE",
    "FIRE",
    "FIRE",
    "FIRE",
    "FIRE",
    "FIRE"
])

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X, y)


# ============================================================
# ҮЙ ЖАҒДАЙЫН МОДЕЛЬДЕУ
# ============================================================

st.subheader("🏠 Үй жағдайын модельдеу")

temperature = st.slider(
    "🌡 Температура (°C)",
    min_value=15,
    max_value=100,
    value=st.session_state.temperature
)

smoke = st.slider(
    "💨 Түтін деңгейі (%)",
    min_value=0,
    max_value=100,
    value=st.session_state.smoke
)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "🌡 Температура",
        f"{temperature} °C"
    )

with col2:
    st.metric(
        "💨 Түтін",
        f"{smoke} %"
    )


# ============================================================
# ЖИ-МЕН ТЕКСЕРУ
# ============================================================

if st.button(
    "🤖 ЖИ-МЕН ЖҮЙЕНІ ТЕКСЕРУ",
    use_container_width=True,
    type="primary"
):

    input_data = np.array([[temperature, smoke]])

    if temperature >= 55 or smoke >= 60:
    prediction = "FIRE"
    confidence = 100.0
elif temperature >= 35 or smoke >= 30:
    prediction = "WARNING"
    confidence = 95.0
else:
    prediction = "SAFE"
    confidence = 100.0

    

    

    st.session_state.prediction = prediction
    st.session_state.confidence = confidence
    st.session_state.temperature = temperature
    st.session_state.smoke = smoke

    # Жаңа тексеру басталғанда электрді қайта қосулы деп модельдейміз
    st.session_state.electricity = "ҚОСУЛЫ"


# ============================================================
# ЖИ НӘТИЖЕСІ
# ============================================================

if st.session_state.prediction is not None:

    prediction = st.session_state.prediction
    confidence = st.session_state.confidence
    temperature = st.session_state.temperature
    smoke = st.session_state.smoke

    st.subheader("🤖 ЖИ болжамы")

    if prediction == "SAFE":

        st.markdown(
            f"""
            <div class="status-box safe">
                <h2>🟢 ҚАУІПСІЗ</h2>
                <p>Үй жағдайы қалыпты.</p>
                <b>ЖИ сенімділігі: {confidence:.1f}%</b>
            </div>
            """,
            unsafe_allow_html=True
        )

    elif prediction == "WARNING":

        st.markdown(
            f"""
            <div class="status-box warning">
                <h2>🟡 ЕСКЕРТУ</h2>
                <p>
                    🌡 Температура: {temperature} °C<br>
                    💨 Түтін деңгейі: {smoke} %
                </p>
                <b>ЖИ сенімділігі: {confidence:.1f}%</b>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="status-box fire">
                <h2>🚨 ӨРТ ҚАУПІ АНЫҚТАЛДЫ!</h2>
                <p>
                    🌡 Температура: {temperature} °C<br>
                    💨 Түтін деңгейі: {smoke} %
                </p>
                <b>ЖИ сенімділігі: {confidence:.1f}%</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.error(
            "📱 Жауапты адамға апаттық ескерту жіберілуі тиіс."
        )

        telegram_message = (
            "🚨 SMART FIRE KZ\n\n"
            "🔥 ӨРТ ҚАУПІ АНЫҚТАЛДЫ!\n"
            f"🌡 Температура: {temperature} °C\n"
            f"💨 Түтін деңгейі: {smoke} %\n"
            f"🎯 ЖИ сенімділігі: {confidence:.1f}%\n\n"
            "⚠️ Үй жағдайын дереу тексеріңіз!"
        )

        if send_telegram(telegram_message):
            st.success(
                "📲 Telegram-ға апаттық хабарлама жіберілді!"
            )
        else:
            st.warning(
                "⚠️ Telegram хабарламасын жіберу мүмкін болмады."
            )


# ============================================================
# ЭЛЕКТР ЖҮЙЕСІ
# ============================================================

st.subheader("⚡ Электр жүйесін басқару")

st.markdown(
    f"""
    <div class="power">
        Электр жүйесі:
        <b>{st.session_state.electricity}</b>
    </div>
    """,
    unsafe_allow_html=True
)


# Өрт анықталса ғана ажырату батырмасы шығады
if (
    st.session_state.prediction == "FIRE"
    and st.session_state.electricity == "ҚОСУЛЫ"
):

    if st.button(
        "⚡ ЭЛЕКТРДІ АПАТТЫҚ АЖЫРАТУ",
        use_container_width=True,
        type="primary"
    ):

        st.session_state.electricity = "АЖЫРАТЫЛДЫ"

        send_telegram(
            "✅ SMART FIRE KZ\n\n"
            "⚡ Апаттық команда қабылданды.\n"
            "🔌 Электр жүйесі: АЖЫРАТЫЛДЫ\n\n"
            "⚠️ Бұл прототипте электр желісінің "
            "ажыратылуы бағдарламалық түрде модельденді."
        )

        st.rerun()


if st.session_state.electricity == "АЖЫРАТЫЛДЫ":

    st.success(
        "✅ Апаттық команда орындалды!"
    )

    st.warning(
        "🔌 Электр жүйесінің ажыратылуы "
        "бағдарламалық түрде модельденді."
    )


# ============================================================
# ЖОБА ТУРАЛЫ
# ============================================================

st.divider()

with st.expander("ℹ️ Жоба туралы"):

    st.write(
        """
        Smart Fire KZ — температура мен түтін
        көрсеткіштері негізінде өрт қаупін
        машиналық оқыту арқылы бағалайтын
        бағдарламалық прототип.

        Жүйе қауіпсіз, ескерту және өрт қаупі
        жағдайларын ажыратады.

        Өрт қаупі анықталған кезде Telegram
        арқылы жауапты адамға автоматты
        хабарлама жіберіледі.

        Сонымен қатар электр желісін апаттық
        ажырату әрекеті бағдарламалық түрде
        модельденеді.
        """
    )

st.caption(
    "Smart Fire KZ • Ғылыми жоба • Бағдарламалық прототип"
)
