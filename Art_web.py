import streamlit as st
import requests
import random
from datetime import datetime
import pytz # مكتبة لضبط فارق التوقيت بدقة

# Page configuration and classic vintage design
st.set_page_config(page_title="Daily Art Explorer", page_icon="🎨", layout="centered")

# CSS for a beautiful vintage/classical look
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
        padding: 0.6rem 2.5rem;
        font-size: 18px !important;
        font-weight: bold;
    }
    .timestamp {
        font-size: 13px;
        color: #7F8C8D;
        font-style: italic;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize art history in session state
if "art_history" not in st.session_state:
    st.session_state.art_history = []

st.title("🎨 Daily Art Explorer")
st.write("Click the button below to discover a masterpiece from world-class museums.")

# The main discovery button in English
if st.button("Discover Artwork"):
    with st.spinner("Searching the gallery archives... 🔍"):
        try:
            # Fetching data from the Metropolitan Museum of Art API
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
                    # Extracting comprehensive details for the description
                    title = art_data.get("title", "Untitled")
                    artist = art_data.get("artistDisplayName", "Unknown Artist")
                    bio = art_data.get("artistDisplayBio", "no details recorded")
                    medium = art_data.get("medium", "unspecified materials")
                    year = art_data.get("objectDate", "an unknown date")
                    dimensions = art_data.get("dimensions", "dimensions not recorded")
                    credit = art_data.get("creditLine", "museum acquisition")
                    dept = art_data.get("department", "Fine Arts")
                    image_url = art_data.get("primaryImageSmall")

                    # Creating a rich, dynamically generated description paragraph in English
                    description = (
                        f"This magnificent artwork, titled **{title}**, was created by the artist **{artist}** "
                        f"({bio}) in **{year}**. Crafted using **{medium}**, this historic piece measures "
                        f"approximately **{dimensions}**. It is currently preserved within the **{dept}** "
                        f"department, brought to the public eye through: *{credit}*."
                    )

                    # جلب تاريخ ووقت الاكتشاف الحالي وتنسيقه بتوقيت بغداد
                    baghdad_tz = pytz.timezone('Asia/Baghdad')
                    discovery_time = datetime.now(baghdad_tz).strftime("%Y-%m-%d %I:%M:%S %p")

                    # Save current painting, its custom description, and discovery timestamp to history
                    st.session_state.art_history.insert(0, {
                        "title": title,
                        "artist": artist,
                        "year": year,
                        "image": image_url,
                        "description": description,
                        "discovered_at": discovery_time
                    })

                    # Display current art piece
                    st.image(image_url, caption=f"🖼️ {title}", use_container_width=True)
                    st.markdown(f"### {title}")
                    st.markdown(f"**By:** {artist} | **Date:** {year}")
                    st.markdown(f"<span class='timestamp'>Discovered on: {discovery_time}</span>", unsafe_allow_html=True)
                    st.markdown("---")
                    st.markdown("#### 📜 Artwork Description")
                    st.write(description)
                else:
                    st.error("Could not fetch a painting this time. Please try again!")
            else:
                st.error("Failed to connect to the museum database.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")

# --- History Section ---
st.markdown("---")
st.subheader("📜 Art Discovery History")

if st.session_state.art_history:
    for idx, item in enumerate(st.session_state.art_history):
        # تظهر تفاصيل كل لوحة في السجل وبجانبها تاريخ ووقت اكتشافها بدقة
        with st.expander(f"Painting #{len(st.session_state.art_history) - idx}: {item['title']} (Discovered: {item['discovered_at']})"):
            st.image(item['image'], use_container_width=True)
            st.write(item['description'])
            st.markdown(f"<span class='timestamp'>Saved to history on: {item['discovered_at']}</span>", unsafe_allow_html=True)
else:
    st.info("Your discovered masterpieces will appear here. Click 'Discover Artwork' to start!")
