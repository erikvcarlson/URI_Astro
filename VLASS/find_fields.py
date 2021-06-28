def find_fields(msfile='', distance='0deg', phase_center=None, matchregex=''):
    import numpy
    import math
    from pipeline.infrastructure import casatools as casa_tools
    # Created STM 2016-May-16 use center direction measure
    # Returns list of fields from msfile within a rectangular box of size distance
    #example: find_fields(msfile='VLASS2.1_Guide.ms/',phase_center='J2000 08h07m57.5 +4d32m34.6',distance='23arcmin')
    qa = casa_tools.quanta
    me = casa_tools.measures
    tb = casa_tools.table

    #msfile = self.vislist[0]
    
    fieldlist = []

    phase_center = phase_center.split()
    center_dir = me.direction(phase_center[0], phase_center[1], phase_center[2])
    center_ra = center_dir['m0']['value']
    center_dec = center_dir['m1']['value']

    try:
        qdist = qa.toangle(distance)
        qrad = qa.convert(qdist, 'rad')
        maxrad = qrad['value']
    except:
        print('ERROR: cannot parse distance {}'.format(distance))
        return

    try:
        tb.open(msfile + '/FIELD')
    except:
        print('ERROR: could not open {}/FIELD'.format(msfile))
        return
    field_dirs = tb.getcol('PHASE_DIR')
    field_names = tb.getcol('NAME')
    tb.close()

    (nd, ni, nf) = field_dirs.shape
    print('Found {} fields'.format(nf))

    # compile field dictionaries
    ddirs = {}
    flookup = {}
    for i in range(nf):
        fra = field_dirs[0, 0, i]
        fdd = field_dirs[1, 0, i]
        rapos = qa.quantity(fra, 'rad')
        decpos = qa.quantity(fdd, 'rad')
        ral = qa.angle(rapos, form=["tim"], prec=9)
        decl = qa.angle(decpos, prec=10)
        fdir = me.direction('J2000', ral[0], decl[0])
        ddirs[i] = {}
        ddirs[i]['ra'] = fra
        ddirs[i]['dec'] = fdd
        ddirs[i]['dir'] = fdir
        fn = field_names[i]
        ddirs[i]['name'] = fn
        if fn in flookup:
            flookup[fn].append(i)
        else:
            flookup[fn] = [i]
    print('Cataloged {} fields'.format(nf))

    # Construct offset separations in ra,dec
    print('Looking for fields with maximum separation {}'.format(distance))
    nreject = 0
    skipmatch = matchregex == '' or matchregex == []

    for i in range(nf):
        dd = ddirs[i]['dir']
        dd_ra = dd['m0']['value']
        dd_dec = dd['m1']['value']
        sep_ra = abs(dd_ra - center_ra)
        if sep_ra > numpy.pi:
            sep_ra = 2.0 * numpy.pi - sep_ra
        # change the following to use dd_dec 2017-02-06
        sep_ra_sky = sep_ra * numpy.cos(dd_dec)

        sep_dec = abs(dd_dec - center_dec)
        print(sep_dec)
        ddirs[i]['offset_ra'] = sep_ra_sky
        ddirs[i]['offset_ra'] = sep_dec
        
        #print(sep_dec)
        if sep_dec <= maxrad:
            print('hello world')
        if sep_ra_sky <= maxrad and sep_dec <= maxrad:
            if skipmatch:
                fieldlist.append(i)
            else:
                # test regex against name
                foundmatch = False
                fn = ddirs[i]['name']
                for rx in matchregex:
                    mat = re.findall(rx, fn)
                    if len(mat) > 0:
                        foundmatch = True
                if foundmatch:
                    fieldlist.append(i)
                else:
                    nreject += 1

    print('Found {} fields within {}'.format(len(fieldlist), distance))
    if not skipmatch:
        print('Rejected {} distance matches for regex'.format(nreject))
        
    for i in range(0,len(fieldlist)):
        fieldlist[i] = str(fieldlist[i])
    fieldlist = ",".join(fieldlist)
    
    print("Maximum Radian = " + str(maxrad))

    return fieldlist
