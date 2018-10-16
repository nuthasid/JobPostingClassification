
def import_raw_data(filename):

    import json

    with open(filename, 'rt', encoding='utf-8') as fin:
        dataset = fin.read()

    dataset = dataset.replace('}\n{', '},{')
    dataset = '[' + dataset[:-1] + ']'
    return json.loads(dataset)


def restructure_data(json_dataset):

    import pickle

    mapping = {'pdate': 'date',
               'company': 'company',
               'com': 'company',
               'pos': 'title',
               'pos2': 'title',
               'posth': 'title',
               'desc': 'desc',
               'resp': 'desc',
               'req': 'desc',
               'func': 'desc',
               'skill_pref': 'desc',
               'skill_req': 'desc',
               'edu': 'qualification',
               'qual': 'qualification',
               'district': 'location',
               'loc_det': 'location',
               'province': 'location',
               'com_loc': 'location',
               'loc': 'location',
               'location': 'location',
               'exp_req': 'experience',
               'exp_pref': 'experience',
               'exp': 'experience',
               'age': 'age',
               'amnt': 'amount',
               'benef': 'benefits',
               'sal': 'salary',
               'sex': 'gender'}

    thai_month = {'กรกฎาคม': 5,
                  'กันยายน': 9,
                  'กุมภาพันธ์': 2,
                  'ตุลาคม': 10,
                  'ธันวาคม': 12,
                  'พฤศจิกายน': 11,
                  'พฤษภาคม': 5,
                  'มกราคม': 1,
                  'มิถุนายน': 6,
                  'มีนาคม': 3,
                  'สิงหาคม': 8,
                  'เมษายน': 4}

    eng_month = {'Jan': 1,
                 'Feb': 2,
                 'Mar': 3,
                 'Apr': 4,
                 'May': 5,
                 'Jun': 6,
                 'Jul': 7,
                 'Aug': 8,
                 'Sep': 9,
                 'Oct': 10,
                 'Nov': 11,
                 'Dec': 12}

    field_set = sorted(list(set([mapping[key] for key in list(mapping)])))

    documents = []
    for doc in json_dataset:
        data = {}
        for key in field_set:
            data[key] = ''
        for key in mapping:
            if key in list(doc):
                data[mapping[key]] = str(doc[key]) + ' \\\\'
        documents.append(data)

    date_pat = pickle.load(open('./Resource/date_pattern.pck', 'rb'))

    #date_pat = [re.compile(r'(20[0-9]{2})(\s|\-|\/)([0-9]{2})(\s|\-|\/)([0-9]{2})'),
    #            re.compile(r'([0-9]{2})(\s|\-|\/)([0-1]{1}[0-9]{1})(\s|\-|\/)(25[0-9]{2})'),
    #            re.compile(r'([0-9]{2})(\s|\-|\/)([0-1]{1}[0-9]{1})(\s|\-|\/)(20[0-9]{2})'),
    #            re.compile(r'([0-9]{1,2})(\s|\-|\/)([\u0e00-\u0e7f]{1,})(\s|\-|\/)([5-9]{1}[0-9]{1})'),
    #            re.compile(r'([0-9]{1,2})(\s|\-|\/)([A-Za-z]{1,})(\s|\-|\/)([0-4]{1}[0-9]{1})'),
    #            re.compile(r'([0-9]{1,2})(\s|\-|\/)([\u0e00-\u0e7f]{1,})(\s|\-|\/)(25[0-9]{2})'),
    #            re.compile(r'(25[0-9]{2})(\s|\-|\/)([0-9]{2})(\s|\-|\/)([0-9]{2})')]

    for i, doc in enumerate(documents):

        if date_pat[0].search(doc['date']):
            match = date_pat[0].search(doc['date'])
            day = int(str(match.group(5)))
            month = int(str(match.group(3)))
            year = int(str(match.group(1)))
        elif date_pat[1].search(doc['date']):
            match = date_pat[1].search(doc['date'])
            day = int(str(match.group(1)))
            month = int(str(match.group(3)))
            year = int(str(match.group(5))) - 543
        elif date_pat[2].search(doc['date']):
            match = date_pat[2].search(doc['date'])
            day = int(str(match.group(1)))
            month = int(str(match.group(3)))
            year = int(str(match.group(5)))
        elif date_pat[3].search(doc['date']):
            match = date_pat[3].search(doc['date'])
            day = int(str(match.group(1)))
            month = thai_month[str(match.group(3))]
            year = int('25' + str(match.group(5))) - 543
        elif date_pat[4].search(doc['date']):
            match = date_pat[4].search(doc['date'])
            day = int(str(match.group(1)))
            month = eng_month[str(match.group(3))]
            year = int('20' + str(match.group(5)))
        elif date_pat[5].search(doc['date']):
            match = date_pat[5].search(doc['date'])
            day = int(str(match.group(1)))
            month = thai_month[str(match.group(3))]
            year = int(str(match.group(5))) - 543
        elif date_pat[6].search(doc['date']):
            match = date_pat[6].search(doc['date'])
            day = int(str(match.group(5)))
            month = int(str(match.group(3)))
            year = int(str(match.group(1))) - 543
        else:
            day = 'na'
            month = 'na'
            year = 'na'
        documents[i]['date'] = str(day) + '-' + str(month) + '-' + str(year)

    return documents
