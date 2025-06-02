# 🎬 Watchlist Streamlit App

**Watchlist** is a collaborative movie recommendation tool that aggregates watchlists from Letterboxd users to suggest films that everyone in a group hasn't seen yet. This web interface idea originates from my original Watchlise iOS app. This version, built with Streamlit,offers a simple and interactive web interface for planning movie nights.

## 🔍 Features

- **Import Watchlists**: Fetch watchlists from multiple Letterboxd users using Beautiful Soup.
- **Profile System**: Create account or log into exisiting account. Add your friends to your account for easy access.
- **Group Recommendations**: Identify movies all or some users want to watch
- **User-Friendly Interface**: Streamlit-powered UI for seamless interaction.
- **Data Storage**: Utilizes PostgreSQL for efficient data management.

## 🧰 Tech Stack

| Layer        | Tools & Libraries                                             |
| ------------ | ------------------------------------------------------------- |
| **Frontend** | [Streamlit](https://streamlit.io) – interactive UI framework  |
| **Backend**  | PostgreSQL, SQLAlchemy – local data storage and processing    |
| **Scraping** | `requests`, `BeautifulSoup` – fetch and parse Letterboxd data |
| **Data**     | `pandas` – data wrangling and filtering logic                 |
| **Styling**  | Streamlit theme config + custom layout tweaks                 |

## 📁 Folder Structure

watchlist_streamlit/

├── .streamlit/ # Streamlit config

│ └── config.toml

├── sql/ # PostgreSQL database (e.g., movie metadata, user lists)

├── src/ # Source code for app logic and UI

│ ├── pages/ # login/create account, movie recommendation pages

│ └── utils/ # BS scrapers

├── requirements.txt # Python package dependencies

└── README.md # Project description

## 🧾 Navigation

### Log in or create new account

<img width="1774" alt="Image" src="https://github.com/user-attachments/assets/faa4ca90-8d4c-482a-b93c-d0ac934639a1" />
<img width="1781" alt="Image" src="https://github.com/user-attachments/assets/329625b5-f4e9-43f1-afc5-6045a85e5aa2" />

### Add your Letterboxd friends (runs BS scrapers to pull history)

<img width="1531" alt="Image" src="https://github.com/user-attachments/assets/f02cff27-d1ac-49e1-bf28-8dcc64bbaf0f" />

### And generate joint watchlist

<img width="1526" alt="Image" src="https://github.com/user-attachments/assets/1e41c259-e28e-4009-8a8d-6863818d731b" />
