import csv

with open('all_cases_controls_v3.txt') as f:
    target3 = set()
    health = set()
    for line in f:
        sample = line.strip()
        target3.add(sample)

            
            
with open('all_cases_controls.txt') as f:
    cases = set()
    health = set()
    for line in f:
        sample = line.strip()
        if sample in target3: continue
        if '1-' in sample and len(sample) == 7:
            cases.add(sample)
        elif 'GT' in sample and sample[-1] not in {'A','B'}:
            cases.add(sample)
        elif sample in {'950400255','950400309-0','M002-5','M003-08',\
        'M004-11','M005-14','M006-17','M007-20','M008-23', 'M009-26'}:
            cases.add(sample)
        else:
            health.add(sample)
        
with open('Familial.ped') as f:
    head = f.readline()
    for line in f:
        lst = line.strip().split('\t')
        if lst[5] == '2' and lst[5] not in cases and lst[5] in health:
            cases.add(lst[1])
            if lst[1] in health:
                health.remove(lst[1])
            


with open('GDF1_v2.vcf') as f:
    info = []
    i = 0
    fw = open('GDF1_v2.csv','wb')
    w = csv.writer(fw)
    head_info = ['GeneName','VarFunc', 'VarClass','ABHet', 'ABHom', 'AC', 'AF', 'AN', 'BaseQRankSum', 'ClippingRankSum', 'DB', 'DP', 'DS', 'Dels', 'END', 'FS', 'GQ_MEAN', \
    'GQ_STDDEV', 'HRun', 'HapMapV3', 'HaplotypeScore', 'InbreedingCoeff', 'MLEAC', 'MLEAF', 'MQ', 'MQ0', 'MQRankSum', 'NCC', \
    'OND', 'QD', 'ReadPosRankSum', 'SOR', 'AAChange', 'ESPfreq', 'ESP.aa.freq', 'ESP.ea.freq', '1KGfreq', '1KG.eur.freq', \
    '1KG.amr.freq', '1KG.eas.freq', '1KG.afr.freq', '1KG.sas.freq', 'ExACfreq', 'ExAC.afr.freq', 'ExAC.amr.freq', 'ExAC.eas.freq', \
    'ExAC.fin.freq', 'ExAC.nfe.freq', 'ExAC.oth.freq', 'ExAC.sas.freq', 'SIFTscr', 'SIFTprd', 'PP2.hdiv.scr', 'PP2.hdiv.prd', 'PP2.hvar.scr',\
    'PP2.hvar.prd', 'MutTscr', 'MutTprd', 'MutAscr', 'MutAprd', 'MetaSVMscr', 'MetaSVMprd', 'CADDraw', 'CADDphred', 'GERP', 'PhyloP', 'SiPhy', \
    'FATHMM_coding', 'FATHMM_noncoding', 'GWAVA_region_score', 'GWAVA_tss_score', 'GWAVA_unmatched_score', 'CADDInDelraw', 'CADDInDelphred', \
    'COSMIC' , 'SegDup']
    w.writerow(['case_carrier', 'case_noncarrier', 'healthy_carrier', 'healthy_noncarrier','proband ID(GT:AD:DP:GQ:PL)'] + head_info)
    for line in f:
        if line.startswith('#'):
            if line.startswith('##INFO=<ID'):
                info.append(line.split(',')[0].split('INFO=<ID=')[1])
            if line.startswith('#CHROM'):
                sample_index = line.strip().split('\t')
            
        else:
            linelist=line.split("\t")
            VariantFilter=linelist[6]
            INFOstring=linelist[7]
            INFOcolumnList=INFOstring.split(";")
            INFOdict={}
            for element in INFOcolumnList:
                if '=' in element:
                    FieldName,FieldValue=element.split('=',1)
                    INFOdict[FieldName]=FieldValue
            if INFOdict['GeneName'] == 'GDF1':
                i += 1
                case_carrier, case_noncarrier,healthy_carrier, healthy_noncarrier = 0, 0, 0, 0
                case_id = []
                for s in cases:
                    index = sample_index.index(s)
                    sample_info =  linelist[index].split(':')
                    gt = sample_info[0]
                    if gt != './.':
                        if gt == '0/0':
                            case_noncarrier += 1
                        else:
                            case_carrier += 1
                            case_id.append( s+'('+linelist[index]+')')
                for s in health:
                    index = sample_index.index(s)
                    sample_info =  linelist[index].split(':')
                    gt = sample_info[0]
                    if gt != './.':
                        if gt == '0/0':
                            healthy_noncarrier += 1
                        else:
                            healthy_carrier += 1
                            
                if case_carrier != 0:
                    new_info = []
                    for e in head_info:
                        new_info.append(str(INFOdict.get(e,'none')))
                    
                    w.writerow( [case_carrier, case_noncarrier,healthy_carrier, healthy_noncarrier,';'.join(case_id)] + new_info)
    fw.close()
                            
                            
    print info
    print i