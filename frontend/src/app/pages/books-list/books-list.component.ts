import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../core/services/api.service';
import { Book, Category } from '../../core/models/book.model';

@Component({
  selector: 'app-books-list-page',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './books-list.component.html'
})
export class BooksListPageComponent implements OnInit {
  private api = inject(ApiService);

  books: Book[] = [];
  categories: Category[] = [];
  loading = true;
  categoriesLoading = true;
  error = '';

  search = '';
  category = '';
  sort = '-created_at';

  ngOnInit(): void {
    this.loadCategories();
    this.loadBooks();
  }

  loadCategories(): void {
    this.categoriesLoading = true;
    this.api.getCategories().subscribe({
      next: (categories) => {
        this.categories = categories;
        this.categoriesLoading = false;
      },
      error: () => {
        this.categories = [];
        this.categoriesLoading = false;
      }
    });
  }

  loadBooks(): void {
    this.loading = true;
    this.error = '';

    this.api.getBooks({
      search: this.search,
      category: this.category,
      ordering: this.sort,
    }).subscribe({
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

  applyFilters(): void {
    this.loadBooks();
  }

  resetFilters(): void {
    this.search = '';
    this.category = '';
    this.sort = '-created_at';
    this.loadBooks();
  }
}

