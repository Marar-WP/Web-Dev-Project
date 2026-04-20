import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { map, Observable, tap } from 'rxjs';
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

interface TokenResponse {
  access: string;
  refresh: string;
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
    return this.http.post<Review>(`${this.baseUrl}/books/${bookId}/reviews/`, payload);
  }

  register(payload: {
    username: string;
    email: string;
    password: string;
    password2: string;
  }): Observable<User> {
    return this.http.post<User>(`${this.baseUrl}/users/register/`, payload);
  }

  login(payload: { username: string; password: string }): Observable<TokenResponse> {
    return this.http.post<TokenResponse>(`${this.baseUrl}/token/`, payload).pipe(
      tap((tokens) => {
        localStorage.setItem('access', tokens.access);
        localStorage.setItem('refresh', tokens.refresh);
      })
    );
  }

  logout(): Observable<unknown> {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    return this.http.post(`${this.baseUrl}/users/logout/`, {});
  }

  me(): Observable<User> {
    return this.http.get<User>(`${this.baseUrl}/users/me/`);
  }

  refreshToken(): Observable<{ access: string }> {
    const refresh = localStorage.getItem('refresh') || '';
    return this.http.post<{ access: string }>(`${this.baseUrl}/token/refresh/`, { refresh }).pipe(
      tap((tokens) => {
        localStorage.setItem('access', tokens.access);
      })
    );
  }
}