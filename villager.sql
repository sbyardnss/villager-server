UPDATE VILLAGER_CHESS_API_MESSAGE
SET date_time = "2023-06-01 21:22:25.057000"
WHERE id = 1

DELETE FROM villager_chess_api_tournament_competitors
WHERE id > 4

DELETE FROM villager_chess_api_tournament
WHERE id > 1

DELETE FROM villager_chess_api_game
WHERE id > 3

UPDATE villager_chess_api_tournament
SET rounds = 1
WHERE id = 15


DELETE FROM villager_chess_api_player
WHERE ID > 4

DELETE FROM auth_user
WHERE ID > 4



DELETE FROM authtoken_token 
WHERE USER_ID = 15

DELETE FROM villager_chess_api_player_friends where id > 13