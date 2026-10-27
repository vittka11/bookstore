export interface Book {
  id: number;
  title: string;
  author: string;
  price: string;
  description: string;
  stock: number;
  category?: {
    id: number;
    name: string;
    slug: string;
  };
}