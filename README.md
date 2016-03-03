# sharkmap

![Mapping Shark Attacks](http://blogofrog.com/images/sharks_map.png "Mapping Shark Attacks")

```bash
pip install -r requirements.txt
wget http://www.sharkattackfile.net/spreadsheets/GSAF5.xls
python sharkmap.py
python csv2geojson.py
cp settings.py.example settings.py
# vi settings.py
python -m SimpleHTTPServer 4104
