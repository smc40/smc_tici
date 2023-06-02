# smc_tici
SMC application tici

### What is TICI?
The objective of TICI is to address the issue of “name confusion” while approving new names for medicaments (LASA problem: look alike sound alike). 

TICI is currently deployed in the Azure Cloud and can be found in the following link:

http://tici.4punkt0.ch/ 

The proposed innitiative by the approval department was inspired on POCA, a tool developed by the FDA. This tool can be found in the following link:

https://poca-public.fda.gov/name_search

POCA cannot be used within Swissmedic because of data protection. The original tool POCA from the FDA cannot be used by Swissmedic Experts.  This is due to the fact that Swissmedic Experts cannot submit private data to external websites. This would put the secrecy of such information (for example names submitted by companies in Switzerland) at risk. This is why an alternative solution, built within swissmedic, comes across as an ideal application so that experts can submit names internally without risks. We release our development here for the community for other users to utilize, modify and locally deploy.

### How it looks

Our application looks as follows: ![image](https://github.com/smc40/smc_tici/assets/40054301/abc229f1-d0f6-4828-b49f-1b00f209b9fc)

With a search engine in the first field that allows users to search through our data and an adjustable Threshold value that can change how many results are displayed to the user. Below there are 4 options for sources of medicinal substances names that are available to search through. Additionally, there are two buttons in the bottom of the page that offer additional information to the users about the application.

### Data Sources

As shown in the application, there are four sources used within TICI: An FDA Source, and RXNorm Source, a USAN Sources and finally the Swissmedic Source. Where these sources are obtained is explained below.


### Contact

If you want to learn more about us you can find more information here:

https://4punkt0.ch/
