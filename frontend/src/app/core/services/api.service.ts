import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { map, Observable } from 'rxjs';
import { Book, Category, Review } from '../models/book.model';
import { User } from '../models/user.model';

interface PaginatedBooksResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Book[];
}

interface PaginatedCategoriesResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Category[];
}

@Injectable({ providedIn: 'root' })
export class ApiService {
  private http = inject(HttpClient);
  private baseUrl = 'http://localhost:8000/api';

  private normalizeListResponse<T>(response: T[] | { results?: T[] } | null | undefined): T[] {
    if (Array.isArray(response)) {
      return response;
    }

    if (response && Array.isArray((response as { results?: T[] }).results)) {
      return (response as { results?: T[] }).results ?? [];
    }

    return [];
  }

  getBooks(filters?: { search?: string; category?: string; ordering?: string }): Observable<Book[]> {
    let params = new HttpParams();

    if (filters?.search?.trim()) {
      params = params.set('search', filters.search.trim());
    }

    if (filters?.category?.trim()) {
      params = params.set('category', filters.category);
    }

    if (filters?.ordering?.trim()) {
      params = params.set('ordering', filters.ordering);
    }

    return this.http
      .get<PaginatedBooksResponse | Book[]>(`${this.baseUrl}/books/`, { params })
      .pipe(map((response) => this.normalizeListResponse<Book>(response)));
  }

  getCategories(): Observable<Category[]> {
    return this.http
      .get<PaginatedCategoriesResponse | Category[]>(`${this.baseUrl}/books/categories/`)
      .pipe(map((response) => this.normalizeListResponse<Category>(response)));
  }

  getBook(id: string | number): Observable<Book> {
    return this.http.get<Book>(`${this.baseUrl}/books/${id}/`);
  }

  addReview(bookId: string | number, payload: { rating: number; text: string }): Observable<Review> {
    return this.http.post<Review>(`${this.baseUrl}/books/${bookId}/reviews/`, payload, {
      withCredentials: true,
    });
  }

  register(payload: { username: string; email: string; password: string; password2: string }): Observable<User> {
    return this.http.post<User>(`${this.baseUrl}/users/register/`, payload, { withCredentials: true });
  }

  login(payload: { username: string; password: string }): Observable<User> {
    return this.http.post<User>(`${this.baseUrl}/users/login/`, payload, { withCredentials: true });
  }

  logout(): Observable<unknown> {
    return this.http.get(`${this.baseUrl}/users/logout/`, { withCredentials: true });
  }

  me(): Observable<User> {
    return this.http.get<User>(`${this.baseUrl}/users/me/`, { withCredentials: true });
  }
}
