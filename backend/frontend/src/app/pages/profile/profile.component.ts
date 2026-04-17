import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../core/services/api.service';
import { User } from '../../core/models/user.model';

@Component({
  selector: 'app-profile-page',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './profile.component.html'
})
export class ProfilePageComponent implements OnInit {
  private api = inject(ApiService);

  user: User | null = null;
  error = '';
  loading = true;

  ngOnInit(): void {
    this.api.me().subscribe({
      next: (user) => {
        this.user = user;
        this.loading = false;
      },
      error: () => {
        this.error = 'Not authenticated or profile is unavailable.';
        this.loading = false;
      }
    });
  }
}
