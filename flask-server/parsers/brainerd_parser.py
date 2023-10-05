# This parser processes the PDF blotters published by the Brainerd Police Dept and Baxter Police Dept in Minnesota.

import fitz
import re
import pandas as pd
from collections import Counter
import usaddress

class BrainerdParser:
    def __init__(self):
        self.headers = None
        self.df = None
    
    def parse(self, pdf_path):
        # Function to extract bold texts from PDF
        def extract_bold_texts(pdf_path):
            doc = fitz.open(pdf_path)
            # Coordinates for the section containing bold texts
            coordinates = (50, 12, 550, 760)
            bold_texts = []
            first_font_attr = None
            header_font_attr = None
            value_font_attr = None

            regex_pattern = r"\(\d{8}\)"

            for page in doc:
                blocks = page.get_text("dict")["blocks"]
                for block in blocks:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span.get("text", "")
                            font_attributes = span.get("font", "")

                            # Check if it matches the regex pattern for headers
                            if not first_font_attr:
                                match = re.search(regex_pattern, text)
                                if match:
                                    first_font_attr = font_attributes
                                    header_font_attr = font_attributes
                                    value_font_attr = "CIDFont+F1" if first_font_attr == "CIDFont+F2" else "CIDFont+F2"

                            if font_attributes == header_font_attr or "bold" in font_attributes.lower():
                                bold_texts.append(text)
            counter = Counter(bold_texts)
            most_common_texts = counter.most_common(4)
            headers = [text for text, count in most_common_texts]
            self.headers = headers
            doc = fitz.open(pdf_path)

            pattern = re.compile(r'(\d{8})\)(.*?)(?=\(\d{8}\))', re.DOTALL)
            df = pd.DataFrame(columns=['caseno', 'info', 'case', 'Datetime'])

            text = ''

            for page in doc:
                for block in page.get_text("dict")["blocks"]:
                    for line in block.get("lines", []):
                        for span in line.get("spans", []):
                            bbox = fitz.Rect(span["bbox"])
                            if coordinates[0] <= bbox.x0 <= coordinates[2] and coordinates[1] <= bbox.y0 <= coordinates[3]:
                                text += span["text"] + "\n"

            text += '(00000000)'

            matches = re.findall(pattern, text)
            if not matches:  # No pattern matches, retrieve all texts in the PDF
                text = ''
                for page in doc:
                    text += page.get_text()
                text += '(00000000)'

                matches = re.findall(pattern, text)

            for match in matches:
                caseno = match[0]
                info = match[1].strip()
                case = ""
                if '\n' in info:
                    case = info.split('\n', 1)[0].strip()
                    info = info.split('\n', 1)[1].strip()
                #df = df.append({'caseno': caseno, 'info': info, 'case': case}, ignore_index=True)
                df = pd.concat([df, pd.DataFrame([{'caseno': caseno, 'info': info, 'case': case}])], ignore_index=True)

            new_df = pd.DataFrame(columns=headers)
            for header in headers:
                df[header] = None

            current_header = None
            for index, row in df.iterrows():
                text = row['info']
                values = [x.strip() for x in text.split('\n') if x.strip()]
                for value in values:
                    found_header = False
                    for header in headers:
                        if value.startswith(header):
                            current_header = header
                            header_value = value.replace(header, '').strip()
                            df.at[index, header] = header_value
                            found_header = True
                            break

                    if not found_header and current_header:
                        if df.at[index, current_header]:
                            df.at[index, current_header] += '\n' + value
                        else:
                            df.at[index, current_header] = value

            split_df = df['info'].str.split('\n', n=3, expand=True)
            reported_values = split_df[1].str.extract(r'(\d{2}-\d{2}-\d{4}\s+\d{4})', expand=False)
            df['Datetime'] = reported_values if reported_values.notnull().any() else split_df[0]
            df[['date', 'time']] = df['Datetime'].str.split(" ", n=1, expand=True)
            df['Desc'] = split_df[2]
            df['Desc'] = df['Desc'].replace(headers, None)

            address = headers[1]
            df[address] = df[address].astype(str)
            df[address] = df[address].str.strip().str.replace(' &,', ',')
            df[address] = df[address].str.strip().str.replace('block of', '').str.replace(',', '')

            def parse_address(row):
                address1 = row[address]
                try:
                    parsed = usaddress.tag(str(address1))[0]  # Get the first (and only) address in the tuple
                except usaddress.RepeatedLabelError:
                    parsed = {}

                city = parsed.get('PlaceName', '')
                state = parsed.get('StateName', '')
                postal_code = parsed.get('ZipCode', '')

                return pd.Series({
                  #  'address1': address2,
                    'city': city,
                    'state': state,
                    'postal_code': postal_code
                })

            # Apply the parsing function to the 'addresses' column and expand the result into separate columns
            df[['city', 'state', 'zipcode']] = df.apply(parse_address, axis=1)
            
            def extract_value(row):
                full_address = row[address]
                city = row['city']

                # Find the index of the city in the full address
                city_index = full_address.find(city)

                if city_index != -1:
                    # Extract the value before the city
                    extracted_value = full_address[:city_index].strip()

                    return extracted_value

                return None

            # Apply the function to create a new column
            df['address1'] = df.apply(extract_value, axis=1)

            df = df.applymap(lambda x: None if pd.notnull(x) and str(x).strip() == '' else x)

            

            for header in headers:
                df['Datetime'] = df['Datetime'].str.replace(header, '')
                
            popcol = ['info', 'Reported: ', headers[0],'Datetime']
            for value in popcol:
                try:
                    df.pop(value)
                except Exception:
                    pass

            
            date_regex = r'\d{2}-\d{2}-\d{4}'
            date_mask = df['date'].astype(str).str.match(date_regex)

            # Split the time column using whitespace if the date is missing
            time_mask = (~date_mask) & df['date'].notna() & df['time'].astype(str).str.contains(' ')
            df.loc[time_mask, 'date'] = df.loc[time_mask, 'time'].astype(str).str.extract(r'(\d{2}-\d{2}-\d{4})', expand=False)
            df.loc[time_mask, 'time'] = df.loc[time_mask, 'time'].astype(str).str.extract(r'\d{2}-\d{2}-\d{4}\s+(\d{4})', expand=False)

            # Remove 'Reported: ' prefix from the date column
#            df['date'] = df['date'].str.replace('Reported: ', '')

            for header in headers:
                df = df.replace(header, '', regex=True)

            df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
            df = df.replace(r'^\s*$', None, regex=True) #replacing empty cells with None 
            df = df.replace('\n', ' ', regex = True) #removing newlines from each cells

            return df

        self.df = extract_bold_texts(pdf_path)
        return self.df


