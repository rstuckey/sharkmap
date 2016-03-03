# sharkmap

![Mapping Shark Attacks](http://blogofrog.com/images/sharks_map.png "Mapping Shark Attacks")

Download the [Chronological GSAF Incident Log](http://www.sharkattackfile.net/spreadsheets/GSAF5.xls) first.

```bash
pip install -r requirements.txt
python sharkmap.py
python csv2geojson.py
cp settings.py.example settings.py
# vi settings.py
python -m SimpleHTTPServer 4104
