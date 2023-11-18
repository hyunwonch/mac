import requests
from bs4 import BeautifulSoup

def crawl_google_scholar(query):
    # base_url = "https://scholar.google.com/scholar"
    # params = {"q": query}

    base_url = "https://scholar.google.co.kr/scholar?hl=ko&as_sdt=0%2C5&q=david+blaauw&btnG="
    # Send an HTTP GET request to Google Scholar
    response = requests.get(base_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # print(soup)
        # Extract information based on the HTML structure
        # Modify this part according to the structure of the Google Scholar page
        results = soup.find_all('h3', {'class': 'gs_rt'})

        # Print the titles of the search results
        for result in results:
            title = result.get_text()
            print(title)

    else:
        print(f"Error: Unable to fetch the page. Status code: {response.status_code}")

# Example usage
query = "david blaauw"
crawl_google_scholar(query)
