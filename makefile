all:
	@echo "Options are bmo, tar or clean"

#targets
bmo:
	docker image build --rm -t localhost:5000/python-docker-sm .

tar:
	docker save -o python-docker-sm.tar localhost:5000/python-docker-sm
	cp python-docker-sm.tar /mnt/nas/docker_images/python-docker-sm.tar
	ls -Alh /mnt/nas/docker_images/

run:
	docker run --rm --name "bmo" -v /root/bmo_data:/opt/data localhost:5000/python-docker-sm

clean:
	docker system prune
	docker rmi $(docker images -f "dangling=true" -q)

