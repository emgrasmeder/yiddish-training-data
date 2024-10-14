import parser


entry = [
    {
        'links': [
            ['Unpointed', 'nikud'],
            ['כּלבֿ', 'כּלבֿ#Yiddish']],
        'raw_glosses': ['(nonstandard) Unpointed form of כּלבֿ (kelev).'],
        'glosses': ['Unpointed form of כּלבֿ (kelev).'],
        'tags': ['nonstandard'],
        'id': 'en-כלב-yi-noun-ewUnihgG',
        'categories': [
            {'name': 'Pages with 3 entries', 'kind': 'other', 'parents': [], 'source': 'w'},
            {'name': 'Pages with entries', 'kind': 'other', 'parents': [], 'source': 'w'},
            {'name': 'Yiddish entries with incorrect language header', 'kind': 'other', 'parents': ['Entries with incorrect language header', 'Entry maintenance'], 'source': 'w'},
            {'name': 'Yiddish terms with non-redundant manual transliterations', 'kind': 'other', 'parents': ['Terms with non-redundant manual transliterations', 'Entry maintenance'], 'source': 'w'},
            {'name': 'Yiddish terms with redundant script codes', 'kind': 'other', 'parents': ['Terms with redundant script codes', 'Entry maintenance'], 'source': 'w'}
        ]
    }
]

def test_finds_doubly_nonstandard_words_and_flags_them_in_error_file(tmp_path):
    nonstandard_entry_1 = {
        'word': 'example',
        'links': [['Unpointed', 'nikud']],
        'tags': ['nonstandard']}
    error_file = f"{tmp_path}/errors.txt"
    actual = parser.flag_if_nonstandard(nonstandard_entry_1, error_file)
    with open(error_file, 'r') as f:
        assert nonstandard_entry_1['word'] in f.readlines()[0]

def test_finds_nonstandard_words_and_flags_them_in_error_file(tmp_path):
    nonstandard_entry_2 = {
        'word': 'example',
        'links': [['something', 'else']],
        'tags': ['nonstandard']}
    error_file = f"{tmp_path}/errors.txt"
    with open(error_file, 'w') as f:
        pass
    actual = parser.flag_if_nonstandard(nonstandard_entry_2, error_file)
    with open(error_file, 'r') as f:
        assert nonstandard_entry_2['word'] in f.readlines()[0]

def test_finds_unpointed_words_and_flags_them_in_error_file(tmp_path):
    nonstandard_entry_3 = {
        'word': 'example',
        'links': [['Unpointed', 'nikud']],
        'tags': ['something else']}
    error_file = f"{tmp_path}/errors.txt"
    with open(error_file, 'w') as f:
        pass
    actual = parser.flag_if_nonstandard(nonstandard_entry_3, error_file)
    with open(error_file, 'r') as f:
        assert nonstandard_entry_3['word'] in f.readlines()[0]

def test_does_nothing_if_word_is_not_nonstandard(tmp_path):
    nonstandard_entry = {
        'word': 'example',
        'links': [],
        'tags': ['something else']}
    error_file = f"{tmp_path}/errors.txt"
    with open(error_file, 'w') as f:
        pass
    actual = parser.flag_if_nonstandard(nonstandard_entry, error_file)
    with open(error_file, 'r') as f:
        assert len(f.readlines()) == 0
