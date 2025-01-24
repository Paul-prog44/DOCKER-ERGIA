import { TestBed } from '@angular/core/testing';
import { AuthService } from './auth.service';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { Router } from '@angular/router';
import jwtDecode from 'jwt-decode';

describe('AuthService', () => {
  let service: AuthService;
  let routerSpy: jasmine.SpyObj<Router>;

  beforeEach(() => {
    routerSpy = jasmine.createSpyObj('Router', ['navigate']);
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [
        AuthService,
        { provide: Router, useValue: routerSpy },
      ],
    });
    service = TestBed.inject(AuthService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should save and retrieve a token', () => {
    const token = 'test-token';
    service.saveToken(token);
    expect(localStorage.getItem('token')).toBe(token);
    expect(service.getToken()).toBe(token);
  });

  it('should identify expired token correctly', () => {
    const expiredToken = jwtEncode({ exp: Math.floor(Date.now() / 1000) - 10 });
    const validToken = jwtEncode({ exp: Math.floor(Date.now() / 1000) + 3600 });

    expect(service.isTokenExpired(expiredToken)).toBeTrue();
    expect(service.isTokenExpired(validToken)).toBeFalse();
  });

  it('should handle invalid token in isTokenExpired', () => {
    const invalidToken = 'invalid-token';
    spyOn(console, 'error');
    expect(service.isTokenExpired(invalidToken)).toBeTrue();
    expect(console.error).toHaveBeenCalledWith(jasmine.any(String), jasmine.any(Error));
  });

  it('should log in and set isAuthenticated to true', () => {
    service.login();
    expect(service.isLoggedIn()).toBeTrue();
  });

  it('should log out and clear authentication state', () => {
    service.login();
    expect(service.isLoggedIn()).toBeTrue();
    service.logout();
    expect(service.isLoggedIn()).toBeFalse();
    expect(localStorage.getItem('token')).toBeNull();
    expect(localStorage.getItem('id_user')).toBeNull();
  });
});

// Helper function to encode JWT tokens for testing
function jwtEncode(payload: any): string {
  const base64UrlEncode = (str: string) => btoa(str).replace(/=+$/, '').replace(/\+/g, '-').replace(/\//g, '_');
  const header = base64UrlEncode(JSON.stringify({ alg: 'HS256', typ: 'JWT' }));
  const body = base64UrlEncode(JSON.stringify(payload));
  return `${header}.${body}.signature`;
}