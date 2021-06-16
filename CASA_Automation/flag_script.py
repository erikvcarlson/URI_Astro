fitsf = '2_uvfits'

importuvfits(fitsfile=fitsf,vis='temp_vis.ms')

flagdata(vis='temp_vis.ms',mode='manual',spw = '0,1,2,14,15')
#flagdata(vis='temp_vis.ms',mode='manual',antenna='W72,N40')
exportuvfits(vis='temp_vis.ms/',fitsfile=fitsf + '_flagged',datacolumn='data',padwithflags=True,overwrite=True)    
os.system('rm -rfv *.ms*')





