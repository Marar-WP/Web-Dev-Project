import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../core/services/api.service';
import { Book } from '../../core/models/book.model';

@Component({
  selector: 'app-books-list-page',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './books-list.component.html'
})
export class BooksListPageComponent implements OnInit {
  private api = inject(ApiService);

  books: Book[] = [];
  loading = true;
  error = '';

  ngOnInit(): void {
    this.api.getBooks().subscribe({
      next: (books) => {
        this.books = books;
        this.loading = false;
      },
      error: () => {
        this.error = 'Could not load books from backend.';
        this.loading = false;
      }
    });
  }
}
