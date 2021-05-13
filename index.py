
#------------------------------------------------
#dash html components
#https://dash.plotly.com/dash-html-components
#------------------------------------------------

# Packages
import dash
import dash_html_components as html 
import dash_core_components as dcc
from dash.dependencies import Input , Output
import plotly.graph_objs as go
import pandas as pd

# Import of dataset url
url_confirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
url_deaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
url_recovered ="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"

# import datast
confirmed = pd.read_csv(url_confirmed)
deaths = pd.read_csv(url_deaths)
recovered = pd.read_csv(url_recovered)

# unpivot datasets
date1 = confirmed.columns[4:] # selection des varable que l'on veut transformer
total_confimed = confirmed.melt(id_vars=['Province/State','Country/Region','Lat','Long'],value_vars=date1,var_name='date',value_name='confirmed' )
date2 = deaths.columns[4:]
total_deaths = deaths.melt(id_vars=['Province/State','Country/Region','Lat','Long'],value_vars=date2,var_name='date',value_name='deaths' )
date3 = recovered.columns[4:]
total_recovered = recovered.melt(id_vars=['Province/State','Country/Region','Lat','Long'],value_vars=date3,var_name='date',value_name='recovered' )

# merging data
covid_data= total_confimed.merge(right=total_deaths, how='left', on=['Province/State','Country/Region','Lat','Long',	'date'] )
covid_data= covid_data.merge(right=total_recovered, how='left', on=['Province/State','Country/Region','Lat','Long',	'date'] )

# conversion de  de la date(string) en format date
covid_data['date']= pd.to_datetime(covid_data['date'])

# Remplacer les NA par 0
covid_data['recovered'] = covid_data['recovered'].fillna(0)

# New column : Création de la table des patients active du covid
covid_data['active'] = covid_data['confirmed']-(covid_data['deaths'] + covid_data['recovered'])

# Donnée de covid groupby date : uniquement en fonction des variables 'confirmed','deaths',	'recovered',et 'active'
covid_data1 = covid_data.groupby(['date'])[['confirmed','deaths',	'recovered',	'active']].sum().reset_index()

# ############################### deuxième ligne du dashboard -------------------------
#------------------------Premier objet -: cas global confirmé ---------------------
# Calcul du nombre total de cas confirmé
sum_tot_confirmed =  covid_data1['confirmed'].iloc[-1]

# Calcul des nouveaux cas confirmés en 24h
new_cas_24h = covid_data1['confirmed'].iloc[-1]-covid_data1['confirmed'].iloc[-2]
# et du pourcentage des nouveaux cas confirmés en 24 par rapport au cas total confirmé 
P_new_cas_24h = round((new_cas_24h / sum_tot_confirmed)*100,2)

#------------------------Deuxième objet -: cas global de déscès ---------------------
# Calcul du nombre total de cas confirmé
sum_tot_deaths =  covid_data1['deaths'].iloc[-1]

# Calcul des nouveaux cas confirmés en 24h
new_deaths_24h = covid_data1['deaths'].iloc[-1]-covid_data1['deaths'].iloc[-2]
# et du pourcentage des nouveaux cas confirmés en 24 par rapport au cas total confirmé 
P_new_deaths_24h = round((new_deaths_24h / sum_tot_deaths)*100,2)

#------------------------Troisème  objet -: Personnes Guérries ---------------------
# Calcul du nombre total de cas confirmé
sum_tot_recovered =  covid_data1['recovered'].iloc[-1]

# Calcul des nouveaux cas confirmés en 24h
new_recovered_24h = covid_data1['recovered'].iloc[-1]-covid_data1['recovered'].iloc[-2]
# et du pourcentage des nouveaux cas confirmés en 24 par rapport au cas total confirmé 
P_new_recovered_24h = round((new_recovered_24h / sum_tot_recovered)*100,2)

#------------------------Quatrième objet -: Personnes Porteurs(saints + malade) du virus   ---------------------
# Calcul du nombre total de porteurs
sum_tot_active =  covid_data1['active'].iloc[-1]

# Calcul des nouveaux cas confirmés en 24h
new_active_24h = covid_data1['active'].iloc[-1]-covid_data1['active'].iloc[-2]
# et du pourcentage des nouveaux cas confirmés en 24 par rapport au cas total confirmé 
P_new_active_24h = round((new_active_24h / sum_tot_active)*100,2)
# ----------------------- -------------------------


#..........................................................................
# ................ Création de l'application dashboard ....................
#..........................................................................

app = dash.Dash(__name__)

app.layout = html.Div([
                       
  #html.Div([
   # html.H2("MY first App")
 # ])
 	#====================== Première ligne du dashboard ===============
 	#=========== DEDUT =======
	html.Div([ 
		# -----------Objet 1 image ---------
		html.Div([
   			html.Img(src=app.get_asset_url('corona_logo.jpg'),
				id='corona-image',
				style={'height':'60px',
                       'width':'auto',
                       'margin-bottom':'25px'})
   		],className='one-third column'),

		# -----------Objet 2 Titre du Dashboard ---------
		html.Div([
			html.H3('Covid-19 ', style={'margin-bottom':'0px','color':'white'}),
			html.H5('Suivi des cas de covid-19',style={'margin-bottom':'0px','color':'white'})
		],className='one-half column',id='title'),

		# -----------Objet 3 Place pour afficher la dernière mise à jour ---------
		html.Div([ 
				html.H6('Dernière mis à jour : ' + str(covid_data['date'].iloc[-1].strftime('%B %d, %Y')) + '00:01 (UTC)',
					style={'color':'orange'})
		],className='one-third column',id='title1')
	#=========== FIN =======
	],id='header',className='row flex-display',style={'margin-bottom':'25px'}), 

	#====================== Deuxième ligne du dashboard ===============
	html.Div([

		# -----------Objet 1 les cas confirmé  ---------
		html.Div([
			html.H6(children='Cas global',
					style= {'textAlign':'center',
						'color':'white'}),

			# Affichage du nombre total de cas confirmé
			html.P(f"{sum_tot_confirmed:,.0f}",
					style= {'textAlign':'center',
						'color':'orange',
						'fontSize':30}),

			# Affichage des nouveaux cas apparue en 24h
			# et du pourcentage du nouveau cas confirmé en 24 par rapport au cas total confirmé 
			html.P("Nouveaux cas confirmés les dernières 24h : " + f"{new_cas_24h:,.0f},\n"+"soit "+str(P_new_cas_24h)+" %  du cas global",
					style= {'textAlign':'center',
						'color':'orange',
						'fontSize':15,
						'margin-top':'-18px'})

		],className='card_container three columns'),


		# -----------Objet 2 nombre cas déscès ---------
		html.Div([
			html.H6(children='La mortalité globale',
					style= {'textAlign':'center',
						'color':'white'}),

			# Affichage du nombre total de déscès
			html.P(f"{sum_tot_deaths:,.0f}",
					style= {'textAlign':'center',
						'color':'red',
						'fontSize':30}),

			# Affichage des nouveaux déscèsen 24h
			# et du pourcentage du nouveau cas confirmé en 24 par rapport au cas total confirmé 
			html.P("Nouveaux décès les dernières 24h : " + f"{new_deaths_24h:,.0f}"+"\n"+"soit "+str(P_new_deaths_24h)+" %  de la mortalité globale",
					style= {'textAlign':'center',
						'color':'red',
						'fontSize':15,
						'margin-top':'-18px'})

		],className='card_container three columns'),


		# -----------Objet 3 le nombre de porteurs  (recovered) ---------
		html.Div([
			html.H6(children='les personnes guéries',
					style= {'textAlign':'center',
						'color':'white'}),

			# Affichage du nombre total de cas confirmé
			html.P(f"{sum_tot_recovered:,.0f}",
					style= {'textAlign':'center',
						'color':'green',
						'fontSize':30}),

			# Affichage des nouveaux cas apparue en 24h
			# et du pourcentage du nouveau cas confirmé en 24 par rapport au cas total confirmé 
			html.P("Nouvelles personnes guéries les dernières 24h : " + f"{new_recovered_24h:,.0f},\n"+"soit "+str(P_new_recovered_24h)+" %  du nombre total guéris",
					style= {'textAlign':'center',
						'color':'green',
						'fontSize':15,
						'margin-top':'-18px'})

		],className='card_container three columns'),


# -----------Objet 4 le nombre personnes malades  (active) ---------
		html.Div([
			html.H6(children='les porteurs du virus',
					style= {'textAlign':'center',
						'color':'white'}),

			# Affichage du nombre total de cas confirmé
			html.P(f"{sum_tot_active:,.0f}",
					style= {'textAlign':'center',
						'color':'darkorchid',
						'fontSize':30}),

			# Affichage des nouveaux cas apparue en 24h
			# et du pourcentage du nouveau cas confirmé en 24 par rapport au cas total confirmé 
			html.P("Nouveaux porteurs les dernières 24h : " + f"{new_active_24h:,.0f},\n"+"soit "+str(P_new_active_24h)+" %  du nombre total des porteurs",
					style= {'textAlign':'center',
						'color':'darkorchid',
						'fontSize':15,
						'margin-top':'-18px'})

		],className='card_container three columns'),
		#=========== FIN =======
	]),

 	#====================== Troisième ligne du dashboard ===============
 	#dash html components : https://dash.plotly.com/dash-html-components
 	#=========== DEDUT =======
	html.Div([ 

#------------------ DEDUT Objet 1 ----------------------
		html.Div([

			html.P('selectionnez le pays:',className='fix_label',
											style={'color':'white',
													'fontSize':15}),
			dcc.Dropdown(id='choix_pays',
						multi= False,
						searchable=True,
						value='US',
						style={'color':'white'},
						placeholder='choix des pays',
						options=[{'label':c,'value':c} for c in (covid_data['Country/Region'].unique())],
						className='dcc_compon'),

			html.P('Nouveaux cas:'+' '+ str(covid_data['date'].iloc[-1].strftime('%B %d, %Y')),
				className='fix_label',
				style={'text-align':'center','color':'white'}),

			#............ graph 1 .............
			dcc.Graph( id='confirmed',
					config={'displayModeBar':True},
				className= 'dcc_compon',
				style={'margin-top':'20px','fontSize':10}),

			#............ graph 2 .............
			dcc.Graph( id='deaths',
					config={'displayModeBar':True},
				className= 'dcc_compon',
				style={'margin-top':'20px','fontSize':10}),

			#............ graph 3 .............
			dcc.Graph( id='recovered',
					config={'displayModeBar':True},
				className= 'dcc_compon',
				style={'margin-top':'20px','fontSize':10}),

			#............ graph 4 .............
			dcc.Graph( id='active',
					config={'displayModeBar':True},
				className= 'dcc_compon',
				style={'margin-top':'20px','fontSize':10})

		],className='create_container three columns'),
			
#------------------ DEDUT Objet 2 Pie chart ----------------------			
		html.Div([
#............ graph 5 .............
	dcc.Graph( id='pie_chart', config={'displayModeBar':'hover'})

		],className='create_container four columns'),

		#------------------ DEDUT Objet 3 Pie chart ----------------------			
		html.Div([
#............ graph 6 .............
	dcc.Graph( id='line_chart', config={'displayModeBar':'hover'})

		],className='create_container five columns')	


	],className= 'row flex-display')
	#=========== FIN Troième ligne =======
],id='mainContener',style={'display':'flex','flex-direction':'column'})
#=========== FIN =======

# """"""""" Début des callback """"""""""

#............callback graph 1 .............
@app.callback(Output('confirmed','figure'),
			  [Input('choix_pays','value')])
def update_confirmed(choix_pays):
	covid_data2= covid_data.groupby(['date', 'Country/Region'])[['confirmed','deaths',	'recovered',	'active']].sum().reset_index()
	value_confirmed = covid_data2[covid_data2['Country/Region'] == choix_pays]['confirmed'].iloc[-1] - covid_data2[covid_data2['Country/Region'] == choix_pays]['confirmed'].iloc[-2]
	delta_confirmed = covid_data2[covid_data2['Country/Region'] == choix_pays]['confirmed'].iloc[-2] - covid_data2[covid_data2['Country/Region'] == choix_pays]['confirmed'].iloc[-3]
	return{
		'data': [go.Indicator(
				mode='number+delta',
				value=value_confirmed,
				delta={'reference': delta_confirmed,
					   'position': 'right',
					   'valueformat': 'g',
					   'relative' : False,
					   'font':{'size':20}},
				number={"font":{"size":20},'valueformat':','},
				# number={'valueformat':','},
				domain={'y':[0, 1], 'x': [0, 1]}
			)],
		'layout':go.Layout(

				title={'text': 'Nouveaux cas confirmés',
						'y':1,
						'x':0.5,
						'xanchor':'center',
						'yanchor':'top'},
				font=dict(color='orange'),
				paper_bgcolor='#1f2c56',
				plot_bgcolor='#1f2c56',

				height=50,
			)

	}

#............callback graph 2 .............
@app.callback(Output('deaths','figure'),
			  [Input('choix_pays','value')])
def update_confirmed(choix_pays):
	covid_data2= covid_data.groupby(['date', 'Country/Region'])[['confirmed','deaths',	'recovered',	'active']].sum().reset_index()
	value_deaths = covid_data2[covid_data2['Country/Region'] == choix_pays]['deaths'].iloc[-1] - covid_data2[covid_data2['Country/Region'] == choix_pays]['deaths'].iloc[-2]
	delta_deaths = covid_data2[covid_data2['Country/Region'] == choix_pays]['deaths'].iloc[-2] - covid_data2[covid_data2['Country/Region'] == choix_pays]['deaths'].iloc[-3]
	return{
		'data': [go.Indicator(
				mode='number+delta',
				value = value_deaths,
				delta={'reference': delta_deaths,
					   'position': 'right',
					   'valueformat': 'g',
					   'relative' : False,
					   'font':{'size':20}},
				number={"font":{"size":20},'valueformat':','},
				#number={'valueformat':','},
				domain={'y':[0, 1], 'x': [0, 1]}
			)],
		'layout':go.Layout(

				title={'text': 'Les Nouveaux déscès',
						'y':1,
						'x':0.5,
						'xanchor':'center',
						'yanchor':'top'},
				font=dict(color='#dd1e35'),
				paper_bgcolor='#1f2c56',
				plot_bgcolor='#1f2c56',

				height=50,
			)

	}

#............callback graph 3 .............
@app.callback(Output('recovered','figure'),
			  [Input('choix_pays','value')])
def update_confirmed(choix_pays):
	covid_data2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed','deaths',	'recovered', 'active']].sum().reset_index()
	value_recovered = covid_data2[covid_data2['Country/Region'] == choix_pays]['recovered'].iloc[-1] - covid_data2[covid_data2['Country/Region'] == choix_pays]['recovered'].iloc[-2]
	delta_recovered = covid_data2[covid_data2['Country/Region'] == choix_pays]['recovered'].iloc[-2] - covid_data2[covid_data2['Country/Region'] == choix_pays]['recovered'].iloc[-3]
	return{
		'data': [go.Indicator(
				mode='number+delta',
				value=value_recovered,
				delta={'reference': delta_recovered,
					   'position': 'right',
					   'valueformat': 'g',
					   'relative' : False,
					   'font':{'size':20}},
				number={"font":{"size":20},'valueformat':','},
				#number={'valueformat':','},
				domain={'y':[0, 1], 'x': [0, 1]}
			)],
		'layout':go.Layout(
				title={'text': 'Les Nouveaux cas guéris',
						'y':1,
						'x':0.5,
						'xanchor':'center',
						'yanchor':'top'},
				font=dict(color='green'),
				paper_bgcolor='#1f2c56',
				plot_bgcolor='#1f2c56',
				height=50,
			)

	}

#............callback graph 4 .............
@app.callback(Output('active','figure'),
			  [Input('choix_pays','value')])
def update_confirmed(choix_pays):
	covid_data2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed','deaths',	'recovered', 'active']].sum().reset_index()
	value_active = covid_data2[covid_data2['Country/Region'] == choix_pays]['active'].iloc[-1] - covid_data2[covid_data2['Country/Region'] == choix_pays]['active'].iloc[-2]
	delta_active = covid_data2[covid_data2['Country/Region'] == choix_pays]['active'].iloc[-2] - covid_data2[covid_data2['Country/Region'] == choix_pays]['active'].iloc[-3]
	return{
		'data': [go.Indicator(
				mode='number+delta',
				value=value_active,
				#style={ 'fontSize':20},
				delta={'reference': delta_active,
					   'position': 'right',
					   'valueformat': 'g',
					   'relative' : False,
					   'font':{'size':20}},
				number={"font":{"size":20},'valueformat':' '},
				#number={'valueformat':','},
				domain={'y':[0, 1], 'x': [0, 1]}
			)],
		'layout':go.Layout(

				title={'text': 'Les Nouveaux porteurs',
						'y':1,
						'x':0.5,
						'xanchor':'center',
						'yanchor':'top'},
				font=dict(color='darkorchid'),
				paper_bgcolor='#1f2c56',
				plot_bgcolor='#1f2c56',

				height=50,
			)

	}
#............callback graph 5 .............

@app.callback(Output('pie_chart','figure'),
			  [Input('choix_pays','value')])
def update_graph(choix_pays):
	covid_data2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed','deaths',	'recovered', 'active']].sum().reset_index()
	confirmed_value = covid_data2[covid_data2['Country/Region'] == choix_pays]['confirmed'].iloc[-1] 
	deaths_value = covid_data2[covid_data2['Country/Region'] == choix_pays]['deaths'].iloc[-1]
	recovered_value = covid_data2[covid_data2['Country/Region'] == choix_pays]['recovered'].iloc[-1]
	active_value = covid_data2[covid_data2['Country/Region'] == choix_pays]['active'].iloc[-1] 
	colors = ['orange', '#dd1e35','green', 'darkorchid']

	return{
		'data': [go.Pie(
			labels=['Cas confirmés','Décès','Guéris','Porteurs'],
			values=[confirmed_value, deaths_value, recovered_value, active_value],
			marker=dict(colors=colors),
			hoverinfo='label+value+percent',
			textinfo='label+value',
			#hole=.7, # Pour changer la forme du cercle
			#rotation=45,
			insidetextorientation='radial'
			)],
		'layout':go.Layout(

				title={'text':  (choix_pays) + ' : condition actuelle',
						'y':1,
						'x':0.5,
						'xanchor':'center',
						'yanchor':'top'},
				titlefont={'color':'white', 'size':20},
				font=dict(family='sans-serif', 
							color = 'white',
							 size= 12),
				hovermode='closest',
				paper_bgcolor='#1f2c56',
				plot_bgcolor='#1f2c56',
				legend={'orientation':'h',
				'bgcolor':'#1f2c56','xanchor':'center','x':0.5,'y':-0.7
						}

			)

	}



#............callback graph 6 .............

@app.callback(Output('line_chart','figure'),
			  [Input('choix_pays','value')])
def update_graph(choix_pays):
	covid_data2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed','deaths',	'recovered', 'active']].sum().reset_index()
	covid_data3 = covid_data2[covid_data2['Country/Region'] == choix_pays][['Country/Region','date','confirmed']].reset_index()
	covid_data3['daily confirmed']= covid_data3['confirmed']- covid_data3['confirmed'].shift(1)
	return{
		'data': [go.Bar(
			x=covid_data3['date'].tail(30),
			y=covid_data3['daily confirmed'].tail(30),
			name='cas confirmés au quotidien',
			marker=dict(color='orange'),
			hoverinfo='text',
			hovertext='<b>Date</b>:' + covid_data3['date'].tail(30).astype(str) + '<br>' +
			'<b>cas confirmés quotidien</b>:' + [f'{x:,.0f}' for x in covid_data3['daily confirmed'].tail(30)] + '<br>' +
			 '<b>pays</b>:' + covid_data3['Country/Region'].tail(30).astype(str) + '<br>'
			 )],
		'layout': go.Layout(

				title={'text':  (choix_pays) + ' : Cas confirmés les 30 derniers jours',
						'y':1,
						'x':0.5,
						'xanchor':'center',
						'yanchor':'top'},
				titlefont={'color':'white', 'size':20},
				font=dict(family='sans-serif', 
							color = 'white',
							 size= 12),
				hovermode='closest',
				paper_bgcolor='#1f2c56',
				plot_bgcolor='#1f2c56',
				legend={'orientation':'h',
				'bgcolor':'#1f2c56','xanchor':'center','x':0.5,'y':-0.7},
				xaxis=dict(title= '<b>Date</b>',
					color='white',
					showline= True,
					showgrid= True),
				yaxis=dict(title= '<b>Cas confirmé au quotidien </b>',
					color='white',
					showline= True,
					showgrid= True)

			)

	}



if __name__ =='__main__':
  app.run_server(debug = True, use_reloader=False)
