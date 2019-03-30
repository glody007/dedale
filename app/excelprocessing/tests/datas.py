DATAS = {
        'row_datas' :   [
                             {
                              'first_name' : 'richard',
                              'last_name' : 'dawkins',
                              'forename' : 'light',
                              'sex' : 'M',
                             },

                            {
                             'first_name' : 'lubaba',
                             'last_name' : 'mbutwile',
                             'forename' : 'dyglo',
                             'sex' : 'M',
                            }
                        ],

        'columns_alias' :  {
                             1 : 'first_name',
                             2 : 'last_name',
                             3 : 'forename',
                             4 : 'sex'
                            },

        'wrong_columns_aliases': [
                                    {
                                     0 : 'first_name',
                                     2 : 'last_name',
                                     3 : 'forename',
                                     4 : 'sex'
                                    },

                                    {
                                     1 : 'first_name',
                                     2 : 'last_name',
                                     3 : 'forename',
                                     5 : 'sex'
                                    }
                                 ],

        'titles_alias' :   {
                            'first_name' : 'first_name',
                            'last_name' : 'last_name',
                            'forename' : 'forename',
                            'sex' : 'sex'
                           },

        'wrong_titles_alias': {
                                'first_name' : 'first_name',
                                'last_name' : 'last_name',
                                'name' : 'forename',
                                'sex' : 'sex'
                              },

        'titles' : ['first_name', 'last_name', 'forename', 'sex']
        }

def get_wrong_titles_alias():
    return DATAS['wrong_titles_alias']

def get_columns_alias_min_key_out_of_interval():
    return DATAS['wrong_columns_aliases'][0]

def get_columns_alias_max_key_out_of_interval():
    return DATAS['wrong_columns_aliases'][1]

def get_datas_by_rows():
    values = []
    row_datas = DATAS['row_datas']
    for data in row_datas:
        value = [
                  data['first_name'],
                  data['last_name'],
                  data['forename'],
                  data['sex']
                ]
        values.append(value)
    return values

def get_labeled_datas():
    return DATAS['row_datas']

def get_columns_alias():
    return DATAS['columns_alias']

def get_titles_alias():
    return DATAS['titles_alias']

def get_columns_titles():
    return DATAS['titles']

def get_datas():
    return DATAS
