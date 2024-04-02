DELETE FROM villager_chess_api_game
WHERE ID = 1691

DELETE FROM villager_chess_api_tournament_guest_competitors
WHERE tournament_id NOT IN (1, 158);