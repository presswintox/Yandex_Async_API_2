from http import HTTPStatus
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.api.v1.schemas.films import FilmDetail, FilmListDetail, FilmSearchQuery, \
    FilmListQuery
from src.services.film import FilmService, get_film_service

router = APIRouter()


@router.get("/search", response_model=List[FilmListDetail],
            description="Поиск фильмов по названию или описанию")
async def search_films(q: FilmSearchQuery = Depends(),
                       film_service: FilmService = Depends(get_film_service)
                       ) -> List[FilmListDetail]:
    """Поиск фильмов по названию или описанию"""
    films = await film_service.search_by_filter(sort=q.sort,
                                                page_size=q.page_size,
                                                page_number=q.page_number,
                                                genre=None,
                                                search=q.query)
    return [FilmListDetail.parse_obj(film) for film in films]


@router.get("/{film_id}", response_model=FilmDetail,
            description="Получение детальной информации о фильме")
async def film_details(film_id: UUID,
                       film_service: FilmService = Depends(get_film_service)
                       ) -> FilmDetail:
    """Получение детальной информации о фильме"""
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='Film not found')

    return FilmDetail.parse_obj(film)


@router.get("", response_model=List[FilmListDetail],
            description="Получение списка фильмов")
async def films(query: FilmListQuery = Depends(),
                film_service: FilmService = Depends(get_film_service)
                ) -> List[FilmListDetail]:
    """Получение списка фильмов"""
    films = await film_service.search_by_filter(sort=query.sort,
                                                page_size=query.page_size,
                                                page_number=query.page_number,
                                                genre=query.genre)
    return [FilmListDetail.parse_obj(film) for film in films]
