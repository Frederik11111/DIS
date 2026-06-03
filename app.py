import streamlit as st
import psycopg2
import pandas as pd
import os

# Sætter lidt bredde på siden og en emoji i fanen
st.set_page_config(page_title="DIS FIFA 22 App", page_icon="⚽", layout="centered")

st.title("⚽ FIFA 22 Scout")
st.write("Klik på knappen for at trække en tilfældig spiller direkte fra PostgreSQL-databasen!")

# Database-informationer fra jeres docker-compose.yml
DB_HOST = os.environ.get("DB_HOST", "db")
DB_USER = os.environ.get("DB_USER", "admin")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password123")
DB_NAME = os.environ.get("DB_NAME", "dis_db")

# Funktion der kører vores SQL
def get_random_player():
    try:
        # 1. Opretter forbindelsen
        conn = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_NAME)
        
        # 2. Vores SQL-query. Vi vælger kun et par af de 110 kolonner, så det ser pænt ud på skærmen!
        query = """
        SELECT short_name, age, overall, club_name, nationality_name, player_positions 
        FROM players 
        ORDER BY RANDOM() 
        LIMIT 1;
        """
        
        # 3. Pandas lader os køre SQL'en og spytter resultatet ud i en Dataframe (perfekt til Streamlit)
        df = pd.read_sql_query(query, conn)
        
        # 4. Lukker forbindelsen pænt igen
        conn.close()
        return df
    except Exception as e:
        st.error(f"Database fejl: {e}")
        return None

# Knappen der sætter det hele i gang
if st.button("🎲 Træk en tilfældig spiller", type="primary", use_container_width=True):
    
    # Kører funktionen
    df_player = get_random_player()
    
    if df_player is not None and not df_player.empty:
        # Vi trækker spillerens navn ud af tabellen til en grøn succes-besked
        spiller_navn = df_player['short_name'].iloc[0]
        st.success(f"Fandt spiller: **{spiller_navn}**")
        
        # Viser spillerens 'overall' rating med stort i Streamlit (bare for blæreværdi)
        st.metric(label="Overall Rating", value=df_player['overall'].iloc[0])
        
        # Viser resten af dataen som en pæn tabel
        st.dataframe(df_player, hide_index=True, use_container_width=True)
        
        # Ekstra: Hvis I vil se ALLE 110 kolonner for spilleren, kan I fjerne hashtagget nedenunder
        # st.write(df_player)