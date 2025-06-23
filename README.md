# Zillow Scraper and Web UI

This project scrapes apartment listings directly from Zillow and optionally submits the address, price and listing link into a Google Form. A Flask based web UI is provided to display the scraped listings in a table.

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

Visit `http://127.0.0.1:5000` in your browser and click **View Listings** to fetch the latest results.

Alternatively, run the command‑line script to automatically fill the form:

```bash
python main.py
```

The script will open a Chrome window, scrape data from Zillow, and submit each entry into your form.

## Notes

- The form fields are located using fixed XPaths. If your form layout changes, update the XPaths in the script.
- Listings are pulled directly from Zillow search results.

## To Do

- Add option to save listings directly into a local spreadsheet
- Add filtering for price range or keywords
- Schedule script to run automatically

## Author

Created by ajs2583
