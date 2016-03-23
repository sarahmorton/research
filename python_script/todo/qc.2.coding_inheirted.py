import os

dir1 = '/home/local/ARCS/hq2130/CHD_MedExomeKit/vcf_0223/vcf_trio/'
CodingCodes={'splicing', 'exonic', 'exonic,splicing'}
fw = open('commom_inheited3.txt','w')
for e in os.listdir(dir1):
    if e.endswith('vcf'):
        with open(dir1 + e) as f:
            s = e.split('_')[0]
            
            count = 0
            for line in f:
                if line[0] != '#':
                    data =  line.split()
                    INFOstring = data[7]
                    INFOcolumnList=INFOstring.split(";")
                    INFOdict={}
                    for element in INFOcolumnList:
                        if '=' in element:
                            FieldName,FieldValue=element.split('=',1)
                            INFOdict[FieldName]=FieldValue
                    MutationFunct=str(INFOdict.get('VarFunc','None').split(',')[0])        
                            
                    proband, father, mother  = line.strip().split()[-3:]
                    proband = proband.split(':')[0]
                    father = father.split(':')[0]
                    mother = mother.split(':')[0]
                    if MutationFunct in CodingCodes and  proband not in {'./.', '0/0'} and (proband[-1] in father or proband[-1] in mother):
                        count += 1
            print s, count
            fw.write('\t'.join([s, str(count), '\n']))
fw.close()
            