import { Injectable } from '@angular/core';
import * as mammoth from 'mammoth';

@Injectable({
  providedIn: 'root'
})
export class DocxParserService {

  constructor() { }

  convertDocxToHtml(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (event: any) => {
        const arrayBuffer = event.target.result;

        mammoth
          .convertToHtml({ arrayBuffer: arrayBuffer })
          .then((result) => resolve(result.value)) // Retourne le HTML
          .catch((error) => reject(error)); // Gère les erreurs
      };

      reader.readAsArrayBuffer(file);
    });
  }
}
