export interface Photo {
  src: string;
  width: number;
  height: number;
  alt: string;
  caption: string;
}

// Her own photographs (from the photos/ archive, resized for the web).
export const photos: Photo[] = [
  {
    src: '/images/gallery/flower-field.jpg',
    width: 1600,
    height: 1200,
    alt: 'Prajakta sitting in a field of yellow wildflowers, mist behind',
    caption: 'In the wildflowers',
  },
  {
    src: '/images/gallery/himalaya.jpg',
    width: 960,
    height: 1280,
    alt: 'Prajakta in a saffron sweater against Himalayan conifers',
    caption: 'Himalayan air',
  },
  {
    src: '/images/gallery/summit.jpg',
    width: 1600,
    height: 720,
    alt: 'Summit selfie at a busy temple top with saffron flags',
    caption: 'Summit, saffron flags',
  },
  {
    src: '/images/gallery/beach.jpg',
    width: 1600,
    height: 900,
    alt: 'Prajakta at a beach shack, palm leaves overhead',
    caption: 'Salt in the air',
  },
  {
    src: '/images/gallery/night-beach.jpg',
    width: 1600,
    height: 900,
    alt: 'Prajakta on the beach after dark, waves behind',
    caption: 'The coast, after dark',
  },
];
