import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../core/services/api.service';

@Component({
  selector: 'app-login-page',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './login.component.html'
})
export class LoginPageComponent {
  private api = inject(ApiService);

  username = '';
  password = '';
  message = '';

  submit(): void {
    this.message = '';
    this.api.login({ username: this.username, password: this.password }).subscribe({
      next: () => this.message = 'Login successful.',
      error: () => this.message = 'Login failed.'
    });
  }
}
