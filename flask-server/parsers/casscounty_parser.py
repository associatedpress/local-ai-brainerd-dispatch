# This parser processes the PDF blotters published by the Cass County Sheriffs Dept in Minnesota.

#!/usr/bin/env python
# coding: utf-8

# In[1]:


from collections import Counter,defaultdict
import fitz  # PyMuPDF
import tabula
import pandas as pd
import numpy as np
import re
import usaddress
import os
from typing import Optional
import datetime


# In[2]:


class CassParser:
    def __init__(self):
        self.headers = None
        self.df = None
    
    def parse(self, pdf_path):
        def extract_df_from_pdf(filepath):
            def visualize_pdf_with_bboxes(filepath, page_num):
                pdf_document = fitz.open(filepath)
                page = pdf_document.load_page(page_num)

                bbox_texts = []
                for block in page.get_text('dict')['blocks']:
                    if 'lines' in block:
                        for line in block['lines']:
                            for span in line['spans']:
                                x0, y0, x1, y1 = span['bbox']  # Corrected the bbox access
                                font_specification = span['font']
                                text = span['text']
                                bbox_texts.append((x0, y0, x1, y1, text, font_specification))

                pdf_document.close()
                return bbox_texts

            def find_most_common_x0(bbox_coordinates):
                x0_values = [bbox[0] for bbox in bbox_coordinates]
                counter = Counter(x0_values)
                most_common_x0_counts = counter.most_common()
                return most_common_x0_counts

            pdf_document = fitz.open(filepath)

            # Create an empty list to store DataFrames for each page
            dfs_per_page = []

            for page_num in range(pdf_document.page_count):
            #    print(f"Visualizing page {page_num + 1}...")
                bbox_coordinates = visualize_pdf_with_bboxes(filepath, page_num)

                most_common_x0_counts = find_most_common_x0(bbox_coordinates)

                # Filter the most common x0 coordinates with a count greater than 10
                most_common_x0_filtered = [(x0, count) for x0, count in most_common_x0_counts if count > 1]

                # Create a nested defaultdict to group texts for each x0 and y1 coordinate
                x0_y1_texts_dict = defaultdict(lambda: defaultdict(list))

                for x0, count in most_common_x0_filtered:
                    for bbox in bbox_coordinates:
                        if bbox[0] == x0:
                            x0_y1_texts_dict[bbox[3]][f'x0_{x0}'].append(bbox[4])

                # Convert the nested defaultdict to a list of dictionaries
                rows = []
                for y1, x0_texts_dict in x0_y1_texts_dict.items():
                    row = {'y1': y1}
                    row.update(x0_texts_dict)
                    rows.append(row)

                # Create the DataFrame for the current page
                df = pd.DataFrame(rows)

                # Append the DataFrame to the list
                dfs_per_page.append(df)
                for i, df in enumerate(dfs_per_page):
                    dfs_per_page[i] = df.applymap(lambda x: x.strip('[]') if isinstance(x, str) else x)

            pdf_document.close()

            # Combine DataFrames for all pages into a single DataFrame
            combined_df = pd.concat(dfs_per_page, ignore_index=True)

            def remove_unwanted_chars(cell):
                if isinstance(cell, list):
                    cell_str = str(cell)
                    cell_str = cell_str.replace('[', '').replace(']', '').replace('\'', '').replace(',', '').replace('+', '').replace('-', '').strip()
                    return ' '.join(cell_str.split())
                return cell

            combined_df = combined_df.applymap(remove_unwanted_chars)


            combined_df = combined_df.drop(columns = ['y1'])


            #combined_df.columns = combined_df.iloc[0]
            new_columns = combined_df.iloc[0].astype(str).tolist()
#            print(new_columns)
            combined_df.columns = new_columns

            if 'nan' in new_columns:
                # Get the index of 'nan' in the list
                nan_index = new_columns.index('nan')

                # Drop the associated column from the DataFrame
                combined_df = combined_df.drop(columns=combined_df.columns[nan_index])

                # Remove 'nan' from the new_columns list
                new_columns.pop(nan_index)

            # Set the header
            combined_df.columns = new_columns

            header = combined_df.columns
            combined_df = combined_df[~combined_df.apply(lambda row: row == header, axis=1).any(axis=1)]

            combined_df = combined_df.dropna(how='all')

            combined_df.reset_index(drop=True, inplace=True)


            # Your previous code here
            if combined_df.shape[1] == 4:
                combined_df.columns = ['date', 'case', 'address1', 'city']
            elif combined_df.shape[1] == 5:
                combined_df.columns = ['date', 'caseno', 'case', 'address1', 'city']


            pattern = r'(?P<Latitude>-?\d+\.\d+)(?:\s+(?P<Longitude>-?\d+\.\d+))?'
            coordinates = combined_df['address1'].str.extract(pattern)

            # Convert coordinates to numeric, while ignoring errors
            latitudes = pd.to_numeric(coordinates['Latitude'], errors='coerce')
            longitudes = pd.to_numeric(coordinates['Longitude'], errors='coerce')

            # Update lat and long columns based on extracted values
            combined_df['lat'] = latitudes
            combined_df['long'] = longitudes

            # Update 'Addresses Involved' column by removing the extracted coordinates
            combined_df['address1'] = combined_df['address1'].str.replace(pattern, '').str.strip()

            combined_df = combined_df.dropna(how='all')

            def parse_address(row):
                address1 = row['city']
                try:
                    parsed = usaddress.tag(str(address1))[0]  # Get the first (and only) address in the tuple
                except usaddress.RepeatedLabelError:
                    parsed = {}
                city = parsed.get('PlaceName', '')
                state = parsed.get('StateName', '')
                postal_code = parsed.get('ZipCode', '')

                if city is None or city == '':
                    city = address1

                return pd.Series({
                    'city': city,
                    'state': state,
                    'postal_code': postal_code
                })


                # Apply the parsing function to the 'addresses' column and expand the result into separate columns
            combined_df[['city', 'state', 'zipcode']] = combined_df.apply(parse_address, axis=1)
            combined_df['time'] = combined_df['date'].str.split(n=1).str[1]
            combined_df['date'] = combined_df['date'].str.split(n=1).str[0]# Split and get the second element
            
            def convert_date(date_str):
                try:
                    dt = datetime.datetime.strptime(date_str, '%m/%d/%y')
                    return dt.strftime('%m-%d-%Y')  # Format as 'mm-dd-yyyy'
                except ValueError:
                    return date_str

            # Apply the function to the date column
            combined_df['date'] = combined_df['date'].apply(convert_date)

            columns_to_check = ['caseno', 'Officers Involved', 'Names Involved', 'Desc', 'Addresses Involved']
            
            
            for col in columns_to_check:
                if col not in combined_df.columns:
                    combined_df[col] = None
                    
#            combined_df['Addresses Involved'] == combined_df['address1']
            
            combined_df = combined_df.astype(object).replace({pd.NA: None})
            combined_df.replace('', None, inplace=True)
            return combined_df
        self.df = extract_df_from_pdf(pdf_path)
        return self.df



