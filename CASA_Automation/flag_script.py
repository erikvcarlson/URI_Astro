fitsf = '42'

importuvfits(fitsfile=fitsf,vis='temp_vis.ms')

flagdata(vis='temp_vis.ms',mode='manual',spw = '8')
#flagdata(vis='temp_vis.ms',mode='manual',antenna='W72,N40')
exportuvfits(vis='temp_vis.ms/',fitsfile=fitsf + '_flagged',datacolumn='data',padwithflags=True,overwrite=True)    
os.system('rm -rfv *.ms*')





