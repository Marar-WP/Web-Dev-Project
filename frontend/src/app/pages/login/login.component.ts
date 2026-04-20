import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from '../../core/services/api.service';
import { AuthStateService } from '../../core/services/auth-state.service';

@Component({
  selector: 'app-login-page',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.component.html'
})
export class LoginPageComponent {
  private api = inject(ApiService);
  private router = inject(Router);
  private authState = inject(AuthStateService);

  username = '';
  password = '';
  message = '';

  submit(): void {
  this.message = '';

  this.api.login({
    username: this.username,
    password: this.password
  }).subscribe({
    next: () => {
      this.api.me().subscribe({
        next: (user) => {
          this.authState.setUser(user);
          this.router.navigateByUrl('/profile');
        },
        error: () => {
          this.message = 'Login succeeded, but profile could not be loaded.';
        }
      });
    },
    error: (error) => {
      this.message = error?.error?.detail || 'Login failed. Please check your credentials.';
    }
  });
}
}