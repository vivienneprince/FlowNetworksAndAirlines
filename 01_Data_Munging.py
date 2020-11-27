import pandas as pd
from pathlib import Path
import requests
import lxml.html as lh


# import given txt data
datpath = Path('data')

routes_info = pd.read_csv(datpath / 'routes_info.csv', header=None)  # routes info was c/p from assignment instructions
routes_info.columns = ['routes_columnid', 'description']

routes = pd.read_csv(datpath / 'routes.dat.txt', header=None)  # import routes data
routes.columns = list(routes_info[:]['routes_columnid'])

planes = pd.read_csv(datpath / 'planes.dat.txt', header=None)  # import planes data
planes.columns = ['plane_name','equipment_id','plane_abbrv']
print(planes)