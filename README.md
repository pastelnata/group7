# Book Recommendation & Search System
This project was developed during our 4th semester at university. The objective of this application is to provide users with a search engine & recommendation system for books.

## Key features:
- **Search Engine & Autocomplete:** the user can search by book by author, title or genre.
- **Recommendation based on search:** besides the search results, a list of recommended books based on genre is displayed, along with author recommendations.
- **Recommendation based on preferences:** the user can select preferences (tags, price, genre, rating) and get related book recommendations.
- **Top 10 books by genre:** the user can look through top 10 books by category.
- **Sorting:** the user can sort books by relevance, rating and price.
- **Lucky Charm:** if the user is unsure about their preferences, they can visit the Lucky Charm page, which recommends random books.

## Tools used
- Python: coding language
- html: for structuring the content
- css: for styling the website
- Django: web framework
- jQuery: for autocomplete
- Bootstrap: for styling some pages
- coverage.py: for measuring code coverage in test execution
- pandas: for organizing the dataset
- Amazon kaggle dataset: books dataset that was used

## Project Setup & Running Locally
### Prerequisites:
- Python 3.11+  
  Install from [python.org](https://www.python.org/downloads/)

- Django  
  ```
  pip install django
  ```

- pandas  
  ```
  pip install pandas
  ```

- coverage.py  
  ```
  pip install coverage
  ```

### Running the project:
1. Ensure you are in the correct folder: group7/BookRecommendationSystem
2. write in the terminal: ``` python manage.py makemigrations ```
3. write in the terminal: ``` python manage.py migrate ```
4. write in the terminal: ``` python manage.py runserver ```
5. To access the application: go to http://127.0.0.1:8000

To stop the application simply kill the terminal where the application is currently running on.

## Pull Request Guidelines

These guidelines make the review process easier, so try to use it :)

### Title Format
- For new features, use: `feat: [Feature Name]`
- For bug fixes, use: `fix: [Bug Description]`
- For code refactoring (improvement of code that was already there): `refactor: [Part of Code or Component]`

### Description
- Write a small description of the changes implemented in the PR, if the title is not clear enough:
  - Include what behavior you expect from your changes / how its supposed to look like.
  - Add a screenshot if it's a UI change.

### Before Submitting
- Ensure your branch is up to date by **rebasing** or **merging** the latest changes.

## Project developed by:
- [Rita Braunschweig](https://github.com/pastelnata)
- [Adriana Jaworska](https://github.com/Adziaaa)
- [Beatrice-Teodora Cimpanu](https://github.com/BeatriceCimpanu)
- [Filip Andrei Sima](https://github.com/filipsima)
- [Iana Pavliuk](https://github.com/kramoda)
- [Kornelia Madela](https://github.com/kornaa)