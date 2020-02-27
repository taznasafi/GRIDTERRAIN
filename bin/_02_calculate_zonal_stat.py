try:
    # append the current working Directory
    import sys

    sys.path.append(r'D:\FCC_GIS_Projects\Terrian\GRIDTERRAIN')
    print('appended GRIDTERRAIN')
except OSError:
    print("Can't change the Current Working Directory")

from GRIDTERRAIN import StdMaker
from bin import path_links
import os
from arcpy import Exists
from arcpy.sa import NbrCircle

output_folder_data = r"D:\FCC_GIS_Projects\Terrian\focal_data"

def lower48(make=False, focal_stat=False, focal_nbr=None, ten_by_10=False, five_by_5=False, two_by_two=False,
            one_by_1=False, radius=None):
    if make:

        zonal = StdMaker.StdMaker()

        # 10 x 10
        zonal.inputGDB = path_links.tenBytenGDB
        zonal.outputGDBName = "ten_by_10"
        zonal.outputpathfolder = output_folder_data
        zonal.outputGDB = os.path.join(zonal.outputpathfolder, zonal.outputGDBName + ".gdb")
        if not Exists(zonal.outputGDB):
            zonal.create_gdb()
        if ten_by_10:
            zonal.zonal_statistics(wildcard="tl_2010_Lower48_bg10_USA_Contiguous_Albers_Equal_Area_Conic_USGS_version",
                                   zone_field="GEOID10", raster_input=path_links.conus_raster, radius=radius, ignor_data="DATA",
                                   raster_wildcard="elev48i0100a_*_std")

        # 5 x 5

        zonal.inputGDB = path_links.fiveByFiveGDB
        zonal.outputGDBName = "five_by_5"
        zonal.outputpathfolder = output_folder_data
        zonal.outputGDB = os.path.join(zonal.outputpathfolder, zonal.outputGDBName + ".gdb")
        if not Exists(zonal.outputGDB):
            zonal.create_gdb()
        if five_by_5:
            zonal.zonal_statistics(wildcard="tl_2010_Lower48_bg10_USA_Contiguous_Albers_Equal_Area_Conic_USGS_version",
                                   zone_field="GEOID10", raster_input=path_links.conus_raster, radius=radius, ignor_data="DATA",
                                   raster_wildcard="elev48i0100a_*_std")

        # 2 x 2
        zonal.inputGDB = path_links.twoBytwoGDB
        zonal.outputGDBName = "two_by_2"
        zonal.outputpathfolder = output_folder_data
        zonal.outputGDB = os.path.join(zonal.outputpathfolder, zonal.outputGDBName + ".gdb")
        if not Exists(zonal.outputGDB):
            zonal.create_gdb()
        if two_by_two:
            zonal.zonal_statistics(wildcard="tl_2010_Lower48_bg10_USA_Contiguous_Albers_Equal_Area_Conic_USGS_version",
                                   zone_field="GEOID10", raster_input=path_links.conus_raster, radius=radius, ignor_data="DATA",
                                   raster_wildcard="elev48i0100a_*_std")

        # 1 x 1
        zonal.inputGDB = path_links.census_blkG
        zonal.outputGDBName = "one_by_1"
        zonal.outputpathfolder = output_folder_data
        zonal.outputGDB = os.path.join(zonal.outputpathfolder, zonal.outputGDBName + ".gdb")
        if not Exists(zonal.outputGDB):
            zonal.create_gdb()

        if one_by_1:
            zonal.zonal_statistics(wildcard="tl_2010_Lower48_bg10_USA_Contiguous_Albers_Equal_Area_Conic_USGS_version",
                                   zone_field="GEOID10", raster_input=path_links.conus_raster,
                                   focal_stat=focal_stat, focal_nbr=focal_nbr, radius=radius, ignor_data="DATA",
                                   raster_wildcard="elev48i0100a_*_std")

        # merge the zonal statistics parts to one table


def guam(make=False, focal_stat=False, focal_nbr=None, ten_by_10=False, five_by_5=False, two_by_two=False,
         one_by_1=False, radius=None):
    if make:
        zonal = StdMaker.StdMaker()
        # 10 x 10
        zonal.inputGDB = path_links.tenBytenGDB
        zonal.outputGDBName = "ten_by_10"
        zonal.outputpathfolder = output_folder_data
        zonal.outputGDB = os.path.join(zonal.outputpathfolder, zonal.outputGDBName + ".gdb")
        if not Exists(zonal.outputGDB):
            zonal.create_gdb()
        if ten_by_10:
            zonal.zonal_statistics(wildcard="*_66_*", zone_field="GEOID10",
                                   raster_input=path_links.guam_raster, radius=radius, ignor_data="DATA",
                                   raster_wildcard="guam_*_std")

        # 5 x 5

        zonal.inputGDB = path_links.fiveByFiveGDB
        zonal.outputGDBName = "five_by_5"
        zonal.outputpathfolder = output_folder_data
        zonal.outputGDB = os.path.join(zonal.outputpathfolder, zonal.outputGDBName + ".gdb")
        if not Exists(zonal.outputGDB):
            zonal.create_gdb()
        if five_by_5:
            zonal.zonal_statistics(wildcard="*_66_*", zone_field="GEOID10",
                                   raster_input=path_links.guam_raster, radius=radius, ignor_data="DATA",
                                   raster_wildcard="guam_*_std")

        # 2 x 2
        zonal.inputGDB = path_links.twoBytwoGDB
        zonal.outputGDBName = "two_by_2"
        zonal.outputpathfolder = output_folder_data
        zonal.outputGDB = os.path.join(zonal.outputpathfolder, zonal.outputGDBName + ".gdb")
        if not Exists(zonal.outputGDB):
            zonal.create_gdb()
        if two_by_two:
            zonal.zonal_statistics(wildcard="*_66_*", zone_field="GEOID10",
                                   raster_input=path_links.guam_raster, radius=radius, ignor_data="DATA",
                                   raster_wildcard="guam*_std")

        # 1 x 1
        zonal.inputGDB = path_links.census_blkG
        zonal.outputGDBName = "one_by_1"
        zonal.outputpathfolder = output_folder_data
        zonal.outputGDB = os.path.join(zonal.outputpathfolder, zonal.outputGDBName + ".gdb")
        if not Exists(zonal.outputGDB):
            zonal.create_gdb()
        if one_by_1:
            zonal.zonal_statistics(wildcard="*_66_*", zone_field="GEOID10", raster_input=path_links.guam_raster,
                                   focal_stat=focal_stat, focal_nbr=focal_nbr, radius=radius, ignor_data="DATA",
                                   raster_wildcard="guam_*_std")


def hawaii(make=False, focal_stat=False, focal_nbr=None, ten_by_10=False, five_by_5=False, two_by_two=False,
           one_by_1=False, radius=None):
    if make:
        zonal = StdMaker.StdMaker()
        # 10 x 10
        zonal.inputGDB = path_links.tenBytenGDB
        zonal.outputGDBName = "ten_by_10"
        zonal.outputpathfolder = output_folder_data

        zonal.outputGDB = os.path.join(zonal.outputpathfolder, zonal.outputGDBName + ".gdb")
        if not Exists(zonal.outputGDB):
            zonal.create_gdb()
        if ten_by_10:
            zonal.zonal_statistics(wildcard="*_15_*", zone_field="GEOID10", raster_input=path_links.hawaii_raster, radius=radius,
                                   raster_wildcard="elevhii0100a_*_std")

        # 5 x 5

        zonal.inputGDB = path_links.fiveByFiveGDB
        zonal.outputGDBName = "five_by_5"
        zonal.outputpathfolder = output_folder_data
        zonal.outputGDB = os.path.join(zonal.outputpathfolder, zonal.outputGDBName + ".gdb")
        if not Exists(zonal.outputGDB):
            zonal.create_gdb()
        if five_by_5:
            zonal.zonal_statistics(wildcard="*_15_*", zone_field="GEOID10", raster_input=path_links.hawaii_raster, radius=radius,
                                   raster_wildcard="elevhii0100a_*_std")

        # 2 x 2
        zonal.inputGDB = path_links.twoBytwoGDB
        zonal.outputGDBName = "two_by_2"
        zonal.outputpathfolder = output_folder_data
        zonal.outputGDB = os.path.join(zonal.outputpathfolder, zonal.outputGDBName + ".gdb")
        if not Exists(zonal.outputGDB):
            zonal.create_gdb()
        if two_by_two:
            zonal.zonal_statistics(wildcard="*_15_*", zone_field="GEOID10", raster_input=path_links.hawaii_raster, radius=radius,
                                   raster_wildcard="elevhii0100a_*_std")

        # 1 x 1
        zonal.inputGDB = path_links.census_blkG
        zonal.outputGDBName = "one_by_1"
        zonal.outputpathfolder = output_folder_data
        zonal.outputGDB = os.path.join(zonal.outputpathfolder, zonal.outputGDBName + ".gdb")
        if not Exists(zonal.outputGDB):
            zonal.create_gdb()
        if one_by_1:
            zonal.zonal_statistics(wildcard="*_15_*", zone_field="GEOID10", raster_input=path_links.hawaii_raster,
                                   focal_stat=focal_stat, focal_nbr=focal_nbr, radius=radius,
                                   raster_wildcard="elevhii0100a_*_std")


def N_M_islands(make=False, focal_stat=False, focal_nbr=None, ten_by_10=False, five_by_5=False, two_by_two=False,
                one_by_1=False, radius=None):
    if make:
        zonal = StdMaker.StdMaker()
        # 10 x 10
        zonal.inputGDB = path_links.tenBytenGDB
        zonal.outputGDBName = "ten_by_10"
        zonal.outputpathfolder = output_folder_data

        zonal.outputGDB = os.path.join(zonal.outputpathfolder, zonal.outputGDBName + ".gdb")
        if not Exists(zonal.outputGDB):
            zonal.create_gdb()
        if ten_by_10:
            zonal.zonal_statistics(wildcard="*_69_*", zone_field="GEOID10", raster_input=path_links.norhter_M_island, radius=radius,
                                   raster_wildcard="elev48i0100a_*")

        # 5 x 5

        zonal.inputGDB = path_links.fiveByFiveGDB
        zonal.outputGDBName = "five_by_5"
        zonal.outputpathfolder = output_folder_data
        zonal.outputGDB = os.path.join(zonal.outputpathfolder, zonal.outputGDBName + ".gdb")
        if not Exists(zonal.outputGDB):
            zonal.create_gdb()
        if five_by_5:
            zonal.zonal_statistics(wildcard="*_69_*", zone_field="GEOID10", raster_input=path_links.norhter_M_island, radius=radius)

        # 2 x 2
        zonal.inputGDB = path_links.twoBytwoGDB
        zonal.outputGDBName = "two_by_2"
        zonal.outputpathfolder = output_folder_data
        zonal.outputGDB = os.path.join(zonal.outputpathfolder, zonal.outputGDBName + ".gdb")
        if not Exists(zonal.outputGDB):
            zonal.create_gdb()
        if two_by_two:
            zonal.zonal_statistics(wildcard="*_69_*", zone_field="GEOID10", raster_input=path_links.norhter_M_island, radius=radius)

        # 1 x 1
        zonal.inputGDB = path_links.census_blkG
        zonal.outputGDBName = "one_by_1"
        zonal.outputpathfolder = output_folder_data
        zonal.outputGDB = os.path.join(zonal.outputpathfolder, zonal.outputGDBName + ".gdb")
        if not Exists(zonal.outputGDB):
            zonal.create_gdb()
        if one_by_1:
            zonal.zonal_statistics(wildcard="*_69_*", zone_field="GEOID10", raster_input=path_links.norhter_M_island,
                                   focal_stat=focal_stat, focal_nbr=focal_nbr, radius=radius,
                                   raster_wildcard="None")


def A_samoas(make=False, focal_stat=False, focal_nbr=None, ten_by_10=False, five_by_5=False, two_by_two=False,
             one_by_1=False, radius = None):
    if make:
        zonal = StdMaker.StdMaker()

        # 10 x 10
        zonal.inputGDB = path_links.tenBytenGDB
        zonal.outputGDBName = "ten_by_10"
        zonal.outputpathfolder = output_folder_data

        zonal.outputGDB = os.path.join(zonal.outputpathfolder, zonal.outputGDBName + ".gdb")
        if not Exists(zonal.outputGDB):
            zonal.create_gdb()
        if ten_by_10:
            zonal.zonal_statistics(wildcard="*_60_*", zone_field="GEOID10", raster_input=path_links.american_sam, radius=radius)

        # 5 x 5
        zonal.inputGDB = path_links.fiveByFiveGDB
        zonal.outputGDBName = "five_by_5"
        zonal.outputpathfolder = output_folder_data

        zonal.outputGDB = os.path.join(zonal.outputpathfolder, zonal.outputGDBName + ".gdb")
        if not Exists(zonal.outputGDB):
            zonal.create_gdb()
        if five_by_5:
            zonal.zonal_statistics(wildcard="*_60_*", zone_field="GEOID10", raster_input=path_links.american_sam, radius=radius)

        # 2 x 2
        zonal.inputGDB = path_links.twoBytwoGDB
        zonal.outputGDBName = "two_by_2"
        zonal.outputpathfolder = output_folder_data
        zonal.outputGDB = os.path.join(zonal.outputpathfolder, zonal.outputGDBName + ".gdb")
        if not Exists(zonal.outputGDB):
            zonal.create_gdb()
        if two_by_two:
            zonal.zonal_statistics(wildcard="*_60_*", zone_field="GEOID10", raster_input=path_links.american_sam, radius=radius)

        # 1 x 1
        zonal.inputGDB = path_links.census_blkG
        zonal.outputGDBName = "one_by_1"
        zonal.outputpathfolder = output_folder_data
        zonal.outputGDB = os.path.join(zonal.outputpathfolder, zonal.outputGDBName + ".gdb")
        if not Exists(zonal.outputGDB):
            zonal.create_gdb()
        if one_by_1:
            zonal.zonal_statistics(wildcard="*_60_*", zone_field="GEOID10", raster_input=path_links.american_sam,
                                   focal_stat=focal_stat, focal_nbr=focal_nbr, radius=radius,
                                   raster_wildcard="None")

def Alaska(make=False, focal_stat=False, focal_nbr=None, ten_by_10=False, five_by_5=False, two_by_two=False,
             one_by_1=False, radius = None):
    if make:
        zonal = StdMaker.StdMaker()

        # 10 x 10
        zonal.inputGDB = path_links.tenBytenGDB
        zonal.outputGDBName = "ten_by_10"
        zonal.outputpathfolder = output_folder_data

        zonal.outputGDB = os.path.join(zonal.outputpathfolder, zonal.outputGDBName + ".gdb")
        if not Exists(zonal.outputGDB):
            zonal.create_gdb()
        if ten_by_10:
            zonal.zonal_statistics(wildcard="*_02_*", zone_field="GEOID10", raster_input=path_links.alaska_raster, radius=radius)

        # 5 x 5
        zonal.inputGDB = path_links.fiveByFiveGDB
        zonal.outputGDBName = "five_by_5"
        zonal.outputpathfolder = output_folder_data

        zonal.outputGDB = os.path.join(zonal.outputpathfolder, zonal.outputGDBName + ".gdb")
        if not Exists(zonal.outputGDB):
            zonal.create_gdb()
        if five_by_5:
            zonal.zonal_statistics(wildcard="*_02_*", zone_field="GEOID10", raster_input=path_links.alaska_raster, radius=radius)

        # 2 x 2
        zonal.inputGDB = path_links.twoBytwoGDB
        zonal.outputGDBName = "two_by_2"
        zonal.outputpathfolder = output_folder_data
        zonal.outputGDB = os.path.join(zonal.outputpathfolder, zonal.outputGDBName + ".gdb")
        if not Exists(zonal.outputGDB):
            zonal.create_gdb()
        if two_by_two:
            zonal.zonal_statistics(wildcard="*_02_*", zone_field="GEOID10", raster_input=path_links.alaska_raster, radius=radius)

        # 1 x 1
        zonal.inputGDB = path_links.census_blkG
        zonal.outputGDBName = "one_by_1"
        zonal.outputpathfolder = output_folder_data
        zonal.outputGDB = os.path.join(zonal.outputpathfolder, zonal.outputGDBName + ".gdb")
        if not Exists(zonal.outputGDB):
            zonal.create_gdb()
        if one_by_1:
            zonal.zonal_statistics(wildcard="*_02_*", zone_field="GEOID10", raster_input=path_links.alaska_raster,
                                   focal_stat=focal_stat, focal_nbr=focal_nbr, radius=radius,
                                   raster_wildcard="None")

if __name__ == "__main__":



    radii_list = [1000, 2500, 5000, 10000]

    #radii_list = [1000]
    for radii in radii_list:

        #Focal Statistics

        focal_nbr = NbrCircle(radius=radii, units='MAP')
        lower48(make=True, one_by_1=True, focal_stat=True, focal_nbr=focal_nbr, radius=radii)
        hawaii(make=True, one_by_1=True, focal_stat=True, focal_nbr=focal_nbr, radius=radii)
        guam(make=True, one_by_1=True, focal_stat=True, focal_nbr=focal_nbr, radius=radii)
        N_M_islands(make=False, one_by_1=True, focal_stat=True, focal_nbr=focal_nbr, radius=radii)
        A_samoas(make=False, one_by_1=True, focal_stat=True, focal_nbr=focal_nbr, radius=radii)
        Alaska(make=True, one_by_1=True, focal_stat=True, focal_nbr=focal_nbr, radius=radii)

        #Zonal statistics

        lower48(make=True, one_by_1=True, focal_stat=False, focal_nbr=focal_nbr, radius=radii)
        hawaii(make=True, one_by_1=True, focal_stat=False, focal_nbr=focal_nbr, radius=radii)
        guam(make=True, one_by_1=True, focal_stat=False, focal_nbr=focal_nbr, radius=radii)
        N_M_islands(make=False, one_by_1=True, focal_stat=False, focal_nbr=focal_nbr, radius=radii)
        A_samoas(make=False, one_by_1=True, focal_stat=False, focal_nbr=focal_nbr, radius=radii)
        Alaska(make=True, one_by_1=True, focal_stat=False, focal_nbr=focal_nbr, radius=radii)
