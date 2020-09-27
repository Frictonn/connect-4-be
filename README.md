# connect-4-be
Connect 4 BE


# Connect 4 

## Create a new Game

```
POST /api/games
```


**Response**

```json
{
    "id": "64a87e83-f39b-41fc-b4c5-ef8741eaf190",
    "status": "initialized",
    "winner": ""
}
```


## Get all moves for a game

```
GET /api/games/:game_id/moves
```


**Response**

```json
[
    {
        "id": "e55f01aa-ecf9-44f4-b885-67f1be452754",
        "column": 5,
        "coin": "red",
        "created_at": "2020-09-27T18:07:11.873054Z",
        "row": 1,
        "game_status": "initialized",
        "game_winner": ""
    },
    {
        "id": "7b759bb3-a085-41e3-828a-7f5e2afd6bea",
        "column": 5,
        "coin": "yellow",
        "created_at": "2020-09-27T18:07:01.751374Z",
        "row": 0,
        "game_status": "initialized",
        "game_winner": ""
    }
]
```


## Make a move  for a game

```
POST /api/games/:game_id/moves
```

**Response**
{
    "column": 5,
    "coin": "red"
}

**Response**

```json
{
    "id": "e55f01aa-ecf9-44f4-b885-67f1be452754",
    "column": 5,
    "coin": "red",
    "created_at": "2020-09-27T18:07:11.873054Z",
    "row": 1,
    "game_status": "initialized",
    "game_winner": ""
}
```
