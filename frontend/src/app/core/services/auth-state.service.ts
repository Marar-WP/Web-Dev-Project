import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { User } from '../models/user.model';

@Injectable({ providedIn: 'root' })
export class AuthStateService {
  private userSubject = new BehaviorSubject<User | null>(null);
  user$ = this.userSubject.asObservable();

  setUser(user: User | null): void {
    this.userSubject.next(user);
  }

  clear(): void {
    this.userSubject.next(null);
  }

  snapshot(): User | null {
    return this.userSubject.value;
  }
}
