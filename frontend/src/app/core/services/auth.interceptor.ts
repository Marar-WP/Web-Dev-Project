import { HttpInterceptorFn } from '@angular/common/http';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const shouldUseCredentials = req.url.includes('localhost:8000');
  const request = shouldUseCredentials ? req.clone({ withCredentials: true }) : req;
  return next(request);
};