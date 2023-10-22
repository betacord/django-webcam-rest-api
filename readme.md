# Webcam API

System umożliwiający operacje CRUD na referencjach do kamer internetowych dostępnych w sieci. 
Kamery podzielone są na kategorie oraz względem lokalizacji (kontynent/kraj). 
Zalogowani użytkownicy mogą dodawać komentarze do kamer. Odczytywać komentarze moga wszyscy użytkownicy.

Zalogowani użytkownicy mogą dodawać nowe kamery, a także komentarze pod nimi. 
Użytkownicy mogą dodawać także istniejące kamery do listy ulubionych.

Kategorie oraz lista krajów i kontynentów może być zarządzana jedynie przez administratora systemu.

## Aplikacje

### Core

Aplikacja przeznaczona na potrzeby wewnętrzne systemu.

### User

Modele

User
- ID
- Nick
- E-mail
- Password
- Favourites

### Locations

Modele

Continent
- ID
- Name

Country
- ID
- Name
- Continent

### Webcam

Modele

Webcam
- ID
- Name
- Description
- URL
- Image URL
- Coords
- Category
- Country
- Comments
- Added (date)
- Added (user)

Category
- ID
- Name

Comment
- ID
- User
- Content
- Date

## Stos technologiczny

System uruchamiany jest za pomocą narzędzia Docker compose, gdzie zawarte są następujące kontenery:
- app: REST API przygotowane w Django REST Framework
- db: relacyjna baza danych PostgreSQL

