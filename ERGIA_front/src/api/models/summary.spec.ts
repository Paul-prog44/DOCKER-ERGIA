import { Summary } from './summary';

describe('Summary', () => {

  it('should correctly initialize with valid data', () => {
    const data = {
      annotator_id: 123,
      content: 'This is a test content.',
      path: 'C:\\folder\\example.txt',
      id_summary: '456',
    };

    const summary = new Summary(data);

    expect(summary.annotator_id).toBe(123);
    expect(summary.content).toBe('This is a test content.');
    expect(summary.path).toBe('C:\\folder\\example.txt');
    expect(summary.id_summary).toBe('456');
    expect(summary.name).toBe('example');
  });


  it('should set name to "not found" if path does not match the pattern', () => {
    const data = {
      annotator_id: 123,
      content: 'Another test content.',
      path: 'C:\\folder\\invalidpath',
      id_summary: '789',
    };

    const summary = new Summary(data);

    expect(summary.name).toBe('not found');
  });
  
  
  it('should extract name correctly from different valid paths', () => {
    const paths = [
      'C:\\folder\\example.txt',
      'D:\\projects\\test\\another_example.txt',
      '/home/user/documents/example_file.txt',
    ];

    paths.forEach((path) => {
      const data = {
        annotator_id: 1,
        content: 'Content',
        path,
        id_summary: 'id',
      };

      const summary = new Summary(data);

      const expectedName = path.match(/\\([^\\]+)\.txt$/)?.[1] || 'not found';
      expect(summary.name).toBe(expectedName);
    });
  });


});