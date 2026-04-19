import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../core/services/api.service';
import { AuthStateService } from '../../core/services/auth-state.service';
import { Book } from '../../core/models/book.model';

@Component({
  selector: 'app-book-details-page',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './book-details.component.html'
})
export class BookDetailsPageComponent implements OnInit {
  private api = inject(ApiService);
  private route = inject(ActivatedRoute);
  private authState = inject(AuthStateService);

  book: Book | null = null;
  loading = true;
  error = '';
  reviewText = '';
  reviewRating = 5;
  reviewMessage = '';
  isSuccessMessage = false;
  isAuthenticated = false;

  ngOnInit(): void {
    this.isAuthenticated = !!this.authState.snapshot();
    const id = this.route.snapshot.paramMap.get('id');
    if (!id) {
      this.error = 'Book id not found.';
      this.loading = false;
      return;
    }

    this.api.getBook(id).subscribe({
      next: (book) => {
        this.book = book;
        this.loading = false;
      },
      error: () => {
        this.error = 'Could not load the book.';
        this.loading = false;
      }
    });
  }

  submitReview(): void {
    if (!this.book) return;
    this.reviewMessage = '';
    this.isSuccessMessage = false;

    if (!this.reviewText.trim()) {
      this.reviewMessage = 'Please enter your review text.';
      return;
    }

    this.api.addReview(this.book.id, {
      rating: this.reviewRating,
      text: this.reviewText.trim()
    }).subscribe({
      next: () => {
        this.reviewMessage = 'Review added successfully.';
        this.isSuccessMessage = true;
        this.reviewText = '';
        this.reviewRating = 5;
        this.ngOnInit();
      },
      error: (error) => {
        const detail = error?.error?.detail;
        this.reviewMessage = detail || 'Could not add review. Please login and try again.';
        this.isSuccessMessage = false;
      }
    });
  }
}
