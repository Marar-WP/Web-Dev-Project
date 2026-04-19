export interface Category {
  id: number;
  name: string;
  slug?: string;
  description?: string;
}

export interface Author {
  id: number;
  name?: string;
  full_name?: string;
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
  published_year?: number;
  year?: number;
  category?: Category;
  authors?: Author[];
  reviews?: Review[];
  average_rating?: number;
  reviews_count?: number;
}

