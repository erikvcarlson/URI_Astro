import os
from multiprocessing import Pool

directory=os.getcwd()
file_list = os.listdir(directory)


def split_files(fitsf):
    importuvfits(fitsfile=fitsf,vis=fitsf + 'temp_vis.ms')

    try: 
        split(vis=fitsf+'temp_vis.ms/',spw = '1000~2000MHz',outputvis=fitsf+'temp_vis_L.ms/',datacolumn='data')
        exportuvfits(vis=fitsf+'temp_vis_L.ms/',fitsfile=fitsf + '_L',datacolumn='data',padwithflags=True,overwrite=True)
    except:
        pass
    try: 
        split(vis=fitsf+'temp_vis.ms/',spw = '2000~4000MHz',outputvis=fitsf+'temp_vis_S.ms/',datacolumn='data')
        exportuvfits(vis=fitsf+'temp_vis_S.ms/',fitsfile=fitsf + '_S',datacolumn='data',padwithflags=True,overwrite=True)
    except:
        pass
    try: 
        split(vis=fitsf+'temp_vis.ms/',spw = '4000~8000MHz',outputvis=fitsf+'temp_vis_C.ms/',datacolumn='data')
        exportuvfits(vis='temp_vis_C.ms/',fitsfile=fitsf + '_C',datacolumn='data',padwithflags=True,overwrite=True)
    except:
        pass
    try: 
        split(vis=fitsf+'temp_vis.ms/',spw = '8000~12000MHz',outputvis=fitsf+'temp_vis_X.ms/',datacolumn='data')
        exportuvfits(vis=fitsf+'temp_vis_X.ms/',fitsfile=fitsf + '_X',datacolumn='data',padwithflags=True,overwrite=True)
    except:
        pass
    try: 
        split(vis=fitsf+'temp_vis.ms/',spw = '12000~18000MHz',outputvis=fitsf+'temp_vis_U.ms/',datacolumn='data')
        exportuvfits(vis=fitsf+'temp_vis_U.ms/',fitsfile=fitsf + '_U',datacolumn='data',padwithflags=True,overwrite=True)
    except:
        pass    
    try: 
        split(vis=fitsf+'temp_vis.ms/',spw = '18000~26500MHz',outputvis=fitsf+'temp_vis_K.ms/',datacolumn='data')
        exportuvfits(vis=fitsf+'temp_vis_K.ms/',fitsfile=fitsf + '_K',datacolumn='data',padwithflags=True,overwrite=True)    
    except:
        pass


if __name__ == '__main__':
    pool = multiprocessing.Pool()
    pool.map(split_files,file_list)
    os.system('rm -rfv *.ms')



