import streamlit as st
import psycopg2
import pandas as pd
import os

# SETUP
st.set_page_config(page_title="FIFA 22 Scout", page_icon="⚽", layout="wide")

DB_HOST = os.environ.get("DB_HOST", "db")
DB_USER = os.environ.get("DB_USER", "admin")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password123")
DB_NAME = os.environ.get("DB_NAME", "dis_db")

# HELPER FUNCTIONS 
def format_price(val):
    try:
        num = float(val)
        if num >= 1_000_000:
            return f"€{num / 1_000_000:.1f} M"
        elif num >= 1_000:
            return f"€{num / 1_000:.0f}K"
        else:
            return f"€{num:.0f}"
    except (ValueError, TypeError):
        return "N/A"

def open_pack(pack_type):
    try:
        conn = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_NAME)
        
        if pack_type == "Bronze":
            query = "SELECT * FROM clean_players WHERE rating < 65 ORDER BY RANDOM() LIMIT 8;"
        elif pack_type == "Silver":
            query = "SELECT * FROM clean_players WHERE rating >= 65 AND rating < 75 ORDER BY RANDOM() LIMIT 8;"
        else:
            query = "SELECT * FROM clean_players WHERE rating >= 75 ORDER BY RANDOM() LIMIT 8;"
            
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Database error: {e}")
        return None

# MAIN APP
st.title("⚽ FIFA 22 Ultimate Scout")
st.write("Search for specific players or test your luck by opening database packs!")
st.divider()

# REGEX SEARCH
st.subheader("🔍 Advanced Player Search (Regex)")
st.write("Use Regular Expressions to find players. Try `^Messi` (starts with) or `(son|sen)$` (ends with son/sen).")

regex_input = st.text_input("Enter Regex pattern for player name:")

if regex_input:
    try:
        conn = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_NAME)
        query = "SELECT name, rating, value_eur, club, nationality FROM clean_players WHERE name ~* %s LIMIT 10;"
        df_regex = pd.read_sql_query(query, conn, params=(regex_input,))
        conn.close()
        
        if not df_regex.empty:
            st.success(f"Found {len(df_regex)} players matching the pattern '{regex_input}'")
            st.dataframe(df_regex, hide_index=True, width="stretch")
        else:
            st.warning("No players matched your Regex pattern.")
    except Exception as e:
        st.error(f"Invalid Regex pattern. Database error: {e}")

st.divider()

# PACK OPENER
st.subheader("📦 Open Player Packs")
st.write("Draw 8 random players directly from the PostgreSQL database")

btn_col1, btn_col2, btn_col3 = st.columns(3)
selected_pack = None

with btn_col1:
    if st.button("🟫 Open Bronze Pack", use_container_width=True):
        selected_pack = "Bronze"
with btn_col2:
    if st.button("⬜ Open Silver Pack", use_container_width=True):
        selected_pack = "Silver"
with btn_col3:
    if st.button("🟨 Open Gold Pack", type="primary", use_container_width=True):
        selected_pack = "Gold"

if selected_pack:
    st.markdown(f"### 🎉 You opened a {selected_pack} pack!")
    df_pack = open_pack(selected_pack)
    
    if df_pack is not None and not df_pack.empty:
        highest_rating = df_pack['rating'].max()
        if highest_rating >= 85:
            st.balloons()
            legend_name = df_pack[df_pack['rating'] == highest_rating]['name'].iloc[0]
            st.success(f"🌟 **WALKOUT!** You packed a LEGEND! Welcome to the club, **{legend_name}** ({highest_rating} OVR) 🌟")
        
        row1 = st.columns(4)
        row2 = st.columns(4)
        all_columns = row1 + row2 
        
        for index, row in df_pack.iterrows():
            with all_columns[index]: 
                is_legend = "🌟" if row['rating'] >= 85 else ""
                st.markdown(f"#### {is_legend} {row['name']}")
                
                face_img = row['face_image'] if pd.notna(row['face_image']) else ""
                club_img = row['club_logo'] if pd.notna(row['club_logo']) else ""
                flag_img = row['flag_image'] if pd.notna(row['flag_image']) else ""
                
                if face_img:
                    st.markdown(f'<img src="{face_img}" width="120" referrerpolicy="no-referrer" style="border-radius: 10px;">', unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div style="display: flex; gap: 10px; margin-top: 10px; margin-bottom: 10px;">
                        <img src="{club_img}" width="30" referrerpolicy="no-referrer" title="{row['club']}">
                        <img src="{flag_img}" width="30" referrerpolicy="no-referrer" title="{row['nationality']}">
                    </div>
                """, unsafe_allow_html=True)
                
                stat_col1, stat_col2, stat_col3 = st.columns(3)
                stat_col1.metric("Rating", row['rating'],)
                
                value = row['value_eur']
                stat_col2.metric("Value", format_price(value))
                

                
                st.write("---")