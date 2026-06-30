import streamlit as st
import requests
import random

# إعدادات الصفحة والتصميم الدافئ (Vintage)
st.set_page_config(page_title="نافذة الفن اليومي", page_icon="🎨", layout="centered")

# تخصيص الألوان والخلفية الكلاسيكية باستخدام CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #F4F1EA;
    }
    h1, h2, h3, p, span, li {
        color: #2C3E50 !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    .stButton>button {
        background-color: #8E7F6E !important;
        color: white !important;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 2rem;
    }
    .history-box {
        background-color: #EFECE4;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# تهيئة سجل اللوحات (History) في ذاكرة الموقع إذا لم يكن موجوداً
if "art_history" not in st.session_state:
    st.session_state.art_history = []

st.title("🎨 اكتشف لوحة اليوم")
st.write("أرسل نقطة لتستلم جرعتك الفنية اليومية من مختلف متاحف العالم.")

# زر إرسال النقطة
if st.button("إرسال نقطة ."):
    with st.spinner("جاري البحث في أروقة المتاحف عن لوحة مميزة... 🔍"):
        try:
            # جلب البيانات من متحف المتروبوليتان
            search_url = "https://collectionapi.metmuseum.org/public/collection/v1/search?hasImages=true&q=painting"
            response = requests.get(search_url)
            data = response.json()
            
            if data and "objectIDs" in data:
                valid_art = False
                attempts = 0
                
                while not valid_art and attempts < 15:
                    object_id = random.choice(data["objectIDs"])
                    object_url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"
                    art_response = requests.get(object_url)
                    art_data = art_response.json()

                    if art_data.get("primaryImageSmall") and art_data.get("artistDisplayName"):
                        valid_art = True
                    attempts += 1

                if valid_art:
                    # استخراج البيانات
                    title = art_data.get("title", "غير معروف")
                    artist = art_data.get("artistDisplayName", "غير معروف")
                    bio = art_data.get("artistDisplayBio", "لا توجد تفاصيل متاحة")
                    medium = art_data.get("medium", "غير معروف")
                    year = art_data.get("objectDate", "غير معروف")
                    culture = art_data.get("culture", "")
                    department = art_data.get("department", "الفنون الجميلة")
                    school = culture if culture else department
                    image_url = art_data.get("primaryImageSmall")

                    # حفظ اللوحة الحالية في بداية قائمة السجل (History)
                    st.session_state.art_history.insert(0, {
                        "title": title,
                        "artist": artist,
                        "year": year,
                        "image": image_url
                    })

                    # عرض الصورة الحالية بشكل متناسق
                    st.image(image_url, caption=f"🖼️ {title}", use_container_width=True)
                    
                    # عرض المعلومات منسقة
                    st.markdown(f"### 👨‍🎨 الفنان: {artist}")
                    st.markdown(f"**📜 نبذة:** {bio}")
                    st.hr()
                    st.markdown(f"**🏛️ المدرسة الفنية / القسم:** {school}")
                    st.markdown(f"**📅 السنة:** {year}")
                    st.markdown(f"**🎨 الوسيط المستخدم:** {medium}")
                else:
                    st.error("لم نتمكن من جلب لوحة هذه المرة، يرجى المحاولة مجدداً.")
            else:
                st.error("فشل في الاتصال بقاعدة بيانات المتحف.")
        except Exception as e:
            st.error(f"حدث خطأ غير متوقع: {str(e)}")

# --- قسم السجل (History Section) ---
st.markdown("---")
st.subheader("📜 سجل اللوحات المكتشفة في هذه الجلسة")

if st.session_state.art_history:
    for idx, item in enumerate(st.session_state.art_history):
        # نضع كل لوحة سابقة في قائمة منسدلة أنيقة (Expander) لكي لا تأخذ مساحة ضخمة
        with st.expander(f"لوحة رقم {len(st.session_state.art_history) - idx}: {item['title']} - {item['artist']}"):
            st.image(item['image'], use_container_width=True)
            st.write(f"**الفنان:** {item['artist']} | **السنة:** {item['year']}")
else:
    st.info("لم تكتشفي أي لوحات بعد. اضغطي على زر 'إرسال نقطة' لتبدأ لوحاتكِ بالظهور هنا!")
