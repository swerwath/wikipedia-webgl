echo Cleaning old data...
rm -rf data/raw/* data/processed/*
echo Downloading latest Wikipedia location data...
curl -o data/raw/dump.sql.gz https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-geo_tags.sql.gz
echo Extracting data...
gzip -d data/raw/dump.sql.gz
echo Performing inital data formatting...
sed -i "" "s/),(/~/g" data/raw/dump.sql
tr '~' '\n' < data/raw/dump.sql > data/processed/processed_tmp.txt
rm data/raw/dump.sql

echo Done
