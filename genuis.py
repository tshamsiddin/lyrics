import requests
from bs4 import BeautifulSoup



def azlyrics(artist, song):

    a=artist.replace(' ','').lower()
    b=song.replace(' ','').lower()
    url=f'https://www.azlyrics.com/lyrics/{a}/{b}.html'

    page=requests.get(url)

    soup=BeautifulSoup(page.content, 'html.parser')

    result=soup.find_all('div', class_="col-xs-12 col-lg-8 text-center")

    result=soup.find_all('div')

    lyric=str(result[20])

    if '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->' not in lyric:
        return '''
 Lyrics not found 
 Please check the information again'''

    clean1=lyric.replace('<br/>',"")
    clean2=clean1.replace('<i>', '')
    clean3=clean2.replace('</i>', '')
    clean4=clean3.replace('<div>', '')
    clean5=clean4.replace('</div>', '')
    clean6=clean5.replace('<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->', '')
    return clean6