BEGIN {
  LASTP=""
  LASTC=""
  FS=","
  OFS=","
}
$2 != LASTP {
  print substr($1,1,1),$2 > "provincias.txt"
}
$3 != LASTC {
  print substr($1,1,1),substr($1,2,2),$3 > "cantones.txt"
}
{
  print substr($1,1,1),substr($1,2,2),substr($1,4,3),gensub(/\ +$/,"","g",$4) > "distritos.txt"
  LASTP=$2
  LASTC=$3
}
