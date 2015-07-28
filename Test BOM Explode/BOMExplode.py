import pandas as pd
from datetime import date
import pdb
bom = pd.DataFrame( {"Part Number":["C","D","E"], "Quantity":[2,10,20]}).set_index("Part Number")

dem = pd.DataFrame({"Units":[2,3], "Due Date":[date(2015,7,29), date(2015, 7, 28)]})


def explode_bom(dem, bom):
    '''
    Explodes BOM based on requirements
    '''
    exploded_req = pd.DataFrame()
    
    for row in dem.iterrows():
        exploded_bom = bom.apply(lambda x: x*row[1]["Units"])
        exploded_bom["Due Date"] = row[1]["Due Date"]
        print(exploded_bom)
        exploded_req= exploded_req.append(exploded_bom)
        
    print(exploded_req)
        
explode_bom(dem,bom)