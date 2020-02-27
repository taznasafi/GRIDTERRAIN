import wget
from GRIDTERRAIN import get_path
import os
fips_list = get_path.pathFinder.make_fips_list()


for fips in fips_list:
    try:
        if not os.path.exists(os.path.join(r"C:\Users\Murtaza.Nasafi\Downloads\tl_2010_tabblock00", "tl_2010_{}_tabblock00.zip".format(fips))):

            print(fips)
            wget.download("https://www2.census.gov/geo/tiger/TIGER2010/TABBLOCK/2000/tl_2010_{}_tabblock00.zip".format(fips),
                          r"C:\Users\Murtaza.Nasafi\Downloads\tl_2010_tabblock00")
    except:
        print("did not find that state or error occured")

