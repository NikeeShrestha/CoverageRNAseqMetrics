def defparse(astr):
    dd = {}
    y = astr.strip().split(';')
    for a in y:
        b = a.split('=')
        dd[b[0]] = b[1]
    return dd

def gff3parse(file):
    gff3_dict={}
    myfile=open(file)
    count=0

    for line in myfile:
        if line.startswith('#'): continue

        myline=line.strip().split('\t')
        if 'chromosome' in myline: continue

        chrom=myline[0]

        # print(myline)
        if myline[2]=='gene':
            defdict = defparse(myline[-1])
            # print(defdict['Name'])
            # print(defdict['ID'])
            if 'Sobic' in defdict['ID']:
                key=defdict['Name']
            else: key=defdict['ID']

            # key = defdict.get('ID') or defdict['Name']
            # print(key)
            if not key in gff3_dict:
                gff3_dict[key]={"chrom": chrom,"strand":myline[6],"start":int(myline[3]),"stop":int(myline[4]),
                                             "cdsstart":[], "cdsend":[],"exonstarts":[], "exonends":[]}
                # print(gff3_dict)
        if myline[2]=='CDS':
            defdict = defparse(myline[-1])
            if '_' in defdict['Parent']:
                gene = defdict['Parent'].split('_')[0]
            else:
                gene = f"{defdict['Parent'].split('.')[0]}.{defdict['Parent'].split('.')[1]}"

            gff3_dict[gene]["cdsstart"].append(int(myline[3]))
            gff3_dict[gene]["cdsend"].append(int(myline[4]))

        if myline[2]=='exon':
            defdict = defparse(myline[-1])
            if '_' in defdict['Parent']:
                gene = defdict['Parent'].split('_')[0]
            else:
                gene = f"{defdict['Parent'].split('.')[0]}.{defdict['Parent'].split('.')[1]}"
            gff3_dict[gene]["exonstarts"].append(int(myline[3]))
            gff3_dict[gene]["exonends"].append(int(myline[4]))
        count+=1
        # if count==50: break
    return gff3_dict

ff=gff3parse("/work/schnablelab/nikees/AlternateSplicing/reference/Zm-B73-REFERENCE-NAM-5.0_Zm00001eb.1.gff3")

with open('/work/schnablelab/nikees/AlternateSplicing/reference/Zm-B73-REFERENCE-NAM-5.0_Zm00001eb.1.reflat.txt', 'w') as file:

    for i in ff:
        gene=i
        chrom=ff[i]['chrom']
        strand=ff[i]['strand']
        start=ff[i]['start']
        end=ff[i]['stop']
        cdsstart=min(ff[i]['cdsstart'])
        cdsend=max(ff[i]['cdsend'])
        exoncounts=len(ff[i]['cdsend'])
        exondstarts=",".join(map(str, ff[i]['exonstarts']))
        exonends=",".join(map(str, ff[i]['exonends']))

        file.write(f"{gene}\t{gene}\t{chrom}\t{strand}\t{start}\t{end}\t{cdsstart}\t{cdsend}\t{exoncounts}\t{exondstarts},\t{exonends},\n")   