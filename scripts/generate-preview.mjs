import sharp from 'sharp';

// Render the editable social card into PNG during the static build.
await sharp('public/preview.svg').resize(1200, 630).png().toFile('public/preview.png');
