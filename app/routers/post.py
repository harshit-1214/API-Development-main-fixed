import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_db
from app.model import Post as table
from app.model import User
from app.oauth2 import get_current_user
from app.schema import CreatePost, Post, PostBase, ResponsePost

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/posts", tags=["Post"])


@router.get("/", response_model=List[Post])
async def get_posts(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    result = await db.execute(select(table).where(table.title.contains(search)).limit(limit).offset(skip))
    posts = result.scalars().all()
    if len(posts) == 0 :
        logger.info("NO POST IS CREATED YET")
        raise HTTPException(status_code=status.HTTP_201_CREATED, detail="NO POST IS CREATED YET")
    logger.debug("posts listed count=%s limit=%s skip=%s search=%r user_id=%s", len(posts), limit, skip, search, current_user.id)
    return posts


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new post",
    description="Insert a post into the database and return the created record",
    response_model=ResponsePost,
)
async def create_post(post: CreatePost, db: AsyncSession = Depends(get_async_db), current_user: User = Depends(get_current_user)):
    new_post = table(**post.model_dump(), owner_id=current_user.id)
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    logger.info("post created id=%s by user_id=%s", new_post.id, current_user.id)
    return {"message": "Post Created Successfully", "data": new_post}


@router.get("/{id}", response_model=Post)
async def get_post(id: int, db: AsyncSession = Depends(get_async_db), current_user: User = Depends(get_current_user)):
    post = await db.get(table, id)
    if post is None:
        logger.info("post not found id=%s user_id=%s", id, current_user.id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NO POST IS FOUND")
    logger.debug("post fetched id=%s user_id=%s", id, current_user.id)
    return post


@router.get("/title/{title}", response_model=Post)
async def get_title(title: str, db: AsyncSession = Depends(get_async_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(table).where(table.title == title))
    post = result.scalars().first()
    if post is None:
        logger.info("post not found title=%r user_id=%s", title, current_user.id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tittle IS NO FOUND : {title} is not in list")
    logger.debug("post fetched title=%r user_id=%s", title, current_user.id)
    return post


@router.delete("/{id}")
async def delete_post(id: int, db: AsyncSession = Depends(get_async_db), current_user: User = Depends(get_current_user)):
    post = await db.get(table, id)
    if post is None:
        logger.info("delete skipped: post not found id=%s user_id=%s", id, current_user.id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": f"Post with ID : {id} Not Found"})
    if post.owner_id != current_user.id:
        logger.warning("delete denied: post id=%s owner_id=%s requester user_id=%s", id, post.owner_id, current_user.id)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"message": "Not allowed to delete this post"})

    await db.delete(post)
    await db.commit()
    logger.info("post deleted id=%s by user_id=%s", id, current_user.id)
    return {"message": "Post Deleted Successfully", "status code": status.HTTP_204_NO_CONTENT}


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all(db: AsyncSession = Depends(get_async_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(delete(table))
    await db.commit()
    logger.warning("ALL posts deleted count=%s by user_id=%s", result.rowcount, current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=ResponsePost)
async def update_post(id: int, updated_post: PostBase, db: AsyncSession = Depends(get_async_db), current_user: User = Depends(get_current_user)):
    post = await db.get(table, id)
    if post is None:
        logger.info("update skipped: post not found id=%s user_id=%s", id, current_user.id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NO Found")
    if post.owner_id != current_user.id:
        logger.warning("update denied: post id=%s owner_id=%s requester user_id=%s", id, post.owner_id, current_user.id)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"message": "Not allowed to update this post"})

    await db.execute(update(table).where(table.id == id).values(**updated_post.model_dump()))
    await db.commit()
    await db.refresh(post)
    logger.info("post updated id=%s by user_id=%s", id, current_user.id)
    return {"message": "Post Updated successfully", "data": post}