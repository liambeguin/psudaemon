from fastapi import APIRouter


router = APIRouter()


@router.get('/measurements')
def get_measurements():
    return []
