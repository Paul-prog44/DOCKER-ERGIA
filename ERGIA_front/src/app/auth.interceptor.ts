import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent, HTTP_INTERCEPTORS } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';
import { Router } from '@angular/router';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(private authService: AuthService, private router: Router) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    
    const token = this.authService.getToken();

    if (token) {
      if (this.authService.isTokenExpired(token)) {
        this.authService.logout();
        console.log("Login expiré");
        this.router.navigate(['/login']);
        return next.handle(req); 
      }

      const clonedReq = req.clone({
        headers: req.headers.set('Authorization', `Bearer ${token}`)
      });
      return next.handle(clonedReq);
    }

    return next.handle(req);
  }
}

export const AuthInterceptorProvider =
{ provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true };
