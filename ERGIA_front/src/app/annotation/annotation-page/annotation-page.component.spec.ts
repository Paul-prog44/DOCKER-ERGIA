import { TestBed, ComponentFixture } from '@angular/core/testing';
import { AnnotationPageComponent } from './annotation-page.component';
import { AnnotationService } from '../../services/annotation.service';
import { CorpusService } from '../../services/corpus.service';
import { DomSanitizer } from '@angular/platform-browser';
import { of, throwError } from 'rxjs';
import { ModalAnnotationComponent } from '../modal-annotation/modal-annotation.component';
import { Annotation } from '../../../api/models/annotation';


class MockAnnotationService {
  createAnnotation() {
    return of({});
  }
}

class MockCorpusService {
  getTexts() {
    return of({ content: 'Document de référence' });
  }

  getSummaries() {
    return of({ content: 'Synthèse du document' });
  }
}

describe('AnnotationPageComponent', () => {
  let component: AnnotationPageComponent;
  let fixture: ComponentFixture<AnnotationPageComponent>;
  let mockAnnotationService: MockAnnotationService;
  let mockCorpusService: MockCorpusService;

  // Mock DomSanitizer
  const mockSanitizer = {
    bypassSecurityTrustHtml: jasmine.createSpy('bypassSecurityTrustHtml').and.callFake((html: string) => html),
  };

  beforeEach(async () => {
    mockAnnotationService = new MockAnnotationService();
    mockCorpusService = new MockCorpusService();

    await TestBed.configureTestingModule({
      imports: [ModalAnnotationComponent, AnnotationPageComponent],
      providers: [
        { provide: AnnotationService, useValue: mockAnnotationService },
        { provide: CorpusService, useValue: mockCorpusService },
        { provide: DomSanitizer, useValue: mockSanitizer }, // Use mock sanitizer
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(AnnotationPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create the component', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize with reference document and summary', () => {
    expect(component.referenceDocument).toBe('Document de référence');
    expect(component.resume).toBe('Synthèse du document');
  });

  it('should handle text selection', () => {
    const selectionSpy = spyOn(window, 'getSelection').and.returnValue({
      rangeCount: 1,
      getRangeAt: () => ({
        commonAncestorContainer: { parentElement: document.createElement('div') },
        startOffset: 0,
      } as unknown as Range),
      toString: () => 'selected text',
    } as unknown as Selection);
  
    // Mock `getTextOffset` pour éviter l'erreur
    spyOn(component, 'getTextOffset').and.returnValue(0);
  
    component.getSelectedText();
  
    expect(selectionSpy).toHaveBeenCalled();
    expect(component.selectedText).toBe('selected text');
    expect(component.isPopupVisible).toBeTrue();
  });
  
  

  it('should hide popup', () => {
    component.isPopupVisible = true;
    component.hidePopup();
    expect(component.isPopupVisible).toBeFalse();
  });

  it('should add annotation and update annotated text', () => {
    const mockAnnotation: Annotation = {
      index: 0,
      length: 10,
      color: 'red',
      scu: 'Example SCU', // Ajoutez une valeur pour chaque propriété obligatoire
      summary_id: 1,
      creator: 1,
    };
  
    component.resume = 'Synthèse du document';
  
    component.onAddAnnotation(mockAnnotation);
  
    expect(component.annotations).toContain(mockAnnotation);
    expect(mockSanitizer.bypassSecurityTrustHtml).toHaveBeenCalled(); // Vérifie l'appel de la méthode
    expect(component.annotatedText).toBeTruthy();
  });
  
  
  
});

