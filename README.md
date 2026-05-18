# Engeto Python Academy – Project 3  
Election Results Scraper

## Project Description
This project extracts election results from the 2017 Czech parliamentary elections.

The script downloads data from the official website:
https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ

It processes all municipalities in a selected district and saves the results into a CSV file.

---

## Installation of Libraries
All required libraries are listed in the file **requirements.txt**.

It is recommended to use a virtual environment.  
To install the dependencies, run:

```bash
pip3 --version
pip3 install -r requirements.txt
```


---

## How to Run the Project
The script **election-scraper.py** requires **two mandatory arguments**:

1. URL of the district page (ps32)
2. Name of the output CSV file

### Example:

```bash
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=5&xnumnuts=4103" results_sokolov.csv
```
---

## Example Output
During the download, the terminal displays progress:
```
Processing: Březová
Processing: Bublava
Processing: Bukovany
Processing: Citice...
```

The resulting CSV file contains columns such as:


```
code;location;registered;envelopes;valid;Občanská demokratická strana;Řád národa - Vlastenecká unie;Česká str.sociálně demokrat.;STAROSTOVÉ A NEZÁVISLÍ;Komunistická str.Čech a Moravy;Strana zelených;ROZUMNÍ-stop migraci,diktát.EU;Strana svobodných občanů;Blok proti islam.-Obran.domova;Občanská demokratická aliance;Česká pirátská strana;Referendum o Evropské unii;TOP 09;ANO 2011;SPR-Republ.str.Čsl. M.Sládka;Křesť.demokr.unie-Čs.str.lid.;REALISTÉ;SPORTOVCI;Dělnic.str.sociální spravedl.;Svob.a př.dem.-T.Okamura (SPD);Strana Práv Občanů
560294;Březová;2263;1206;1192;112;20;93;42;108;17;10;7;1;0;106;0;27;457;3;13;8;7;6;151;4
560308;Bublava;337;198;195;19;0;13;10;13;2;1;5;0;0;22;0;9;64;0;4;1;1;3;28;0
```

The output may vary depending on the selected district.

