

def check_rare_exon(INFOstring):# find variant with propability < 0.1%
    threshold = 0.1 / 100
    CodingCodes={'splicing', 'exonic', 'exonic,splicing'}
    
    INFOcolumnList=INFOstring.split(";")
    INFOdict={}
    for element in INFOcolumnList:
        if '=' in element:
            FieldName,FieldValue=element.split('=',1)
            INFOdict[FieldName]=FieldValue
    
    # Get values from INFO fields
    KGscore= max(map(float,[ rate  for rate in INFOdict.get('1KGfreq',str(threshold)).split(',') if rate != '.' ]))
    ESPscore= max(map(float,[ rate  for rate in INFOdict.get('ESPfreq',str(threshold)).split(',') if rate != '.' ]))
    ExAcscore= max(map(float,[ rate  for rate in INFOdict.get('ExACfreq',str(threshold)).split(',') if rate != '.' ]))
    MutationFunct=str(INFOdict.get('VarFunc','None').split(',')[0])
    return KGscore <= threshold and ESPscore <= threshold and  ExAcscore <= threshold and MutationFunct in CodingCodes



def check_denovo(trio):

    proband= trio[0].split(':')
    Father = trio[1].split(':')
    Mother = trio[2].split(':')
    proband_GT = proband[0]
    Father_GT = Father[0]
    Mother_GT = Mother[0]
    
    if proband_GT in {'./.','0/0'}: #proband genotype missing or not denovo
        return False
    else:#GT:AD:DP:GQ:PL    0/1:16,9:.:99:205,0,501
        if Father_GT == '0/0' and Mother_GT == '0/0':
            return True
        else:
            return False

def get_GQ(dicts):
    GQ = dicts.get('GQ','0')
    if GQ.isdigit():
        return int(GQ)
    else:
        return 0

def get_DP(dicts):
    GQ = dicts.get('DP','0')
    if GQ.isdigit():
        return int(GQ)
    else:
        return 0

def check_inherited(trio, name):# trio =[s,f,m]

    proband = dict(zip(name.split(':'),trio[0].split(':')))
    Father = dict(zip(name.split(':'),trio[1].split(':')))
    Mother = dict(zip(name.split(':'),trio[2].split(':')))
    proband_GT = proband['GT']
    proband_GQ = get_GQ(proband)
    Father_GT = Father['GT']
    Father_GQ = get_GQ(Father)
    Mother_GT = Mother['GT']
    Mother_GQ = get_GQ(Mother)

    GQ_threshold = 30
    GQ_threshold2 = 60
    GQ_threshold3 = 80
    
    # not inherited or unknown
    inherited = False
    if proband_GT  in {'./.', '0/0'} : 
        inherited = False
    else:
        # homozygous
        if proband_GT[0] == proband_GT[-1]: 
            # find in both parents
            if proband_GT[-1] in Father_GT and proband_GT[-1] in Mother_GT:
                if proband_GQ >= GQ_threshold and Father_GQ >= GQ_threshold and Mother_GQ >= GQ_threshold:
                    inherited = True
            # found in father, unknown in mother
            elif proband_GT[-1] in Father_GT and Mother_GT in {'./.'}:
                if proband_GQ >= GQ_threshold2 and Father_GQ >= GQ_threshold:
                    inherited = True
            elif proband_GT[-1] in Mother_GT and Father_GT in {'./.'}:
                if proband_GQ >= GQ_threshold2 and Mother_GQ >= GQ_threshold:
                    inherited = True
            # both unknown
            else:
                if proband_GQ >= GQ_threshold3 and Mother_GT == './.' and  Father_GT == './.' :
                    inherited = True
        # het
        else:
            if proband_GT[-1] in Father_GT and proband_GT[-1] in Mother_GT:
                if proband_GQ >= GQ_threshold and max(Father_GQ, Mother_GQ) >= GQ_threshold:
                    inherited = True
            elif proband_GT[-1] in Father_GT:
                if proband_GQ >= GQ_threshold and Father_GQ >= GQ_threshold:
                    inherited = True
            elif proband_GT[-1] in Mother_GT:
                if proband_GQ >= GQ_threshold and Mother_GT >= GQ_threshold:
                    inherited = True
            else:
                # both unknown
                if proband_GQ >= GQ_threshold2 and ( Mother_GT == './.' or  Father_GT == './.' ):
                    inherited = True

    return inherited

def get_variant_type(INFOstring):
    '''
    function to add noise to data

    Parameters
    ----------
    :type INFOstring: str
    :param INFOstring: info column from vcf file


    returns
    ----------
    :type vartype : str
        variant type 
    '''    

    INFOcolumnList=INFOstring.split(";")
    variants={}
    for element in INFOcolumnList:
        if '=' in element:
            FieldName,FieldValue=element.split('=',1)
            variants[FieldName]=FieldValue

    LGD = {'splicing','frameshiftsubstitution','frameshiftinsertion','frameshiftdeletion','stopgain','stoploss'}
    varclass = [ x for x in variants.get('VarClass','NA').replace(' ','').split(',') if x != '.' ][0]
    varfunc = [ x for x in variants.get('VarFunc','NA').replace(' ','').split(',') if x != '.' ][0]         
    vartype = 'unknown'
    metaSVM = variants.get('MetaSVMprd','NA')
    pp2 = variants.get('PP2.hdiv.prd','NA')
    cadd = variants.get('CADDphred','0')

    if varclass == 'synonymousSNV':
        vartype = 'silent'
    if varfunc in  LGD or varclass in LGD:
        vartype = 'LGD'
    if varclass in { 'nonframeshiftsubstitution','nonframeshiftinsertion','nonframeshiftdeletion'}:
        vartype =  'inframe'
    if varclass in {'nonsynonymousSNV'}:
        if metaSVM == 'D' : 
            vartype =  'D-mis/meta'
        elif pp2 == 'D' and float(cadd)  >= 15:
            vartype = 'D-mis/PP2CADD'
        else:
            vartype = 'B-mis'
    return vartype












