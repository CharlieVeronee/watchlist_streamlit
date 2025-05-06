import streamlit as st
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from utils.scrapers.check_username_scraper import is_valid_account
from utils.scrapers.watchlist_scraper import watchlist_call

st.title("Group Watchlist")

if "app_username" not in st.session_state or not st.session_state.app_username:
    st.warning("Please log in first from the home page.")
    st.stop()

app_username = st.session_state.app_username
st.write(f"User: {st.session_state.app_username}")

st.header("Who's Watching")

st.write("Your Friends")

conn = st.connection("postgresql", type="sql")

people = conn.session.execute(
        text("SELECT lb_username, added_at, added_by FROM people WHERE added_by = :added_by;"),
        params={"added_by": app_username},
    )

people = people.fetchall()

if not people:
    st.info("You haven't added any friends. Go add some below")
else:
    for row in people:
        col1, col2, col3 = st.columns([4, 1.5, 1.5])

        with col1:
            st.write(f"{row.lb_username}")

        with col2:
            if st.button("🔄 Update", key=f"update_{row.lb_username}"):
                watchlist_call(lb_username=row.lb_username, added_by=app_username)
                st.success("Updated!")
                st.rerun()
        
        with col3:
            if st.button("❌ Remove", key=f"remove_{row.lb_username}"):
                with conn.session as session:
                    session.execute(
                        text(
                            "DELETE FROM People WHERE lb_username = :lb AND added_by = :ab"
                        ),
                        params={"lb": row.lb_username, "ab": app_username},
                    )
                    session.commit()
                st.success(f"Removed!")
                st.rerun()


with st.form("add_friend_form"):
        new_friend = st.text_input("Add Letterboxd Account")
        submit = st.form_submit_button("Add Friend")

        if submit and new_friend:
            exists, has_watchlist = is_valid_account(new_friend.strip())
            if not exists:
                st.error("That Letterboxd profile doesn't exist.")
            elif not has_watchlist:
                st.error("Profile exists but has no watchlist.")
            else:
                try:
                    with conn.session as session:
                        session.execute(
                            text(
                                "INSERT INTO People (lb_username, added_by) "
                                "VALUES (:lb_username, :added_by)"
                            ),
                            params = {"lb_username": new_friend.strip(), "added_by": app_username},
                        )
                        session.commit()
                        watchlist_call(lb_username=new_friend, added_by=app_username)

                    st.success("Added Friend.")
                    st.rerun()
                except IntegrityError as e:
                    if isinstance(e.orig, UniqueViolation):
                        st.error("Friend already added")
                    else:
                        st.error(f"Database error: {e}")            

usernames = [row.lb_username for row in people]


selected_lb_usernames = st.multiselect(
    "Choose friends to include:",
    options=usernames
)

if len(selected_lb_usernames) >=2 and st.button("🎬 Show Shared Watchlist"):
    placeholders = ", ".join([f":user{i}" for i in range(len(selected_lb_usernames))])
    query = text(f"""
        SELECT m.slug, COUNT(*) as num_people
        FROM Watchlist w
        JOIN Movies m ON m.slug = w.slug
        WHERE w.added_by = :added_by AND w.lb_username IN ({placeholders})
        GROUP BY m.title, m.slug
        HAVING COUNT(*) > 1
        ORDER BY num_people DESC
    """)
    params = {"added_by": app_username}
    
    for i, username in enumerate(selected_lb_usernames):
        params[f"user{i}"] = username

    result = conn.session.execute(query, params=params).fetchall()

    if not result:
        st.info("No overlapping movies found.")
    else:
        st.subheader(f"🍿 Shared Movies Among Selected Friends ({len(result)} total)")
        for row in result:
            if row.num_people == len(selected_lb_usernames):
                st.write(f"🎞(https://letterboxd.com/film/{row.slug}/) — in all watchlists")
            else:
                st.write(f"🎞(https://letterboxd.com/film/{row.slug}/) — in {row.num_people} watchlists")

else:
    st.caption("Select at least two people to see shared results.")

