import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.session import get_session
from app.models import Poll, PollOption, PollVote
from app.schemas import PollCreate, PollOptionResponse, PollResponse, PollVoteCreate

router = APIRouter()


def _serialize_poll(poll: Poll) -> PollResponse:
    option_payload = [
        PollOptionResponse(
            id=option.id,
            label=option.label,
            capacity=option.capacity,
            tags=option.tags,
            votes=len(option.votes),
        )
        for option in poll.options
    ]
    return PollResponse(
        id=poll.id,
        title=poll.title,
        month=poll.month,
        description=poll.description,
        options=option_payload,
    )


@router.get("/", response_model=list[PollResponse])
def list_polls(session: Session = Depends(get_session)) -> list[PollResponse]:
    stmt = select(Poll).options(selectinload(Poll.options).selectinload(PollOption.votes))
    polls = session.scalars(stmt).all()
    return [_serialize_poll(poll) for poll in polls]


@router.post("/", response_model=PollResponse, status_code=status.HTTP_201_CREATED)
def create_poll(payload: PollCreate, session: Session = Depends(get_session)) -> PollResponse:
    poll = Poll(title=payload.title, month=payload.month, description=payload.description)
    for option in payload.options:
        poll.options.append(PollOption(label=option.label, capacity=option.capacity, tags=option.tags))
    session.add(poll)
    session.commit()
    stmt = (
        select(Poll)
        .where(Poll.id == poll.id)
        .options(selectinload(Poll.options).selectinload(PollOption.votes))
    )
    persisted = session.scalars(stmt).first()
    if persisted is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Poll creation failed")
    return _serialize_poll(persisted)


@router.post("/{poll_id}/vote", status_code=status.HTTP_201_CREATED)
def vote_on_poll(poll_id: uuid.UUID, payload: PollVoteCreate, session: Session = Depends(get_session)) -> dict:
    option = session.get(PollOption, payload.option_id)
    if option is None or option.poll_id != poll_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Option not found for poll")

    vote = PollVote(poll_id=poll_id, option_id=payload.option_id, resident_id=payload.resident_id, priority=payload.priority)
    session.add(vote)
    session.commit()
    return {"status": "recorded"}
