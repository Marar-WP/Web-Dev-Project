import { HttpInterceptorFn } from '@angular/common/http';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const shouldUseCredentials = req.url.includes('127.0.0.1:8000') || req.url.includes('localhost:8000');
  const request = shouldUseCredentials ? req.clone({ withCredentials: true }) : req;
  return next(request);
};
