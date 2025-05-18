import requests
from bs4 import BeautifulSoup


def get_data():
    url = 'https://olimpiada.ru/activities'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find_all("div", class_="o-block")
    data = []

    for item in items:
        subject = item.find(class_='subject_tag').get_text()
        form = item.find(class_='classes_dop').get_text()
        raiting = item.find(class_='pl_rating').get_text()
        title = item.find(class_='headline').get_text()
        time = item.find(class_='headline red')
        time = time.get_text() if time != None else ''
        desc = item.find(class_='none_a black olimp_desc')
        desc = desc.get_text() if desc != None else ''
        link = str(item.find(class_='none_a black')).split()[3].split('=')[1][1:-1]
  
        #title = item.find("h2", class_="title").get_text()
        #date = item.find("time").get_text().split()[0]
        #link = item.a["href"]
        data.append({
            'subject': subject,
            'form': form,
            'raiting': raiting,
            'title': title,
            'time': time,
            'desc': desc,
            'link': 'https://olimpiada.ru' + link
        })

    return data
