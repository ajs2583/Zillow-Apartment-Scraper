# Zillow Clone Scraper and Web UI

This project scrapes apartment listings from a Zillow clone site and can optionally submit the address, price, and link of each listing into a Google Form. A simple Flask UI is included to easily display the scraped listings in a table for presentation purposes.

## Features

- Scrapes addresses, prices, and links from listings
- Submits each listing to a Google Form
- Web interface for viewing scraped listings
- Data is saved into a linked Google Sheet when using the auto‑filler
- Browser closes automatically when done

## Requirements

- Python 3.10 or higher
- Chrome and ChromeDriver installed for the form auto‑filler

### Python packages

Install dependencies with:

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```text
selenium
beautifulsoup4
requests
python-dotenv
Flask
```

## How to Use

1. Clone the repository
2. Update the `FORM_URL` and verify the XPaths match your Google Form if you wish to auto‑submit listings
3. Run the web interface:

```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser to view the listings.

Alternatively, run the command‑line script to automatically fill the form:

```bash
python main.py
```

The script will open a Chrome window, scrape data from the Zillow clone, and submit each entry into your form.

## Notes

- The form fields are located using fixed XPaths. If your form layout changes, update the XPaths in the script.
- Listings are currently pulled from: https://appbrewery.github.io/Zillow-Clone/

## To Do

- Add option to save listings directly into a local spreadsheet
- Add filtering for price range or keywords
- Schedule script to run automatically

## Author

Created by ajs2583
