# E/R Diagram

The application uses a compact database model based on the FIFA 22 player dataset.

`players` is the base entity loaded from `players_22.csv`. `clean_players` is a SQL view derived from `players`; it keeps only the columns needed by the Streamlit UI.

```mermaid
erDiagram
    PLAYERS {
        int sofifa_id PK
        text player_url
        varchar short_name
        varchar long_name
        varchar player_positions
        int overall
        int potential
        text value_eur
        text wage_eur
        int age
        text dob
        text height_cm
        text weight_kg
        varchar club_name
        varchar league_name
        varchar club_position
        varchar nationality_name
        varchar nation_position
        varchar preferred_foot
        varchar work_rate
        varchar body_type
        text player_tags
        text player_traits
        text player_face_url
        text club_logo_url
        text nation_flag_url
    }

    CLEAN_PLAYERS_VIEW {
        int player_id
        varchar name
        int rating
        text value_eur
        varchar club
        varchar nationality
        text face_image
        text club_logo
        text flag_image
    }

    PLAYERS ||--|| CLEAN_PLAYERS_VIEW : derives
```

## Model Notes

- `players.sofifa_id` is the primary key.
- `clean_players` is not a stored table. It is a SQL view created with `CREATE OR REPLACE VIEW`.
- The app reads from `clean_players` for both player pack opening and regex search.
- The full table definition is in `scripts/init.sql`.
