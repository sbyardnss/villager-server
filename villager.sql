UPDATE VILLAGER_CHESS_API_MESSAGE
SET date_time = "2023-06-01 21:22:25.057000"
WHERE id = 1

DELETE FROM villager_chess_api_tournament_competitors
WHERE tournament_id > 1

DELETE FROM villager_chess_api_tournament
WHERE id > 1

DELETE FROM villager_chess_api_tournament_guest_competitors
WHERE tournament_id > 1

DELETE FROM villager_chess_api_game
WHERE id =22

UPDATE villager_chess_api_tournament
SET complete = 0
WHERE ID = 1


DELETE FROM villager_chess_api_player
WHERE ID > 4

DELETE FROM auth_user
WHERE ID > 4

update villager_chess_api_tournament
SET rounds = 2
Where id = 1

DELETE FROM villager_chess_api_chessclub_guest_members
WHERE ID = 3

DELETE FROM authtoken_token 
WHERE USER_ID = 15

DELETE FROM villager_chess_api_player_friends where id > 13

UPDATE villager_chess_api_game
-- SET PGN = '1. d4 a5 2. Bf4 Nf6 3. e3 e6 4. Nc3 a4 5. Nb5 Ba3 6. Nxc7+ Ke7 7. Nxa8 Ng4 8. Qxg4 g6 9. bxa3 b6 10. Bb5 h6 11. Bg5+ Ke8 12. Bxd8 Ba6 13. Bxb6 f6 14. Bxa6 Rh7 15. Qxg6+ Ke7 16. Qxh7+ Ke8 17. Bc5 f5'
-- SET win_style = '' 
-- SET PGN = '1. d4 a5 2. Bf4 Nf6 3. e3 e6 4. Nc3 a4 5. Nb5 Ba3 6. Nxc7+ Ke7 7. Nxa8 Ng4 8. Qxg4 g6 9. bxa3 b6 10. Bb5 h6 11. Bg5+ Ke8 12. Bxd8 Ba6 13. Bxb6 f6 14. Bxa6 Rh7 15. Qxg6+ Ke7 16. Qxh7+ Ke8 17. Bc5 f5', win_style = '', target_winner_ct_id= NULL, target_winner_id=NULL
SET win_style = 'checkmate'
WHERE ID = 5

UPDATE villager_chess_api_game
SET win_style = ''
WHERE ID = 131

DELETE FROM villager_chess_api_game
WHERE tournament_id = 32


DROP TABLE villager_chess_api_tournament_competitors