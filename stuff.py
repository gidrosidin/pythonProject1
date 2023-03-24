import requests as r
import geopy


def git_search(query, language):
    url = 'https://api.github.com/search/repositories'
    params = {'q': query,
              'l': language}
    res = r.get(url, params=params).json()
    message = ''
    for repo in res['items']:
        message += f'<a href="{repo["svn_url"]}">{repo["name"]}</a>\n'
    return message


def get_image():
    content = r.get('https://random.dog/woof.json').json()
    url = content['url']
    return url


def get_city(lat, lon):
    locator = geopy.geocoders.Nominatim(user_agent='geoapiExercises')
    location = locator.reverse(str(lat) + "," + str(lon))
    address = location.raw['address']
    return