import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import requests
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

# -------------------------------------------------
# SMART FIRE KZ
# -------------------------------------------------

st.set_page_config(
    page_title="Smart Fire KZ",
    page_icon="🔥",
    layout="centered"
)

# -------------------------------------------------
# ДИЗАЙН
# -------------------------------------------------

st.markdown("""
<style>
.block-container {
    max-width: 900px;
    padding-top: 2rem;
}

.main-title {
    text-align: center;
    font-size: 45px;
    font-weight: 800;
}

.subtitle {
    text-align: center;
    color: #666;
    font-size: 18px;
    margin-bottom: 25px;
}

.status-box {
    padding: 22px;
    border-radius: 16px;
    text-align: center;
    margin: 15px 0;
}

.safe {
    background: #e8f5e9;
    border: 2px solid #4caf50;
}

.warning {
    background: #fff8e1;
    border: 2px solid #ffc107;
}

.fire {
    background: #ffebee;
    border: 2px solid #f44336;
}

.power {
    padding: 18px;
    border-radius: 14px;
    background: #f4f6f8;
    text-align: center;
    font-size: 20px;
}
</style>
""", unsafe_allow_html=True)


# -------------------------------------------------
# ML МОДЕЛІ
# -------------------------------------------------

@st.cache_resource
def train_model():

    np.random.seed(42)

    n = 1000

    temperature = np.random.randint(15, 101, n)
    smoke = np.random.randint(0, 101, n)

    labels = []

    for t, s in zip(temperature, smoke):

        if t >= 60 and s >= 60:
            labels.append("FIRE")

        elif t >= 45 or s >= 40:
            labels.append("WARNING")

        else:
            labels.append("SAFE")

    X = pd.DataFrame({
        "temperature": temperature,
        "smoke": smoke
    })

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )

    model.fit(X, labels)

    return model


model = train_model()


# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------

if "electricity" not in st.session_state:
    st.session_state.electricity = "ҚОСУЛЫ ⚡"


# -------------------------------------------------
# ТАҚЫРЫП
# -------------------------------------------------

st.markdown(
    '<div class="main-title">🔥 SMART FIRE KZ</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Өрт қаупін интеллектуалды бақылау жүйесі'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# -------------------------------------------------
# КӨРСЕТКІШТЕР
# -------------------------------------------------

st.subheader("🏠 Үй жағдайын модельдеу")

temperature = st.slider(
    "🌡 Температура (°C)",
    min_value=15,
    max_value=100,
    value=25
)

smoke = st.slider(
    "💨 Түтін деңгейі (%)",
    min_value=0,
    max_value=100,
    value=10
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


# -------------------------------------------------
# ЖИ ТЕКСЕРУ
# -------------------------------------------------

if st.button(
    "🤖 ЖИ-МЕН ЖҮЙЕНІ ТЕКСЕРУ",
    use_container_width=True,
    type="primary"
):

    test_data = pd.DataFrame(
        [[temperature, smoke]],
        columns=["temperature", "smoke"]
    )

    prediction = model.predict(test_data)[0]

    probabilities = model.predict_proba(test_data)[0]

    confidence = max(probabilities) * 100

    st.session_state.prediction = prediction
    st.session_state.confidence = confidence


# -------------------------------------------------
# НӘТИЖЕ
# -------------------------------------------------

if "prediction" in st.session_state:

    prediction = st.session_state.prediction
    confidence = st.session_state.confidence

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
                <p>Көрсеткіштердің бірі қалыпты деңгейден жоғары.</p>
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
            st.success("📲 Telegram-ға апаттық хабарлама жіберілді!")
        else:
            st.warning("⚠️ Telegram хабарламасын жіберу мүмкін болмады.")


# -------------------------------------------------
# ЭЛЕКТР ЖҮЙЕСІ
# -------------------------------------------------

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


if (
    "prediction" in st.session_state
    and st.session_state.prediction == "FIRE"
):

    if st.button(
        "⚡ ЭЛЕКТРДІ АПАТТЫҚ АЖЫРАТУ",
        use_container_width=True,
        type="primary"
    ):

        st.session_state.electricity = "АЖЫРАТЫЛДЫ 🔌"

        st.success(
            "✅ Апаттық команда орындалды!"
        )

        st.warning(
            "🔌 Электр жүйесінің ажыратылуы "
            "бағдарламалық түрде модельденді."
        )

        st.rerun()


# -------------------------------------------------
# АҚПАРАТ
# -------------------------------------------------

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

        Өрт қаупі анықталған кезде электр жүйесін
        апаттық ажырату әрекеті бағдарламалық
        түрде модельденеді.
        """
    )

st.caption(
    "Smart Fire KZ • Ғылыми жоба • Бағдарламалық прототип"
)
