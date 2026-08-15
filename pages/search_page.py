import os

import streamlit as st
import requests
from dotenv import load_dotenv
from utils.citation_types import Book, Dissertation, Article, Proceeding, Author

load_dotenv()

# Map literal publication types to their corresponding classes
INTERNAL_CLASSES_MAP = {
    "Книга": Book,
    "Дисертація": Dissertation,
    "Стаття у журналі": Article,
    "Тези конференції": Proceeding,
}

# Map internal work types to Crossref work types
CROSSREF_TYPE_MAP = {
    "Книга": "book,type:monograph",
    "Стаття у журналі": "journal-article",
    "Дисертація": "dissertation",
    "Тези конференції": "proceedings-article",
}

def get_crossref_metadata(title, work_type, last_name):
    crossref_type = CROSSREF_TYPE_MAP.get(work_type)
    filters = f"type:{crossref_type}" if crossref_type else ""
    params = {
        "rows": 5,
        "mailto": os.getenv("CROSSREF_MAILTO", "your-email@example.com"),
        "filter": filters
    }
    if (last_name):
        params["query.author"] = last_name
    if title:
        params["query.title"] = title
    url = f"https://api.crossref.org/works"
    response = requests.get(url, params=params)
    if response.status_code == 200:
        items = response.json().get("message", {}).get("items", [])
        if items:
            return items
    return None

def extract_authors(crossref_authors):
    authors = []
    for author in crossref_authors:
        given = author.get("given", "")
        given = given.rstrip('.')
        family = author.get("family", "")

        if not given and not family:
            continue

        given_split = given.split() 

        if len(given_split) < 2:
            given_split = given.split(".")
        first = ""
        middle = ""

        if len(given_split) > 1:
            first = given_split[0]
            middle = given_split[1]

        else:
            first = given
            middle = ""
        last = family

        first = first.rstrip(".")
        middle = middle.rstrip(".")
        last = last.rstrip(".")
        authors.append(Author(first_name=first, last_name=last, middle_name=middle))
    return authors

def get_base_metadata(item):
    year = None
    date_parts = item.get("issued", {}).get("date-parts", [[]])
    if date_parts and date_parts[0]:
        year = date_parts[0][0]
    return {
        "title": item.get("title", [""])[0],
        "year": year,
        "url": item.get("URL"),
        "language": item.get("language", "en"),
        "authors": extract_authors(item.get("author", [])),
    }

def get_book_metadata(item):
    data = get_base_metadata(item)
    data.update({
        "type": "Book",
        "publisher": item.get("publisher", None),
        "pages_count": item.get("page", None).split("-") if "page" in item else None,
        "city": None,  
        "publishing_number": None,
        "publishing_type": "монографія" if item.get("type") == "monograph" else None,
    })
    return data

def get_article_metadata(item):
    data = get_base_metadata(item)
    data.update({
        "type": "Article",
        "journal": item.get("container-title", [""])[0],
        "issue": item.get("issue"),
        "number": item.get("volume"),
        "pages_cited": item.get("page", ""),
    })
    return data

def get_dissertation_metadata(item):
    data = get_base_metadata(item)
    data.update({
        "type": "Dissertation",
        "university": item.get("publisher", None),
        "dissertation_type": None,
        "pages_count": None,
        "db_name": "Crossref",
    })
    return data

def get_proceeding_metadata(item):
    data = get_base_metadata(item)
    data.update({
        "conference": item.get("container-title", [""])[0],
        "publishing_type": None,
        "conference_city": None,
        "conference_date": None,
        "publisher": item.get("publisher", None),
        "pages_cited": item.get("page", None),
        "city": None
    })
    return data

def get_metadata_by_type(work_type, item):
    extractors = {
        "Книга": get_book_metadata,
        "Стаття у журналі": get_article_metadata,
        "Дисертація": get_dissertation_metadata,
        "Тези конференції": get_proceeding_metadata,
    }
    return extractors[work_type](item)

def switch_to_entry_page(entry):
    st.session_state['entry'] = entry
    st.session_state['is_first_load'] = True
    st.session_state['switch_page'] = True
    st.session_state['edit_message'] = f"Дані про знайдене джерело не повні. Будь ласка, заповніть їх, опираючись на дані за посиланням: {entry.url}. Відсутні дані у тексті посилання будуть замінені на None або відображені некоректно."
    

if st.session_state.get('switch_page', False):
    st.session_state['switch_page'] = False
    st.switch_page("pages/edit_page.py")

if st.button(":arrow_left: Повернутися на попередню сторінку"):
    st.switch_page("index.py")

work_type = st.selectbox("Тип джерела", list(INTERNAL_CLASSES_MAP.keys()))

with st.form("search_form"):
    title_input = st.text_input("Назва")
    last_name = st.text_input("Автор")
    submitted = st.form_submit_button("Пошук")

status_placeholder = st.empty()
if submitted and (title_input or last_name):
    status_placeholder.info("Пошук...")
    crossref_items = get_crossref_metadata(title_input, work_type, last_name)

    if crossref_items:
        status_placeholder.success("Результати знайдено!")
        st.subheader("Знайдені роботи:")
        try:
            works = []
            col1, col2 = st.columns([9,3])
            for idx, crossref_item in enumerate(crossref_items):
                metadata = get_metadata_by_type(work_type, crossref_item)
                work_obj = INTERNAL_CLASSES_MAP[work_type](metadata)
                works.append(work_obj)
                with col1:
                    with st.container(height=70, border=True):
                        st.write(work_obj)
                with col2:
                    with st.container(height=70, border=False):
                        st.button(label=":pencil2:", key=idx, use_container_width=True, on_click=switch_to_entry_page, args=(work_obj,))
        except Exception as e:
            status_placeholder.error(f"Не вдалося створити об'єкт: {e}")
    else:
        status_placeholder.warning("Не вдалося знайти роботу за вказаною назвою та автором.")
elif submitted:
    status_placeholder.warning("Заповніть хоча б одне поле для пошуку.")
