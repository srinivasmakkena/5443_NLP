import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
import csv

# Defining the main asynchronous function to fetch the page content
async def main(url=None):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)
    await asyncio.sleep(2)
    content = await page.content()
    await browser.close()   
    return content

# Function to get dynamic content from Amazon product review pages
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
            except Exception as ex:
                print("Connection issue. Retrying...",ex.__str__)

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

# URL of the Amazon product review page
url1 = "https://www.amazon.com/SAMSUNG-Smartphone-Unlocked-Android-Titanium/product-reviews/B0CMDNKZ92/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews" # correct URL
url2 = "https://www.amazon.com/Apple-iPhone-15-Pro-Titanium/product-reviews/B0CMZ8ZBVN/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews" # correct URL
# url = "https://www.amazon.com/Samsung-Galaxy-S22-5G-Unlocked/dp/B09VD33WHW/"  #Wrong URL
try:
    content1 = get_dynamic_content(url1)
    content2 = get_dynamic_content(url2)
    # Write the extracted data to a CSV file
    fields = ['Review Text', 'Date', 'Rating', 'Person Name']

    with open('result1.csv', 'w', encoding="utf-8", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for review_data in content1:
            writer.writerow(review_data)
    with open('result2.csv', 'w', encoding="utf-8", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for review_data in content2:
            writer.writerow(review_data)

except:
    print("Something is wrong with the url's. Please provide correct product review page url's in below format.\n https://www.amazon.com/product_name/product-reviews/Product_id/")
