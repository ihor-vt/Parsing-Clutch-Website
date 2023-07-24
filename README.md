# Clutch.co Scraper using Selenium

This script allows you to scrape company information from the Clutch.co website using Selenium, which enables automated browser control and actions on web pages.

## Requirements

Before using the script, make sure you have the following dependencies installed:

- Python 3 (recommended version 3.10 or higher)
- Instaling requirements.txt

You will also need a web driver for your browser. The example uses Google Chrome for mac64, so ensure you have the web driver for Google Chrome installed and add its path to the variable url in main function.

## Usage

1. Clone the repository or download the scraper files.

2. Edit the `parse_selenium.py` file to change paramets do you want to scrapy in main function:

```python
# Example: 
    url = "https://clutch.co/it-services" # here you can insert any category that interests you
    pages = 50 # how many pages you want to scrapy
    filename_links = "company_links.json"
    filename_company = "company_data.json"
    service = Service("chromedriver_mac/chromedriver") # path to the your browser driver
```

3. Run the script from the command line:

```bash
python3 parse_selenium.py
```

4. The scraping results will be saved in 2 files:

1) company_links.json with the Clutch.co URLs of the companies.

2) company_data.json with the scraped information of the companies.

Additionally, in the terminal, you can view the time taken by functions and the script.

## Additional Settings

If you don't want the browser to be displayed during scraping, you can use the headless mode for the browser. In the `parse_selenium.py` file, uncomment the line that adds the parameter for the headless mode:

```python
# Set options for the headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Add argument for headless mode

# Launch the web driver in headless mode
driver = webdriver.Chrome(options=chrome_options)
```

## License

This script is distributed under the MIT license. For more information, see the LICENSE file.