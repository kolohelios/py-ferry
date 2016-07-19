# py-ferry

## What is it?
Right now, not much of anything; just a concept. I ride the Seattle - Bainbridge Island ferry each day and I am impressed with the smoothness of the operation. I also like simulation and strategy games. Among my favorites are SimCity, Civ, Pharaoh, Cities: Skylines, and so on. I also like more casual games like Mini Metro. I guess the scale doesn't matter to me as much as having some resource, business, or economic element.

## Where can I learn more?
There are some images in the /notes folder that are photos that were taken from some hand-written notes from a whiteboard and a notebook.

## Sidelines

* add storage for finished game (stats and history)
* score board (not that interesting to me)
* upgrades to ferries
* terminal purchase and upgrades
    * start with passenger terminal and then upgrade to handle vehicles later
* dashboard upgrades
* ferry upgrades
    * LPG
    * speed
    * galley
    * services
    * more tall spaces

## REST API Endpoints
### /api - base URI
no endpoints

### /api/terminals
GET - returns all of the terminals available

### /api/ferry_classes
GET - returns all of the ferry classes available

### /api/games
GET - returns all games for a user
POST - create a game for user

### /api/games/{game ID}
GET - returns a player's game
DELETE - destroy a game for user

### /api/games/{game ID}/endturn
GET ends the current week's turn

### /api/games/{game ID}/ferries
GET - returns all of a player's ferries
POST - buy ferry

### /api/games/{game ID}/ferries/{ferry ID}
GET - ferry details (unknown if this will be used)
DELETE - sell ferry

### /api/games/{game ID}/routes
GET - returns all routes for a player's game
POST - create route

### /api/games/{game ID}/routes/{route ID}
GET - returns a single route for a player's game
PUT - update route
DELETE - destroy route
