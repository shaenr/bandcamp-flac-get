#!/bin/bash

touch album_links.txt

if [ -z "$1" ]; then
  echo "usage:"
  echo "    $0 <url>"
  echo ""
  echo "<url> can be domain.tld or domaine.tld/music"
  exit
fi

base=$(echo $1 | sed -e "s/\/$//")

urls=$(curl $base -o /tmp/bandcamp_out &> /dev/null ; cat /tmp/bandcamp_out | grep "href=\"/album" | cut -d"\"" -f2)

base=$(echo $base | sed -e "s/\/music$//")

echo "Writing album links to file..."
for url in $urls; do
#   echo "Downloading $(echo $url | sed -e "s/^\/album\///g") album..."
  echo $base$url >> album_links.txt
  if [ $? -ne 0 ]; then
    echo "Are you sure that $base$url is a valid album url?"
    exit
  fi
done

cat album_links.txt
