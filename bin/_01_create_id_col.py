from GRIDTERRAIN import StdMaker
from bin import path_links


idmaker = StdMaker.StdMaker()

#create grid id for 10x10
idmaker.make_grid_id(input_gdb=path_links.tenBytenGDB,
                     create_field=False, make_id=False)

#create grid id for 5x5
idmaker.make_grid_id(input_gdb=path_links.fiveByFiveGDB,
                     create_field=False, make_id=False)

#create grid id for 2x2
idmaker.make_grid_id(input_gdb=path_links.twoBytwoGDB,
                     create_field=False, make_id=False)

#create grid id for 1x1
idmaker.make_grid_id(input_gdb=path_links.oneByoneGDB,
                     create_field=True, make_id=True)




