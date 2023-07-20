from typing import List

from fastapi import APIRouter, Depends
from starlette.requests import Request

from managers.auth import is_complainer, oauth2_scheme
from managers.complaint import ComplaintManager
from schemas.request.complaint import ComplaintIn
from schemas.response.complaint import ComplaintOut

router = APIRouter(tags=["Complaints"])


@router.get(
    "/complaints/",
    dependencies=[Depends(oauth2_scheme)],
    response_model=List[ComplaintOut],
)
async def get_complaints(request: Request):
    user = request.state.user
    result = await ComplaintManager.get_complaints(user)
    complaints = [ComplaintOut(**complaint_data) for complaint_data in result]
    return complaints


@router.post(
    "/complaints/",
    dependencies=[Depends(oauth2_scheme), Depends(is_complainer)],
    response_model=ComplaintOut,
)
async def create_complaint(request: Request, complaint: ComplaintIn):
    user = request.state.user
    created_complaint = await ComplaintManager.create_complaint(
        complaint.model_dump(), user
    )
    created_complaint_out = ComplaintOut(**created_complaint)
    return created_complaint_out
