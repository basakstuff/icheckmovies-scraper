"""scraper for icheckmovies.com"""

from urllib.request import urlopen
import re
import pandas as pd

user = 'enter_user_name'
output_file = 'output_file.csv'


def get_total_number_of_pages():
    url = f'https://www.icheckmovies.com/movies/checked/?user={user}'

    page = urlopen(url)
    html_str = page.read().decode("utf-8")

    # get total number of pages
    start = 'Go to page '
    end = '">'
    pattern = start + "(.*?)" + end
    out = re.findall(pattern, html_str, re.IGNORECASE)

    return int(out[-1])


total_pages = get_total_number_of_pages()


def get_list_movies(page_number):
    if page_number == 1:
        url = f'https://www.icheckmovies.com/movies/checked/?user={user}'
    else:
        url = f'https://www.icheckmovies.com/movies/checked/?page={page_number}&user={user}'

    page = urlopen(url)
    html_str = page.read().decode("utf-8")

    start = '<a class="optionIcon optionIMDB external" href='
    end = "\'s IMDb page\">Visit IMDb page</a>"
    pattern = start + "(.*?)" + end
    ls_all_lines = re.findall(pattern, html_str, re.IGNORECASE)

    ls_movies = []

    for i in ls_all_lines:
        i = i.replace('&#039;', "'")
        tup = i.split(' title="Visit ')
        name = tup[1]
        imdb_link = tup[0][1:-1]  # get rid of quotes
        ls_movies.append([name, imdb_link])
    return ls_movies


ls_all_movies = []
for num in range(1, total_pages+1):
    print(f'working on page {num}/{total_pages}')
    ls_all_movies += get_list_movies(num)

df = pd.DataFrame(ls_all_movies)
df.columns = ['Title', 'imdburl']

df['IMDB_ID'] = df['imdburl'].apply(lambda s: s.split('title/')[1][:-1])
df['Type'] = 'movie'
df['Watchlist'] = 'completed'

ls_col = ['simkl_id', 'TVDB_ID', 'TMDB', 'IMDB_ID', 'MAL_ID', 'Type', 'Title', 'Year', 'LastEpWatched', 'Watchlist',
          'WatchedDate', 'Rating', 'Memo']
df = df.reindex(columns=ls_col)

df.to_csv(output_file)
