from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from typing import List
from typing import Optional

# Создаем подключение к PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@db:5432/tracks"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Track(Base):
    __tablename__ = "tracks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    artist = Column(String, index=True)

class FavoriteTrack(Base):
    __tablename__ = "favorite_tracks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    track_id = Column(Integer, ForeignKey("tracks.id"))
    user = relationship("User", back_populates="favorite_tracks")
    track = relationship("Track")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    favorite_tracks = relationship("FavoriteTrack", back_populates="user")

Base.metadata.create_all(bind=engine)

app = FastAPI()

class TrackModel(BaseModel):
    title: str
    artist: str

    class Config:
        orm_mode = True

class FavoriteTrackCreate(BaseModel):
    track_id: int

class FavoriteTrackResponse(BaseModel):
    id: int
    user_id: int
    track_id: int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str

class UserResponse(BaseModel):
    id: int
    username: str
    favorite_tracks: List[FavoriteTrackResponse] = []

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    new_user = User(username=user.username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/tracks/", response_model=TrackModel)
def create_track(track: TrackModel, db: Session = Depends(get_db)):
    new_track = Track(title=track.title, artist=track.artist)
    db.add(new_track)
    db.commit()
    db.refresh(new_track)
    return new_track

@app.post("/users/{user_id}/favorite-tracks/", response_model=FavoriteTrackResponse)
def create_favorite_track_for_user(user_id: int, favorite_track: FavoriteTrackCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    track = db.query(Track).filter(Track.id == favorite_track.track_id).first()
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")
    favorite_track_obj = FavoriteTrack(user_id=user_id, track_id=favorite_track.track_id)
    db.add(favorite_track_obj)
    db.commit()
    db.refresh(favorite_track_obj)
    return favorite_track_obj

@app.get("/tracks/", response_model=list[TrackModel])
def get_tracks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Track).offset(skip).limit(limit).all()

@app.get("/users/{user_id}/favorite-tracks/", response_model=list[FavoriteTrackResponse])
def get_favorite_tracks_for_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user.favorite_tracks

@app.delete("/users/{user_id}/favorite-tracks/{favorite_track_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_favorite_track_for_user(user_id: int, favorite_track_id: int, db: Session = Depends(get_db)):
    favorite_track = db.query(FavoriteTrack).filter(FavoriteTrack.id == favorite_track_id, FavoriteTrack.user_id == user_id).first()
    if not favorite_track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Favorite track not found")
    db.delete(favorite_track)
    db.commit()
