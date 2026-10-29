import { cpSync, copyFileSync, mkdirSync } from 'node:fs';
mkdirSync('dist', { recursive: true });
copyFileSync('index.html', 'dist/index.html');
copyFileSync('src/styles.css', 'dist/styles.css');
cpSync('public/assets', 'dist/assets', { recursive: true });
console.log('CONFERATUS preview compiled into dist/');
