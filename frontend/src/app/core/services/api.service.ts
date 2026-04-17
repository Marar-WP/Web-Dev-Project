import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map, Observable } from 'rxjs';
import { Book, Review } from '../models/book.model';
import { User } from '../models/user.model';

interface PaginatedBooksResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Book[];
}

@Injectable({ providedIn: 'root' })
export class ApiService {
  private http = inject(HttpClient);
  private baseUrl = 'http://localhost:8000/api';

  getBooks(): Observable<Book[]> {
  return this.http
    .get<PaginatedBooksResponse>(`${this.baseUrl}/books/`)
    .pipe(map((response) => response.results));
}

  getBook(id: string | number): Observable<Book> {
    return this.http.get<Book>(`${this.baseUrl}/books/${id}/`);
  }

  addReview(bookId: string | number, payload: { rating: number; text: string }): Observable<Review> {
    return this.http.post<Review>(`${this.baseUrl}/books/${bookId}/reviews/`, payload);
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
