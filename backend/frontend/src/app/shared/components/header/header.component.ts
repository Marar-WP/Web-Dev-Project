import { Component, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../../core/services/api.service';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent {
  private api = inject(ApiService);

  logout(): void {
    this.api.logout().subscribe({
      next: () => window.location.href = '/',
      error: () => window.location.href = '/'
    });
  }
}
