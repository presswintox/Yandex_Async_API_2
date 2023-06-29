from models.film import Film
from models.person import Actor, Writer, Director


def test_create_film_model():
    in_data = {
        "id": "57d671e5-dc33-4233-99cc-71aea310e40b",
        "title": "test",
        "description": "test",
        "imdb_rating": 1,
        "actors": [
            {
                "id": "57d671e5-dc33-4233-99cc-71aea310e40b",
                "full_name": "test"
            }
        ],
        "writers": [
            {
                "id": "57d671e5-dc33-4233-99cc-71aea310e40b",
                "full_name": "test"
            }
        ],
        "directors": [
            {
                "id": "57d671e5-dc33-4233-99cc-71aea310e40b",
                "full_name": "test"
            }
        ],
        "actors_names": ["test"],
        "writers_names": ["test"]
    }
    out_data = Film(id="57d671e5-dc33-4233-99cc-71aea310e40b",
                    title="test",
                    description="test",
                    imdb_rating=1,
                    actors=[
                        Actor(id="57d671e5-dc33-4233-99cc-71aea310e40b",
                              full_name="test")
                    ],
                    writers=[
                        Writer(id="57d671e5-dc33-4233-99cc-71aea310e40b",
                              full_name="test")
                    ],
                    directors=[
                        Director(id="57d671e5-dc33-4233-99cc-71aea310e40b",
                               full_name="test")
                    ],
                    actors_names=["test"],
                    writers_names=["test"]
                    )
    assert Film(**in_data) == out_data

