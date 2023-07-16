from http import HTTPStatus
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from src.services.genre import GenreService, get_genre_service
from src.api.v1.schemas.genres import (
    GenreDetail,
    GenreListDetail,
    GenreListQuery,
    GenreSearchQuery
)


router = APIRouter()


@router.get("", response_model=List[GenreListDetail],
            summary="Получение списка жанров",
            description="Получение списка жанров")
async def genres(
            query: GenreListQuery = Depends(),
            genre_service: GenreService = Depends(get_genre_service)
        ) -> List[GenreListDetail]:
    """Получение списка жанров"""
    genres = await genre_service.search_by_filter(
                                                page_size=query.page_size,
                                                page_number=query.page_number)
    return [GenreListDetail.parse_obj(genre) for genre in genres]


@router.get("/search", response_model=List[GenreListDetail],
            summary="Поиск жанров",
            description="Поиск жанров по названию или описанию")
async def search_genres(
            q: GenreSearchQuery = Depends(),
            genre_service: GenreService = Depends(get_genre_service)
        ) -> List[GenreListDetail]:
    """Поиск жанров по названию или описанию"""
    genres = await genre_service.search_by_filter(
                                                page_size=q.page_size,
                                                page_number=q.page_number,
                                                search=q.query)
    return [GenreListDetail.parse_obj(genre) for genre in genres]


@router.get("/{genre_id}", response_model=GenreDetail,
            summary="Получение детальной информации о жанре",
            description="Получение детальной информации о жанре.")
async def genre_details(
            genre_id: str,
            genre_service: GenreService = Depends(get_genre_service)
        ) -> GenreDetail:
    """Получение детальной информации о жанре"""
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='Genre not found')

    return GenreDetail.parse_obj(genre)
