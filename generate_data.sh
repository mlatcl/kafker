python -m kafker register -n markus
python -m kafker register -n fanboy
python -m kafker register -n nena
sleep 3s

python -m kafker follow -a fanboy -p markus --follow
python -m kafker follow -a fanboy -p nena --follow
python -m kafker follow -a markus -p nena --follow

python -m kafker post -a markus -t "Coffee is good."
python -m kafker post -a markus -t "Coffee is even better."
python -m kafker post -a markus -t "Why not Zoidberg?"
python -m kafker post -a markus -t "Mein Maserati fährt 210."
python -m kafker post -a nena -t "99 Luftballons auf ihrem Weg zum Horizont..."
python -m kafker follow -a fanboy -p nena --unfollow
python -m kafker follow -a fanboy -p nena --follow
python -m kafker post -a nena -t "... hielt man für Ufos aus dem all..."
python -m kafker post -a nena -t "... darum schickte ein General..."
