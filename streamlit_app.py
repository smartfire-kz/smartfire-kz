import streamlit as st
import requests

st.set_page_config(
    page_title="Smart Fire KZ",
    page_icon="🔥",
    layout="centered"
)


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


st.markdown(
    """
    <style>
    .block-container {
        max-width: 900px;
        padding-top: 2rem;
    }

    .title {
        text-align: center;
        font-size: 44px;
        font-weight: 800;
    }

    .subtitle {
        text-align: center;
        color: #666;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .box {
        padding: 28px;
        border-radius: 18px;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .safe {
        background: #eaf7ee;
        border: 2px solid #4caf50;
    }

    .warning {
        background: #fff6df;
        border: 2px solid #f0ad4e;
    }

    .fire {
        background: #fff0f0;
        border: 2px solid #e53935;
    }

    .power {
        padding: 20px;
        background: #f5f5f5;
        border-radius: 15px;
        text-align: center;
        font-size: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    '<div class="title">🔥 SMART FIRE KZ</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Өрт қаупін интеллектуалды бақылау жүйесі</div>',
    unsafe_allow_html=True
)

st.divider()


if "prediction" not in st.session_state:
    st.session_state.prediction = None

if "temperature" not in st.session_state:
    st.session_state.temperature = 25

if "smoke" not in st.session_state:
    st.session_state.smoke = 10

if "confidence" not in st.session_state:
    st.session_state.confidence = 100.0

if "electricity" not in st.session_state:
    st.session_state.electricity = "ҚОСУЛЫ"

if "fire_alert_sent" not in st.session_state:
    st.session_state.fire_alert_sent = False


st.subheader("🏠 Үй жағдайын модельдеу")

temperature = st.slider(
    "🌡 Температура (°C)",
    15,
    100,
    st.session_state.temperature
)

smoke = st.slider(
    "💨 Түтін деңгейі (%)",
    0,
    100,
    st.session_state.smoke
)


col1, col2 = st.columns(2)

with col1:
    st.metric("🌡 Температура", f"{temperature} °C")

with col2:
    st.metric("💨 Түтін", f"{smoke} %")


check = st.button(
    "🤖 ЖИ-МЕН ЖҮЙЕНІ ТЕКСЕРУ",
    use_container_width=True,
    type="primary"
)


if check:
    prediction = (
        "FIRE"
        if temperature >= 55 or smoke >= 60
        else "WARNING"
        if temperature >= 35 or smoke >= 30
        else "SAFE"
    )

    confidence = 95.0 if prediction == "WARNING" else 100.0

    st.session_state.prediction = prediction
    st.session_state.temperature = temperature
    st.session_state.smoke = smoke
    st.session_state.confidence = confidence
    st.session_state.electricity = "ҚОСУЛЫ"
    st.session_state.fire_alert_sent = False


prediction = st.session_state.prediction
temperature = st.session_state.temperature
smoke = st.session_state.smoke
confidence = st.session_state.confidence


if prediction == "SAFE":
    st.subheader("🤖 ЖИ болжамы")

    st.markdown(
        f"""
        <div class="box safe">
            <h2>🟢 ҚАУІПСІЗ</h2>
            <p>Үй жағдайы қалыпты.</p>
            <p>🌡 Температура: {temperature} °C</p>
            <p>💨 Түтін деңгейі: {smoke} %</p>
            <b>Жүйе сенімділігі: {confidence:.1f}%</b>
        </div>
        """,
        unsafe_allow_html=True
    )


if prediction == "WARNING":
    st.subheader("🤖 ЖИ болжамы")

    st.markdown(
        f"""
        <div class="box warning">
            <h2>🟡 ЕСКЕРТУ</h2>
            <p>Көрсеткіштердің бірі қалыпты деңгейден жоғары.</p>
            <p>🌡 Температура: {temperature} °C</p>
            <p>💨 Түтін деңгейі: {smoke} %</p>
            <b>Жүйе сенімділігі: {confidence:.1f}%</b>
        </div>
        """,
        unsafe_allow_html=True
    )


if prediction == "FIRE":
    st.subheader("🤖 ЖИ болжамы")

    st.markdown(
        f"""
        <div class="box fire">
            <h2>🚨 ӨРТ ҚАУПІ АНЫҚТАЛДЫ!</h2>
            <p>🌡 Температура: {temperature} °C</p>
            <p>💨 Түтін деңгейі: {smoke} %</p>
            <b>Жүйе сенімділігі: {confidence:.1f}%</b>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.fire_alert_sent:
        message = (
            "🚨 SMART FIRE KZ\n\n"
            "🔥 ӨРТ ҚАУПІ АНЫҚТАЛДЫ!\n"
            f"🌡 Температура: {temperature} °C\n"
            f"💨 Түтін деңгейі: {smoke} %\n"
            f"🎯 Жүйе сенімділігі: {confidence:.1f}%\n\n"
            "⚠️ Үй жағдайын дереу тексеріңіз!"
        )

        sent = send_telegram(message)

        if sent:
            st.session_state.fire_alert_sent = True
            st.success("📲 Telegram-ға апаттық хабарлама жіберілді!")
        else:
            st.warning("⚠️ Telegram хабарламасы жіберілмеді.")


st.divider()

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


show_power_button = (
    prediction == "FIRE"
    and st.session_state.electricity == "ҚОСУЛЫ"
)


if show_power_button:
    disconnect = st.button(
        "⚡ ЭЛЕКТРДІ АПАТТЫҚ АЖЫРАТУ",
        use_container_width=True,
        type="primary"
    )

    if disconnect:
        st.session_state.electricity = "АЖЫРАТЫЛДЫ"

        send_telegram(
            "✅ SMART FIRE KZ\n\n"
            "⚡ Апаттық команда қабылданды.\n"
            "🔌 Электр жүйесі: АЖЫРАТЫЛДЫ\n\n"
            "⚠️ Электр желісінің ажыратылуы "
            "бағдарламалық түрде модельденді."
        )

        st.rerun()


if st.session_state.electricity == "АЖЫРАТЫЛДЫ":
    st.success("✅ Апаттық команда орындалды!")

    st.warning(
        "🔌 Электр жүйесінің ажыратылуы "
        "бағдарламалық түрде модельденді."
    )


st.divider()

with st.expander("ℹ️ Жоба туралы"):
    st.write(
        """
        Smart Fire KZ — температура мен түтін көрсеткіштері
        бойынша өрт қаупін бағалайтын бағдарламалық прототип.

        Жүйе үш жағдайды көрсетеді:
        қауіпсіз, ескерту және өрт қаупі.

        Өрт қаупі анықталғанда жауапты адамға
        Telegram арқылы автоматты хабарлама жіберіледі.

        Электр жүйесін апаттық ажырату әрекеті
        бұл прототипте бағдарламалық түрде модельденеді.
        """
    )


st.caption(
    "Smart Fire KZ • Ғылыми жоба • Бағдарламалық прототип"
)
