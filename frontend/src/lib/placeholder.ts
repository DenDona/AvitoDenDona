const NO_IMAGE_SVG = `<svg xmlns="http://www.w3.org/2000/svg" width="300" height="200" viewBox="0 0 300 200">
  <rect width="100%" height="100%" fill="#f1f3f5"/>
  <g fill="#c1c5cb">
    <path d="M115 75h70a6 6 0 0 1 6 6v38a6 6 0 0 1-6 6h-70a6 6 0 0 1-6-6V81a6 6 0 0 1 6-6Z" fill="none" stroke="#c1c5cb" stroke-width="3"/>
    <circle cx="131" cy="93" r="6"/>
    <path d="M109 113l20-18 16 14 12-10 24 20v3a6 6 0 0 1-6 6h-60a6 6 0 0 1-6-6v-9Z"/>
  </g>
  <text x="50%" y="138" dominant-baseline="middle" text-anchor="middle" fill="#9aa0a6" font-family="system-ui, sans-serif" font-size="13">Нет фото</text>
</svg>`

export const NO_IMAGE = `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(NO_IMAGE_SVG)}`
