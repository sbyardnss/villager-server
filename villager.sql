UPDATE VILLAGER_CHESS_API_MESSAGE
SET date_time = "2023-06-01 21:22:25.057000"
WHERE id = 1

DELETE FROM villager_chess_api_tournament_competitors
WHERE id > 110

DELETE FROM villager_chess_api_tournament
WHERE id > 21

DELETE FROM villager_chess_api_game
WHERE id = 437

UPDATE villager_chess_api_tournament
SET rounds = 1
WHERE ID = 14


DELETE FROM villager_chess_api_player
WHERE ID > 4

DELETE FROM auth_user
WHERE ID > 4



DELETE FROM authtoken_token 
WHERE USER_ID = 15

DELETE FROM villager_chess_api_player_friends where id > 13

UPDATE villager_chess_api_game
-- SET PGN = '1. d4 a5 2. Bf4 Nf6 3. e3 e6 4. Nc3 a4 5. Nb5 Ba3 6. Nxc7+ Ke7 7. Nxa8 Ng4 8. Qxg4 g6 9. bxa3 b6 10. Bb5 h6 11. Bg5+ Ke8 12. Bxd8 Ba6 13. Bxb6 f6 14. Bxa6 Rh7 15. Qxg6+ Ke7 16. Qxh7+ Ke8 17. Bc5 f5'
-- SET win_style = '' 
SET winner_id = null, PGN = '1. d4 a5 2. Bf4 Nf6 3. e3 e6 4. Nc3 a4 5. Nb5 Ba3 6. Nxc7+ Ke7 7. Nxa8 Ng4 8. Qxg4 g6 9. bxa3 b6 10. Bb5 h6 11. Bg5+ Ke8 12. Bxd8 Ba6 13. Bxb6 f6 14. Bxa6 Rh7 15. Qxg6+ Ke7 16. Qxh7+ Ke8 17. Bc5 f5', win_style = '' 
WHERE ID = 426

UPDATE villager_chess_api_game
SET win_style = ''
WHERE ID = 131