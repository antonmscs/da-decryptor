# For simplicity this code doesn't catch individual exceptions, it's just fool-proof with generic except
import requests
from bs4 import BeautifulSoup

# URL of the DA Google Doc
# Encrypted Letter "F"
#URL = "https://docs.google.com/document/d/1H1633rA4E5K7O28vT1sbeEtcD07i7iC2d78emxyxOwQ/pub"

# Encrypted Message "EICWDKO"
URL = "https://docs.google.com/document/d/1K3hXvgnJE25-p8jcv2BuczevTg0sdoEUfnsA9LUMZzk/pub"

LAST_TABLE_HEADER = "y-coordinate"
BLANK_CHAR = " "

def ingest_content(url):
    # Send a GET request to the URL
    try:
        response = requests.get(url)
    except Exception as e:
        print(f"ingest_content: requests.get: An unexpected error occurred: {e}")
        return []

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the text from the document within paragraph tags <p>
        text = soup.find_all('p')
        
        # Return content as a list
        return [p.get_text() for p in text]
    else:
        print(f"Failed to retrieve document. Status code: {response.status_code}")
        return []   

# Add a character c to the matrix with coordinates (x,y)
def add_character(y_list, x, y, c):
    # Add blank lists if needed for a currently proceesed coordinate Y
    i = len(y_list)
    while i <= y:
        y_list.append([])  
        i += 1
        
    # Add blank characters if needed for a currently proceesed coordinate X for the list with coordinate Y
    x_list = y_list[y]
    i = len(x_list)
    while i <= x:
        x_list.append(BLANK_CHAR)
        i += 1
    x_list[x] = c

# Takes in one argument, which is a string containing the URL for the Google Doc with the input data
# Prints the grid of characters specified by the input data, displaying a graphic of correctly oriented uppercase letters.
def process_url(url):
    data = ingest_content(url)
    # If there is an isssue with ingesing data stop here
    if len(data) == 0:
        return
    
    matrix = []
    # Data we care about starts after 'y-coordinate'
    i = data.index(LAST_TABLE_HEADER) + 1
    # We don't want to calculate len each iteration of the loop
    length = len(data)
    # We know there are triplets - x-coordinate, Character, y-coordinate, so we retrieve them together
    while i + 3 <= length:
        # We assume the document if properly formatted and the type casting will be safe
        try:
            add_character(matrix, int(data[i]), int(data[i+2]), data[i+1])                
        except Exception as e:
             print(f"process_url: add_character: An unexpected error occurred: {e}")
             return
        i += 3
        
    for row in reversed(matrix):
        for char in row:
            print(char, end="") 
        print("")    
    
def main():
    process_url(URL)        
     
if __name__ == "__main__":
  main()