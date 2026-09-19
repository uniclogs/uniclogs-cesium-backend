docker:
	python -m pip wheel . -w build --no-deps
	docker compose build --build-arg VERSION=`grep -i 'version' pyproject.toml | cut -d'"' -f2`

hub:
	docker image tag cesium-api oresat/cesium-api:latest
	docker image tag cesium-api oresat/cesium-api:`grep -i 'version' pyproject.toml | cut -d'"' -f2`
	docker push --all-tags oresat/cesium-api

tiles:
	mkdir -p geo-tiles
	wget https://eoimages.gsfc.nasa.gov/images/imagerecords/74000/74218/world.200412.3x21600x10800.png -O geo-tiles/world.png
	gdal_translate -of GTiff -a_srs EPSG:4326 -a_ullr -180 90 180 -90 geo-tiles/world.png geo-tiles/world.tif
	gdal2tiles.py geo-tiles/world.tif geo-tiles/tiles -p geodetic --tmscompatible --process=4
	find geo-tiles -type d -exec chmod 700 {} \;
	find geo-tiles -type f -exec chmod 600 {} \;

clean:
	rm -rf build cesium_api.egg-info
	pyclean