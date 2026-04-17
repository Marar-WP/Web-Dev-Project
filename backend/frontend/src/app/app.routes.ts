import { Routes } from '@angular/router';
import { HomePageComponent } from './pages/home/home.component';
import { BooksListPageComponent } from './pages/books-list/books-list.component';
import { BookDetailsPageComponent } from './pages/book-details/book-details.component';
import { LoginPageComponent } from './pages/login/login.component';
import { RegisterPageComponent } from './pages/register/register.component';
import { ProfilePageComponent } from './pages/profile/profile.component';

export const routes: Routes = [
  { path: '', component: HomePageComponent },
  { path: 'books', component: BooksListPageComponent },
  { path: 'books/:id', component: BookDetailsPageComponent },
  { path: 'login', component: LoginPageComponent },
  { path: 'register', component: RegisterPageComponent },
  { path: 'profile', component: ProfilePageComponent },
  { path: '**', redirectTo: '' }
];
