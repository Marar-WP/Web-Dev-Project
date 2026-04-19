import { CommonModule } from '@angular/common';
import { Component, OnDestroy, OnInit, inject } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { Subject, takeUntil } from 'rxjs';
import { ApiService } from '../../../core/services/api.service';
import { AuthStateService } from '../../../core/services/auth-state.service';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent implements OnInit, OnDestroy {
  private api = inject(ApiService);
  private router = inject(Router);
  private authState = inject(AuthStateService);
  private destroy$ = new Subject<void>();

  isAuthenticated = false;
  username = '';

  ngOnInit(): void {
    this.authState.user$
      .pipe(takeUntil(this.destroy$))
      .subscribe((user) => {
        this.isAuthenticated = !!user;
        this.username = user?.username ?? '';
      });

    this.api.me().subscribe({
      next: (user) => this.authState.setUser(user),
      error: () => this.authState.clear(),
    });
  }

  logout(): void {
    this.api.logout().subscribe({
      next: () => {
        this.authState.clear();
        this.router.navigateByUrl('/');
      },
      error: () => {
        this.authState.clear();
        this.router.navigateByUrl('/');
      }
    });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}