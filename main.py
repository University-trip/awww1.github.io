import requests
from bs4 import BeautifulSoup

# from googlesearch import search
#
# # Lista elementów zescrapowanych z tabeli
# from googlesearch import search

GIT_URL = "https://github.com/University-trip/awww1"
from duckduckgo_search import DDGS

def search_info_about_language(language_name):
    # print("xd")
    query = language_name + " programming description"
    results = DDGS().text(language_name, max_results=2)
    # print(results)
    return results

    # for j in search(query, num=2, stop=2, pause=1):
    #     lang_urls[language_name].append(j)
    #     # print(j)


# res = search_info_about_language("python")
# exit()

class Markdown:
    filename = 'output.md'
    file = None
    closed = 0

    def __init__(self, name='output.md'):
        # print(name)
        self.filename = name.replace('/', '_').replace(' ', '_')
        self.file = open(self.filename, 'w', encoding='utf-8')


    def open(self):
        self.closed = 0
        self.file = open(self.filename, 'w', encoding='utf-8')

    def write(self, text):
        self.file.write(text)

    def close(self):
        self.closed = 1
        self.file.close()

    def __del__(self):
        # Zamknięcie pliku w destruktorze klasy
        if self.closed == 0:
            self.file.close()


def scrape_subpage(lang, file_handler):
    lang_urls = {}
    # See more
    # file_handler.write("See more:<br>")
    # Przykład użycia
    lang_urls[lang] = []
    file_src = lang+".md"
    # print(file_src + "HEELO")
    # return
    file = Markdown(file_src)
    result = search_info_about_language(lang)
    first_r = result[0]
    post = {
        "title":first_r["title"],
        "body":first_r['body'],
        "url": first_r['href']
    }
    file.write("## Description about "+ lang+"\n\n")
    file.write(post["body"])
    file.write("\n\nMore:\n\n")
    for row in result:
        url = row["href"]
        file.write("* "+url+"\n")

    file.write("\n\n\n\nReturn: [Main page](/output.md)")

    file.close()



# Funkcja do pobierania i zescrapowania danych z witryny
def scrape_website(url, gen_url):
    # Pobranie zawartości strony internetowej
    response = requests.get(url)

    # Sprawdzenie czy pobranie danych zakończyło się sukcesem
    if response.status_code != 200:
        print("Nie można pobrać strony.")

    # Parsowanie zawartości strony za pomocą BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Tutaj można znaleźć odpowiednie elementy HTML zawierające interesujące nas informacje
    # i wyodrębnić z" nich potrzebne dane
    # Na przykład:
    # - dla listy języków programowania:
    languages_table = soup.find('table', class_='table table-striped table-top20')
    # print(soup)
    # print(languages_table)
    header = "Top programming languages\n"

    file_handler = Markdown()
    # file_handler.open()

    # generate markdown
    if not languages_table:
        return None
    # Otwarcie pliku markdown do zapisu
    # with open('output.md', 'w', encoding='utf-8') as file:

    idx = 0
    file_handler.write("## " + header)
    # Iteracja przez wiersze tabeli
    for row in languages_table.find_all('tr'):
        # Pobranie wszystkich komórek w danym wierszu
        cells = row.find_all(['th', 'td'])
        cell_with_class = row.find(['th', 'td'], class_='td-top20')
        # print(cells)
        # Jeśli wiersz zawiera komórki
        if cells:
            # Uzyskanie danych z komórek (np. tekst, linki do obrazków itp.)
            # W tym przykładzie zakładamy, że dane są w kolejnych komórkach
            # i mają odpowiednio tekst, link, obrazek itp.
            # Możesz dostosować to do swojej własnej struktury tabeli
            cell_data = []
            for cell in cells:
                # print(cell.get('class', [])['td-top20'])
                # Sprawdzenie, czy komórka zawiera klasę 'td-top20'
                if 'td-top20' in cell.get('class', []):
                    img_src = cell.find('img')['src']
                    cell_data.append(f'![Python Logo]({gen_url + img_src})')
                    continue  # Pomijanie komórki
                # Sprawdzenie, czy komórka zawiera obrazek w górę
                img_upup = cell.find('img', {'alt': 'change',
                                             'src': '/wp-content/themes/tiobe/tpci/images/upup.png'})
                if img_upup:
                    cell_data.append('⇈')  # Zamiana na podwójną strzałkę w górę
                    continue
                # Sprawdzenie, czy komórka zawiera podwójny obrazek w dół
                img_downdown = cell.find('img', {'alt': 'change',
                                                 'src': '/wp-content/themes/tiobe/tpci/images/downdown.png'})
                if img_downdown:
                    cell_data.append('⇊')  # Zamiana na podwójną strzałkę w dół
                    continue
                img_up = cell.find('img',
                                   {'alt': 'change', 'src': '/wp-content/themes/tiobe/tpci/images/up.png'})
                if img_up:
                    cell_data.append('↑')  # Zamiana na ^
                    continue
                # Sprawdzenie, czy komórka zawiera obrazek w dół
                img_down = cell.find('img', {'alt': 'change',
                                             'src': '/wp-content/themes/tiobe/tpci/images/down.png'})
                if img_down:
                    cell_data.append('↓')  # Zamiana na ↓
                    continue
                # Jeśli komórka nie zawiera obrazka, pobierz tekst
                cell_data.append(cell.get_text().strip())
            # print(cell_data)
            lang = cell_data[4]
            sub_filename = lang.replace('/', '_').replace(' ', '_')
            skip = 0
            if idx == 0:
                skip = 1
                cell_data.insert(3, "Img")
                cell_data.append("Description")
            else:

                cell_data.append("[Desc](/"+sub_filename + ".md)")

            idx += 1

            # Tworzenie wiersza w pliku markdown z danymi z komórek
            # Dla przykładu używamy formatu | dane1 | dane2 | dane3 |
            markdown_row = "| " + " | ".join(cell_data) + " |"
            # Zapisanie wiersza do pliku
            file_handler.write(markdown_row + '\n')

            if skip == 1:
                markdown_row = "|"
                for _ in cell_data:
                    markdown_row += "-|"
                # Zapisanie wiersza do pliku
                file_handler.write(markdown_row + '\n')
                continue

            # print(cell_data)
            # print(lang)
            scrape_subpage(sub_filename, file_handler)

            # nastepna iteracja


    print("Plik markdown został wygenerowany.")



# HOME PAGE
home_pg = "README.MD"
file = Markdown(home_pg)
text = """
## Hello! 


Let's talk about top programming languages. I prepared list of the top 20 programming languages:

Check it here: [top20](/output.md)

"""
file.write(text)
file.close()
# URL do witryny z listą elementów do zescrapowania (można zmienić na odpowiedni dla danej witryny)
url = "https://www.tiobe.com/tiobe-index/"
gen_url = "https://www.tiobe.com"
scrape_website(url, gen_url)
