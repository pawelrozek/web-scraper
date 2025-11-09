# web-scraper
This is a python application that allows for scraping web.
You may need to modify a little bit to make it work for you.

## pre-requisites
- Chrome Driver
- python3
- python3-pip
- selenium
- pandas
- requests
- beautifulsoup4
- duckduckgo-search
- openpyxl
- requests
- urllib3
- chardet
- python3-tk

## running application
In order to execute this application, you can either run ``python3 ai_scraper_backend.py`` which will open the application in terminal, or by running ``python3 ai_scraper_gui.py`` which will open the GUI application which uses the backend application and displays the output in GUI.
The application will create output to an Excel file in new directories called ``ai_scraper_output`` and it will generate screenshots of all the pages it opens and put them in ``ai_scraper_output\screenshots\`` directory.