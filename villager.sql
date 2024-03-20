UPDATE VILLAGER_CHESS_API_MESSAGE
SET date_time = "2023-06-01 21:22:25.057000"
WHERE id = 1

DELETE FROM villager_chess_api_tournament_competitors
WHERE id = 49

DELETE FROM villager_chess_api_tournament
WHERE id > 1

DELETE FROM villager_chess_api_tournament_guest_competitors
WHERE id = 33

DELETE FROM villager_chess_api_game
WHERE id = 1643

UPDATE villager_chess_api_tournament
-- SET pairings = '[{"round": 1, "match": 1, "player1": 3, "player2": "g5"}, {"round": 1, "match": 2, "player1": 4, "player2": 6}, {"round": 1, "match": 3, "player1": 1, "player2": "g8"}, {"round": 1, "match": 4, "player1": "g1", "player2": null}]'
SET rounds = 1
WHERE ID = 16


DELETE FROM villager_chess_api_player
WHERE ID > 4

DELETE FROM auth_user
WHERE ID > 4

update villager_chess_api_tournament
SET complete = false
Where id = 1

DELETE FROM villager_chess_api_guestplayer
WHERE id >11

DELETE FROM villager_chess_api_chessclub_guest_members
WHERE guestplayer_id > 8


DELETE FROM authtoken_token 
WHERE USER_ID = 15

DELETE FROM villager_chess_api_player_friends where id > 13

UPDATE villager_chess_api_game
SET PGN = '1. d4 a5 2. Bf4 Nf6 3. e3 e6 4. Nc3 a4 5. Nb5 Ba3 6. Nxc7+ Ke7 7. Nxa8 Ng4 8. Qxg4 g6 9. bxa3 b6 10. Bb5 h6 11. Bg5+ Ke8 12. Bxd8 Ba6 13. Bxb6 f6 14. Bxa6 Rh7 15. Qxg6+ Ke7 16. Qxh7+ Ke8 17. Bc5 f5'
-- SET win_style = '' 
-- SET PGN = '1. d4 a5 2. Bf4 Nf6 3. e3 e6 4. Nc3 a4 5. Nb5 Ba3 6. Nxc7+ Ke7 7. Nxa8 Ng4 8. Qxg4 g6 9. bxa3 b6 10. Bb5 h6 11. Bg5+ Ke8 12. Bxd8 Ba6 13. Bxb6 f6 14. Bxa6 Rh7 15. Qxg6+ Ke7 16. Qxh7+ Ke8 17. Bc5 f5', win_style = '', target_winner_ct_id= NULL, target_winner_id=NULL
-- SET win_style = 'checkmate'
WHERE ID = 144

UPDATE villager_chess_api_game
SET win_style = ''
WHERE ID = 131

DELETE FROM villager_chess_api_game
WHERE id = 1613


DROP TABLE villager_chess_api_tournament_competitors




UPDATE villager_chess_api_tournament
SET pairings = '{"round": 1, "match": 1, "player1": 3, "player2": "g7"}, {"round": 1, "match": 2, "player1": "g5", "player2": 4}, {"round": 1, "match": 3, "player1": 2, "player2": "g1"}, {"round": 1, "match": 4, "player1": 1, "player2": null}, {"round": 2, "match": 1, "player1": 2, "player2": "g5"}, {"round": 2, "match": 2, "player1": 1, "player2": "g1"}, {"round": 2, "match": 3, "player1": 4, "player2": 3}, {"round": 2, "match": 4, "player1": "g7", "player2": null}, {"round": 3, "match": 1, "player1": "g5", "player2": "g1"}, {"round": 3, "match": 2, "player1": "g7", "player2": 2}, {"round": 3, "match": 3, "player1": 1, "player2": 4}, {"round": 3, "match": 4, "player1": 3, "player2": null}, {"round": 4, "match": 1, "player1": 3, "player2": "g1"}, {"round": 4, "match": 2, "player1": 1, "player2": "g5"}, {"round": 4, "match": 3, "player1": "g7", "player2": 4}, {"round": 4, "match": 4, "player1": 2, "player2": null}'
WHERE id = 79

UPDATE villager_chess_api_tournament
-- SET pairings = '[{"round": 1, "match": 1, "player1": 3, "player2": "g7"}, {"round": 1, "match": 2, "player1": "g5", "player2": 4}, {"round": 1, "match": 3, "player1": 2, "player2": "g1"}, {"round": 1, "match": 4, "player1": 1, "player2": null}, {"round": 2, "match": 1, "player1": 2, "player2": "g5"}, {"round": 2, "match": 2, "player1": 1, "player2": "g1"}, {"round": 2, "match": 3, "player1": 4, "player2": 3}, {"round": 2, "match": 4, "player1": "g7", "player2": null}, {"round": 3, "match": 1, "player1": "g5", "player2": "g1"}, {"round": 3, "match": 2, "player1": "g7", "player2": 2}, {"round": 3, "match": 3, "player1": 1, "player2": 4}, {"round": 3, "match": 4, "player1": 3, "player2": null}, {"round": 4, "match": 1, "player1": 3, "player2": "g1"}, {"round": 4, "match": 2, "player1": 1, "player2": "g5"}, {"round": 4, "match": 3, "player1": "g7", "player2": 4}, {"round": 4, "match": 4, "player1": 2, "player2": null}]'
-- SET rounds = 1


SET pairings = '[{"round": 1, "match": 1, "player1": "g74", "player2": 5}, {"round": 1, "match": 2, "player1": "g73", "player2": "g72"}, {"round": 1, "match": 3, "player1": 1, "player2": null}]'
WHERE id = 151;