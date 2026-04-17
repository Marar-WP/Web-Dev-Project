import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../core/services/api.service';
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

  book: Book | null = null;
  loading = true;
  error = '';
  reviewText = '';
  reviewRating = 5;
  reviewMessage = '';

  ngOnInit(): void {
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

    this.api.addReview(this.book.id, {
      rating: this.reviewRating,
      text: this.reviewText
    }).subscribe({
      next: () => {
        this.reviewMessage = 'Review added successfully.';
        this.reviewText = '';
        this.reviewRating = 5;
        this.ngOnInit();
      },
      error: () => {
        this.reviewMessage = 'Could not add review. Maybe login is required.';
      }
    });
  }
}
