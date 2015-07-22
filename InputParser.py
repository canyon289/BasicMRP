'''
Takes Dataframe and bins dates into datetime index
'''

import pandas as pd
a = Cell("a1").table
d = pd.DataFrame(a, columns = a.pop(0))
d.set_index("Receipt Date", inplace = True)
d = d.to_period("W-SUN")