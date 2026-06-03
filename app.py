import streamlit as st
import psycopg2
import pandas as pd
import os

st.set_page_config(page_title="DIS FIFA 22 App", page_icon="⚽", layout="centered")

st.title("⚽ FIFA 22 Scout")
st.write("Klik på knappen for at trække en tilfældig spiller direkte fra PostgreSQL-databasen!")

DB_HOST = os.environ.get("DB_HOST", "db")
DB_USER = os.environ.get("DB_USER", "admin")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password123")
DB_NAME = os.environ.get("DB_NAME", "dis_db")

def get_random_player():
    try:
        conn = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_NAME)
        
        # 1. Vi har nu tilføjet billed-URL'erne til vores SELECT statement
        query = """
        SELECT short_name, age, overall, club_name, nationality_name, player_positions,
               player_face_url, club_logo_url, nation_flag_url 
        FROM players 
        ORDER BY RANDOM() 
        LIMIT 1;
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Database fejl: {e}")
        return None

if st.button("🎲 Træk en tilfældig spiller", type="primary", use_container_width=True):
    df_player = get_random_player()
    
    if df_player is not None and not df_player.empty:
        navn = df_player['short_name'].iloc[0]
        st.success(f"Fandt spiller: **{navn}**")
        
        # --- NYT BILLED-LAYOUT ---
        # Vi deler skærmen op i 3 lige store kolonner
        col1, col2, col3 = st.columns(3)
        
# --- NYT BILLED-LAYOUT MED HTML BYPASS ---
        col1, col2, col3 = st.columns(3)
        
        with col1:
            ansigt_url = df_player['player_face_url'].iloc[0]
            if pd.notna(ansigt_url) and ansigt_url != "":
                # Vi bruger HTML for at skjule 'referrer' og undgå blokeringen
                st.markdown(f'<img src="{ansigt_url}" width="120" referrerpolicy="no-referrer"><br><small style="color: gray;">Spiller</small>', unsafe_allow_html=True)
                
        with col2:
            klub_url = df_player['club_logo_url'].iloc[0]
            if pd.notna(klub_url) and klub_url != "":
                st.markdown(f'<img src="{klub_url}" width="100" referrerpolicy="no-referrer"><br><small style="color: gray;">{df_player["club_name"].iloc[0]}</small>', unsafe_allow_html=True)
                
        with col3:
            nation_url = df_player['nation_flag_url'].iloc[0]
            if pd.notna(nation_url) and nation_url != "":
                st.markdown(f'<img src="{nation_url}" width="100" referrerpolicy="no-referrer"><br><small style="color: gray;">{df_player["nationality_name"].iloc[0]}</small>', unsafe_allow_html=True)        
        st.divider() # Laver en pæn streg
        
        # Viser overall rating
        st.metric(label="Overall Rating", value=df_player['overall'].iloc[0])
        
        # Fjerner billed-links fra den tabel vi viser, for ikke at forvirre brugeren med lange grimme tekst-strenge
        visnings_df = df_player.drop(columns=['player_face_url', 'club_logo_url', 'nation_flag_url'])
        st.dataframe(visnings_df, hide_index=True, width="stretch")