import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from '../../core/services/api.service';

@Component({
  selector: 'app-register-page',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './register.component.html'
})
export class RegisterPageComponent {
  private api = inject(ApiService);
  private router = inject(Router);

  username = '';
  email = '';
  password = '';
  password2 = '';
  message = '';

  submit(): void {
    this.message = '';

    if (this.password !== this.password2) {
      this.message = 'Passwords do not match.';
      return;
    }

    this.api.register({
      username: this.username,
      email: this.email,
      password: this.password,
      password2: this.password2
    }).subscribe({
      next: () => {
        this.router.navigateByUrl('/login');
      },
      error: () => {
        this.message = 'Registration failed.';
      }
    });
  }
}