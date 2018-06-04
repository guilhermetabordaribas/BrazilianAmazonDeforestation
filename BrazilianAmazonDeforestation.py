"""
Copyright (c) 2018 Guilherme Taborda Ribas.

Copyright (c) 2012-2013 Matplotlib Development Team; All Rights Reserved.

Copyright (c) 2015-02-18 Cartopy. Met Office. git@github.com:SciTools/cartopy.git. 7b2242e.

Copyright (c) 2007, (Shapely) Sean C. Gillies All rights reserved. 

Copyright (c) 2017 NumPy developers.

Copyright (c) 2008-2012, (Pandas) AQR Capital Management, LLC, Lambda Foundry, Inc. and PyData Development Team All rights reserved.

Copyright (c) 2016 Riverbank Computing Limited.

Copyright (c) 2017 The Qt Company.


This file is part of BrazilianAmazonDeforestation.

    BrazilianAmazonDeforestation is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or any later version.

    BrazilianAmazonDeforestation is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with BrazilianAmazonDeforestation.  If not, see <http://www.gnu.org/licenses/>.


USED DATA:

Brazilian Legal Amazon '.shp' file: http://mapas.mma.gov.br/i3geo/datadownload.htm
For general Map '.shp' file: https://github.com/nvkelso/natural-earth-vector/tree/master/zips
Deforestation and CO2 Emission: http://www.dpi.inpe.br/Ambdata/unidades_administrativas.php

"""


import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import shapely.geometry as sgeom

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.axes_grid1.inset_locator import (inset_axes, InsetPosition, mark_inset)

import pandas as pd
import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets


class Gera_graficoPyqt5Amazonia():
    def __init__(self):        
        self.patches = []
        self.amAnnotade = []
        self.primeiroClick = 0
        self.play = False
        self.countPlay = 0

    def setupUi(self, Form):
        font10 = QtGui.QFont()
        font10.setPointSize(10)
        
        Form.setObjectName("Form")
        Form.resize(1250, 750)
        
        self.verticalLayoutForm = QtWidgets.QVBoxLayout(Form)        
        self.tabWidget = QtWidgets.QTabWidget(Form)

        ##TabGraphs
        self.tabGraph = QtWidgets.QWidget()
        self.gridLayoutGraph = QtWidgets.QGridLayout(self.tabGraph)
        
        self.scrollArea = QtWidgets.QScrollArea(self.tabGraph)
        self.scrollArea.setWidgetResizable(False)
        
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
##        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1200, 650))
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1320, 800))
        
        self.gridLayoutGraphScrollArea = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayoutGraph.addWidget(self.scrollArea, 1, 0, 1, 1)
        
        self.tabWidget.addTab(self.tabGraph, "Deforestation and CO2 Emission Charts")   

    ######
    ##INFO    
    ######
        font = QtGui.QFont()
        font.setPointSize(7)
        self.pushButtonInfo = QtWidgets.QPushButton(self.tabGraph)
        self.pushButtonInfo.setFont(font)
        self.pushButtonInfo.hide()
        self.pushButtonInfo.setText('INFO (mouse over):')        
        self.pushButtonInfo.setToolTip("""<html><head/><body><p><span><strong><u>The graphs are arranged as follows::</u></strong>
<ul>
    <li>
        A chart with the map of the Brazilian legal Amazon: 
        In this graph it's possible to follow the total deforestation in each state and the total deforestation of the Brazilian Amazon between 1988 and 2017.
        And also the rate of deforestation and CO2 emissions in each year.
    </li>
    <br>
    <li>
        A red line plot showing the evolution of the annual deforestation rate and a yellow line showing the evolution of the carbon dioxide emission rate due to deforestation.

    </li>
    <br>
    <li>
        A scatter diagram with the x-axis the deforestation rate and the y-axis CO2 emission rate.
    </li>
</ul>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The data were obtained from the website of the National Institute of Space Research of Brazil (INPE) for projects PRODES and INPE-EM</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The coordinates and '.shp' files for the Brazilian Legal Amazon were obtained from the website of the Ministry of the Environment in:
http://mapas.mma.gov.br/i3geo/datadownload.htm (date: 23/05/2018)</p>
</span></p></body></html>""")

        self.gridLayoutGraphScrollArea.addWidget(self.pushButtonInfo, 0, 0, 1, 5)
    ##########
    ##GRÁFICOS
    ##########
##        self.figure  = matplotlib.pyplot.figure()
##        self.canvas = matplotlib.backends.backend_qt5agg.FigureCanvasQTAgg(self.figure)
        self.figure  = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.gridLayoutGraphScrollArea.addWidget(self.canvas, 1, 0, 1, 30)        

    #############
    ##BOTÕES ANOS
    #############
        self.btn_grp = QtWidgets.QButtonGroup(self.tabGraph)
        self.btn_grp.setExclusive(True)
        
        self.pushButtonAnos = [QtWidgets.QPushButton(self.tabGraph) for i in range(2017-1988+1)]
        for i in range(2017-1988+1):
            self.gridLayoutGraphScrollArea.addWidget(self.pushButtonAnos[i], 2, i, 1, 1)
            self.pushButtonAnos[i].setText(str(1988+i))            
            self.pushButtonAnos[i].setFont(font)
            self.btn_grp.addButton(self.pushButtonAnos[i])

        self.gridLayoutGraphScrollArea.setSpacing(0)        
        

    ########################
    ##BOTÕES PLAY/PAUSE/STOP
    ########################        
        self.pushButtonPlay = QtWidgets.QPushButton(self.tabGraph)
        self.pushButtonPlay.setText('Play')
        self.gridLayoutGraphScrollArea.addWidget(self.pushButtonPlay, 3, 13, 1, 3)

        self.pushButtonPause = QtWidgets.QPushButton(self.tabGraph)
        self.pushButtonPause.setText('Pause')
        self.gridLayoutGraphScrollArea.addWidget(self.pushButtonPause, 3, 16, 1, 2)

        
        self.timer = QtCore.QTimer(self.tabGraph)

        ##
        self.verticalLayoutForm.addWidget(self.tabWidget)
    ##FUNÇÕES
        
        self.graficoBase()
        
        self.btn_grp.buttonClicked.connect(self.onClickButton)              
        self.pushButtonPlay.clicked.connect(self.onClickPlay)
        self.pushButtonPause.clicked.connect(self.onClickPause)
        self.timer.timeout.connect(self.onClickPlay)
        

    def onClickButton(self, btn):
        idBtn = self.btn_grp.id(btn)
        self.graficosAnos(-2-idBtn)
        self.primeiroClick = 1

    def onClickPlay(self):
        if self.countPlay > 29:
            self.countPlay = 0
            self.graficosAnos(self.countPlay)
            
        self.timer.start(250)        
        self.graficosAnos(self.countPlay)

        self.countPlay+=1
        self.primeiroClick = 1

    def onClickPause(self):
        self.timer.stop()
        
    def getDatas(self):
        arqDes = 'prodes_rates_15_4_2018_1526392490073.csv'
        frame = pd.read_csv(arqDes, header=0)        
        
        arqEm = 'inpe_EM_BRAmz_resultados1960-2016.csv'
        emissoesDF = pd.read_csv(arqEm, header=0)
        emissoesDF = emissoesDF[['Year', 'net_CO2_2ndOrder']].iloc[28:,:].reset_index(drop=True)
        
        coordDF = pd.DataFrame({'AC_Coord':[(-69.08,-9.82)],
                                'AM_Coord':[(-63.42,-4.56)],
                                'AP_Coord':[(-51.71,1.61)],
                                'MA_Coord':[(-45.26,-4.68)],
                                'MT_Coord':[(-56.11,-12.73)],
                                'PA_Coord':[(-52.68,-4.51)],
                                'RO_Coord':[(-62.91,-10.45)],
                                'RR_Coord':[(-61.37,2.)],
                                'TO_Coord':[(-48.23,-10.39)],
                                'AMZ_Coord':[(-58.21,-7.)],

                                'AC_CoordArea':[(-72.92, -14.83)],
                                'AM_CoordArea':[(-73.3, 2.75)],
                                'AP_CoordArea':[(-43.7, 0.)],
                                'MA_CoordArea':[(-41.9, -8.9)],
                                'MT_CoordArea':[(-55.35, -21.42)],
                                'PA_CoordArea':[(-56.9, 5.)],
                                'RO_CoordArea':[(-69.3, -21.2)],
                                'RR_CoordArea':[(-65.7, 5.)],
                                'TO_CoordArea':[(-47.6, -16.7)],
                                'AMZ_CoordArea':[(-63.21,-30.)],
                                })

        
        frame[frame.columns.values[1:]]=frame[frame.columns.values[1:]].astype(float)

        taxaDesDF = frame[['AMZ']]
        
        frame[frame.columns.values[1:]] = frame[frame.columns.values[1:]].cumsum()

        DesmAcum = (frame.copy()/1000).round(2)
        
        ##Estipolou-se que um circulo de r = 12.5 cobriria toda a área amazônica.
        ##Logo: 100km² correspondem a um círculo de r = 0.55... R = 0.55*Area/100
        fct = np.sqrt(156.25/5088200)
        
        frame[frame.columns.values[1:]] = np.sqrt(frame[frame.columns.values[1:]])*fct


        return taxaDesDF, frame, coordDF, emissoesDF, DesmAcum

    def sample_data(self):
        
        lons = [-55, -62, -71.6, -64.2, -61.5, -52.5, -51.5, -48.5, -46.5]
        lats = [-12, -10, -9, -4.5, 2.5, -4.3, 2.1, -10, -5]
        return lons, lats

    def graficoBase(self):
        self.taxaDes, self.amazonRaio, self.amazonCoord, self.amazonEmiss, self.DesmAcum = self.getDatas()
        self.ax = self.figure.add_subplot(2, 3, (1,5), projection=ccrs.PlateCarree())
 
        self.anoText = self.ax.text(-38, 5.7, "", size=20,
         ha="center", va="center", color="white",
         bbox=dict(boxstyle="round",
                   ec='white',
                   fc=(0.59375 , 0.71484375, 0.8828125)
                   )
                                    )


        ##Gráfico de Desmatamento
        self.axDes = plt.axes([0,0,1,1], facecolor=[ 0.59375 , 0.71484375, 0.8828125 ])        
        width = 1/1.5 
        self.axDes.bar(['Desma'], .2, align='center',
            color=['red'], ecolor='black', alpha=.5)
        self.axDes.set_xticks([])
        self.axDes.set_yticks([])
        self.axDes.spines['bottom'].set_color('white')
        self.axDes.spines['top'].set_color('white')
        self.axDes.spines['right'].set_color('white')
        self.axDes.spines['left'].set_color('white')
        ip = InsetPosition(self.ax, [0.85,.05,.05,.85])
        self.axDes.set_axes_locator(ip)

        ##Gráfico de Emissão CO2
        self.axEmiss = plt.axes([1,1,1,1], facecolor=[ 0.59375 , 0.71484375, 0.8828125 ])
        width = 1/1.5
        self.axEmiss.bar(['Emissao'], .2, align='center',
                    color=['yellow'], ecolor='black', alpha=.8)
        self.axEmiss.set_xticks([])
        self.axEmiss.set_yticks([])
        self.axEmiss.tick_params(axis='y', labelsize=6)
        self.axEmiss.yaxis.tick_left()        
        self.axEmiss.spines['bottom'].set_color('white')
        self.axEmiss.spines['top'].set_color('white')
        self.axEmiss.spines['right'].set_color('white')
        self.axEmiss.spines['left'].set_color('white')
        ip = InsetPosition(self.ax, [0.80,.05,.05,.85])
        self.axEmiss.set_axes_locator(ip)

        ##Gráfico Linhas
        self.axLinhas = self.figure.add_subplot(2, 3, 3)
        self.axLinhas.axis('off')
        
        self.axLinhasEmiss = self.axLinhas.twinx()
        self.axLinhasEmiss.axis('off')

        self.axScatter = self.figure.add_subplot(2, 3, 6)
        self.axScatter.axis('off')

        ##Mapa Brasil e Amazônia Legal
        self.ax.set_title('The Brazilian Legal Amazon Deforestation Map', fontsize=11, color='#595959')
        self.ax.outline_patch.set_edgecolor('#d9d9d9')
        self.ax.set_extent([-74, -20, 7.7, -35.5], crs=ccrs.PlateCarree())
        self.ax.add_feature(cfeature.LAND)
        self.ax.add_feature(cfeature.OCEAN)
        self.ax.add_feature(cfeature.COASTLINE)
        self.ax.add_feature(cfeature.BORDERS, linestyle='-')
        self.ax.add_feature(cfeature.LAKES)
        self.ax.add_feature(cfeature.RIVERS)    

        lons, lats = self.sample_data()        
        track = sgeom.LineString(list(zip(lons, lats)))
        states_shp = 'CoordStates/50m_admin_1_states_provinces_lakes_shp.shp'
        for state in shpreader.Reader(states_shp).geometries():
            facecolor = 'none'
            edgecolor = 'none'
            if state.intersects(track):
                edgecolor = 'gray'
            self.ax.add_geometries([state], ccrs.PlateCarree(),
                          facecolor=facecolor, edgecolor=edgecolor,
                              alpha = .3)
            
        amazon_shp = 'CoordAmazon/amazlegal.shp'
        for state in shpreader.Reader(amazon_shp).geometries():
            facecolor = 'none'
            edgecolor = 'none'
            if state.intersects(track):
                facecolor = 'green'
                edgecolor = 'olive'
            self.ax.add_geometries([state], ccrs.PlateCarree(),
                          facecolor=facecolor, edgecolor=edgecolor,
                              alpha = .3)




        text1 = """The graphs are arranged as follows:

- A chart with the map of the Brazilian legal Amazon:
  In this graph it's possible to follow the total deforestation in each state
  and the total deforestation of the Brazilian Amazon between 1988 and 2017.
  And also the rate of deforestation and CO2 emissions in each year.\n"""
        
        text2 = """
- A red line plot showing the evolution of the annual deforestation rate and
  a yellow line showing the evolution of the carbon dioxide emission rate due
  to deforestation.\n"""

        text3 = """
- A scatter diagram with the x-axis the deforestation rate and the y-axis CO2
  emission rate.\n"""

        text4 = """
  Please, press play or any year button below!
"""

        text = text1+text2+text3+text4
        self.descricaoText = self.figure.text(.4, .4, text, size='medium',#stretch="ultra-condensed",
                                          ha="left", va="baseline", color="#595959",
                                          bbox=dict(boxstyle="round",
                                                    ec='#d9d9d9',
                                                    fc='white'#(0.59375 , 0.71484375, 0.8828125)
                                                    )
                                          )
        

        
    def graficosAnos(self, indexYear):        
        
        if self.primeiroClick == 0:
            self.pushButtonInfo.show()
            for estado in (self.amazonRaio.columns.values)[1:]:
                facecolor='brown'
                if estado == 'AMZ':
                    facecolor = 'purple'
                self.patches.append(mpatches.Circle(xy=self.amazonCoord[estado+'_Coord'][0], radius=self.amazonRaio[estado][indexYear],
                                            facecolor=facecolor,
                                            alpha=1.0,
                                           transform=ccrs.PlateCarree()))
                ##Anotações de área desmatada
                annText = ''
                self.amAnnotade.append(self.ax.annotate(annText, self.amazonCoord[estado+'_Coord'][0],
                                                   self.amazonCoord[estado+'_CoordArea'][0], color="white",fontsize=10,
                                                        bbox=dict(boxstyle="round", fc='#595959', ec='white'),
                                                   arrowprops=dict(arrowstyle="->", color='white'),
                                                   ))

            for ptc in self.patches:
                self.ax.add_patch(ptc)

           

            ##Gráfico de Desmatamento
            self.axLinhas.set_title('Evolution of Deforestation and CO2 Emission Rates', fontsize=10, color='#595959')
            self.axLinhas.plot(self.amazonRaio['year'].values, self.taxaDes['AMZ'].values, 'r-^', alpha=.5)
            self.axLinhas.axis('on')
            self.axLinhas.set_xticks(self.amazonRaio['year'].values)
            self.axLinhas.tick_params(axis='x', labelsize=7, rotation=90, colors='gray')
            self.axLinhas.tick_params(axis='y', labelsize=7, colors='r')
            self.axLinhas.spines['bottom'].set_color('#b3b3b3')
            self.axLinhas.spines['top'].set_color('#b3b3b3')
            self.axLinhas.spines['right'].set_color('#b3b3b3')
            self.axLinhas.spines['left'].set_color('#b3b3b3')

            ##Gráfico de Emissão de CO2
            self.axLinhasEmiss.plot(self.amazonRaio['year'].values, self.amazonEmiss['net_CO2_2ndOrder'].values, 'y-o', alpha=.5)
            self.axLinhasEmiss.axis('on')
            self.axLinhasEmiss.tick_params(axis='y', labelsize=7, colors='y')
            self.axLinhasEmiss.spines['bottom'].set_color('#b3b3b3')
            self.axLinhasEmiss.spines['top'].set_color('#b3b3b3')
            self.axLinhasEmiss.spines['right'].set_color('#b3b3b3')
            self.axLinhasEmiss.spines['left'].set_color('#b3b3b3')

            self.rectEmissDesm = mpatches.Rectangle((self.amazonRaio['year'][indexYear]-.5, 250), 1, 1200, facecolor="black", alpha=0.1)
            self.axLinhasEmiss.add_patch(self.rectEmissDesm)

            ##Gráfico Scatter            
            self.axScatter.set_title('Deforestation vs CO2 Emission Rates', fontsize=10, color = '#595959')
            self.axScatter.axis('on')
            self.axScatter.tick_params(axis='x', labelsize=7, colors='r')
            self.axScatter.tick_params(axis='y', labelsize=7, colors='y')
            self.axScatter.spines['bottom'].set_color('#b3b3b3')
            self.axScatter.spines['top'].set_color('#b3b3b3')
            self.axScatter.spines['right'].set_color('#b3b3b3')
            self.axScatter.spines['left'].set_color('#b3b3b3')
            self.axScatter.scatter(self.taxaDes['AMZ'].values, self.amazonEmiss['net_CO2_2ndOrder'].values, color='#096BB2')

            ##Legenda do Mapa
            emissLeg = mpatches.Rectangle((0, 0), 1, 1, facecolor="yellow")
            desmatLeg = mpatches.Rectangle((0, 0), 1, 1, facecolor="red", alpha=.7)
            desEstadoLeg = mpatches.Rectangle((0, 0), 1, 1, facecolor="brown")
            desTotalLeg = mpatches.Rectangle((0, 0), 1, 1, facecolor="purple")
            
            labels = ['Deforestation by state',
                      'Amazon deforestation',
                      'Annual CO2 Emission Rate (Mton)',
                      'Annual Deforestation Rate (km²)'
                      ]
            
            self.ax.legend([desEstadoLeg, desTotalLeg, emissLeg, desmatLeg],
                           labels, loc='upper left',bbox_to_anchor=(0., -.09, 1., .102),
                           fancybox=True, fontsize='small', ncol=2,
                           framealpha=.85, mode='expand')

        ##Alterações após primeira chamada da função
        ##Clear
        self.axDes.clear()
        self.axEmiss.clear()
        self.descricaoText.set_visible(False)
        #######

        ##Altera os raios do desmatamento
        i = 0
        for estado in (self.amazonRaio.columns.values)[1:]:
            self.patches[i].set_radius(radius=self.amazonRaio[estado][indexYear])
            if estado == 'AMZ':
                annText = 'Legal Amazon'+':\n'+str(self.DesmAcum[estado][indexYear]) + r'$x10^{3}km^{2}$'
            else:
                annText = estado+':\n'+str(self.DesmAcum[estado][indexYear]) + r'$x10^{3}km^{2}$'
            self.amAnnotade[i].set_text(annText)
            i+=1            

        ##Altera Ano
        self.anoText.set_text('Year: '+str(1988+indexYear))
        ##Altera retângulo das linhas
        self.rectEmissDesm.set_x(self.amazonRaio['year'][indexYear]-.5)        
        
        
        ####
        ##Gráfico de Desmatamento
        width = 1/1.5

        barsAMZ = [self.taxaDes['AMZ'][indexYear]]
        self.axDes.bar(['Desma'], barsAMZ, align='center',
            color=['red'], ecolor='black', alpha=.7)
        for des in self.taxaDes['AMZ']:
            self.axDes.axhline(des, color='gray', linewidth=0.5)
        self.axDes.set_xticks([])
        self.axDes.tick_params(axis='y', labelsize=7, colors='white')
        self.axDes.yaxis.tick_right()

        ##Gráfico de Emissão CO2
        width = 1/1.5

        barsAMZ = [self.amazonEmiss['net_CO2_2ndOrder'][indexYear]]
        self.axEmiss.bar(['Emissao'], barsAMZ, align='center',
                    color=['yellow'], ecolor='black', alpha=.7)
        for emi in self.amazonEmiss['net_CO2_2ndOrder']:
            self.axEmiss.axhline(emi, color='gray', linewidth=0.5)
        self.axEmiss.set_xticks([])
        self.axEmiss.tick_params(axis='y', labelsize=7, colors='white')
        self.axEmiss.yaxis.tick_left()

        if self.primeiroClick == 0: 
            self.figure.tight_layout()
        self.canvas.draw()

##########################
##########################
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Gera_graficoPyqt5Amazonia()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
