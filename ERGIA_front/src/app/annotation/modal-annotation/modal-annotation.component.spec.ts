import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ModalAnnotationComponent } from './modal-annotation.component';
import { ReactiveFormsModule } from '@angular/forms';
import { AnnotationService } from '../../services/annotation.service';
import { Annotation } from '../../../api/models/annotation';
import { By } from '@angular/platform-browser';
import { EventEmitter } from '@angular/core';
import { signal } from '@angular/core'; // Assurez-vous que cette ligne est au top level


describe('ModalAnnotationComponent', () => {
  let component: ModalAnnotationComponent;
  let fixture: ComponentFixture<ModalAnnotationComponent>;
  let mockAnnotationService: jasmine.SpyObj<AnnotationService>;


  beforeEach(async () => {
    mockAnnotationService = jasmine.createSpyObj('AnnotationService', ['createAnnotation']);

    await TestBed.configureTestingModule({
      imports: [ReactiveFormsModule, ModalAnnotationComponent],
      providers: [
        { provide: AnnotationService, useValue: mockAnnotationService },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(ModalAnnotationComponent);
    component = fixture.componentInstance;

    // Simuler les @Input avec WritableSignal pour Angular
    (component as any).index = signal(0); // Simuler une valeur pour `index`
    (component as any).length = signal(10); // Simuler une valeur pour `length`
    (component as any).annotations = signal<Annotation[]>([
      { scu: 'SCU 1', color: 'red', summary_id: 1, index: 0, length: 10, creator: 1 },
      { scu: 'SCU 2', color: 'blue', summary_id: 2, index: 5, length: 15, creator: 2 },
    ]);

    fixture.detectChanges();
  });
  

  
  

  it('should create the component', () => {
    expect(component).toBeTruthy();
  });

  it('should close the popup when closePopup is called', () => {
    spyOn(component.close, 'emit');

    component.closePopup();

    expect(component.close.emit).toHaveBeenCalled();
  });

  it('should emit addAnnotation event with correct data when handleAddAnnotation is called with existing SCU', () => {
    spyOn(component.addAnnotation, 'emit');

    component.addAnnotationForm.setValue({ oldScu: 'SCU 1', scu: '', color: '' });
    component.handleAddAnnotation();

    expect(component.addAnnotation.emit).toHaveBeenCalledWith({
      scu: 'SCU 1',
      color: 'red',
      summary_id: 1,
      index: 0,
      length: 10,
      creator: 1,
    });
  });

  it('should emit addAnnotation event with new SCU when handleAddAnnotation is called with new SCU data', () => {
    spyOn(component.addAnnotation, 'emit');

    component.addAnnotationForm.setValue({ oldScu: '', scu: 'New SCU', color: '#e66465' });
    component.handleAddAnnotation();

    expect(component.addAnnotation.emit).toHaveBeenCalledWith({
      scu: 'New SCU',
      color: '#e66465',
      summary_id: 12, // As per the hardcoded value in your method
      index: 0,
      length: 10,
      creator: 42, // As per the hardcoded value in your method
    });
  });

  it('should display an error message if SCU is missing when handleAddAnnotation is called', () => {
    component.addAnnotationForm.setValue({ oldScu: '', scu: '', color: '#e66465' });

    component.handleAddAnnotation();

    expect(component.errorMessage).toBe('Vous devez mettre une Scu');
  });

  it('should render the annotations in the dropdown', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    const options = compiled.querySelectorAll('select[formControlName="oldScu"] option');

    expect(options.length).toBe(2); // Vérifie qu'il y a 2 options
    expect(options[0].textContent).toBe('SCU 1'); // Vérifie que la première option est 'SCU 1'
    expect(options[1].textContent).toBe('SCU 2'); // Vérifie que la deuxième option est 'SCU 2'
  });
  

  it('should call closePopup when the cancel button is clicked', () => {
    spyOn(component, 'closePopup');

    const cancelButton = fixture.debugElement.query(By.css('button:last-of-type')).nativeElement;
    cancelButton.click();

    expect(component.closePopup).toHaveBeenCalled();
  });
});
