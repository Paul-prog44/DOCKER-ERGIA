import { ComponentFixture, TestBed } from '@angular/core/testing';
import { CampaignCreationComponent } from './campaign-creation.component';
import { ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { of, throwError } from 'rxjs';
import { CampaignService } from '../services/campaign.service';
import { By } from '@angular/platform-browser';

describe('CampaignCreationComponent', () => {
  let component: CampaignCreationComponent;
  let fixture: ComponentFixture<CampaignCreationComponent>;
  let mockCampaignService: jasmine.SpyObj<CampaignService>;
  let mockRouter: jasmine.SpyObj<Router>;

  beforeEach(async () => {
    mockCampaignService = jasmine.createSpyObj('CampaignService', ['createCampaign']);
    mockCampaignService.createCampaign.and.returnValue(of({ status: true })); // Simule un succès
  
    mockRouter = jasmine.createSpyObj('Router', ['navigate']);
  
    await TestBed.configureTestingModule({
      imports: [ReactiveFormsModule, CampaignCreationComponent],
      providers: [
        { provide: CampaignService, useValue: mockCampaignService },
        { provide: Router, useValue: mockRouter },
      ],
    }).compileComponents();
  
    fixture = TestBed.createComponent(CampaignCreationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });
  
  

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize the form with default values', () => {
    const form = component.createCampaignForm;
    expect(form.get('owner_id')?.value).toBe(localStorage.getItem('id_user'));
    expect(form.get('status_id')?.value).toBe('2');
    expect(form.get('campaign_name')?.value).toBe('');
    expect(form.get('date_phase_1')?.value).toBe('');
    expect(form.get('date_phase_2')?.value).toBe('');
    expect(form.get('file')?.value).toBeNull();
  });

  it('should display an error if campaign_name is empty on submit', () => {
    component.createCampaignForm.patchValue({ campaign_name: '' });
    component.handleSubmit();
    expect(component.errorMessage).toBe('Le nom est obligatoire');
  });

  it('should display an error if date_phase_1 is in the past', () => {
    const pastDate = new Date(Date.now() - 86400000).toISOString().split('T')[0];
    component.createCampaignForm.patchValue({ date_phase_1: pastDate });
    component.handleSubmit();
    expect(component.errorMessage).toBe('La date de phase 1 ne peut être dans le passé');
  });

  it('should display an error if date_phase_2 is before date_phase_1', () => {
    const futureDate = new Date(Date.now() + 86400000).toISOString().split('T')[0];
    const earlierDate = new Date(Date.now() + 43200000).toISOString().split('T')[0];
    component.createCampaignForm.patchValue({ date_phase_1: futureDate, date_phase_2: earlierDate });
    component.handleSubmit();
    expect(component.errorMessage).toBe('La date de phase 2 ne peut être avant la phase 1');
  });

  it('should call createCampaign and navigate on successful submission', () => {
    mockCampaignService.createCampaign.and.returnValue(of({ status: true }));
    const validData = {
      campaign_name: 'Test Campaign',
      date_phase_1: new Date(Date.now() + 86400000).toISOString().split('T')[0],
      date_phase_2: new Date(Date.now() + 172800000).toISOString().split('T')[0],
      file: null,
    };
    component.createCampaignForm.patchValue(validData);
    component.handleSubmit();
    expect(mockCampaignService.createCampaign).toHaveBeenCalled();
    expect(mockRouter.navigate).toHaveBeenCalledWith(['/campaignDashboard'], {
      state: { message: 'Votre campagne a bien été créée !' },
    });
  });

  it('should log error on failed submission', () => {
    const consoleSpy = spyOn(console, 'error');
    mockCampaignService.createCampaign.and.returnValue(
      throwError(() => ({ status: 500, message: 'Internal Server Error' }))
    );
    component.createCampaignForm.patchValue({ campaign_name: 'Test Campaign' });
    component.handleSubmit();
    expect(consoleSpy).toHaveBeenCalledWith('Status Code:', 500);
    expect(consoleSpy).toHaveBeenCalledWith('Error occurred:', 'Internal Server Error');
  });

  it('should update the form file control when onFolderSelected is called', () => {
    const file = new File(['content'], 'test.zip', { type: 'application/zip' });
    const event = {
      target: { files: [file] },
    } as unknown as Event;

    component.onFolderSelected(event);
    expect(component.createCampaignForm.get('file')?.value).toBe(file);
  });
});
