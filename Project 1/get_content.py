import asyncio
import os
from pyppeteer import launch
from bs4 import BeautifulSoup

current_location = os.path.dirname(os.path.abspath(__file__))

async def main(url=None):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)
    await asyncio.sleep(2)
    content = await page.content()
    await browser.close()   
    return content

def get_dynamic_content(url):
    extracted_data = []
    page_count = 1

    while url:
        flag = True
        print("Getting data from page", page_count)
        while flag:
            try:
                content = asyncio.get_event_loop().run_until_complete(main(url))
                flag = False
            except:
                print("Connection issue. Retrying...")

        page_count += 1
        formatted_html = BeautifulSoup(content, 'html.parser')
        
        reviews = formatted_html.find_all('div', class_='a-section celwidget')
        
        for review in reviews:
            review_text = review.find(class_='review-text').get_text(strip=True)
            date = review.find('span', class_='a-size-base a-color-secondary review-date').get_text(strip=True)
            rating = review.find('span', class_='a-icon-alt').get_text(strip=True)
            person_name = review.find('span', class_='a-profile-name').get_text(strip=True)
            
            data = {
                'Review Text': review_text,
                'Date': date,
                'Rating': rating,
                'Person Name': person_name
            }
            
            extracted_data.append(data)
        print("Got",len(extracted_data),"reviews.")
        next_page_element = formatted_html.find(class_='a-last')
        try:
            next_page_url = next_page_element.find('a')['href']
            url = f"https://www.amazon.com{next_page_url}"
        except:
            url = None
    print("completed Reading all comments..")
    return extracted_data

url = "https://www.amazon.com/Samsung-Galaxy-S22-5G-Unlocked/product-reviews/B09VD33WHW/"
content = get_dynamic_content(url)

# Write the extracted data to a CSV file
import csv

fields = ['Review Text', 'Date', 'Rating', 'Person Name']

with open('result.csv', 'w', encoding="utf-8", newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    for review_data in content:
        writer.writerow(review_data)
