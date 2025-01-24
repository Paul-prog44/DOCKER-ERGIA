import { OriginalText } from './original-text';
import { Summary } from './summary';

describe('OriginalText', () => {

  it('should correctly initialize with valid data', () => {
    const data = {
      text_id: 1,
      path: 'folder\\subfolder\\example.txt',
      content: 'This is the content of the original text.',
    };

    const originalText = new OriginalText(data);

    expect(originalText.idOriginalText).toBe(1);
    expect(originalText.path).toBe('folder\\subfolder\\example.txt');
    expect(originalText.name).toBe('example.txt');
    expect(originalText.content).toBe('This is the content of the original text.');
    expect(originalText.summaries).toEqual([]); // Empty array by default
  });


  it('should set name to "not found" if path does not match the pattern', () => {
    const data = {
      text_id: 2,
      path: 'invalidpath',
      content: 'Some content',
    };

    const originalText = new OriginalText(data);

    expect(originalText.name).toBe('not found');
  });


  it('should extract name correctly from different valid paths', () => {
    const paths = [
      'folder\\subfolder\\file1.txt',
      'another\\path\\file2.txt',
      'yet\\another\\path\\file3.txt',
    ];

    paths.forEach((path) => {
      const data = {
        text_id: 3,
        path,
        content: 'Dummy content',
      };

      const originalText = new OriginalText(data);

      const expectedName = path.match(/^([^\\]*\\){2}([^\\]*)/)?.[2] || 'not found';
      expect(originalText.name).toBe(expectedName);
    });
  });

});
