import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Book, Review } from '../models/book.model';
import { User } from '../models/user.model';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private http = inject(HttpClient);
  private baseUrl = 'http://127.0.0.1:8000/api';

  getBooks(): Observable<Book[]> {
    return this.http.get<Book[]>(`${this.baseUrl}/books/`);
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
    return this.http.post(`${this.baseUrl}/users/logout/`, {}, { withCredentials: true });
  }

  me(): Observable<User> {
    return this.http.get<User>(`${this.baseUrl}/users/me/`, { withCredentials: true });
  }
}
