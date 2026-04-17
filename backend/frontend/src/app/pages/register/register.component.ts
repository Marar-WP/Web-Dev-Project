import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../core/services/api.service';

@Component({
  selector: 'app-register-page',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './register.component.html'
})
export class RegisterPageComponent {
  private api = inject(ApiService);

  username = '';
  email = '';
  password = '';
  password2 = '';
  message = '';

  submit(): void {
    this.message = '';
    this.api.register({
      username: this.username,
      email: this.email,
      password: this.password,
      password2: this.password2
    }).subscribe({
      next: () => this.message = 'Registration successful.',
      error: () => this.message = 'Registration failed.'
    });
  }
}
