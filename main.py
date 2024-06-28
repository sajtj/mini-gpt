from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends, HTTPException, status
from datetime import timedelta
from schemas import UserBase, Token, Query, QueryBase
from langchain_handeler import get_llm_response
from database import get_db
from crud import authenticate_user, create_access_token, get_current_user, get_user, create_user, get_queries, create_query, ACCESS_TOKEN_EXPIRE_MINUTES

app = FastAPI()

@app.post("/api/register/", response_model=UserBase) 
async def register(user: UserBase, db: AsyncSession = Depends(get_db)):
    db_user = await get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    created_user = await create_user(db=db, user=user)
    return  created_user


@app.post("/api/login/", response_model=Token)
async def login(user: UserBase, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, user.username)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/llm/", response_model=Query)
async def llm(prompt_request: QueryBase, db: AsyncSession = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    result = await get_llm_response(prompt_request.prompt)
    response_text = result.generations[0][0].text
    tokens = result.llm_output.get("token_usage").get("total_tokens")
    model_name = result.llm_output.get("model_name")
    created_query = await create_query(db=db, prompt=prompt_request.prompt, response=response_text, tokens=tokens, llm_name=model_name, user_id=current_user.id)
    return created_query


@app.get("/usage/", response_model=list[Query])
async def usage(db: AsyncSession = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    try :
        queries = await get_queries(db, user_id=current_user.id)
        return queries
    except :  
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not exist.")

