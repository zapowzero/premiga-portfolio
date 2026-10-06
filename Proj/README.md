# CMS — Company Management System (MYP, Group 4)

A desktop app that puts a company's everyday employee workflows in one place: login and registration, an employee contact list, request and approval, and an IT helpdesk. Built with Python and Tkinter for the Interactive Programming course, DME, Khon Kaen University.

## Features

| Feature | What it does |
|---|---|
| Login / Register | Sign in with an employee ID, an email name or a full email. Registration shows a progress bar, assigns an employee ID from the chosen position's range and checks password strength. |
| Contact List | Search employees by ID. Support and HR can edit records; everyone else sees name, position and email only. |
| Request & Approve | Send requests (with CC and an attachment) to any employee. The recipient can approve or deny them. |
| Helpdesk | Support staff see every reported problem, open its details and mark it finished. |
| Report | Any employee can report a hardware, software or network problem. |
| Profile | Click the emoji avatar to change it; click your name to see your profile. |

## Role-based access

| Position | ID range | Extra access |
|---|---|---|
| Support | 1001–1999 | Helpdesk, edit employee records |
| Board | 2001–2999 | — |
| Human Resources | 3001–3999 | Edit employee records |
| Manager | 4001–4999 | — |
| Worker | 5001–5999 | — |

## Run it

```bash
pip install Pillow tkcalendar
cd Proj/Submit
python login.py
```

The first run creates a `data/` folder with demo accounts. Passwords are stored hashed (PBKDF2-SHA256).

| Email | Password |
|---|---|
| support@myp.com | Support123 |
| board@myp.com | Board123 |
| hr@myp.com | Hr123456 |
| manager@myp.com | Manager123 |
| worker@myp.com | Worker123 |

## Project files

| File | Contents |
|---|---|
| `Submit/login.py` | Login and registration window, password hashing, data paths |
| `Submit/main_page.py` | Main app: contact list, request and approve, helpdesk, report, profile |
| `Project proposal_ CMS.docx` | Project proposal, objectives and timeline |
| `CMS_Flowchart.pdf` | Flowchart of the system |
| `User_diagram_Group4_MYP.pdf` | User diagram |
| `CMS_Group4_MYP.pdf` | GUI screen-flow diagram |

## Team

| Name | Responsibilities |
|---|---|
| Amon Oswald Hackl | Planning, register, contact list, user data |
| **Premiga Pengtap** | GUI, login page, main page, helpdesk |
| Yu Thandar Kyaw | UX/UI, report, error handling, main page, approval |

## Tech stack

Python · Tkinter · Pillow · tkcalendar · JSON storage · hashlib (PBKDF2)