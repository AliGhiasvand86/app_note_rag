# FastAPI application

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.agent.graph import graph
from src.database import get_connection
from src.note_edit_service import edit_note, remove_note
from src.note_service import get_user_notes


app = FastAPI(
    title="Notes AI API",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AgentRequest(BaseModel):
    user_id: int
    message: str


class AgentResponse(BaseModel):
    response: str


class LoginRequest(BaseModel):
    username: str


class LoginResponse(BaseModel):
    user_id: int
    username: str


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: str
    updated_at: str


class NoteUpdateRequest(BaseModel):
    user_id: int
    title: str
    content: str


@app.post(
    "/login",
    response_model=LoginResponse,
)
def login(
    request: LoginRequest,
) -> LoginResponse:
    """Find an existing user or create a new user by username."""

    username = request.username.strip()

    if not username:
        raise HTTPException(
            status_code=400,
            detail="Username cannot be empty.",
        )

    connection = get_connection()

    user = connection.execute(
        """
        SELECT id, username
        FROM users
        WHERE username = %s
        """,
        (username,),
    ).fetchone()

    if user is None:
        user = connection.execute(
            """
            INSERT INTO users (username)
            VALUES (%s)
            RETURNING id, username
            """,
            (username,),
        ).fetchone()

        connection.commit()

    connection.close()

    return LoginResponse(
        user_id=user[0],
        username=user[1],
    )


@app.post(
    "/register",
    response_model=LoginResponse,
)
def register(
    request: LoginRequest,
) -> LoginResponse:
    """Create a new user with a unique username."""

    username = request.username.strip()

    if not username:
        raise HTTPException(
            status_code=400,
            detail="Username cannot be empty.",
        )

    connection = get_connection()

    user = connection.execute(
        """
        SELECT id, username
        FROM users
        WHERE username = %s
        """,
        (username,),
    ).fetchone()

    if user is not None:
        connection.close()

        raise HTTPException(
            status_code=409,
            detail="Username already exists.",
        )

    user = connection.execute(
        """
        INSERT INTO users (username)
        VALUES (%s)
        RETURNING id, username
        """,
        (username,),
    ).fetchone()

    connection.commit()
    connection.close()

    return LoginResponse(
        user_id=user[0],
        username=user[1],
    )


@app.post(
    "/agent",
    response_model=AgentResponse,
)
def run_agent(
    request: AgentRequest,
) -> AgentResponse:
    """Run the LangGraph agent for a user."""

    result = graph.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": request.message,
                }
            ]
        },
        config={
            "configurable": {
                "user_id": request.user_id,
            }
        },
    )

    return AgentResponse(
        response=result["messages"][-1].content,
    )


@app.get(
    "/notes",
    response_model=list[NoteResponse],
)
def list_notes(
    user_id: int,
) -> list[NoteResponse]:
    """Return all notes belonging to a user."""

    notes = get_user_notes(user_id)

    return [
        NoteResponse(
            id=note[0],
            title=note[1],
            content=note[2],
            created_at=str(note[3]),
            updated_at=str(note[4]),
        )
        for note in notes
    ]


@app.put(
    "/notes/{note_id}",
    response_model=NoteResponse,
)
def edit_note_endpoint(
    note_id: int,
    request: NoteUpdateRequest,
) -> NoteResponse:
    """Update a user's note and synchronize its RAG index."""

    updated = edit_note(
        user_id=request.user_id,
        note_id=note_id,
        title=request.title,
        content=request.content,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Note not found.",
        )

    notes = get_user_notes(request.user_id)

    note = next(
        note
        for note in notes
        if note[0] == note_id
    )

    return NoteResponse(
        id=note[0],
        title=note[1],
        content=note[2],
        created_at=str(note[3]),
        updated_at=str(note[4]),
    )


@app.delete(
    "/notes/{note_id}",
)
def delete_note_endpoint(
    note_id: int,
    user_id: int,
) -> dict:
    """Delete a user's note and its RAG chunks."""

    deleted = remove_note(
        user_id=user_id,
        note_id=note_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Note not found.",
        )

    return {
        "message": "Note deleted successfully.",
        "note_id": note_id,
    }
