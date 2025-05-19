from fastapi import APIRouter, Request, Depends, status, HTTPException
from .. import schemas, database, models, oauth2, utils
from sqlalchemy.orm import Session

router = APIRouter(prefix = '/url', tags = ['URL'])

@router.post('/shorten', response_model= schemas.UrlOut)
def shorten_url(url_data: schemas.UrlCreate, 
                request: Request, 
                db: Session = Depends(database.get_db), 
                current_user: models.User = Depends(oauth2.get_current_user)):
    
    url_already_exists = db.query(models.Url).filter(models.Url.original == str(url_data.original) , models.Url.owner_id == current_user.id).first()

    if url_already_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Url already shortened")

    short_code = utils.generate_short_code()
    while db.query(models.Url).filter(models.Url.short == short_code).first():
        short_code = utils.generate_short_code()

    new_url = models.Url(
        original = str(url_data.original),
        short = short_code,
        owner_id = current_user.id
        )
    
    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return new_url
    # short_url = str(request.base_url) + short_code
    # return {"short_url": short_url}