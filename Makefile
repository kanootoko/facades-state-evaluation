env:
	cp env.example .env
	cp backend/.env.example backend/.env
	cp hosting/.env.example hosting/.env
	cp classifier/.env.example classifier/.env
	cp db.env.example db.env
	echo "Edit variables in .env-files (.env, db.env, backend/.env, hosting/.env and classifier/.env) as you need"