# Ransomware_Compromission
A python script that retrieves the latest victims of ransomware groups available on the [Ransomwatch Project](https://github.com/joshhighet/ransomwatch), and export it on CSV and Excel format with :
* The victims of the incident
* Ransomware operators behind the incidents
* The Date of the claim by the operators 
* The URLs of the victims

## Requirements

This script requires the installation of 4 libraries for its proper functioning:
* pandas which was used to convert the raw JSON file in a Dataframe, much easier to manipulate.
* google which was used for the creation of URLs.
* beautifulsoup4 which was necessary for the proper functioning of the google library
* openpyxl which was necessary for the exportation in Excel Format

for installing the libraries you can type the command:
```
pip install -r requirements.txt
```

## To-Do-List
- [X] Adding the country of the victims
- [X] Export the files in an ZIP archive
- [X] Adding of an option for the user to choose the number of days difference  

## Credits
* Josh Highet for his Ransomwatch Project
* Mario Vilas for his google library

