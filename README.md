# Zillow Clone Scraper and Form Auto-Filler

This Python script scrapes apartment listings from a Zillow clone site and automatically submits the address, price, and link of each listing into a Google Form. The responses are stored in a connected Google Spreadsheet for easy tracking.

## Features

- Scrapes addresses, prices, and links from listings
- Submits each listing to a Google Form
- Data is saved into a linked Google Sheet
- Browser closes automatically when done

## Requirements

- Python 3.10 or higher
- Chrome and ChromeDriver installed

### Python packages

Install dependencies with:

```
pip install -r requirements.txt
```

**requirements.txt:**
```
selenium
beautifulsoup4
requests
python-dotenv
```

## How to Use

1. Clone the repository
2. Update the `FORM_URL` and verify the XPaths match your Google Form
3. Run the script:

```
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
