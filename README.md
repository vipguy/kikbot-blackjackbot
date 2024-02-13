
kikbot
The Blackjack Room! 
 I'm here to enhance your chat experience with various fun and useful features. Here's a quick rundown:
Need help? Just Type: intro

BLACKJACK: 
 -Start a game with: 
 /bet <amount>. 
 

LEADERBOARD: 
 -Set Nickname:
 /nickname <name>
 -Check Leaderboard:
 /leaderboard   

YOUTUBE: 
 -Videos/Songs DL:
 /search <url> or <title/song>

WEATHER:
 -Temperature of city type:
 temp <city>.

CHUCK JOKES: 
 -Get jokes
 chuck.

WORD SCRAMBLE
 -Start a new game:
 /scramble
 -Guess the word:
 /sguess [your_guess]
 -Guess help
 /scramblehelp
 Rules:
  - Try to unscramble the word.
  - You have 3 attempts to guess the word.
  - Use hints wisely if needed.

CUSTOM TRIGGERS:
  -Create: 
  /save <word> <response>. 
  -Admins can view/delete:
  /listsave and /deletesave.

ANIMAL PICTURES:
 -Random animals:
 random fox, random monkey, monkey, cat, dog, panda, wolve, duck.

WELCOME MESSAGE
 -On user join message:
 /welcome <words>
 -View welcome:
 /getw
 -Remove welcome:
 /dwelcome  

## Deck Initialization ##
# Creates a standard deck of 52 cards with suits (Hearts, Diamonds, Clubs, Spades) and ranks (2-10, J, Q, K, A).
# Shuffles the deck randomly using the random.shuffle() function.
# Returns the shuffled deck for use in the game.

## Start Blackjack Game ##
# Initializes a game for a specific group and user if not already initialized.
# Checks if a game is already ongoing in the group. If not, starts a new round.
# Deducts the bet amount from the user's chips if a bet is placed and starts a new round.
# Sends messages to prompt users to place bets if necessary conditions are not met.

## Start New Blackjack Round ##
# Sets the game status as "in progress" and initializes a shuffled deck.
# Deals hands to the player and the dealer, updating their hands in the game state.
# Sets the current phase of the game to "player_turn" and informs the group about the game details.

## Check and Execute Dealer Play ##
# Triggers the dealer's play if all player hands are finished.
# Calls the dealer_play method to handle the dealer's turn and determine winners.

## Dealer Play ##
# Handles the dealer's turn by drawing cards until their hand score reaches or exceeds 17.
# Updates the dealer's hand in the game state and determines winners for each player's hand.
# Sends outcome messages to the group chat and ends the game by resetting the game state.

## Place Bet ##
# Deducts the bet amount from the user's chips if valid and updates the game state with the bet amount.
# Sends confirmation or error messages to the group chat based on the outcome.

## Stand ##
# Executes the dealer's play and determines winners after all player hands are finished.
# Sends outcome messages to the group chat and ends the game.

## Hit ##
# Draws a new card for the player's hand and updates the dealer's visible card.
# Determines outcomes based on the player's hand score and sends messages accordingly.

## Double Down ##
# Allows the player to double their bet and draw one additional card.
# Handles the outcome based on the player's hand score and updates the game state accordingly.

## Determine Winner ##
# Calculates scores for player and dealer hands and determines the winner for each hand.
# Updates player chip counts and constructs outcome messages for each hand.

## Show Leaderboard ##
# Fetches leaderboard data from the database for a specific group.
# Formats and displays the leaderboard information, including user nicknames and chip counts.

## Blackjack Database ##
# Manages user and group data, including chips, bets, and nicknames, using SQLite.
# Provides methods for database operations, concurrency control, and logging.

## Game State ##
# Stores the current state of each Blackjack game, including deck, player hands, and game phase.
# Initializes game state with default values for a new game.

## Send Heartbeat ##
# Sends periodic heartbeat messages to maintain connection and check status.
# Sends a status check message to a specified group or user at regular intervals.

## Start Heartbeat ##
# Initiates the heartbeat mechanism by creating a new thread for sending heartbeats.

