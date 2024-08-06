# TICI

### What is TICI?
The objective of TICI is to address the issue of “name confusion” while approving new names for medicaments (LASA problem: look alike sound alike). 

TICI is currently deployed in the Azure Cloud and can be found in the following link:

http://tici.4punkt0.ch/ 

The proposed innitiative by the Sector market authorization was inspired on POCA, a tool developed by the FDA. This tool can be found in the following link:

https://poca-public.fda.gov/name_search

Swissmedic cannot use the FDA's POCA tool due to data protection issues, as experts cannot submit private data to external websites. To avoid compromising sensitive information, an internal alternative has been developed. This solution allows experts to submit names securely within Swissmedic.

### How it looks

Our application looks as follows: ![image](https://github.com/smc40/smc_tici/assets/40054301/abc229f1-d0f6-4828-b49f-1b00f209b9fc)

The first field features a search engine to explore our data, with an adjustable Threshold value to control the number of displayed results. Users can search through four sources of medicinal substance names.

### How to deploy locally (debian based linux)
Prerequisites: `git`, `python3.9`

1. Clone repository: `git clone https://github.com/smc40/smc_tici.git `
2. Change working directory: `cd smc_tici`
3. Create a virtual environment: `python3.9 -m venv venv`
4. Activate virtual environment: `source venv/bin/activate`
5. Install requirements: `pip install -r req_freeze.txt`
6. Run flask app: `python -m flask run` 

### Data Sources

There are four sources used within TICI: 
- **FDA**: https://www.fda.gov/drugs/drug-approvals-and-databases/drugsfda-data-files
- **RXNorm**: https://www.nlm.nih.gov/research/umls/rxnorm/index.html
- **USAN**: (404: page not found)
- **Swissmedic**: https://www.swissmedic.ch/swissmedic/de/home/services/listen_neu.html

### Contact

If you want to learn more about us you can find more information here:

https://swissmedic.4punkt0.ch/
