import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { RegisterService } from './register.service';
import { environment } from '../environments/environments';
import { InterfaceUser } from '../../api/models/interface-user';

describe('RegisterService', () => {
  let service: RegisterService;
  let httpMock: HttpTestingController;
  const apiUrl = environment.apiUrl;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [RegisterService]
    });
    service = TestBed.inject(RegisterService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should register a user', () => {
    const mockUser: InterfaceUser = {
      email: 'testuser@example.com',
      password: 'securepassword',
      firstname: 'John',
      lastname: 'Doe',
      acceptCgu: true
    };

    const mockResponse = {
      status: 201,
      statusText: 'Created',
      body: { success: true, message: 'User registered successfully' }
    };

    service.register(mockUser).subscribe(response => {
      expect(response.status).toBe(201);
      expect(response.body).toEqual(mockResponse.body);
    });

    const req = httpMock.expectOne(`${apiUrl}/register`);
    expect(req.request.method).toBe('POST');
    expect(req.request.headers.get('Content-Type')).toBe('application/json');
    expect(req.request.headers.get('Accept')).toBe('application/json');
    expect(req.request.body).toEqual(JSON.stringify(mockUser));

    req.flush(mockResponse.body, {
      status: mockResponse.status,
      statusText: mockResponse.statusText
    });
  });

  it('should handle errors when registering a user', () => {
    const mockUser: InterfaceUser = {
      email: 'testuser@example.com',
      password: 'securepassword',
      firstname: 'John',
      lastname: 'Doe',
      acceptCgu: true
    };

    const mockErrorResponse = {
      status: 400,
      statusText: 'Bad Request'
    };

    service.register(mockUser).subscribe({
      next: () => fail('Expected an error, but got a response'),
      error: (error) => {
        expect(error.status).toBe(mockErrorResponse.status);
        expect(error.statusText).toBe(mockErrorResponse.statusText);
      }
    });

    const req = httpMock.expectOne(`${apiUrl}/register`);
    expect(req.request.method).toBe('POST');
    req.flush(null, mockErrorResponse);
  });
});
