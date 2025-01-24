import { TestBed } from '@angular/core/testing';
import { CampaignService } from './campaign.service';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { environment } from '../environments/environments';

describe('CampaignService', () => {
  let service: CampaignService;
  let httpMock: HttpTestingController;
  const apiUrl = environment.apiUrl;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [CampaignService],
    });

    service = TestBed.inject(CampaignService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should fetch campaigns', () => {
    const mockResponse = [{ id: 1, name: 'Test Campaign' }];

    service.getCampaigns().subscribe((campaigns) => {
      expect(campaigns).toEqual(mockResponse);
    });

    const req = httpMock.expectOne(`${apiUrl}/campaigns`);
    expect(req.request.method).toBe('GET');
    req.flush(mockResponse);
  });

  it('should fetch a campaign by ID', () => {
    const mockResponse = { id: 1, name: 'Test Campaign' };

    service.getCampaign(1).subscribe((campaign) => {
      expect(campaign).toEqual(mockResponse);
    });

    const req = httpMock.expectOne(`${apiUrl}/campaigns/1`);
    expect(req.request.method).toBe('GET');
    req.flush(mockResponse);
  });

  it('should fetch a campaign by name', () => {
    const mockResponse = { id: 1, name: 'Test Campaign' };

    service.getCampaignByName('Test Campaign').subscribe((campaign) => {
      expect(campaign).toEqual(mockResponse);
    });

    const req = httpMock.expectOne(`${apiUrl}/campaignsName/Test Campaign`);
    expect(req.request.method).toBe('GET');
    req.flush(mockResponse);
  });

  it('should create a campaign', () => {
    const mockResponse = { status: true };
    const formData = new FormData();

    service.createCampaign(formData).subscribe((response) => {
      expect(response.body).toEqual(mockResponse);
    });

    const req = httpMock.expectOne(`${apiUrl}/campaigns`);
    expect(req.request.method).toBe('POST');
    req.flush(mockResponse);
  });

  it('should delete a campaign', () => {
    const mockResponse = { status: true };

    service.deleteCampaign('1').subscribe((response) => {
      expect(response).toEqual(mockResponse);
    });

    const req = httpMock.expectOne(`${apiUrl}/campaigns/1`);
    expect(req.request.method).toBe('DELETE');
    req.flush(mockResponse);
  });

  it('should fetch joined campaigns by user ID', () => {
    const mockResponse = [{ id: 1, name: 'Joined Campaign' }];

    service.getJoinedCampaigns('user1').subscribe((campaigns) => {
      expect(campaigns).toEqual(mockResponse);
    });

    const req = httpMock.expectOne(`${apiUrl}/campaigns/user/user1`);
    expect(req.request.method).toBe('GET');
    req.flush(mockResponse);
  });

  it('should join a campaign', () => {
    const mockResponse = { status: true };
    const data = { userId: 'user1', campaignId: '1' };

    service.joinCampaigns(data).subscribe((response) => {
      expect(response).toEqual(mockResponse);
    });

    const req = httpMock.expectOne(`${apiUrl}/add_user_to_campaign`);
    expect(req.request.method).toBe('POST');
    req.flush(mockResponse);
  });

  it('should leave a campaign', () => {
    const mockResponse = { status: true };
    const data = { userId: 'user1', campaignId: '1' };

    service.leaveCampaign(data).subscribe((response) => {
      expect(response).toEqual(mockResponse);
    });

    const req = httpMock.expectOne(`${apiUrl}/delete_user_to_campaign`);
    expect(req.request.method).toBe('POST');
    req.flush(mockResponse);
  });

  it('should fetch original texts for a campaign', () => {
    const mockResponse = [{ id: 1, text: 'Original Text' }];

    service.getOriginalTexts(1).subscribe((texts) => {
      expect(texts).toEqual(mockResponse);
    });

    const req = httpMock.expectOne(`${apiUrl}/campaigns/originalTexts/1`);
    expect(req.request.method).toBe('GET');
    req.flush(mockResponse);
  });

  it('should fetch campaigns by owner', () => {
    const mockResponse = [{ id: 1, name: 'Owned Campaign' }];

    service.getCampaignsByOwner('user1').subscribe((campaigns) => {
      expect(campaigns).toEqual(mockResponse);
    });

    const req = httpMock.expectOne(`${apiUrl}/campaigns/getOwnerCampagn/user1`);
    expect(req.request.method).toBe('GET');
    req.flush(mockResponse);
  });

  it('should update campaign status', () => {
    const mockResponse = { status: true };
    const data = { campaignId: '1', status: 'updated' };

    service.updateCampaignStatus(data).subscribe((response) => {
      expect(response).toEqual(mockResponse);
    });

    const req = httpMock.expectOne(`${apiUrl}/campaigns/update_status`);
    expect(req.request.method).toBe('PUT');
    req.flush(mockResponse);
  });

  it('should fetch campaign statuses by user ID', () => {
    const mockResponse = [{ id: 1, status: 'active' }];

    service.getStatus('user1').subscribe((statuses) => {
      expect(statuses).toEqual(mockResponse);
    });

    const req = httpMock.expectOne(`${apiUrl}/campaigns/getStatusCampagn/user1`);
    expect(req.request.method).toBe('GET');
    req.flush(mockResponse);
  });
});
