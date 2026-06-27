# Polk Positive Growth News

A simple GitHub Pages site for positive Polk County, Florida growth news.

## What it tracks

- New restaurants
- Housing developments
- Highways and roads
- Hotels
- Retail
- Business and development news

## What it excludes

- Crime
- Arrests
- Fatal crashes
- Politics
- Scandals
- Negative breaking news

## How it updates

The GitHub Action `.github/workflows/update-growth-news.yml` runs every 8 hours and updates `data/stories.json`.

To run manually:

1. Go to your GitHub repository.
2. Click **Actions**.
3. Select **Update Positive Growth News**.
4. Click **Run workflow**.

## Publish

Upload all files to the root of your GitHub Pages repository.
