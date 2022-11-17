import asyncio
from typing import Any, Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.clients.reddit import RedditClient
from app.schemas.route import (
    Route,
    RouteCreate,
    routesearchResults,
    RouteUpdateRestricted,
)
from app.models.user import User

router = APIRouter()
Route_SUBREDDITS = ["routes", "easyroutes", "TopSecretroutes"]


@router.get("/{Route_id}", status_code=200, response_model=Route)
def fetch_Route(
    *,
    Route_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Fetch a single Route by ID
    """
    result = crud.Route.get(db=db, id=Route_id)
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Route with ID {Route_id} not found"
        )

    return result


@router.get("/search/", status_code=200, response_model=routesearchResults)
def search_routes(
    *,
    keyword: str = Query(None, min_length=3, example="chicken"),
    max_results: Optional[int] = 10,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Search for routes based on label keyword
    """
    routes = crud.Route.get_multi(db=db, limit=max_results)
    results = filter(lambda Route: keyword.lower() in Route.label.lower(), routes)

    return {"results": list(results)}


@router.post("/", status_code=201, response_model=Route)
def create_Route(
    *,
    Route_in: RouteCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    """
    Create a new Route in the database.
    """
    if Route_in.submitter_id != current_user.id:
        raise HTTPException(
            status_code=403, detail=f"You can only submit routes as yourself"
        )
    Route = crud.Route.create(db=db, obj_in=Route_in)

    return Route


@router.put("/", status_code=201, response_model=Route)
def update_Route(
    *,
    Route_in: RouteUpdateRestricted,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Update Route in the database.
    """
    Route = crud.Route.get(db, id=Route_in.id)
    if not Route:
        raise HTTPException(
            status_code=400, detail=f"Route with ID: {Route_in.id} not found."
        )

    # if Route.submitter_id != current_user.id:
    #     raise HTTPException(
    #         status_code=403, detail=f"You can only update your routes."
    #     )

    updated_Route = crud.Route.update(db=db, db_obj=Route, obj_in=Route_in)
    db.commit()
    return updated_Route


async def get_reddit_top_async(subreddit: str) -> list:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://www.reddit.com/r/{subreddit}/top.json?sort=top&t=day&limit=5",
            headers={"User-agent": "Route bot 0.1"},
        )

    subreddit_routes = response.json()
    subreddit_data = []
    for entry in subreddit_routes["data"]["children"]:
        score = entry["data"]["score"]
        title = entry["data"]["title"]
        link = entry["data"]["url"]
        subreddit_data.append(f"{str(score)}: {title} ({link})")
    return subreddit_data


@router.get("/ideas/async")
async def fetch_ideas_async(
    user: User = Depends(deps.get_current_active_superuser),
) -> dict:
    results = await asyncio.gather(
        *[get_reddit_top_async(subreddit=subreddit) for subreddit in Route_SUBREDDITS]
    )
    return dict(zip(Route_SUBREDDITS, results))


@router.get("/ideas/")
def fetch_ideas(reddit_client: RedditClient = Depends(deps.get_reddit_client)) -> dict:
    return {
        key: reddit_client.get_reddit_top(subreddit=key) for key in Route_SUBREDDITS
    }
