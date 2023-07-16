import uuid
from http import HTTPStatus
from typing import List, Optional

from fastapi import Depends, APIRouter, HTTPException

from src.api.v1.schemas.films import FilmListDetail
from src.api.v1.schemas.persons import PersonDetail, PersonSearchQuery
from src.services.person import get_person_service, PersonService

router = APIRouter()


@router.get(
    "/{person_id}/",
    response_model=PersonDetail,
    summary="Получение детальной информации о персоне",
    description="Получение детальной информации о персоне"
)
async def person_details(
    person_id: uuid.UUID,
    person_service: PersonService = Depends(get_person_service)
) -> PersonDetail:

    person_detail = await person_service.get_person_with_films_and_roles(
        person_id=person_id
    )
    if not person_detail:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Person not found",
        )

    return PersonDetail.parse_obj(person_detail)


@router.get(
    "/{person_id}/film/",
    response_model=List[FilmListDetail],
    summary="Получение фильмов персоны",
    description="Получение фильмов персоны"
)
async def person_films(
    person_id: uuid.UUID,
    person_service: PersonService = Depends(get_person_service)
) -> List[Optional[FilmListDetail]]:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Person not found",
        )
    films = await person_service.search_films_by_person_uid(
        person_id=person_id
    )
    return [FilmListDetail.parse_obj(film) for film in films]


@router.get(
    "/search",
    response_model=List[PersonDetail],
    summary="Поиск персон",
    description="Поиск персон по имени и фамилии."
)
async def search_persons(
    query_params: PersonSearchQuery = Depends(),
    person_service: PersonService = Depends(get_person_service)
) -> List[PersonDetail]:
    person_detail_list = await person_service.get_persons_with_films_by_query(
        page_size=query_params.page_size,
        page_number=query_params.page_number,
        search=query_params.query)
    return [PersonDetail.parse_obj(film) for film in person_detail_list]
