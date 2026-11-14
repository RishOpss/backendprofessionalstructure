# frontend

## Stack
React 19, Vite, JavaScript (JSX), CSS

## Project Type
Frontend UI

## Commands
- `npm install` (dependencies)
- `npm run dev` (development server, http://localhost:5173)
- `npm run build` (production build to `dist/`)
- `npm run preview` (preview production build locally)

## Layout
```
src/
  config/
    index.js          API base URL (defaults to http://localhost:8000/api/v1)
  api/
    courses.js        raw fetch calls (GET /, POST /, DELETE /{id})
  services/
    courseService.js  thin service layer wrapping API calls
  components/
    CourseForm.jsx    create new course (id, name, duration)
    CourseList.jsx    list all courses in a card grid
    CourseCard.jsx    single course card with delete button
  pages/
    HomePage.jsx      combines form and list
  styles/
    main.css          full styling (layout, cards, forms, buttons)
  App.jsx             entry point
  main.jsx            React mount point
```

## Conventions
- Three-layer architecture: `config` → `api` → `services` → `components` → `pages`
- API base URL from `VITE_API_URL` env variable (fallback: `http://localhost:8000/api/v1`)
- No framework CSS — plain CSS only
