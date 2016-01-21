DEBUG = True
TESTING = True
PRESERVE_CONTEXT_ON_EXCEPTION = False
Z3950_DATABASES = {'loc': {'host': 'z3950.loc.gov', 'db': 'Voyager',
                           'port': '7090'},
                   'copac': {'host': 'z3950.copac.ac.uk', 'db': 'copac',
                             'port': '210', 'syntax': 'SUTRS'}}
