env:
	cp env.example .env
	cp backend/.env.example backend/.env
	cp hosting/.env.example hosting/.env
	echo "Edit variables in .env-files (here, in backend and hosting) as you need"