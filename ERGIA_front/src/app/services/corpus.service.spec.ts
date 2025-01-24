import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { CorpusService } from './corpus.service';
import { environment } from '../environments/environments';

describe('CorpusService', () => {
  let service: CorpusService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [CorpusService],
    });

    service = TestBed.inject(CorpusService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify(); // Vérifie qu'aucune requête HTTP n'est en attente
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should fetch texts by ID', () => {
    const mockText = { id: 1, content: 'Mock text content' };
    const textId = 1;

    service.getTexts(textId).subscribe((response) => {
      expect(response).toEqual(mockText);
    });

    const req = httpMock.expectOne(`${environment.apiUrl}/text/${textId}`);
    expect(req.request.method).toBe('GET');
    req.flush(mockText); // Simule une réponse HTTP avec les données mockées
  });

  it('should fetch summaries by ID', () => {
    const mockSummary = { id: 1, content: 'Mock summary content' };
    const summaryId = 1;

    service.getSummaries(summaryId).subscribe((response) => {
      expect(response).toEqual(mockSummary);
    });

    const req = httpMock.expectOne(`${environment.apiUrl}/summary/${summaryId}`);
    expect(req.request.method).toBe('GET');
    req.flush(mockSummary); // Simule une réponse HTTP avec les données mockées
  });
});
