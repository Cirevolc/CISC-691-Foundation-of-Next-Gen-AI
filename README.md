CISC0691 Foundation of Next Gen AI: A02

## Steps to run the improved author identification

1. Install the requirement using the [requirements.txt](requirements.txt)
2. You can use `pip install -r requirements.txt`
3. Download spacy required files using `python -m spacy download en_core_web_sm`
3. Run the code `python improved_authorship_identification.py` to predict authors
4. You can run individual codes by using `python authorship_identifier_firstname.py`
5. If you want to predict for a new unknown authors add text to [ch7](./A02-A-Simple-Authorship-Identification-System/ch7/) as `unknown5.txt`
6. This will help you predict for new unknown author
7. Note the system can only predict if author's text has been shown to system in [known_authors](./A02-A-Simple-Authorship-Identification-System/ch7/known_authors)