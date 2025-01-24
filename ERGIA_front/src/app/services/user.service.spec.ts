import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { UserService } from './user.service';
import { environment } from '../environments/environments';
import { ApiCampaign } from '../../api/models/campaign';

describe('UserService', () => {
  let service: UserService;
  let httpMock: HttpTestingController;
  const apiUrl = environment.apiUrl;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [UserService]
    });
    service = TestBed.inject(UserService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should get user details', () => {
    const mockUser = { id: '123', name: 'John Doe', email: 'john.doe@example.com' };

    service.getUser().subscribe(user => {
      expect(user).toEqual(mockUser);
    });

    const req = httpMock.expectOne(`${apiUrl}/user`);
    expect(req.request.method).toBe('GET');
    req.flush(mockUser);
  });

  it('should update user details', () => {
    const userId = '123';
    const updateData = { name: 'John Updated', email: 'john.updated@example.com' };
    const mockResponse = { success: true };

    service.updateUser(userId, updateData).subscribe(response => {
      expect(response).toEqual(mockResponse);
    });

    const req = httpMock.expectOne(`${apiUrl}/register/${userId}`);
    expect(req.request.method).toBe('PUT');
    expect(req.request.body).toEqual(updateData);
    req.flush(mockResponse);
  });

  it('should delete a user', () => {
    const userId = '123';
    const mockResponse = { success: true };

    service.deleteUser(userId).subscribe(response => {
      expect(response).toEqual(mockResponse);
    });

    const req = httpMock.expectOne(`${apiUrl}/user/${userId}`);
    expect(req.request.method).toBe('DELETE');
    req.flush(mockResponse);
  });

  it('should change user password', () => {
    const userId = '123';
    const passwordData = { old_password: 'oldPass', new_password: 'newPass' };
    const mockResponse = { success: true };

    service.changePassword(userId, passwordData).subscribe(response => {
      expect(response).toEqual(mockResponse);
    });

    const req = httpMock.expectOne(`${apiUrl}/register/password/${userId}`);
    expect(req.request.method).toBe('PUT');
    expect(req.request.body).toEqual(passwordData);
    req.flush(mockResponse);
  });

  it('should get campaigns joined by the user', () => {
    const mockCampaigns: ApiCampaign[] = [
      {
        id_campaign: 1,
        creation_date: new Date('2023-01-01'),
        date_phase_1: new Date('2023-02-01'),
        date_phase_2: new Date('2023-03-01'),
        name: 'Campaign 1',
        owner_id: 10,
        status_id: 1
      },
      {
        id_campaign: 2,
        creation_date: new Date('2023-04-01'),
        date_phase_1: new Date('2023-05-01'),
        date_phase_2: new Date('2023-06-01'),
        name: 'Campaign 2',
        owner_id: 20,
        status_id: 2
      }
    ];

    service.getUserCompaignJoined().subscribe(campaigns => {
      expect(campaigns).toEqual(mockCampaigns);
    });

    const req = httpMock.expectOne(`${apiUrl}/campaigns/joined`);
    expect(req.request.method).toBe('GET');
    req.flush(mockCampaigns);
  });
});
