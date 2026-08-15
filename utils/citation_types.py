from utils.citation_bits import abbreviations_DSTU

    

class Author:
    def __init__(self, first_name, last_name, middle_name, id = None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name

    def is_empty(self):
        return not (self.first_name or self.last_name or self.middle_name)
    
    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "middle_name": self.middle_name,
        }

    def get_abbr_name(self):
        if ('-' in self.first_name):
            first_name_parts = self.first_name.split('-')
            first_name = '-'.join([part[0].upper() + '.' for part in first_name_parts])
            return first_name
        return self.first_name[0].upper() + '.'
    
    def get_first_name(self):
        if (len(self.first_name) > 1):
            first_name = self.first_name
        else:
            first_name = self.first_name[0].upper() + '.'
        return first_name
    
    def get_middle_name(self):
        if (self.middle_name):
            if (len(self.middle_name) > 1):
                middle_name = self.middle_name + ' '
            else:
                middle_name = self.middle_name[0].upper() + '. '
            return middle_name
        return ""

    def __repr__(self):
        return f"{self.last_name} {self.first_name}{' ' + self.middle_name if self.middle_name else ''}"
    
    def get_full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

class Entry:
    id = None
    type = "Entry"
    language = "uk"
    authors = []
    url = None
    title = None
    city = None
    year = None
    pages_count = None
    access_date = None
    
    def __init__(self, data):
        self.id = data.get("id", self.id)
        self.type = data.get("type", self.type)
        self.authors = data.get("authors", self.authors)
        self.language = data.get("language", self.language)
        self.url = data.get("url", self.url)
        self.access_date = data.get("access_date", self.access_date)
        self.title = data.get("title", self.title)
        self.city = data.get("city", self.city)
        self.year = data.get("year", self.year)
        self.pages_count = data.get("pages_count", self.pages_count)
        
    def __repr__(self):
        types = {
            "Book": "Книга",
            "Dissertation": "Дисертація",
            "Article": "Стаття",
            "Proceeding": "Тези",
            "Site": "Сайт",
        }
        result = f"Тип: {types[self.type]}, Назва: {self.title}, Мова: {'українська' if self.language == 'uk' else 'англійська або невизначена'}, URL: {self.url}"
        if self.authors and not any(author.is_empty() for author in self.authors):
            result += f", Автори: {', '.join([str(author) for author in self.authors])}"
        result += f", Рік: {self.year}"
        return result
    
    def _get_translated_text(self, text):
        translations = {}
        if self.language == "uk":
            translations = {
                "pages" : "с.",
                "pages-cited" : "С.",
                "no-date" : "б.д.",
                "mla-multiple-authors": "та ін.",
                "mla-single-author": "та",
                "edition" : "вид.",
                "retrieved" : "Взято",
                "from" : "з",
                "access-date": "дата звернення",
                "access-mode": "Режим доступу",
                "title": "Назва з екрана",
                "resource": "Електронний ресурс",
                "dissertation" : "дис.",
                "access-date-mla": "Останній перегляд",
                "unpublished": "Неопубл.",
                "volume": "Т.",
                "issue": "№",
                "volume-mla": "т.",
                "city": "м. ",
            }
        if self.language == "en":
            translations = {
                "pages" : "p.",
                "pages-cited" : "P.",
                "mla-multiple-authors": "et al.",
                "mla-single-author": "and",
                "no-date" : "n.d.",
                "edition" : "ed.",
                "retrieved" : "Retrieved",
                "from" : "from",
                "city": "",
                "access-date": "date of access",
                "access-mode": "Mode of access",
                "title": "Title from screen",
                "resource": "Electronic resource",
                "dissertation" : "dissertation",
                "access-date-mla": "Accessed",
                "unpublished": "Unpublished",
                "volume": "Vol.",
                "issue": "no.",
                "volume-mla": "vol.",
            }
        return translations.get(text, "")

    def get_data(self):
        return (self.type, self.title, self.language, self.url, self.access_date, self.city, self.pages_count, self.year,)
    
    def get_data_with_authors(self):
        return (self.type, self.title, self.language, self.url, self.access_date, self.city, self.pages_count, self.year, self.authors,)
    
    def _get_authors_text(self, citation_style):

        if len(self.authors) == 0 or self.authors[0].is_empty():
            return ""
        if citation_style == "DSTU_2015":
            return ', '.join([f"{author.last_name} {author.first_name[0]}.{' ' + author.middle_name[0] + '.' if author.middle_name else ''}" for author in self.authors])
        if citation_style == "DSTU_2006":
            first = self.authors[0]
            name = ""
            if (len(self.authors) < 4):
                name = ', '.join([f"{author.get_first_name()} {author.get_middle_name()}{author.last_name}" for author in self.authors])
            else:
                name = f"{first.get_first_name()} {first.get_middle_name()}{first.last_name}"
            return name
        if citation_style == "APA":
            name = ""
            if len(self.authors) == 1:
                first = self.authors[0]
                name = f"{self.authors[0].last_name}, {self.authors[0].first_name[0]}. {first.middle_name[0] + '. ' if first.middle_name else ''}"
            elif len(self.authors) < 20:
                name = ', '.join([f"{author.last_name}, {author.first_name[0]}. {author.middle_name[0] + '.' if author.middle_name else ''}" for author in self.authors[:-1]])
                name += f" & {self.authors[-1].last_name}, {self.authors[-1].first_name[0]}. {self.authors[-1].middle_name[0] + '. ' if self.authors[-1].middle_name else ''}"
            else:
                name = ', '.join([f"{author.last_name}, {author.first_name[0]}. {author.middle_name[0] + '.' if author.middle_name else ''}" for author in self.authors[:19]])
                name += f" & {self.authors[-1].last_name}, {self.authors[-1].first_name[0]}. {self.authors[-1].middle_name[0] + '. ' if self.authors[-1].middle_name else ''}"
            return name
        if citation_style == "MLA":
            name = ""
            if len(self.authors) == 1:
                first = self.authors[0]
                first_name = first.get_first_name()
                middle_name = first.get_middle_name()
                name = f"{first.last_name}, {first_name} {middle_name}"
            elif len(self.authors) >= 2:
                first = self.authors[0]
                second = self.authors[1]
                name = f"{first.last_name}, {first.get_first_name()} {first.get_middle_name()}"
                name = name.strip()
                if len(self.authors) == 2:
                    name += f", {self._get_translated_text('mla-single-author')} {second.get_first_name()} {second.get_middle_name()}{second.last_name}."
                else:
                    name += f", {self._get_translated_text('mla-multiple-authors')}"
            return name
        raise ValueError("Unknown citation style")

    def _get_url_text(self, citation_style):
        if not self.url:
            return ""
        if citation_style == "DSTU_2015":
            return f" URL: {self.url} ({self._get_translated_text('access-date')}: {self.access_date})."
        if citation_style == "DSTU_2006":
            return f" - {self._get_translated_text('access-mode')}: {self.url} ({self._get_translated_text('access-date')}: {self.access_date}). - {self._get_translated_text('title')}."
        if citation_style == "APA":
            return f" {self.url}."
        if citation_style == "MLA":
            return f" {self.url}. {self._get_translated_text('access-date-mla')} {self.access_date}."
        if citation_style == "APA-site":
            return f" {self._get_translated_text('retrieved')} {self.access_date} {self._get_translated_text('from')} {self.url}."
        

class Book(Entry):
    type = "Book"
    publisher = None
    publishing_number = None
    publishing_type = None
    def __init__(self, data):
        super().__init__(data)
        self.type = "Book"
        self.publisher = data.get("publisher", self.publisher)
        self.publishing_number = data.get("publishing_number", self.publishing_number)
        self.publishing_type = data.get("publishing_type", self.publishing_type)

    def __repr__(self):
        return f"{super().__repr__()}"
    
    def _get_number_ending(self):
        """first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh, twelfth"""
        result = self.publishing_number
        if self.language == "uk":
            result+= "-"
        number = int(self.publishing_number) 
        if number % 100 >= 10 and number % 100 <= 20:
            if self.language == "uk":
                result += "те"
            else:
                result += "th"
        last_digit = number % 10
        if self.language == "uk":
            match last_digit:
                case 0:
                    result += "те"
                case 1:
                    result += "ше"
                case 2:
                    result += "ге"
                case 3:
                    result += "тє"
                case 4 | 5 | 6 | 9:
                    result += "те"
                case 7 | 8:
                    result += "ме"
        elif self.language == "en":
            match last_digit:
                case 1:
                    result += "st"
                case 2:
                    result += "nd"
                case 3:
                    result += "rd"
                case _:
                    result += "th"
        return result
    
    def _get_publishing_text(self, citation_style):
        publishing_number = self.publishing_number
        if publishing_number is None or publishing_number == "":
            return ""
        result =  f"{self._get_number_ending()} {super()._get_translated_text('edition')}"
        if citation_style == "DSTU_2015":
            return f"{result} "
        if citation_style == "DSTU_2006":
            return f"{result} — "
        if citation_style == "APA":
            return f" ({result})"    
        if citation_style == "MLA":
            return f"{result}, "
    
    def get_DSTU2015_citation(self):
        if (len(self.authors) < 4):
            name = super()._get_authors_text('DSTU_2015')
            result = f"{name} {self.title}"
        else:
            result = f"{self.title}"
        if (self.publishing_type):
            result += f" : {self.publishing_type}"
        if (len(self.authors) < 4):
            result += f"."
        else:
            result += f" / {self.authors[0].get_abbr_name()} {self.authors[0].middle_name[0] + '. ' if self.authors[0].middle_name else ''}{self.authors[0].last_name} {super()._get_translated_text('mla-multiple-authors')}"
        result += f" {self._get_publishing_text('DSTU_2015')}{getattr(self, 'city', '')} : {self.publisher}, {self.year}. {self.pages_count} {super()._get_translated_text('pages')}"
        result += super()._get_url_text('DSTU_2015')
        return result


    def get_DSTU2006_citation(self):
        first = self.authors[0]
        name = super()._get_authors_text('DSTU_2006')
        result = ""
        if (len(self.authors) < 4):
            result = f"{first.last_name} {first.get_abbr_name()} {first.middle_name[0] + '. ' if first.middle_name else ''}{self.title}"
        else:
            result = f"{self.title}"
        
        if (self.publishing_type):
            result += f" : {self.publishing_type}"
        if (self.url):
            result += f" [{super()._get_translated_text('resource')}]"
        result += " / "
        if (len(self.authors) < 4):
            result += f" {name}"
        else:
            result += f" {first.get_first_name()} {first.get_middle_name()}{first.last_name} [{super()._get_authors_text('mla-multiple-authors')}]"
        result += f". — {self._get_publishing_text('DSTU_2006')}{self.city} : {self.publisher}, {self.year}. — {self.pages_count} {super()._get_translated_text('pages')}"
        result += super()._get_url_text('DSTU_2006')
        return result

    def get_APA_citation(self):
        name = super()._get_authors_text('APA')
        result = f"{name}({self.year}). {self.title}{self._get_publishing_text('APA')}. {self.publisher}."
        result += super()._get_url_text('APA')
        return result

    def get_MLA_citation(self):
        name = super()._get_authors_text('MLA')
        result = f"{name} {self.title}. {self._get_publishing_text('MLA')}{self.publisher}, {self.year}."
        result += super()._get_url_text('MLA')
        return result

    def get_data(self):
        return super().get_data() + (self.publisher, self.publishing_number, self.publishing_type,)
    
    def get_data_with_authors(self):
        return super().get_data_with_authors() + (self.publisher, self.publishing_number, self.publishing_type,)
    
class Dissertation(Entry):
    type = "Dissertation"
    dissertation_type = None
    university = None
    degree = None
    specialty = None
    specialty_code = None
    db_name = None
    def __init__(self, data):
        super().__init__(data)
        self.type = "Dissertation"
        self.db_name = data.get("db_name", self.db_name)
        self.dissertation_type = data.get("dissertation_type", self.dissertation_type)
        self.university = data.get("university", self.university)
        self.degree = data.get("degree", self.degree)
        self.specialty = data.get("specialty", self.specialty)
        self.specialty_code = data.get("specialty_code", self.specialty_code)

    def _get_degree_text(self):
        if not self.degree:
            if self.dissertation_type:
                return f"{self.dissertation_type}"
            else:
                return None
        result = f"{super()._get_translated_text('dissertation')} ... {abbreviations_DSTU[self.language][self.degree]} "
        if self.degree == 'кандидат наук' or self.degree == 'доктор наук':
            result += f"{abbreviations_DSTU[self.language][self.specialty][0]} : {self.specialty_code}"
        if self.degree == 'доктор філософії':
            result += f"{abbreviations_DSTU[self.language][self.specialty][1]} : {self.specialty_code}"


    def __repr__(self):
        return f"{super().__repr__()}"
    
    def get_data(self):
        return super().get_data() + (self.dissertation_type, self.university, self.degree, self.specialty, self.specialty_code, self.db_name,)
    
    def get_data_with_authors(self):
        return super().get_data_with_authors() + (self.dissertation_type, self.university, self.degree, self.specialty, self.specialty_code, self.db_name,)

    def get_DSTU2006_citation(self):
        first = self.authors[0]
        name = super()._get_authors_text('DSTU_2006')
        degree_text = self._get_degree_text()
        result = f"{first.last_name} {first.get_abbr_name()} {first.middle_name[0] + '. ' if first.middle_name else ''}{self.title}"
        if (self.url):
            result += f"[{super()._get_translated_text('resource')}]"
        if degree_text:
            result += f" {degree_text} /"
        result += f"{first.get_first_name()} {first.get_middle_name()} {first.last_name}"
        result += f". — {self.city}, {self.year}. — {self.pages_count} {super()._get_translated_text('pages')}."
        result += super()._get_url_text('DSTU_2006')
        return result
    
    def get_DSTU2015_citation(self):
        name = super()._get_authors_text('DSTU_2015')
        degree_text = self._get_degree_text()
        result = f"{name} {self.title}"
        if degree_text:
            result += f" : {self._get_degree_text()}."
        result += f". {self.city}, {self.year}. {self.pages_count} {super()._get_translated_text('pages')}"
        result += super()._get_url_text('DSTU_2015')


        return result
    
    def get_APA_citation(self):
        name = super()._get_authors_text('APA')
        result = f"{name} ({self.year}). {self.title} "
        degree_text = self._get_degree_text()
        if degree_text:
            if not self.url:
                result += f"[{super()._get_translated_text('unpublished')} {self._get_degree_text()}]. {self.university}."
            else:
                result += f"[{self._get_degree_text()}, {self.university}]."
        else:
            if not self.url:
                result += f". {self.university}."
            else:
                result += f"[{self.university}]."
        if self.db_name:
            result += f" {self.db_name + '. ' if self.db_name else ''}"
        result += super()._get_url_text('APA')
        
        return result
        
    def get_MLA_citation(self):
        name = super()._get_authors_text('MLA')
        degree_text = self._get_degree_text()
        result =  f"{name}. {self.title}. {self.year}. {self.university}"
        if degree_text:
            result += f", {degree_text}."
        else:
            result += "."
        if self.db_name:
            result += f" {self.db_name + ', ' if self.db_name else ''}"
        result += f"{super()._get_url_text('MLA')}"
        return result

class Article(Entry):
    type = "Article"
    journal = None
    issue = None
    number = None
    pages_cited = None
    def __init__(self, data):
        super().__init__(data)
        self.type = "Article"
        self.journal = data.get("journal", self.journal)
        self.issue = data.get("issue", self.issue)
        self.number = data.get("number", self.number)
        self.pages_cited = data.get("pages_cited", self.pages_cited)

    def __repr__(self):
        return f"{super().__repr__()}"
    
    def get_data(self):
        return super().get_data() + (self.journal, self.issue, self.number, self.pages_cited,)
    
    def get_data_with_authors(self):
        return super().get_data_with_authors() + (self.journal, self.issue, self.number, self.pages_cited,)

    def _get_container_text(self, citation_style):
        result = ""
        if not self.number and not self.issue:
            return ""
        if citation_style == "DSTU_2015" or citation_style == "DSTU_2006":
            if (self.issue and self.number):
                result += f"{super()._get_translated_text('volume')} {self.number}, № {self.issue}"
            elif self.number:
                result += f"{super()._get_translated_text('volume')} {self.number}"
            elif self.issue:
                result += f"{super()._get_translated_text('issue')} {self.issue}"
        
        if citation_style == "APA":
            if self.number:
                result += f"{self.number}"
            if self.issue:
                result += f"({self.issue})"

        if citation_style == "MLA":
            if (self.issue and self.number):
                result += f"{super()._get_translated_text('volume-mla')} {self.number}, {super()._get_translated_text('issue')} {self.issue}"
            elif self.number:
                result += f"{super()._get_translated_text('volume-mla')} {self.number}"
            elif self.issue:
                result += f"{super()._get_translated_text('issue')} {self.issue}"
        return result


    def get_DSTU2006_citation(self):
        first = self.authors[0]
        name = super()._get_authors_text('DSTU_2006')
        if (len(self.authors) < 4):
            result = f"{first.last_name} {first.get_abbr_name()} {first.middle_name[0] + '. ' if first.middle_name else ''}{self.title}"
        else:
            result = f"{self.title}"
        if (self.url):
            result += f" [{super()._get_translated_text('resource')}]"
        result += " / "
        if len(self.authors) < 4:
            result += f"{name}"
        else:
            result += f"{first.get_first_name()} {first.get_middle_name()}{first.last_name} [{super()._get_authors_text('mla-multiple-authors')}]"
        result += f" // {self.journal}. — {self.year}. — {self._get_container_text('DSTU_2006')}. — {super()._get_translated_text('pages-cited')} {self.pages_cited}."
        result += super()._get_url_text('DSTU_2006')
        return result
    
    def get_DSTU2015_citation(self):
        if (len(self.authors) < 4):
            name = super()._get_authors_text('DSTU_2015')
            result = f"{name} {self.title}. "
        else:
            result = f"{self.title} / {self.authors[0].get_abbr_name()} {self.authors[0].middle_name[0] + '. ' if self.authors[0].middle_name else ''}{self.authors[0].last_name} {super()._get_authors_text('mla-multiple-authors')} "
        result += f"{self.journal}. {self._get_container_text('DSTU_2015')}. {super()._get_translated_text('pages-cited')} {self.pages_cited}."
        result += super()._get_url_text('DSTU_2015')
        return result
    
    def get_APA_citation(self):
        name = super()._get_authors_text('APA')
        result = f"{name}({self.year}). {self.title}. {self.journal}, {self._get_container_text('APA')}, {self.pages_cited}."
        result += super()._get_url_text('APA')
        return result
    
    def get_MLA_citation(self):
        name = super()._get_authors_text('MLA')
        result = f"{name}. \"{self.title}\". {self.journal}, {self._get_container_text('MLA')}, {self.year}, {super()._get_translated_text('pages')} {self.pages_cited}."
        result += super()._get_url_text('MLA')
        return result

class Proceeding(Entry):
    type = "Proceeding"
    conference = None
    publishing_type = None
    conference_date = None
    conference_city = None
    publisher = None
    pages_cited = None

    def __init__(self, data):
        super().__init__(data)
        self.type = "Proceeding"
        self.publishing_type = data.get("publishing_type", self.publishing_type)
        self.conference_date = data.get("conference_date", self.conference_date)
        self.conference_city = data.get("conference_city", self.conference_city)
        self.publisher = data.get("publisher", self.publisher)
        self.conference = data.get("conference", self.conference)
        self.pages_cited = data.get("pages_cited", self.pages_cited)

    def __repr__(self):
        return f"{super().__repr__()}"
    
    def get_data(self):
        return super().get_data() + (self.conference, self.publishing_type, self.conference_date, self.conference_city, self.publisher, self.pages_cited,)
    
    def get_data_with_authors(self):
        return super().get_data_with_authors() + (self.conference, self.publishing_type, self.conference_date, self.conference_city, self.publisher, self.pages_cited,)
    
    def get_DSTU2006_citation(self):
        first = self.authors[0]
        name = super()._get_authors_text('DSTU_2006')
        if (len(self.authors) < 4):
            result = f"{first.last_name} {first.get_abbr_name()} {first.middle_name[0] + '. ' if first.middle_name else ''}{self.title}"
        else:
            result = f"{self.title}"
        if (self.url):
            result += f" [{super()._get_translated_text('resource')}]"
        result += " / "
        if len(self.authors) < 4:
            result += f"{name}"
        else:
            result += f"{first.name} {first.get_middle_name()}{first.last_name} [{super()._get_authors_text('mla-multiple-authors')}]"
        result += f" // {self.conference} : {self.publishing_type}, {self.conference_city}, {self.conference_date}. — {self.city}, {self.year}. — {super()._get_translated_text('pages-cited')} {self.pages_cited}."
        result += super()._get_url_text('DSTU_2006')
        return result

    def get_DSTU2015_citation(self):
        result = ""
        if (len(self.authors) < 4):
            name = super()._get_authors_text('DSTU_2015')
            result += f"{name} {self.title}."
        else:
            result += f"{self.title} / {self.authors[0].get_abbr_name()} {self.authors[0].middle_name[0] + '. ' if self.authors[0].middle_name else ''}{self.authors[0].last_name} {super()._get_authors_text('mla-multiple-authors')}"
        result += f" {self.conference} : {self.publishing_type}, {super()._get_translated_text('city')}{self.conference_city}, {self.conference_date}. {self.publisher}, {self.year}. {super()._get_translated_text('pages-cited')} {self.pages_cited}."
        result += super()._get_url_text('DSTU_2015')
        return result
    
    def get_MLA_citation(self):
        name = super()._get_authors_text('MLA')
        result = f"{name} \"{self.title}\". {self.conference}, {self.publisher}, {self.year}, {super()._get_translated_text('pages')} {self.pages_cited}."
        result += super()._get_url_text('MLA')
        return result
    
    def get_APA_citation(self):
        name = super()._get_authors_text('APA')
        result = f"{name} ({self.year}). {self.title}. {self.conference} ({super()._get_translated_text('pages')} {self.pages_cited}). {self.publisher}."
        result += super()._get_url_text('APA')
        return result
    
class Site(Entry):
    def __init__(self, data):
        super().__init__(data)
        self.type = "Site"
        self.publisher = data.get("publisher", None)

    def __repr__(self):
        return f"{super().__repr__()}"
    
    def get_data(self):
        return super().get_data() + (self.publisher,)
    
    def get_data_with_authors(self):
        return super().get_data_with_authors() + (self.publisher,)
    
    def get_DSTU2006_citation(self):
        first = self.authors[0]
        name = super()._get_authors_text('DSTU_2006')
        result = ""
        if (len(self.authors) < 4 and name):
            result = f"{first.last_name} {first.get_abbr_name()} {first.middle_name[0] + '. ' if first.middle_name else ''}"
        result += f"{self.title}"
        
        if (self.url):
            result += f" [{super()._get_translated_text('resource')}]"
        if (len(self.authors) < 4 and name):
            result += f" / {name}"
        elif (len(self.authors) >= 4 and name):
            result += f" {first.get_first_name()} {first.get_middle_name()}{first.last_name} [{super()._get_authors_text('mla-multiple-authors')}]"
        result += f". {super()._get_url_text('DSTU_2006')}"
        return result

    def get_DSTU2015_citation(self):
        name = super()._get_authors_text('DSTU_2015')
        if (name):
            if (len(self.authors) < 4):
                result = f"{name} {self.title}."
            else:
                result = f"{self.title} / {self.authors[0].get_abbr_name()} {self.authors[0].middle_name[0] + '. ' if self.authors[0].middle_name else ''}{self.authors[0].last_name} {super()._get_authors_text('mla-multiple-authors')}."
        else:
            result = f"{self.title}."
        if (self.publisher):
            result += f" {self.publisher}."
        result += super()._get_url_text('DSTU_2015')
        return result
    
    def get_APA_citation(self):
        name = super()._get_authors_text('APA')
        result = ""
        if (name):
            result = f"{name} ({self.year}). {self.title}. "
        else:
            result = f"{self.publisher} {self.title}. "
        result += f"({super()._get_translated_text('no-date')}). {self.title}."
        result += super()._get_url_text('APA-site')
        return result
    
    def get_MLA_citation(self):
        name = super()._get_authors_text('MLA')
        result = ""
        if (name):
            result = f"{name}. \"{self.title}\""
        else:
            result = f"\"{self.title}\""
        if (self.publisher):
            result += f" {self.publisher}, "
        result += self._get_url_text('MLA')
        return result


    
