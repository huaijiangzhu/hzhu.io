# hzhu.io

Personal website built with SvelteKit and Tailwind CSS.

## Tech Stack

- [SvelteKit](https://kit.svelte.dev/) - Web framework
- [Tailwind CSS](https://tailwindcss.com/) - Styling
- [KaTeX](https://katex.org/) - LaTeX math rendering for blog posts
- [Cloudflare Pages](https://pages.cloudflare.com/) - Hosting

## Development

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Deployment

### Cloudflare Pages

1. Connect your GitHub repository to [Cloudflare Pages](https://dash.cloudflare.com/?to=/:account/pages)

2. Configure build settings:
   | Setting | Value |
   |---------|-------|
   | Build command | `npm install && npm run build` |
   | Build output directory | `build` |
   | Node.js version | `20` (set via `NODE_VERSION` environment variable) |

3. Deploy - Cloudflare will automatically rebuild on each push to main

## Credits

Based on [Eric Zhang's personal website](https://github.com/ekzhang/ekzhang.github.io).
