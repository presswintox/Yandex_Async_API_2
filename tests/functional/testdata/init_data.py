import uuid

PERSONS_DATA = [{
    'id': str(uuid.uuid4()),
    'full_name': 'Ann',
} for _ in range(10)]

FIRST_PERSON_ID = PERSONS_DATA[0]['id']

GENRE_DATA = [{
    'id': str(uuid.uuid4()),
    'name': 'Sci-fi',
    'description': 'Some text'
} for _ in range(10)]

FILMS_DATA = [{
    'id': str(uuid.uuid4()),
    'imdb_rating': 8.5,
    'genre': [{'id': '97f168bd-d10d-481b-ad38-89d252a13feb',
               'name': 'Ben'},
              {'id': '97f168bd-d10d-481b-ad38-89d252a13feb',
               'name': 'Howard'}],
    'title': 'The Star',
    'description': 'New World',
    'actors_names': ['Ann', 'Bob'],
    'writers_names': ['Ben', 'Howard'],
    'actors': [
        {'id': FIRST_PERSON_ID, 'full_name': 'Ann'},
        {'id': '97f168bd-d10d-481b-ad38-89d252a13feb', 'full_name': 'Bob'}
    ],
    'writers': [
        {'id': '97f168bd-d10d-481b-ad38-89d252a13feb', 'full_name': 'Ben'},
        {'id': '97f168bd-d10d-481b-ad38-89d252a13feb',
         'full_name': 'Howard'}
    ],
    'directors': [
        {'id': '97f168bd-d10d-481b-ad38-89d252a13feb', 'full_name':
            'Stan'},
        {'id': '97f168bd-d10d-481b-ad38-89d252a13feb', 'full_name':
            'Howard'}
    ]
} for _ in range(10)]
