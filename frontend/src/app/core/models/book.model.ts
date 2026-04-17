export interface Category {
  id: number;
  name: string;
}

export interface Author {
  id: number;
  name: string;
  bio?: string;
}

export interface Review {
  id: number;
  rating: number;
  text: string;
  created_at?: string;
  user?: number;
  username?: string;
}

export interface Book {
  id: number;
  title: string;
  description: string;
  year?: number;
  category?: Category;
  authors?: Author[];
  reviews?: Review[];
  average_rating?: number;
  reviews_count?: number;
}
