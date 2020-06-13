wget https://tse.go.cr/zip/padron/padron_completo.zip
unzip padron_completo.zip
iconv -f iso-8859-1 -t utf-8 -o Distelec.txt.utf8 Distelec.txt
iconv -f iso-8859-1 -t utf-8 -o PADRON_COMPLETO.txt.utf8 PADRON_COMPLETO.txt
fromdos Distelec.txt.utf8 
fromdos PADRON_COMPLETO.txt.utf8
awk -f ./separardist.awk Distelec.txt.utf8
awk -f prepararpersonas.awk PADRON_COMPLETO.txt.utf8
createdb padron
psql padron -f estructura.sql
psql padron <<eow
\copy provincia FROM './provincias.txt' CSV ;
\copy canton FROM './cantones.txt' CSV ;
\copy distrito FROM ./distritos.txt CSV;
\copy ciudadano FROM ./personas.txt CSV;
eow
