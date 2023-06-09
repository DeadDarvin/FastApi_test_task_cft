up:
	sudo docker compose -f docker-compose-local.yaml up -d

down:
	sudo docker compose -f docker-compose-local.yaml down && sudo docker network prune --force


run:
	sudo docker compose -f docker-compose-ci.yaml up -d

stop:
	sudo docker compose -f docker-compose-ci.yaml down && sudo docker network prune --force

enter:
	sudo docker exec -it cft_test_app bash
