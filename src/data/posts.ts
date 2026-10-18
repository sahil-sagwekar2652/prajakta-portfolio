export interface Post {
  title: string;
  date: string;
  displayDate: string;
  url: string;
  image: string;
  imageWidth: number;
  imageHeight: number;
  imageAlt: string;
  excerpt: string;
  featured?: boolean;
}

// The five posts scraped (verbatim) from yatrawithprajakta.blogspot.com.
// Cards link out to the original posts; excerpts are trimmed from her own text.
export const posts: Post[] = [
  {
    title: 'Kalsubai Trek Guide From Mumbai – Route, Cost, Night Trek Experience & Tips',
    date: '2026-03-07',
    displayDate: '7 March 2026',
    url: 'https://yatrawithprajakta.blogspot.com/2026/03/kalsubai-trek-guide-from-mumbai-route.html',
    image: '/images/blog/kalsubai.jpg',
    imageWidth: 539,
    imageHeight: 303,
    imageAlt: 'Tent pitched on the Kalsubai plateau, the pinnacle rising behind',
    excerpt:
      'Planning the Kalsubai trek from Mumbai? Route, cost, night trekking, camping under the stars and a magical sunrise at the highest peak in Maharashtra — the “Everest of Maharashtra” at 1646 metres.',
    featured: true,
  },
  {
    title: "Children's day vibe in 20s",
    date: '2025-11-14',
    displayDate: '14 November 2025',
    url: 'https://yatrawithprajakta.blogspot.com/2025/11/childrens-day-vibe-in-20s.html',
    image: '/images/blog/childrens-day.jpg',
    imageWidth: 241,
    imageHeight: 320,
    imageAlt: 'A childhood photograph of Prajakta in costume',
    excerpt:
      'A small reminder of innocence, joy and the playful spark we often lose while growing up.',
  },
  {
    title: 'Tanzania Wildlife Safari – Where Wilderness Meets Culture',
    date: '2025-09-29',
    displayDate: '29 September 2025',
    url: 'https://yatrawithprajakta.blogspot.com/2025/09/tanzania-wildlife-safari-where.html',
    image: '/images/blog/tanzania.jpg',
    imageWidth: 691,
    imageHeight: 461,
    imageAlt: 'Leopards with a kill in the Tanzanian bush',
    excerpt: 'In every journey, a story takes flight — a safari where wilderness meets culture.',
  },
  {
    title: "Nakhind Trek – Ridge Walk, Needle Hole & Nature's Calm in the Sahyadris",
    date: '2025-09-16',
    displayDate: '16 September 2025',
    url: 'https://yatrawithprajakta.blogspot.com/2025/09/nakhind-trek-ridge-walk-needle-hole.html',
    image: '/images/blog/nakhind.jpg',
    imageWidth: 400,
    imageHeight: 292,
    imageAlt: 'Prajakta looking out over the green Sahyadri valley from Nakhind',
    excerpt:
      'Peace, raw nature, and a ridge walk that gives you goosebumps — one of the lesser-known but truly breathtaking treks in Maharashtra.',
  },
  {
    title: 'Gorakhgad Trek – Complete Guide, Route, Tips & My Experience',
    date: '2025-08-28',
    displayDate: '28 August 2025',
    url: 'https://yatrawithprajakta.blogspot.com/2025/08/gorakhgad-trek-complete-guide-route.html',
    image: '/images/blog/gorakhgad.jpg',
    imageWidth: 202,
    imageHeight: 320,
    imageAlt: 'The moss-covered rock pinnacle of Gorakhgad',
    excerpt:
      'Twice climbed — the second time a sudden plan and a funny story. My honest experience, trek details and tips; best in monsoon.',
  },
];
