# Paralympic Athletes — Django Web App (DME Studio 3)

A website for browsing and managing Paralympic athletes and events. Anyone can browse athletes, search them and see event details. Logged-in staff can add, edit and delete athletes and events.

## Features

| Page | What it does |
|---|---|
| Home | Hero banner and quick links |
| Players | Athlete list with ID, country, classification and date of birth, 25 per page |
| Search | Search by name (partial or full name), ID, country, classification or gender |
| Events | Event list and detail pages with date, time, location, sport and the players taking part |
| FAQ | Common questions about the site |
| Staff login | Add, edit and delete athletes and events (login required) |

## Run it

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py import_members      # loads 100 athletes from members/Athlests.member.csv
python manage.py createsuperuser     # your staff account
python manage.py runserver
```

Open http://127.0.0.1:8000. Log in at `/members/login/` with the account you created.

`import_members` can be run again at any time. It updates athletes that already exist instead of adding copies, and merges duplicates left by older imports.

## Tests

```bash
python manage.py test members
```

The tests cover: the login redirect, partial-name and gender search, keeping an athlete's gender when editing, pagination, removing every player from an event, and importing twice without duplicates.

## Project structure

```
backend/
├── manage.py
├── myWeb/            settings and root URLs
├── members/          models (Member, Event), views, forms, import command, tests
├── templates/members/ pages (base layout, lists, forms, detail, search, FAQ, login)
└── static/images/    logo, hero and athlete photos
```

## Tech stack

Python · Django · SQLite · HTML/CSS (Django templates)