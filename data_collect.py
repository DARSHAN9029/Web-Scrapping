from bs4 import BeautifulSoup
import os
import pandas as pd

d = {'Title': [], 'Ratings': [], 'Original_Price': [], 'Discounted_Price': [], 'Link': []}
data_folder = "data"

for filename in os.listdir(data_folder):
    try:
        print(f"Processing: {filename}")
        
        file_path = os.path.join(data_folder, filename)
        with open(file_path, encoding="utf-8") as f:
            html_doc = f.read()

        soup = BeautifulSoup(html_doc, 'html.parser')

        t = soup.find("h3")
        title = t.get_text(strip=True) if t else "NA"

        # Extract link (default: "NA" if missing)
        l = soup.find("a", href=True)
        link = "https://bigbasket.in" + l["href"] if l else "NA"

        r = soup.find("span", attrs={"class": 'Label-sc-15v1nk5-0 Badges___StyledLabel-sc-1k3p1ug-0 gJxZPQ kAyiFy leading-xxs'})
        ratings = r.get_text(strip=True) if r else "NA"

        # Extract original price (default: "NA" if missing)
        op = soup.find("span", attrs={"class": 'Label-sc-15v1nk5-0 Pricing___StyledLabel2-sc-pldi2d-2 gJxZPQ hsCgvu'})
        og_price = op.get_text(strip=True) if op else "NA"

        # Extract discounted price (default: "NA" if missing)
        dp = soup.find("span", attrs={"class": 'Label-sc-15v1nk5-0 Pricing___StyledLabel-sc-pldi2d-1 gJxZPQ AypOi'})
        ds_price = dp.get_text(strip=True) if dp else "NA"

        # Append data to dictionary
        d['Title'].append(title)
        d['Ratings'].append(ratings)
        d['Original_Price'].append(og_price)
        d['Discounted_Price'].append(ds_price)
        d['Link'].append(link)

    except Exception as e:
        print(f"\n Error processing file: {filename}")
        print(f"{e}")
        print("Continuing to the next file.\n")

# Convert to DataFrame and save to CSV
df = pd.DataFrame(data=d)
df.to_csv("data.csv", index=False)
print("Data extraction completed. CSV saved.")
