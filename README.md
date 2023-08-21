# FlaskCard-App

## Description

A Web2 FlashCard App, that allows User to CRUD the flash Cards, based on his/her choices, that would help them in Memorization of any subject of their Choice, For this I have created 3 DB Models, USERS, DECKS, CARDS
use of APIs to undergo CRUD Operations for Users to add,create, update delete of cards for memory learning.
A many-to- many relationship is established between Users and Decks, connected by uid so
That each and every deck created could be uniquely identified by any user.
All Cards are stored in Cards Database and each card is uniquely identified by card_no and
Also each card has a deck_id (Which would let us identify each card’s parent deck and in turn we would also know which user created that card.
I have also implemented the APIs, YAML File is attached below for reference, POSTMAN can be used to hit the APIs, and execute the CRUD on the Cards.

## API DESIGN

User -> POST (API for Creating a new User)
Deck -> GET(Retrieves All the Decks created by a User)
          ->POST(Creating a New Deck)
          ->PUT(Updating the Name of a Particular Deck)
          ->DELETE(Deleting the Deck& all the Cards inside that Deck)
Cards->GET(Gets all the Cards inside a deck  created by a user)
	POST(Adding new Cards to a deck by some User)
	PUT(Updating a Particular card by card_no by a User)
	DELETE(Deleting a card in a deck by the card number)
Score -> GET (Retrieves the Average Score of the Deck(Last visited Score)

## Executing the Program

1. Clone the Repo
2. Install flask, flask_restful and flask_sqlalchemy
3. Run main.py
4. After the Server starts goto localhost and try it out.(user_1 & user_2) are created by default for you.

## Authors
RAJ SIRUVANI

