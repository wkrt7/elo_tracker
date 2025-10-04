my todos

- [ ] ---CICD deployment to aws or gcp of backend---
- [x] connect to supabase from python script
- [x] how to simplify this, do i need matchParticipants, TeamParticipants etc? I don't think so
- [ ] run in serverless environment AWS lambda + API Gateway
- [x] run in vercel, fast api is ready already, test if this will be free
- [ ] create a deployment by github acitons
- [ ] solve warning in main while adding the match
- [ ] !!secure this wit jwt or oath!!
- [ ] refractor elo computation

poorject tree generator
https://tree.nathanfriend.com/?s=(%27options!(%27fancy!true~fullPath!false~trailingSlash!true~rootDot!false)~4(%274%27elo_tracker*api3crud3models3schemas3_init__5app5config.py-3requirements.tx02oo0level*forntend%202eac0fron0end*test*pyproject.toml*vercel.json%27)~version!%271%27)*%5Cn--%20%200t%202%23%20r3*-4source!5.py3%0154320-*

elo_tracker
api
crud
models
schemas
\_init\_\_.py
app.py
config.py
 requirements.txt # root level
forntend # react front end
test
pyproject.toml
vercel.json

elo_tracker/
├── api/
│ ├── crud
│ ├── models
│ ├── schemas
│ ├── \_init\_\_.py
│ ├── app.py
│ ├── config.py
│ └── requirements.txt # root level
├── forntend # react front end
├── test
├── pyproject.toml
└── vercel.json
