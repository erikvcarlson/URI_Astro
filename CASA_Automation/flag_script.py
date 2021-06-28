fitsf = '2_uvfits'

importuvfits(fitsfile=fitsf,vis='temp_vis.ms')

flagdata(vis='temp_vis.ms',mode='manual',spw = '13')
#flagdata(vis='temp_vis.ms',mode='manual',antenna='E16,W64')
exportuvfits(vis='temp_vis.ms/',fitsfile=fitsf + '_flagged',datacolumn='data',padwithflags=True,overwrite=True)    
os.system('rm -rfv *.ms*')





