import arcpy
import sys
import os
import logging
import time
import traceback
from GRIDTERRAIN import get_path
import re


formatter = ('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(filename=r"{}_Log_{}.csv".format(__name__.replace(".", "_"), time.strftime("%Y_%m_%d_%H_%M")),
                                 level=logging.DEBUG, format=formatter)

arcpy.env.parallelProcessingFactor = "30%"
class LicenseError(Exception):
    pass

class StdMaker:
    def __init__(self, input_path=None, inputGDB=None, inputGDB2 = None, referenceGDB = None,
                 outputGDBname=None, outputpathfolder=None, outputfolder_name = None, outputGDB=None):
        self.inputpath = input_path
        self.inputGDB = inputGDB
        self.inputGDB2 = inputGDB2
        self.referenceGDB = referenceGDB
        self.outputGDBName = outputGDBname
        self.outputpathfolder = outputpathfolder
        self.outputfolder_name = outputfolder_name
        self.outputGDB = outputGDB


        arcpy.env.qualifiedFieldNames = False
        arcpy.env.overwriteOutput = False
        try:
            if arcpy.CheckExtension("Spatial") == "Available":
                arcpy.CheckOutExtension("Spatial")
            elif arcpy.CheckOutExtension('Spatial') == 'Unavailable':
                print("spatial Analyst tool not available")

        except LicenseError:
            print("Spatial Analyst license is unavailable")

        except arcpy.ExecuteError:
            print(arcpy.GetMessages())


    def create_folder(self):
        print("creating folder")
        logging.info("creating folder")
        try:
            if not os.path.exists(self.outputpathfolder):
                os.makedirs(self.outputpathfolder)

        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            message = "Traceback info:\n" + tbinfo
            print(message)
            logging.warning(message)

    def create_gdb(self):
        print("Creating gdb")
        logging.info("Creating GDB named: {}".format(self.outputGDBName))
        try:
            arcpy.CreateFileGDB_management(out_folder_path=self.outputpathfolder, out_name=self.outputGDBName)
            print(arcpy.GetMessages(0))
            logging.info("created GDB, messages: {}".format(arcpy.GetMessages(0)))


        except arcpy.ExecuteError:
            msgs = arcpy.GetMessages(2)
            arcpy.AddError(msgs)
            print(msgs)
            logging.info(msgs)
        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
            msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
            arcpy.AddError(pymsg)
            arcpy.AddError(msgs)
            print(pymsg)
            print(msgs)
            logging.info(pymsg)
            logging.info(msgs)

    @classmethod
    def make_grid_id(cls, input_gdb, create_field=True, make_id=True):
        print("createing Grid IDs")
        fc_list = get_path.pathFinder(env_0=input_gdb).get_path_for_all_feature_from_gdb()
        # id_fields = ["STATE_FIPS", "GRID_COL", "GRID_ROW"]

        for x in fc_list:
            print(x)
            if create_field:
                arcpy.AddField_management(x, "ID", "Text")

            codeblock = """def cont(col ,row):return "G"+str(col).zfill(4) + str(row).zfill(4)"""

            if make_id:

                arcpy.CalculateField_management(x, "ID",
                                                "cont({},{})".format("!GRID_COL!", "!GRID_ROW!"),
                                                expression_type="PYTHON3",
                                                code_block=codeblock)
                print("added id field to: {}".format(os.path.basename(x)))



    def zonal_statistics(self, wildcard, zone_field, raster_input, focal_stat=False, focal_nbr=None,
                         radius=None, ignor_data='DATA', raster_wildcard=None):

        from arcpy.sa import ZonalStatisticsAsTable, FocalStatistics

        try:


            fc_list = get_path.pathFinder(env_0=self.inputGDB).get_file_path_with_wildcard_from_gdb(wildcard=wildcard)

            focal_raster_list = get_path.pathFinder(env_0=self.outputGDB).get_file_path_with_wildcard_from_gdb(
                wildcard=raster_wildcard,
                data_type='raster')

            for fc in fc_list:
                print(os.path.basename(fc))
                if focal_stat:
                    output = os.path.join(self.outputGDB, os.path.basename(raster_input).strip(".tif") + "_{}m_Focal_Statitics_std".format(radius))
                else:
                    output = ""
                print(output)

                if arcpy.Exists(output):
                    print("{} exits, skipping".format(output))

                else:
                    if focal_stat:

                        print("Calcualting Focal Statistics for {}".format(os.path.basename(raster_input)))
                        out_focal_statistics = FocalStatistics(in_raster=raster_input,
                                                               neighborhood=focal_nbr,
                                                               statistics_type="STD",
                                                               ignore_nodata=ignor_data)
                        out_focal_statistics.save(output)
                        del out_focal_statistics
                        print(arcpy.GetMessages())
                    else:



                        for raster in focal_raster_list:

                            output = os.path.join(self.outputGDB, os.path.basename(raster)+"_zonal_statistics")
                            print(output)

                            if not arcpy.Exists(output):

                                print("Calcualting Zonal Statistics for {} ".format(os.path.basename(fc)))
                                ZonalStatisticsAsTable(in_zone_data=fc,
                                                       zone_field=zone_field,
                                                       in_value_raster=raster,
                                                       out_table=output, statistics_type="ALL")
                                print(arcpy.GetMessages())

        except arcpy.ExecuteError:
            msgs = arcpy.GetMessages(2)
            arcpy.AddError(msgs)
            print(msgs)
        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(
                sys.exc_info()[1])
            msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
            arcpy.AddError(pymsg)
            arcpy.AddError(msgs)
            print(pymsg)
            print(msgs)


    def intersect_grid_w_census_BG(self, wildcard=None):

        state_list = get_path.pathFinder.make_fips_list()
        grid_list = get_path.pathFinder(env_0=self.inputGDB).get_path_for_all_feature_from_gdb()
        Census_BG = get_path.pathFinder(env_0=self.inputGDB2).get_path_for_all_feature_from_gdb()

        territory_list = ["02","15","60","66","69", "72","78"]


        for island in territory_list:

            print(island)


            filtered_island_bg_list = get_path.pathFinder.filter_List_of_featureclass_paths_with_wildcard(Census_BG,
                                                                                                          "*_{}_bg10".format(island))
            filtered_grid_list = get_path.pathFinder.filter_List_of_featureclass_paths_with_wildcard(grid_list,
                                                                                                     "*_{}_*".format(island))


            if len(filtered_island_bg_list)==0 or len(filtered_grid_list)==0:
                print("state:{} has zero len list(s) as inputs")
                continue

            output = os.path.join(self.outputGDB,
                                  "_{}_intersected_with_BG_{}".format(os.path.basename(filtered_grid_list[0]), island))

            if not arcpy.Exists(output):

                arcpy.Intersect_analysis(filtered_island_bg_list+filtered_grid_list,output)
                print(arcpy.GetMessages())



        consus_grid = get_path.pathFinder.filter_List_of_featureclass_paths_with_wildcard(grid_list, "full_*_conus_*")

        for state in [x for x in state_list if x not in territory_list]:
            print(state)

            filtered_lower_bg = get_path.pathFinder.filter_List_of_featureclass_paths_with_wildcard(Census_BG,
                                                                                                     "*_{}_bg10".format(state))
            if len(filtered_lower_bg) != 0 and len(consus_grid) != 0:

                output = os.path.join(self.outputGDB,
                                      "_{}_intersected_with_BG_{}".format(os.path.basename(consus_grid[0]), state))

                if not arcpy.Exists(output):

                    arcpy.Intersect_analysis(consus_grid+filtered_lower_bg,output)
                    print(arcpy.GetMessages())

            else:
                print("check you queries, fc(s) not found in your in list")
                print("lower 48 list:{}\nGrid list: {}".format(filtered_lower_bg, consus_grid))
                continue

    def merge_parted_conus_tables(self, input_gdb):

        master_table_list = get_path.pathFinder(env_0=input_gdb).get_path_for_all_feature_from_gdb(type="Table",
                                                                                                   data_type="Table")

        filtered_table_list = get_path.pathFinder.filter_List_of_featureclass_paths_with_wildcard(master_table_list,
                                                                                                  wildcard="*conus*")

        output = os.path.join(self.outputGDB, "full_uniform_grid_conus_wgs84_1x1_zonal_statistics")
        if arcpy.Exists(output):
            print("the output exits, skipping!!!!!")
        else:

            if len(filtered_table_list)==0:
                print("Did not find any tables, check your wildcard")
            else:
                arcpy.Merge_management(filtered_table_list,output=output)
                print(arcpy.GetMessages())




    def add_join_table(self,in_data_gdb,in_field, join_table_gdb, join_field, fields, test=False,join_data_type=None, join_type=None,filtered_table_wildcard=None):

        state_list = get_path.pathFinder.make_fips_list()
        fc_list = get_path.pathFinder(env_0=in_data_gdb).get_path_for_all_feature_from_gdb()
        table_list = get_path.pathFinder(env_0=join_table_gdb).get_path_for_all_feature_from_gdb(
            data_type=join_data_type, type=join_data_type)



        territory_list = ["02", "15", "60", "66", "69", "72", "78"]

        for island in territory_list:

            print(island)


            filtered_island_bg_list = get_path.pathFinder.filter_List_of_featureclass_paths_with_wildcard(fc_list,
                                                                                                          "*_{}".format(island))
            filtered_table_list = get_path.pathFinder.filter_List_of_featureclass_paths_with_wildcard(table_list,
                                                                                                     "*_{}_*".format(island))

            print(filtered_island_bg_list)
            print(filtered_table_list)


            if len(filtered_table_list)==0 or len(filtered_island_bg_list)==0:
                print("One of the list has zero length, passing")
            else:
                arcpy.JoinField_management(in_data=filtered_island_bg_list[0], in_field=in_field,
                                           join_table=filtered_table_list[0],
                                           join_field=join_field, fields=fields)



        filtered_table_list=get_path.pathFinder.filter_List_of_featureclass_paths_with_wildcard(table_list,
                                                                                                "full_*_conus*")


        for state in [x for x in state_list if x not in territory_list]:
            print(state)

            if filtered_table_wildcard is True:

                filtered_table_list = get_path.pathFinder.filter_List_of_featureclass_paths_with_wildcard(table_list,
                                                                                                          "*_{}_*".format(
                                                                                                              state))

            filtered_bg_list = get_path.pathFinder.filter_List_of_featureclass_paths_with_wildcard(fc_list,
                                                                                                          "*_{}".format(
                                                                                                              state))

            if len(filtered_bg_list) == 0 or len(filtered_table_list) ==0:


                print("check you queries, fc(s) not found in your in list")
                print("lower 48 block group list:{}".format(filtered_bg_list))
                print("lower 48 Table list:{}".format(filtered_table_list))
                continue

            else:
                arcpy.JoinField_management(in_data=filtered_bg_list[0], in_field=in_field,
                                           join_table=filtered_table_list[0],
                                           join_field=join_field, fields=fields)

    def export_table(self, in_gdb, outpath,fields):
        import pandas as pd
        fc_list= get_path.pathFinder(env_0=in_gdb).get_path_for_all_feature_from_gdb()

        for fc in fc_list:
            print(fc)
            try:

                if not arcpy.Exists(os.path.join(outpath,"table_{}".format(os.path.basename(fc)))):
                    df = pd.DataFrame(arcpy.da.FeatureClassToNumPyArray(fc,fields))
                    df.to_csv(os.path.join(outpath,"table_{}.csv".format(os.path.basename(fc))))
            except:
                tb = sys.exc_info()[2]
                tbinfo = traceback.format_tb(tb)[0]
                message = "Traceback info:\n" + tbinfo
                print(message)
                print(arcpy.GetMessages())
                logging.warning(message)

    @classmethod
    def calculate_field(cls, input_gdb, field, expression):
        print("calculating field using the following expression: {}".format(expression))

        fc_list = get_path.pathFinder(env_0=input_gdb).get_path_for_all_feature_from_gdb()

        for x in fc_list:
            print(x)
            arcpy.CalculateField_management(x, field=field, expression=expression, expression_type="PYTHON3")

    @classmethod
    def addField(cls, input_gdb, fc_wildcard, field_name, field_type, field_length=None):

        fc_list = get_path.pathFinder(env_0=input_gdb).get_file_path_with_wildcard_from_gdb(fc_wildcard)

        for fc in fc_list:
            print(os.path.basename(fc))
            arcpy.AddField_management(fc, field_name, field_type, field_length=field_length)
            print(arcpy.GetMessages(0))