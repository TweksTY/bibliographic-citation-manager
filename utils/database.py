import sqlite3
from datetime import datetime
from utils.citation_types import Book, Article, Dissertation, Author, Proceeding, Site

def dict_factory(cursor, row):
    """Convert rows to dictionaries."""
    d = {}
    for idx, col in enumerate(cursor.description):
        if (row[idx] is not None):
            d[col[0]] = row[idx]
    return d

def object_factory(row):
    d = row
    if d['type'] == "Book":
        return Book(d)
    elif d['type'] == "Dissertation":
        return Dissertation(d)
    elif d['type'] == "Article":
        return Article(d)
    elif d['type'] == "Proceeding":
        return Proceeding(d)
    elif d['type'] == "Site":
        return Site(d)

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False) 
        conn.row_factory = dict_factory
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn):
    """ create a table from the create_table_sql statement """
    c = None
    try:
        sql_create_citations_table = """ CREATE TABLE IF NOT EXISTS citations (
                                            id integer PRIMARY KEY,
                                            type text NOT NULL,
                                            title text NOT NULL,
                                            language text DEFAULT 'uk' NOT NULL, 
                                            db_name text,
                                            url text,
                                            access_date text,
                                            city text,
                                            pages_count integer,
                                            pages_cited text,
                                            year integer,
                                            publisher text,
                                            publishing_number text,
                                            publishing_type text,
                                            dissertation_type text,
                                            university text,
                                            degree text,
                                            specialty text,
                                            specialty_code text,
                                            journal text,
                                            issue integer,
                                            number integer,
                                            conference text,
                                            conference_date text,
                                            conference_city text,
                                            incl_date text,
                                            active integer DEFAULT 1
                                        ); """
        sql_create_authors_table = """ CREATE TABLE IF NOT EXISTS authors (
                                            id integer PRIMARY KEY,
                                            first_name text NOT NULL,
                                            last_name text NOT NULL,
                                            middle_name text
                                        ); """
        sql_create_author_list_table = """ CREATE TABLE IF NOT EXISTS author_list (
                                            citation_id integer NOT NULL,
                                            author_id integer NOT NULL,
                                            FOREIGN KEY (citation_id) REFERENCES citations (id),
                                            FOREIGN KEY (author_id) REFERENCES authors (id),
                                            PRIMARY KEY (citation_id, author_id)
                                        ); """
        
        c = conn.cursor()
        c.execute(sql_create_citations_table)
        c.execute(sql_create_authors_table)
        c.execute(sql_create_author_list_table)
    except sqlite3.Error as e:
        print(e)
    finally:
        if c:
            c.close()

def update_entry(conn, entry):
    cur = conn.cursor()
    try:
        entry_id = entry.id
        cur.execute("DELETE FROM author_list WHERE citation_id = ?", (entry_id,))
        for author in entry.authors:
            if (author.is_empty()):
                continue
            author_id = get_or_create_author(conn, author)
            sql = ''' INSERT INTO author_list(citation_id, author_id)
                      VALUES(?,?) '''
            cur.execute(sql, (entry_id, author_id))
            
        if entry.type == "Book":
            sql = ''' UPDATE citations
                      SET type = ?,
                          title = ?,
                          language = ?,
                          url = ?,
                          access_date = ?,
                          city = ?,
                          pages_count = ?,
                          year = ?,
                          publisher = ?,
                          publishing_number = ?,
                          publishing_type = ?
                      WHERE id = ? '''
        elif entry.type == "Dissertation":
            sql = ''' UPDATE citations
                      SET type = ?,
                          title = ?,
                          language = ?,
                          url = ?,
                          access_date = ?,
                          city = ?,
                          pages_count = ?,
                          year = ?,
                          dissertation_type = ?,
                          university = ?,
                          degree = ?,
                          specialty = ?,
                          specialty_code = ?,
                          db_name = ?
                      WHERE id = ? '''
        elif entry.type == "Article":
            sql = ''' UPDATE citations
                      SET type = ?,
                          title = ?,
                          language = ?,
                          url = ?,
                          access_date = ?,
                          city = ?,
                          pages_count = ?,
                          year = ?,
                          journal = ?,
                          issue = ?,
                          number = ?,
                          pages_cited = ?
                      WHERE id = ? '''
        elif entry.type == "Proceeding":
            sql = ''' UPDATE citations
                      SET type = ?,
                          title = ?,
                          language = ?,
                          url = ?,
                          access_date = ?,
                          city = ?,
                          pages_count = ?,
                          year = ?,
                          conference = ?,
                          publishing_type = ?,
                          conference_date = ?,
                          conference_city = ?,
                          publisher = ?,
                          pages_cited = ?
                      WHERE id = ? '''
        elif entry.type == "Site":
            sql = ''' UPDATE citations
                      SET type = ?,
                          title = ?,
                          language = ?,
                          url = ?,
                          access_date = ?,
                          city = ?,
                          pages_count = ?,
                          year = ?,
                          publisher = ?
                      WHERE id = ? '''

        cur.execute(sql, (entry.get_data()+ (entry_id,)))
        conn.commit()
    finally:
        cur.close()

def insert_entry(conn, entry):
    sql = ''
    authors = entry.authors
    cur = conn.cursor()
    try:
        if entry.type == "Book":
            sql = ''' INSERT INTO citations(type, title, language, url, access_date, city, pages_count, year, publisher, publishing_number, publishing_type, incl_date)
                      VALUES(?,?,?,?,?,?,?,?,?,?,?,datetime('now')) '''
        elif entry.type == "Dissertation":
            sql = ''' INSERT INTO citations(type, title, language, url, access_date, city, pages_count, year, dissertation_type, university, degree, specialty, specialty_code, db_name, incl_date)
                      VALUES(?,?,?,?,?,?,?,?,?,?,?,datetime('now')) '''
        elif entry.type == "Article":
            sql = ''' INSERT INTO citations(type, title, language, url, access_date, city, pages_count, year, journal, issue, number, pages_cited, incl_date)
                      VALUES(?,?,?,?,?,?,?,?,?,?,?,?,datetime('now')) '''
        elif entry.type == "Proceeding":
            sql = ''' INSERT INTO citations(type, title, language, url, access_date, city, pages_count, year, conference, publishing_type, conference_date, conference_city, publisher, pages_cited, incl_date)
                      VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,datetime('now')) '''
        elif entry.type == "Site":
            sql = ''' INSERT INTO citations(type, title, language, url, access_date, city, pages_count, year, publisher, incl_date)
                      VALUES(?,?,?,?,?,?,?,?,?,datetime('now')) '''
        cur.execute(sql, entry.get_data())
        conn.commit()
        entry_id = cur.lastrowid
        for author in authors:
            if (not author.is_empty()):
                author_id = get_or_create_author(conn, author)
                sql = ''' INSERT INTO author_list(citation_id, author_id)
                          VALUES(?,?) '''
                cur.execute(sql, (entry_id, author_id))
        conn.commit()
        return cur.lastrowid
    finally:
        cur.close()

def get_author_by_citation(conn, citation_id):
    cur = conn.cursor()
    try:
        cur.execute("SELECT authors.first_name, authors.last_name, authors.middle_name FROM author_list JOIN authors ON author_list.author_id = authors.id WHERE author_list.citation_id = ? ORDER BY author_list.rowid", (citation_id,))
        rows = cur.fetchall()
        authors = []
        if (not rows):
            authors.append(Author("", "", None))
        else:
            for row in rows:
                authors.append(Author(row['first_name'], row['last_name'], row.get('middle_name', None)))
        return authors
    finally:
        cur.close()

def update_author(conn, author):
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id FROM authors WHERE first_name=? AND last_name=? AND (middle_name IS ? OR middle_name=?)",
            (author.first_name, author.last_name, author.middle_name, author.middle_name)
        )
        row = cur.fetchone()
        if row:
            return "Автор з таким ім'ям вже існує."
        cur.execute(
            "UPDATE authors SET first_name=?, last_name=?, middle_name=? WHERE id=?",
            (author.first_name, author.last_name, author.middle_name, author.id)
        )
        conn.commit()
        return None
    finally:
        cur.close()

def get_or_create_author(conn, author):
    first_name = author.first_name.strip()
    last_name = author.last_name.strip()
    middle_name = author.middle_name.strip() if author.middle_name else None
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id FROM authors WHERE first_name=? AND last_name=? AND (middle_name IS ? OR middle_name=?)",
            (first_name, last_name, middle_name, middle_name)
        )
        row = cur.fetchone()
        if row:
            return row['id']
        cur.execute(
            "INSERT INTO authors(first_name, last_name, middle_name) VALUES (?, ?, ?)",
            (first_name, last_name, middle_name)
        )
        conn.commit()
        return cur.lastrowid
    finally:
        cur.close()

def get_authors(conn):
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM authors")
        rows = cur.fetchall()
        return [Author(row['first_name'], row['last_name'], row.get('middle_name', None), row.get('id')) for row in rows]
    finally:
        cur.close()

def delete_author(conn, author_id):
    cur = conn.cursor()
    try:
        cur.execute('SELECT COUNT(*) as cnt FROM author_list WHERE author_id=?', (author_id,))
        if cur.fetchone()['cnt'] > 0:
            return "Неможливо видалити автора, оскільки він використовується в записах цитувань."
        sql_author_list = 'DELETE FROM author_list WHERE author_id=?'
        cur.execute(sql_author_list, (author_id,))

        sql_authors = 'DELETE FROM authors WHERE id=?'
        cur.execute(sql_authors, (author_id,))
        conn.commit()
        return None
    finally:
        cur.close()

def delete_entry(conn, entry_id):
    cur = conn.cursor()
    try:
        sql_author_list = 'DELETE FROM author_list WHERE citation_id=?'
        cur.execute(sql_author_list, (entry_id,))
        sql_citations = 'UPDATE citations SET active = 0 WHERE id=?'
        cur.execute(sql_citations, (entry_id,))
        conn.commit()
    finally:
        cur.close()

def get_entries(conn, entry_type = None, sort_by = "time"):
    sql_sort_dict = {
        'time_temp' : '',
        'time' : ' ORDER BY julianday(incl_date) ASC',
        'title': ' ORDER BY title ASC',
    }
    sql_sort_str = sql_sort_dict.get(sort_by, '')
    cur = conn.cursor()
    try:
        if (entry_type is None):
            cur.execute("SELECT * FROM citations WHERE active=1" + sql_sort_str)
        else:
            cur.execute("SELECT * FROM citations WHERE type=? AND active = 1" + sql_sort_str, (entry_type,))
        rows = cur.fetchall()
    finally:
        cur.close()

    for row in rows:
        row['authors'] = get_author_by_citation(conn, row['id'])

    rows = [object_factory(row) for row in rows]
    return rows

def get_entry_by_id(conn, entry_id):
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM citations WHERE id=?", (entry_id,))
        row = cur.fetchone()
    finally:
        cur.close()
    if row:
        row['authors'] = get_author_by_citation(conn, row['id'])
    return object_factory(row) if row else None