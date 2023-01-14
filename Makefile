env:
	cp env.example .env
	cp backend/.env.example backend/.env
	cp hosting/.env.example hosting/.env
	cp classifier/.env.example classifier/.env
	echo "Edit variables in .env-files (here, in backend, hosting and classifier) as you need"