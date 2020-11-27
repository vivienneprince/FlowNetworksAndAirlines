import pandas as pd
from pathlib import Path



# import given txt data
datpath = Path('data')

routes_info = pd.read_csv(datpath / 'routes_info.csv', header=None)  # routes info was c/p from assignment instructions
routes_info.columns = ['routes_columnid', 'description']

routes = pd.read_csv(datpath / 'routes.dat.txt', header=None)  # import routes data
routes.columns = list(routes_info[:]['routes_columnid'])

planes = pd.read_csv(datpath / 'planes.dat.txt', header=None)  # import planes data
planes.columns = ['plane_name', 'equipment_id', 'plane_abbrev']

URL = 'https://blog.thetravelinsider.info/airplane-types'  # import planes info from site
planes_info = pd.read_html(URL, header=2)[0]


# clean up planes info and merge it with planes

print(planes_info)