fitsf = 'J0824+5552_A_S_PE2_16B-306'
fitsf1 = '5_uvfits'

importuvfits(fitsfile=fitsf,vis='temp_vis.ms')
importuvfits(fitsfile=fitsf1,vis='temp_vis_1.ms')

concat(vis=['temp_vis.ms','temp_vis_1.ms'],concatvis = 'temp_vis_2.ms',freqtol = '50MHz',dirtol = '100mas')

exportuvfits(vis='temp_vis_2.ms/',fitsfile=fitsf +  fitsf1 + '_concat',datacolumn='data',padwithflags=True,overwrite=True)    
os.system('rm -rfv *.ms*')
