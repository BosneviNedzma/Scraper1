import requests
from bs4 import BeautifulSoup
import csv
import time

base_url = 'https://eshop.tropic.ba/?product-page='
current_page=1

with open('tropic.csv', "w", encoding='utf-8') as textfile:
    writer = csv.writer(textfile)
    writer.writerow(["Rb.", "Artikl", "Cijena"])
    
    count_items = 0
    total_items_req = base_url + str(current_page)
    tropic_req = requests.get(total_items_req)
    tropic_req_soup = BeautifulSoup(tropic_req.text, 'html.parser')
    tropic_req_soup.prettify()
    
    content = tropic_req_soup.findAll('p', {'class': 'woocommerce-result-count'})
    total_items = int(content[0].text.split(" ")[3])
    
while current_page < (total_items/36):
    print("==========================================================================")
    print("Upisano: " + str(current_page * 36))
    
    url = base_url + str(current_page)
    tropic_r = requests.get(url)
    tropic_soup = BeautifulSoup(tropic_r.text, 'html.parser')
    tropic_soup.prettify()
    
    all_content = tropic_soup.findAll('a', {'class': 'woocommerce-LoopProduct-link woocommerce-loop-product__link'})
    try:
        with open('tropic.csv', "a", encoding='utf-8') as textfile:
            writer = csv.writer(textfile)
            for link in all_content:
                name = link.findAll('h2', {'class': 'woocommerce-loop-product__title'})
                price = link.findAll('span', {'class': 'woocommerce-Price-amount amount'})
                if price:
                    writer.writerow([count_items+1, name[0].text, price[0].text])
                    print(name[0].text + " " + price[0].text)
                count_items += 1
            current_page += 1
            #time.sleep(3)
    except Exception as e:
        print(e)
        
    
    
    