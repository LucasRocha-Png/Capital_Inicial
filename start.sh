echo "-------------RODANDO APLICATIVO-------------"
python3 src/main.py
echo "-------------SAIDA LOG-------------"
cat data/log.txt
echo "-------------TABLES DATABASE-------------"
sqlite3 data/database.db ".tables"
echo "-------------PESSOAS TABLE-------------"
sqlite3 data/database.db "SELECT * FROM PESSOA;"
echo "-------------CARTEIRA TABLE-------------"
sqlite3 data/database.db "SELECT * FROM CARTEIRA;"
echo "-------------BOLETA TABLE-------------"
sqlite3 data/database.db "SELECT * FROM BOLETA;"
echo "-------------ACAO TABLE-------------"
sqlite3 data/database.db "SELECT * FROM ACAO;"