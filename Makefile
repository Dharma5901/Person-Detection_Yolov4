build:
	docker-compose build
	
start:
	docker-compose run -d --name ${condo} person_detection
	

follow: start
	docker-compose logs -f

stop:
	docker-compose down

usage:
	$(info make start condo=<Name of the condo> config_file=<configuration file of the specified residency>) @true
	$(info Example : make start condo=mpa residency_name=virtual_dataset config_file=mpa.json) @true