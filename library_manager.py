# Full updated Streamlit app with improved readability and visual styling

import streamlit as st
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(page_title="Library Manager", layout="wide")

# --- Custom CSS with clearer colors over background ---
custom_css = """
<style>
.stApp {
    background-image: linear-gradient(rgba(255,255,255,0.8), rgba(255,255,255,0.8)),
                      url('https://images.unsplash.com/photo-1524995997946-a1c2e315a42f');
    background-size: cover;
    background-position: center;
    color: #111 !important;
    font-family: 'Segoe UI', sans-serif;
}

h1, h2, h3, h4 {
    color: #0d306b;
    font-weight: bold;
}

.stButton > button {
    background-color: #1e4fa0;
    color: white;
    border-radius: 10px;
    padding: 0.5em 1em;
    border: none;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #173c80;
}

section[data-testid="stSidebar"] {
    background-color: rgba(255, 255, 255, 0.95);
    color: #111;
    border-right: 2px solid #ddd;
}

.stRadio > div {
    background-color: #f1f6fb;
    padding: 1rem;
    border-radius: 12px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

.stMetric {
    background-color: #f5faff;
    padding: 1rem;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}

footer {
    visibility: hidden;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- File Setup ---
DATA_FILE = "library.txt"

def load_library():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

def save_library(library):
    with open(DATA_FILE, "w") as file:
        json.dump(library, file, indent=4)

library = load_library()

# --- Title ---
st.title("📚 Library Management System")
st.markdown("""
Effortlessly manage your collection of books. Add, remove, search, or analyze your library in one place.
""")

# --- Sidebar Menu ---
menu = ["Add Book", "Remove Book", "Search Book", "Display All Books", "Display Statistics", "Exit"]
choice = st.sidebar.radio("📌 Menu", menu)

# --- Add Book ---
if choice == "Add Book":
    st.subheader("➕ Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=1900, max_value=2100, step=1)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Mark as Read")

    if st.button("Add Book"):
        if title and author and genre:
            new_book = {
                "Title": title,
                "Author": author,
                "Year": int(year),
                "Genre": genre,
                "Read": read_status
            }
            library.append(new_book)
            save_library(library)
            st.success(f"✅ Book '{title}' added!")
        else:
            st.warning("⚠️ Please fill in all the fields.")

# --- Remove Book ---
elif choice == "Remove Book":
    st.subheader("❌ Remove a Book")
    remove_title = st.text_input("Enter the book title to remove")

    if st.button("Remove Book"):
        initial_count = len(library)
        library = [book for book in library if book["Title"].lower() != remove_title.lower()]
        save_library(library)
        if len(library) < initial_count:
            st.success(f"✅ Book '{remove_title}' removed.")
        else:
            st.warning("⚠️ Book not found.")

# --- Search Book ---
elif choice == "Search Book":
    st.subheader("🔍 Search for a Book")
    search_query = st.text_input("Enter title or author")
    year_filter = st.number_input("Filter by Publication Year (optional)", min_value=1900, max_value=datetime.now().year, step=1, value=1900)

    if search_query or year_filter > 1900:
        results = [
            book for book in library
            if (search_query.lower() in book["Title"].lower() or search_query.lower() in book["Author"].lower())
            and (book["Year"] == year_filter if year_filter > 1900 else True)
        ]
        if results:
            st.success(f"🔎 Found {len(results)} result(s):")
            for book in results:
                st.json(book)
        else:
            st.warning("❌ No matching books found.")

# --- Display All Books ---
elif choice == "Display All Books":
    st.subheader("📖 All Books in the Library")
    if library:
        for idx, book in enumerate(library, start=1):
            st.markdown(f"**Book {idx}:**")
            st.json(book)
    else:
        st.info("📂 No books found. Start adding some!")

# --- Display Statistics ---
elif choice == "Display Statistics":
    st.subheader("📊 Library Statistics")
    if not library:
        st.warning("📂 No books to show statistics.")
    else:
        df = pd.DataFrame(library)
        total_books = len(df)
        read_books = df["Read"].sum()
        unread_books = total_books - read_books
        read_percentage = (read_books / total_books) * 100

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Books", total_books)
        col2.metric("Books Read", read_books)
        col3.metric("Read %", f"{read_percentage:.2f}%")

        st.markdown("### 📘 Book Distribution by Title")
        title_counts = df["Title"].value_counts()
        fig1, ax1 = plt.subplots()
        ax1.pie(title_counts, labels=title_counts.index, autopct="%1.1f%%", startangle=90)
        ax1.axis("equal")
        st.pyplot(fig1)

        st.markdown("### 📗 Read vs Unread")
        read_data = pd.DataFrame({
            "Status": ["Read", "Unread"],
            "Count": [read_books, unread_books]
        })
        fig2, ax2 = plt.subplots()
        sns.barplot(data=read_data, x="Status", y="Count", palette="pastel", ax=ax2)
        ax2.set_title("Books Read Status")
        st.pyplot(fig2)

# --- Exit App ---
elif choice == "Exit":
    st.subheader("👋 Exit")
    st.info("Thanks for using the Library Management System!")
    if st.button("Close the App"):
        st.stop()
