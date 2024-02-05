# https://www.udemy.com/api-2.0/search-courses/?src=ukw&q=PYTHON&skip_price=true

import requests
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0',
    'Referer': 'https://www.udemy.com/courses/search/?src=ukw&q=PYTHON'
}

c = 0
cursos_final = []

for i in range(1, 4):
  # usamor la url que obtuvimos de inspeccionar las peticiones de udemy
  url_api = "https://www.udemy.com/api-2.0/search-courses/?src=ukw&q=PYTHON&skip_price=true&p=" + str(i)

  response = requests.get(url_api, headers=headers)

  data = response.json()

  cursos = data["courses"]
  
  for curso in cursos:
    print(c)
    print(curso["title"])
    print(curso["num_reviews"])
    print(curso["rating"])
    print()
    cursos_final.append({
      'titulo': curso["title"],
      'num_reviews': curso["num_reviews"],
      'rating': curso["rating"]
    })
    c+=1

df = pd.DataFrame(cursos_final)

print(df)

df.to_csv('cursos_udemy.csv')