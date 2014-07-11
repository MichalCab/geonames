#!/bin/bash
#title           :generate_geonames.geo.sh
#description     :This script will make geonames.locations & geonames.museums.
#author          :Michal Cáb <xcabmi00@stud.fit.vutbr.cz>    
#usage           :./generate_geonames.sh

_old=`stat -c %y all_countries | sed 's/^\([0-9\-]*\).*/\1/'`
_now=$(date +"%m%d%Y%H%M%S")

# save old files
echo -e "Backup all data (links, alternateEnglishNames, allCountries, KB.geo) ... \n"
mkdir help
rm help/links 1>&2
rm help/alternate_english_names 1>&2
rm all_countries 1>&2
mv geonames.locations geonames.locations.${_old} 1>&2
mv geonames.museums geonames.museums.${_old} 1>&2
echo -e "(links, alternateEnglishNames, allCountries, KB.geo) Backuped \n"

# download allCountries
echo -e "- Download allCountries ...\n"
wget http://download.geonames.org/export/dump/allCountries.zip -O allCountries.${_now}.zip
unzip allCountries.${_now}.zip -d allCountriesDir.${_now}
mv allCountriesDir.${_now}/allCountries.txt all_countries
rm -r allCountriesDir.${_now} 1>&2
rm allCountries.${_now}.zip 1>&2
echo -e "allCountries downloaded \n "

# download links and alternateEnglishNames
echo -e "Download and generate links and alternateEnglishNames...\n"
wget http://download.geonames.org/export/dump/alternateNames.zip -O alternateNames.${_now}.zip
unzip alternateNames.${_now}.zip -d alternateNames.${_now}
mv alternateNames.${_now}/alternateNames.txt help/alternate_names 1>&2
rm -r alternateNames.${_now} 1>&2
rm alternateNames.${_now}.zip 1>&2

grep $'\tlink\t' help/alternate_names | awk -F $'\t' '{print $2"\t"$4}' | grep "http://en.wikipedia.org/wiki" > help/links
grep $'\ten\t' help/alternate_names | awk -F $'\t' '{print $4}' | sort -u > help/alternate_english_names

rm help/alternate_names 1>&2
echo -e "links and alternateEnglishNames downloaded and generated\n"


# download admin1CodesASCII.txt
rm help/admin1_codes_ascii 1>&2
wget http://download.geonames.org/export/dump/admin1CodesASCII.txt -O help/admin1_codes_ascii

echo -e "Generate geonames.locations... \n"
cat all_countries | ./filter_geonames.py -b -t location > geonames.locations 
if [ $? == 1 ]
then
  echo "error in script filter_geonames.py -b -t location"
  rm geonames.locations
  mv geonames.locations.${_old} geonames.locations
  exit 1
fi
echo -e "geonames.locations generated \n"

echo -e "Generate geonames.museums... \n"
cat all_countries | ./filter_geonames.py -b -t museum > geonames.museums
if [ $? == 1 ]
then
  echo "error in script filter_geonames.py -b -t museum"
  rm geonames.museums
  mv geonames.museums.${_old} geonames.museums
  exit 1
fi
echo -e "geonames.museums generated \n"
