from bin import path_links
from GRIDTERRAIN import StdMaker
import os
from arcpy import Exists

def make_grid(make=False, calculate_area=False, export=False, ten_by_ten=None, five_by_five=None, two_by_two=None, one_by_one=None):
    gridmaker = StdMaker.StdMaker()

    # ten by ten
    if ten_by_ten is True:
        gridmaker.inputGDB = path_links.tenBytenGDB
        gridmaker.inputGDB2 = path_links.census_blkG
        gridmaker.outputGDBName = "ten_by_10"
        gridmaker.outputpathfolder = r"D:\FCC_GIS_Projects\Terrian\data"
        gridmaker.outputGDB = os.path.join(gridmaker.outputpathfolder,
                                           gridmaker.outputGDBName + ".gdb")
        csv_folder = os.path.join(gridmaker.outputpathfolder, "csv")
        if not Exists(csv_folder):
            os.mkdir(csv_folder)

        if not Exists(gridmaker.outputGDB):
            gridmaker.create_gdb()
        gridmaker.intersect_grid_w_census_BG()

        if make is True:

            gridmaker.add_join_table(gridmaker.outputGDB, "ID", gridmaker.outputGDB, "ID", ["COUNTS", "STD"], True,
                                     "Table", "Table")
            gridmaker.add_join_table(gridmaker.outputGDB, "GEOID10", path_links.census_blkG, "GEOID10", ["blk_area"], True,
                                     "FeatureClass", "Polygon", filtered_table_wildcard=True)
        if calculate_area is True:
            gridmaker.addField(gridmaker.outputGDB,"*","AREA","Double")

            gridmaker.calculate_field(gridmaker.outputGDB,"AREA","!Shape.GEODESICAREA@SQUAREMETERS!")

        if export is True:
            gridmaker.export_table(gridmaker.outputGDB, csv_folder,["GEOID10","ID","blk_area","AREA","STD"])

    # 5 by 5
    if five_by_five is True:

        gridmaker.inputGDB = path_links.fiveByFiveGDB
        gridmaker.inputGDB2 = path_links.census_blkG
        gridmaker.outputGDBName = "five_by_5"
        gridmaker.outputpathfolder = r"D:\FCC_GIS_Projects\Terrian\data"
        gridmaker.outputGDB = os.path.join(gridmaker.outputpathfolder,
                                           gridmaker.outputGDBName + ".gdb")
        csv_folder = os.path.join(gridmaker.outputpathfolder, "csv")
        if not Exists(gridmaker.outputGDB):
            gridmaker.create_gdb()
        gridmaker.intersect_grid_w_census_BG()
        gridmaker.inputGDB = gridmaker.outputGDB
        if make is True:
            gridmaker.add_join_table(gridmaker.outputGDB, "ID", gridmaker.outputGDB, "ID", ["COUNTS", "STD"], True,
                                     "Table", "Table")
            gridmaker.add_join_table(gridmaker.outputGDB, "GEOID10", path_links.census_blkG, "GEOID10", ["blk_area"],
                                     True,
                                     "FeatureClass", "Polygon", filtered_table_wildcard=True)
        if calculate_area is True:
            gridmaker.addField(gridmaker.outputGDB, "*", "AREA", "Double")

            gridmaker.calculate_field(gridmaker.outputGDB, "AREA", "!Shape.GEODESICAREA@SQUAREMETERS!")

        if export is True:
            gridmaker.export_table(gridmaker.outputGDB, csv_folder, ["GEOID10", "ID", "blk_area", "AREA", "STD"])

    # two by two

    if two_by_two is True:

        gridmaker.inputGDB = path_links.twoBytwoGDB
        gridmaker.inputGDB2 = path_links.census_blkG
        gridmaker.outputGDBName = "two_by_2"
        gridmaker.outputpathfolder = r"D:\FCC_GIS_Projects\Terrian\data"
        gridmaker.outputGDB = os.path.join(gridmaker.outputpathfolder,
                                           gridmaker.outputGDBName + ".gdb")
        csv_folder = os.path.join(gridmaker.outputpathfolder, "csv")
        if not Exists(gridmaker.outputGDB):
            gridmaker.create_gdb()
        gridmaker.intersect_grid_w_census_BG()
        gridmaker.inputGDB = gridmaker.outputGDB
        if make is True:

            gridmaker.add_join_table(gridmaker.outputGDB, "ID", gridmaker.outputGDB, "ID", ["COUNTS", "STD"], True,
                                     "Table", "Table")
            gridmaker.add_join_table(gridmaker.outputGDB, "GEOID10", path_links.census_blkG, "GEOID10", ["blk_area"], True,
                                     "FeatureClass", "Polygon", filtered_table_wildcard=True)
        if calculate_area is True:
            gridmaker.addField(gridmaker.outputGDB, "*", "AREA", "Double")

            gridmaker.calculate_field(gridmaker.outputGDB, "AREA", "!Shape.GEODESICAREA@SQUAREMETERS!")

        if export is True:
            gridmaker.export_table(gridmaker.outputGDB, csv_folder,["GEOID10","ID","blk_area","AREA","STD"])

    # 1 x 1

    if one_by_one is True:


        gridmaker.inputGDB = path_links.oneByoneGDB
        gridmaker.inputGDB2 = path_links.census_blkG
        gridmaker.outputGDBName = "one_by_1"
        gridmaker.outputpathfolder = r"D:\FCC_GIS_Projects\Terrian\data"
        gridmaker.outputGDB = os.path.join(gridmaker.outputpathfolder,
                                           gridmaker.outputGDBName + ".gdb")
        csv_folder = os.path.join(gridmaker.outputpathfolder, "csv")
        if not Exists(gridmaker.outputGDB):
            gridmaker.create_gdb()

        print("intersecting the grid\n\n")
        gridmaker.intersect_grid_w_census_BG()
        gridmaker.inputGDB = gridmaker.outputGDB

        # merge the parted grid tables into one
        print("\n\n\n\nmerging tables\n\n")
        gridmaker.merge_parted_conus_tables(gridmaker.outputGDB)

        if make is True:
            print("joining the field with the table\n\n")
            gridmaker.add_join_table(gridmaker.outputGDB, "ID", gridmaker.outputGDB, "ID", ["COUNTS", "STD"], True,
                                     "Table", "Table")
            print('\b\nJoining block area with the ')
            gridmaker.add_join_table(gridmaker.outputGDB, "GEOID10", path_links.census_blkG, "GEOID10", ["blk_area"], True,
                                     "FeatureClass", "Polygon", filtered_table_wildcard=True)
        if calculate_area is True:
            gridmaker.addField(gridmaker.outputGDB, "*", "AREA", "Double")

            gridmaker.calculate_field(gridmaker.outputGDB, "AREA", "!Shape.GEODESICAREA@SQUAREMETERS!")

        if export is True:
            gridmaker.export_table(gridmaker.outputGDB, csv_folder, ["GEOID10","ID","blk_area","AREA","STD"])


if __name__=="__main__":
    make_grid(make=False,calculate_area=False,export=True, one_by_one=True)