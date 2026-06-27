# Business Analytics & AI — Knowledge Test

An interactive, self-contained quiz web app testing understanding of core
business analytics and AI concepts (definitions, concepts, and applications) —
analytics types, machine learning, generative AI, data infrastructure,
statistics and AI ethics. Content is generic and based on widely available
course/textbook material (no proprietary case study).

- **100-question bank**, with **20 drawn at random** each attempt
- A built-in **knowledge base** (`reference.html`): 16 in-depth topic sections with diagrams and links to free, open-access source documents (NIST, scikit-learn, OpenIntro, ISL, the Deep Learning Book, EUR-Lex GDPR, and more). Every question's feedback links straight to the relevant section.
- Answer options are **shuffled** every run, so no two tests are identical
- Instant right/wrong feedback with a short explanation after each question
- Progress bar, live score, and an end-of-test breakdown
- Pure HTML/CSS/JS in a single file — no server, build step, or dependencies

## Play it

If published with GitHub Pages, the live link is:

`https://<your-username>.github.io/<repo-name>/`

## Publish on GitHub Pages (no command line)

1. Sign in to GitHub and click **New repository**. Name it (e.g. `analytics-quiz`), set it **Public**, and create it.
2. On the repo page, click **Add file → Upload files**, then drag in `index.html` (and optionally this `README.md`). Commit.
3. Go to **Settings → Pages**.
4. Under **Build and deployment**, set **Source = Deploy from a branch**, **Branch = main**, **Folder = / (root)**, and **Save**.
5. Wait ~1 minute, then refresh. The page shows your public URL. Share that link with anyone.

## Publish via command line (alternative)

```bash
git init
git add index.html README.md
git commit -m "Add analytics quiz"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

Then enable Pages under **Settings → Pages** as in step 3 above.

## Notes

- The file must be named **`index.html`** for the bare repo URL to load it automatically.
- Everything runs in the visitor's browser; **no scores are collected** centrally.
  Adding a leaderboard or saved results would require a backend (e.g. a Google
  Form, Supabase, or Firebase) — out of scope for this static version.
