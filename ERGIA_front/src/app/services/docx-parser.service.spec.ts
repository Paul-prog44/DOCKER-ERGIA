import { TestBed } from '@angular/core/testing';
import { DocxParserService } from './docx-parser.service';
import * as mammoth from 'mammoth';

describe('DocxParserService', () => {
  let service: DocxParserService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DocxParserService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should convert a DOCX file to HTML successfully', async () => {
    // Mock file
    const mockFile = new File(['mock content'], 'test.docx', {
      type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    });

    // Redéfinir temporairement mammoth.convertToHtml
    const originalConvertToHtml = mammoth.convertToHtml;
    (mammoth as any).convertToHtml = async () => ({
      value: '<p>Test Content</p>',
      messages: [],
    });

    // Appeler le service
    const result = await service.convertDocxToHtml(mockFile);

    // Vérifications
    expect(result).toBe('<p>Test Content</p>');

    // Restaurer la méthode originale après le test
    (mammoth as any).convertToHtml = originalConvertToHtml;
  });

  it('should handle errors during DOCX to HTML conversion', async () => {
    // Mock file
    const mockFile = new File(['mock content'], 'test.docx', {
      type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    });

    // Redéfinir temporairement mammoth.convertToHtml pour simuler une erreur
    const originalConvertToHtml = mammoth.convertToHtml; // Sauvegarder l'original
    (mammoth as any).convertToHtml = async () => {
      throw new Error('Conversion error');
    };

    try {
      await service.convertDocxToHtml(mockFile);
      fail('Expected an error to be thrown');
    } catch (error) {
      expect((error as Error).message).toBe('Conversion error');
    }

    // Restaurer la méthode originale après le test
    (mammoth as any).convertToHtml = originalConvertToHtml;
  });
});
