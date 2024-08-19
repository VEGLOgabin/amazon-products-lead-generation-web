# Product_Name
# Price
# Product_Rating
# Number_of_Reviews
# Product_Description
# Brand
# Product_URL



from playwright.sync_api import sync_playwright
import streamlit as st
import time
import pandas as pd
from io import BytesIO
import plotly.express as px
from datetime import datetime

URL = "https://www.amazon.com"

def amazon_products_lead_generation(product_name):
    data_scraped = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        # Open a new page in incognito mode
        page = context.new_page()
        # page = browser.new_page()
        page.goto(URL)
        
        time.sleep(2)
            
        
        page.wait_for_selector('input#twotabsearchtextbox', timeout=10000)
        page.locator("input#twotabsearchtextbox").fill(product_name)
        page.locator("input#nav-search-submit-button").click()
        
        time.sleep(10)
        up = True
        product_hrefs = []
        while up:
            time.sleep(10)
            
            page.wait_for_selector('a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal', timeout=10000)
            
            if page.locator("a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal").count() > 0:
                product_list = page.locator("a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal").all()
                for product in product_list:
                    href  = URL + product.get_attribute("href")
                    product_hrefs.append(href)
                    
            try:      
                    
                if page.locator("a.s-pagination-next").count() > 0:
                    page.locator("a.s-pagination-next").click()
                
                else:
                    up=False
                    print("No more pages available.")
                    
            except Exception   as e:
                print(f"An error occurred: {e}")
                
            # up= False # It is for testing phase
                
            
                
                
        if len(product_hrefs) > 0:
            print(len(product_hrefs))

            for item in product_hrefs:
                page.goto(item)
                time.sleep(3)      
                Product_URL = page.url
                print("----------------------------------------------------------------------------------------------------------------------------")
                print(Product_URL)
                
                if page.locator("h1#title").count() > 0:
                    Product_Name = page.locator("h1#title").inner_text().strip()
                    print("----------------------------------------------------------------------------------------------------------------------------")
                    print(Product_Name)
                    
                else:
                    Product_Name = "N/A"
                    
                
        
                if page.locator("#acrCustomerReviewLink").count() > 0:
                    # Handling multiple matches by choosing the first or appropriate one
                    Number_of_Reviews = page.locator("#acrCustomerReviewLink").first.inner_text().strip()
                    print("----------------------------------------------------------------------------------------------------------------------------")
                    print(f'Number_of_Reviews : {Number_of_Reviews.split("ratings")[0]}')
                    
                else:
                    Number_of_Reviews = "N/A"
                
                if page.locator("a.a-popover-trigger.a-declarative").count() > 0:
                    Product_Rating = page.locator("span.a-size-base.a-color-base").first.inner_text().strip()
                    # class="a-size-base a-color-base"
                    print("----------------------------------------------------------------------------------------------------------------------------")
                    print(f'Product_Rating : {Product_Rating}')
                    
                else:
                    Product_Rating = "N/A"
                    
                if page.locator('span.a-size-base.po-break-word').count() > 0:
                    Brand = page.locator('span.a-size-base.po-break-word').first.inner_text().strip()
                    print("----------------------------------------------------------------------------------------------------------------------------")
                    # class="a-size-base po-break-word"
                    print(f'Brand : {Brand}')
                    
                else:
                    Brand = "N/A"
                    
                if page.locator('ul.a-unordered-list.a-vertical.a-spacing-mini').count() > 0:
                    Product_Description = page.locator('ul.a-unordered-list.a-vertical.a-spacing-mini').first.inner_text().strip()
                    print("----------------------------------------------------------------------------------------------------------------------------")
                    print(f'Product_Description : {Product_Description}')
                    
                else:
                    Product_Description = "N/A"
                    
                if page.locator('div.a-section.a-spacing-medium').count() > 0:
                    Product_Note = page.locator('div.a-section.a-spacing-medium').first.inner_text().strip()
                    print("----------------------------------------------------------------------------------------------------------------------------")
                    print(f'Product_Note : {Product_Note}')
                else:
                    Product_Note = "N/A"
                    
                if page.get_by_test_id("price-whole").count() > 0:
                    Price = page.get_by_test_id("price-whole").first.inner_text().strip()
                    print("----------------------------------------------------------------------------------------------------------------------------")
                    print(f'Price : {Price}')
                    # data-testid="price-whole"
                    
                else:
                    Price = None
                
                    
                
                # Add your scraped data to the list
                data_scraped.append([Product_Name, Price, Product_Description, Number_of_Reviews, Product_Rating, Brand, Product_URL])
                print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                time.sleep(5)
                    
        time.sleep(5)
        page.close()
        browser.close()
        
    return data_scraped
    
if __name__ == "__main__":
    

    
    HEADERS = ["PRODUCT NAME", "PRICE", "PRODUCT DESCRIPTION", "NUMBER OF REVIEWS", "PRODUCT RATING", "BRAND", "PRODUCT URL"]
    
    st.title("Welcome to AMAZON Productss Lead Lead Generation web app")
    
    product_name = st.text_input("# Product name", "e.g: smartphone")
    
    
    if product_name  == "e.g: smartphone":
        product_name = "smartphone"
    
    data_scraped = []
    
    df = pd.DataFrame(data=data_scraped, columns=HEADERS)
    
        
    # Downloaded data filtered as csv files
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        if st.button(f'Scrape all {product_name}  available from amazon.com'):
            with st.spinner("Load ..."):
                try:
                    data_scraped = amazon_products_lead_generation(product_name)
                except Exception as e:
                    st.error(f"An error occurred during scraping: {e}")
                    
            st.info(f'{len(data_scraped)} items scraped from amazon.com')
            st.success("Data scraped successfully")          
    with col2:
        
        if len(data_scraped)!=0:
            
            df = pd.DataFrame(data = data_scraped, columns = HEADERS)
        
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download the dataset as CSV",
                data=csv,
                file_name=f'{product_name}-{datetime.now()}.csv',
                mime='text/csv'
            )
            
        else:
            pass
            
    with col3:
        
        if len(data_scraped)!=0:
            
            df = pd.DataFrame(data = data_scraped, columns = HEADERS)
            
            # Create an Excel file in memory
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer, index=False)
            writer.close()
            xlsx_data = output.getvalue()
            
            
            # xlsx = df.to_excel(index=False).encode('utf-8')
            # Provide the download button
            st.download_button(
                label="Download the dataset as xlsx",
                data=xlsx_data,
                file_name=f'{product_name}-{datetime.now()}.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
        else:
            pass
        

    if not df.empty:
        view_df_as_table = st.checkbox("View the dataset as a table", key="one")
        
        if view_df_as_table:
            st.table(df)
    else:
        pass
        
   
    
    
    
    
    
    
    