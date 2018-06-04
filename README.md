# BrazilianAmazonDeforestation
Acompanhamento do desmatamento e emissão de CO2 da Amazônia Legal Brasileira

In order to, clearly and intuitively, disseminate and to demonstrate the impact and extent of deforestation in the Brazilian Amazon forest, a dynamic chart was created consisting of three plots: the annual forest deforestation in each Brazilian state, the deforestation rate at each year, the rate of carbon dioxide (CO2) emissions due to deforestation and the dispersion between the values of deforestation rates and CO2 emissions. The data plotted refer to the values obtained in the years 1988 to 2017, and they were obtained through the PRODES and INPE-EM projects of the National Institute of Space Research of Brazil (INPE).

To report the Amazon deforestation, a map of Brazil was used (through the Cartopy library), highlighting the borders of the Brazilian legal Amazon, as well as the borders of the Brazilian states which the Amazon belongs. The deforestation per States is illustrated by brown circles, which the area is proportional to the deforested area. The total Amazon deforestation, in the center of the map, is indicated by purple circle. The areas of these circles are updated each year as the deforestation progresses, in addition to the circles, the deforested area values are reported in km² for each State and for the Legal Amazon.

Futhermore in map of Brazil, two bar graphs are plotted to the right. In yellow it is shown the emission rate of CO2, and, in red, it is shown the deforestation. Both values are always corresponding to the analyzed year .

In the line chart located to the right-top, the values of annual rates of deforestation (in red) and CO2 emission (in yellow) are plotted, then the direct relationship between the two rates can be visualized. It is clear that increasing deforestation rate generates an increase in CO2 emissions.

Located to the right-bottom, a scatter plot can be visualized correlating these two variables.

Below the graphs, there is a menu formed by buttons named with the years in which was processed the data, by clicking on one of these buttons, the program will plot all the deforestation and emissions information for that year. There are also another two buttons, 'play' and 'pause'. If the user would like to see the graphs in an animated and in an automatic way, he would be able to click on 'play' then the graphs update every 500ms going through every year. And clicking 'pause' to end this animation.

In addition to the objective of alerting everyone about the Amazon deforestation problem, which certainly deserves our attention, to surveillance and to claiming the authorities solutions, the project aims to demonstrate that a research can be done cheaply and relatively quickly when we use an open source tools such as Python, and when data, from other research, are available to the community. In this case, data obtained from the INPE website for free. Certainly, Open Data, Open Source and collaborative initiatives accelerate worldwide scientific development, as well as the dissemination of knowledge.
