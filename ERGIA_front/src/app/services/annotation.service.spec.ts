import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { AnnotationService } from './annotation.service';
import { environment } from '../environments/environments';
import { Annotation } from '../../api/models/annotation';

describe('AnnotationService', () => {
  let service: AnnotationService;
  let httpMock: HttpTestingController;
  const apiUrl = environment.apiUrl;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [AnnotationService],
    });

    service = TestBed.inject(AnnotationService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    // Vérifie qu'il n'y a pas de requêtes non gérées après chaque test
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should create annotations', () => {
    const mockAnnotations: Annotation[] = [
      { scu: 'SCU 1', color: 'red', summary_id: 1, index: 0, length: 10, creator: 1 },
      { scu: 'SCU 2', color: 'blue', summary_id: 2, index: 5, length: 15, creator: 2 },
    ];

    service.createAnnotation(mockAnnotations).subscribe((response) => {
      expect(response).toEqual({ success: true });
    });

    const req = httpMock.expectOne(`${apiUrl}/annotations`);
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual(mockAnnotations);
    req.flush({ success: true });
  });

  it('should get annotations by resume ID', () => {
    const resumeId = 123;
    const mockAnnotations: Annotation[] = [
      { scu: 'SCU 1', color: 'red', summary_id: 1, index: 0, length: 10, creator: 1 },
      { scu: 'SCU 2', color: 'blue', summary_id: 2, index: 5, length: 15, creator: 2 },
    ];

    service.getAnnotations(resumeId).subscribe((annotations) => {
      expect(annotations).toEqual(mockAnnotations);
    });

    const req = httpMock.expectOne(`${apiUrl}/synthese/${resumeId}/annotations/`);
    expect(req.request.method).toBe('GET');
    req.flush(mockAnnotations);
  });

  it('should delete an annotation by ID', () => {
    const annotationId = 789;

    service.deleteAnnotation(annotationId).subscribe((response) => {
      expect(response).toEqual({ success: true });
    });

    const req = httpMock.expectOne(`${apiUrl}/synthese/annotations/${annotationId}`);
    expect(req.request.method).toBe('DELETE');
    req.flush({ success: true });
  });
});
